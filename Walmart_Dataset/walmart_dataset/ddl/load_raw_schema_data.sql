-- Load CSV files into the raw schema in walmart_db using psql \copy
CREATE SCHEMA IF NOT EXISTS raw;
SET search_path = raw;

\copy customers FROM '../data/customers.csv' WITH CSV HEADER
\copy stores FROM '../data/stores.csv' WITH CSV HEADER
\copy products FROM '../data/products.csv' WITH CSV HEADER
\copy employees FROM '../data/employees.csv' WITH CSV HEADER
\copy orders FROM '../data/orders.csv' WITH CSV HEADER
\copy order_items FROM '../data/order_items.csv' WITH CSV HEADER
