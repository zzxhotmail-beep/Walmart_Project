#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

try:
    import psycopg2
    from psycopg2 import sql
except ImportError as exc:
    raise SystemExit(
        "psycopg2 is required to run this script. Install it with: `pip install psycopg2-binary`"
    ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Load Walmart dataset CSV files into the raw schema of walmart_db."
    )
    parser.add_argument("--dbname", default="walmart_db", help="Target PostgreSQL database name")
    parser.add_argument("--user", default=None, help="Database user")
    parser.add_argument("--password", default=None, help="Database password")
    parser.add_argument("--host", default="localhost", help="Database host")
    parser.add_argument("--port", default="5432", help="Database port")
    parser.add_argument(
        "--data-dir",
        default=str(Path(__file__).resolve().parent / "data"),
        help="Path to the CSV data folder",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data_dir = Path(args.data_dir).resolve()

    table_files = {
        "customers": "customers.csv",
        "stores": "stores.csv",
        "products": "products.csv",
        "employees": "employees.csv",
        "orders": "orders.csv",
        "order_items": "order_items.csv",
    }

    if not data_dir.exists():
        print(f"ERROR: data directory not found: {data_dir}", file=sys.stderr)
        return 1

    conn_args = {
        "dbname": args.dbname,
        "host": args.host,
        "port": args.port,
    }
    if args.user:
        conn_args["user"] = args.user
    if args.password:
        conn_args["password"] = args.password

    with psycopg2.connect(**conn_args) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE SCHEMA IF NOT EXISTS raw")
            cur.execute("SET search_path = raw")

            for table_name, csv_file in table_files.items():
                csv_path = data_dir / csv_file
                if not csv_path.exists():
                    raise FileNotFoundError(f"Missing CSV file: {csv_path}")

                print(f"Loading {csv_path} into raw.{table_name}...")
                with csv_path.open("r", encoding="utf-8") as source_file:
                    cur.copy_expert(
                        sql.SQL("COPY {} FROM STDIN WITH CSV HEADER").format(
                            sql.Identifier(table_name)
                        ),
                        source_file,
                    )

    print("Data load complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
