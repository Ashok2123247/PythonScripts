# Basic Script 

## Find the SQL Service Status only for Default instance
import psutil

def check_service_status(service_name="MSSQLSERVER"):
    for service in psutil.win_service_iter():
        if service.name() == service_name:
            print(f"Service: {service.name()}")
            print(f"Status: {service.status()}")
            return
    print(f"Service '{service_name}' not found.")

if __name__ == "__main__":
   check_service_status()
   



## find the disk space on current system
import psutil

def check_disk_space():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        print(f"Drive: {partition.device}")
        print(f"Total Space: {usage.total / (1024**3):.2f} GB")
        print(f"Free Space: {usage.free / (1024**3):.2f} GB")
        print(f"Used Space: {usage.used / (1024**3):.2f} GB\n")
        return usage
if __name__ == "__main__":
    check_disk_space()
    

## Database health check on SQL Server
import pyodbc
import pandas as pd

def connect_to_sql(server, database):
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        )
        print(f"Connected to database: {database}")
        return conn
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def check_db_status(conn):
    query = "SELECT name, state_desc FROM sys.databases"
    df = pd.read_sql_query(query, conn)
    print(df)
    df.to_excel("db_status.xlsx", index=False)
    print("Database status saved to Excel.")

if __name__ == "__main__":
    server = 'WIN-O2Q4BM3O2QL'
    database = 'master'
    connection = connect_to_sql(server, database)
    if connection:
        check_db_status(connection)
        connection.close()
        
        
 ## Disply in html format
 import pandas as pd

def generate_html_report(data, file_name="report.html"):
    html_content = data.to_html()
    with open(file_name, "w") as file:
        file.write(html_content)
    print(f"HTML report saved as {file_name}")

if __name__ == "__main__":
    # Example usage
    data = pd.DataFrame({
        'Database': ['master', 'tempdb'],
        'Status': ['ONLINE', 'ONLINE']
    })
    generate_html_report(data)
