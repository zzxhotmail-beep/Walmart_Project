#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import psycopg2
from psycopg2 import sql


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new PostgreSQL database fork from the Walmart dataset schema and CSV files."
    )
    parser.add_argument(
        "--target-db",
        default="walmart_db_fork",
        help="Name of the database to create for the fork",
    )
    parser.add_argument(
        "--env-file",
        default=str(Path(__file__).resolve().parent.parent / "walmart_dataset" / ".env"),
        help="Path to the .env file containing the Postgres connection string",
    )
    parser.add_argument(
        "--ddl-file",
        default=str(Path(__file__).resolve().parent.parent / "walmart_dataset" / "ddl" / "create_raw_schema.sql"),
        help="Path to the SQL file that creates the raw schema and tables",
    )
    parser.add_argument(
        "--data-dir",
        default=str(Path(__file__).resolve().parent.parent / "walmart_dataset" / "data"),
        help="Path to the directory containing Walmart CSV files",
    )
    return parser.parse_args()


def read_connection_string(env_path: Path) -> str:
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("Postgres_Connection:"):
                return line.split(":", 1)[1].strip()
            if line.startswith("POSTGRES_CONNECTION="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")

    env_value = os.getenv("POSTGRES_CONNECTION") or os.getenv("Postgres_Connection")
    if env_value:
        return env_value

    raise FileNotFoundError(
        "No Postgres connection string found. Provide --env-file or set POSTGRES_CONNECTION."
    )


def connection_kwargs(connection_string: str) -> dict[str, object]:
    parsed = urlparse(connection_string)
    if not parsed.hostname:
        raise ValueError("The connection string is missing a host")

    kwargs: dict[str, object] = {
        "host": parsed.hostname,
        "port": parsed.port or 5432,
        "user": parsed.username,
        "password": parsed.password,
        "dbname": parsed.path.lstrip("/") or "postgres",
        "sslmode": "require",
    }
    return kwargs


def ensure_schema(target_schema: str, conn_kwargs: dict[str, object]) -> None:
    conn = psycopg2.connect(**conn_kwargs)
    try:
        with conn.cursor() as cur:
            cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}" ).format(sql.Identifier(target_schema)))
            print(f"Schema {target_schema} is ready.")
    finally:
        conn.close()


def load_schema_and_data(target_schema: str, ddl_file: Path, data_dir: Path, conn_kwargs: dict[str, object]) -> None:
    conn = psycopg2.connect(**conn_kwargs)
    try:
        with conn.cursor() as cur:
            ddl_sql = ddl_file.read_text(encoding="utf-8")
            ddl_sql = ddl_sql.replace("CREATE SCHEMA IF NOT EXISTS raw;", f"CREATE SCHEMA IF NOT EXISTS {target_schema};")
            ddl_sql = ddl_sql.replace("SET search_path = raw;", f"SET search_path = {target_schema};")
            cur.execute(ddl_sql)

            table_files = {
                "customers": "customers.csv",
                "stores": "stores.csv",
                "products": "products.csv",
                "employees": "employees.csv",
                "orders": "orders.csv",
                "order_items": "order_items.csv",
            }

            for table_name, csv_name in table_files.items():
                csv_path = data_dir / csv_name
                if not csv_path.exists():
                    raise FileNotFoundError(f"Missing CSV file: {csv_path}")

                print(f"Loading {csv_path.name} into {target_schema}.{table_name}...")
                with csv_path.open("r", encoding="utf-8") as source_file:
                    cur.copy_expert(
                        sql.SQL("COPY {}.{} FROM STDIN WITH CSV HEADER").format(
                            sql.Identifier(target_schema),
                            sql.Identifier(table_name),
                        ),
                        source_file,
                    )
        conn.commit()
        print("Schema and data load complete.")
    finally:
        conn.close()


def main() -> int:
    args = parse_args()
    env_path = Path(args.env_file).expanduser().resolve()
    ddl_file = Path(args.ddl_file).expanduser().resolve()
    data_dir = Path(args.data_dir).expanduser().resolve()

    if not ddl_file.exists():
        print(f"ERROR: DDL file not found: {ddl_file}", file=sys.stderr)
        return 1
    if not data_dir.exists():
        print(f"ERROR: Data directory not found: {data_dir}", file=sys.stderr)
        return 1

    connection_string = read_connection_string(env_path)
    conn_kwargs = connection_kwargs(connection_string)

    target_schema = re.sub(r"[^a-zA-Z0-9_]", "_", args.target_db)
    ensure_schema(target_schema, conn_kwargs)
    load_schema_and_data(target_schema, ddl_file, data_dir, conn_kwargs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
