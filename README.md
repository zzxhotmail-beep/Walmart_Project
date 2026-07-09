![Pipeline](https://cdn.jsdelivr.net/gh/zzxhotmail-beep/Walmart_Project@main/logo2.png)
# 🛍️ Walmart End-to-End Data Engineering Project

## 📌 Project Overview

This project demonstrates an end-to-end modern data engineering pipeline by integrating **Agentic Database, PostgreSQL, Amazon S3, Databricks, dbt, and Apache Airflow**.

The pipeline follows a **Medallion Architecture (Bronze → Silver → Gold)** to build a scalable data platform, including:

- Automated database schema generation using Agentic Database and GitHub Copilot
- Incremental data ingestion with CDC (Change Data Capture)
- Data transformation and modeling with dbt
- Metadata-driven pipeline development using Jinja templates
- Dimensional modeling with Star Schema
- Historical data tracking with SCD Type 2
- Workflow orchestration and scheduling using Apache Airflow

## 🏗️ Architecture Overview

```
CSV Files
    |
    v
Agentic Database
(Ghost Agentic DB + GitHub Copilot)
    |
    v
PostgreSQL Database
    |
    | CDC Incremental Load
    v
Databricks Bronze Layer
    |
    | dbt Transformation
    v
Databricks Silver Layer
    |
    | Dimensional Modeling
    v
Databricks Gold Layer
    |
    v
Analytics Ready Data Model

Apache Airflow
(Workflow Orchestration)
```

## 📷 Architecture Preview

![architecture](https://cdn.jsdelivr.net/gh/zzxhotmail-beep/Walmart_project@main/structure.jpg)

# 🛠️ Technology Stack

| Category | Tools |
|---|---|
| Database | PostgreSQL |
| AI Development | Ghost Agentic Database, GitHub Copilot |
| Cloud Storage | Amazon S3 |
| Data Platform | Databricks |
| Data Transformation | dbt |
| Programming | SQL, Python, Jinja |
| Data Architecture | Medallion Architecture, Star Schema |
| Data Processing | CDC, Incremental Load |
| Orchestration | Apache Airflow |
| Containerization | Docker |

# 🚀 Implementation Details

## 1. Agentic Database & Data Ingestion

The project first utilizes **Agentic Database** with Ghost Agentic DB and GitHub Copilot.

By providing natural language instructions to AI agents:

- PostgreSQL database schemas are automatically generated
- CSV datasets are loaded into PostgreSQL
- Corresponding tables are created automatically


Source datasets:

- customers
- employees
- order_items
- orders
- products
- stores

# 🥉 Bronze Layer - Data Ingestion

The Bronze Layer focuses on raw data ingestion.

## CDC-based Incremental Loading

Agentic Database CDC (Change Data Capture) is used to synchronize data from PostgreSQL into Databricks Bronze Schema.

Instead of reloading the entire dataset, CDC captures only changed records, improving ingestion efficiency.

Key components:

- PostgreSQL
- Databricks
- CDC
- Databricks Jobs
- Databricks Pipelines

# 🥈 Silver Layer - Data Transformation

The Silver Layer uses **dbt** for data transformation and data engineering workflows.

The dbt project is organized into:

```
models/
│
├── silver_technical/
│
└── silver_business/
```


## Silver Technical Layer

The technical layer performs standardization and data quality processing.

Implemented features:

- Added `current_timestamp()` column for data tracking
- Supported incremental loading
- Applied dbt tests for data quality validation

Data quality checks include:

- Duplicate detection
- NULL value validation


Example:

```
silver_technical/
│
├── customers_t.sql
├── employees_t.sql
├── orders_t.sql
├── products_t.sql
├── stores_t.sql
└── order_items_t.sql
```


## Silver Business Layer

The business layer implements a **metadata-driven pipeline**.

Using Jinja templates:

- Table names
- Table aliases
- Column information
- Join conditions

are stored inside configuration arrays (`configs`).

The pipeline dynamically generates SQL queries through loops and automatically creates multi-table LEFT JOIN transformations.

The final output combines six technical tables into:

**One Big Table (OBT)**


## dbt Macro

dbt Macro is used to automate schema creation.

Benefits:

- Reduce repetitive SQL code
- Improve pipeline maintainability
- Increase scalability

# 🥇 Gold Layer - Data Modeling

The Gold Layer focuses on business-ready analytical models.

A **Star Schema** is implemented for analytical workloads.

## SCD Type 2 Implementation

Using:

- dbt Snapshot
- dbt Ephemeral Models


Implemented dimension tables:

```
dim_customers
dim_employees
dim_orders
dim_products
dim_stores
```


SCD Type 2 enables:

- Historical data tracking
- Change history preservation
- Slowly changing dimension management

## Fact Table

A Fact Table is created to support:

- Business analytics
- Reporting
- Downstream data consumption

## dbt Ephemeral Models

Ephemeral models are used for intermediate transformations.

Characteristics:

- SQL is expanded during compilation
- No physical table or view is created in Databricks
- Reduces unnecessary storage

# 🔄 Workflow Orchestration with Apache Airflow

After completing the Bronze, Silver, and Gold layers, Apache Airflow is introduced for pipeline orchestration.

## Airflow Setup

- Built Airflow environment using Docker
- Configured DAG workflows
- Defined pipeline execution dependencies


Airflow manages:

- Scheduling
- Task orchestration
- Pipeline monitoring
- Automated execution

# 📂 Project Structure

```
project/
│
├── airflow/
│   ├── dags/
│   └── docker-compose.yml
│
├── dbt/
│   ├── models/
│   │   ├── silver_technical/
│   │   ├── silver_business/
│   │   └── gold/
│   │
│   ├── macros/
│   └── snapshots/
│
├── data/
│
└── README.md
```

# 🎯 Key Engineering Concepts Demonstrated

✅ Agentic Database Automation  
✅ CDC Incremental Data Loading  
✅ Databricks Medallion Architecture  
✅ dbt ELT Framework  
✅ Metadata-driven Pipeline Design  
✅ Jinja SQL Generation  
✅ dbt Macro Automation  
✅ Star Schema Modeling  
✅ SCD Type 2 Historical Tracking  
✅ Apache Airflow Orchestration  
✅ Docker-based Development Environment  

## 👤 Author - Zixuan Zhang

This project demonstrates my ability to build an end-to-end Data Engineering pipeline for Walmart retail data.

Key areas covered include Agentic Database, PostgreSQL, Amazon S3, Databricks, dbt, CDC (Change Data Capture), Metadata-Driven Pipelines, Data Quality Validation, Star Schema Modeling, SCD Type 2 implementation, and Apache Airflow orchestration.

The architecture follows modern data engineering best practices by implementing a Medallion Architecture (Bronze → Silver → Gold) and reflects commonly used technologies and patterns in scalable lakehouse data platforms.
- **LinkedIn**: [My Professional Profile](https://www.linkedin.com/in/zixuan-zhang-78ba38274)
