import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=master;"  # or 'WarehouseDB' if you created that
    "UID=sa;"
    "PWD=YourStrong!Passw0rd"
)

try:
    conn = pyodbc.connect(conn_str, timeout=5)
    print("✅ Connection to SQL Server successful!")
    conn.close()
except Exception as e:
    print(f"❌ Failed to connect: {e}")