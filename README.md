
# JrDE ETL Project

This project is a simple ETL (Extract, Load, Transform and Warehousing) pipeline built for a Junior Data Engineer role.

It uses Python and Docker to:
- Extract data from a public API
- Store raw data in a PostgreSQL database
- Transform the data
- Load the final result into a SQL Server database

---

## 📦 What’s Included

- `docker-compose.yml` – runs PostgreSQL and MS SQL Server in containers
- `etl/` – contains Python code for each ETL step
- `requirements.txt` – Python dependencies
- `.env` – environment variables
- `README.md` – this file

---

## ⚙️ How to Set Up and Run

### 1. Clone the repository

```bash
git clone https://github.com/suryadeipreddyk/jrde-etl-pipeline.git
cd jrde-etl-pipeline
```

### 2. Check your `.env` file

This file stores database usernames and passwords.

---

### 3. Start the databases

This command will start PostgreSQL, SQL Server, and Adminer (a database viewer):

```bash
docker-compose up -d
```

You can open Adminer in your browser: [http://localhost:8080](http://localhost:8080)

---

### 4. Install Python packages

Activate the virtual environment and install packages:

```bash
source env/bin/activate
pip install -r requirements.txt
```

---

### 5. Run the pipeline

```bash
python etl/main.py
```

This will:
1. Download data from the API
2. Store it in PostgreSQL
3. Transform it
4. Load it into SQL Server

---

## 🔄 How the Pipeline Works

1. **Extract**: Gets user and post data from JSONPlaceholder API.
2. **Load to PostgreSQL**: Saves the raw data into 2 tables: `staging_users` and `staging_posts`.
3. **Transform**: Joins the two tables, selects useful columns.
4. **Load to SQL Server**: Saves the final result into `FactUserPosts`.

---

## 🧱 Tables Created

### 📌 PostgreSQL (staging_db)

#### `staging_users`

| Column        | Type    |
|---------------|---------|
| id            | INT     |
| name          | TEXT    |
| username      | TEXT    |
| email         | TEXT    |
| phone         | TEXT    |
| website       | TEXT    |
| street        | TEXT    |
| suite         | TEXT    |
| city          | TEXT    |
| zipcode       | TEXT    |
| company_name  | TEXT    |

#### `staging_posts`

| Column   | Type |
|----------|------|
| id       | INT  |
| userId   | INT  |
| title    | TEXT |
| body     | TEXT |

---

### 📌 SQL Server (warehouse_db)

#### `FactUserPosts`

| Column      | Type         |
|-------------|--------------|
| post_id     | INT          |
| post_title  | NVARCHAR(MAX)|
| post_body   | NVARCHAR(MAX)|
| user_name   | NVARCHAR(255)|
| user_email  | NVARCHAR(255)|

---

## 💡 Design Decisions

- Used Docker Compose to make setup easy
- Used `.env` file to protect sensitive info
- Stored raw data in PostgreSQL for transparency
- Final clean data goes to SQL Server for reporting
- Code is modular for each step (extract, load, transform)

---

## 🧪 Tools Used

- Python 3
- Docker
- PostgreSQL
- SQL Server
- Adminer
- JSONPlaceholder API

---

## 📬 How to Check the Output

You can view the final data in:

- **SQL Server**: Connect via Azure Data Studio or Adminer
- Run this query:

```sql
USE warehouse_db;
GO

SELECT TOP 10 * FROM FactUserPosts;
```

---

## 📁 Folder Summary

```
etl-pipeline/
├── etl/                 # Python ETL scripts
│   ├── extract.py
│   ├── load.py
│   ├── transform.py
│   ├── warehousing.py
│   └── main.py
├── docker-compose.yml   # Starts PostgreSQL & SQL Server
├── requirements.txt     # Python packages
├── .env                 # Database secrets (not in repo)
└── README.md            # This guide
```

---

## 🎉 That’s It!

You’ve now completed a full ETL pipeline using Docker and Python 🚀
