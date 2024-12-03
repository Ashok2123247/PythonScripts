import pyodbc
import psutil
import pandas as pd
from sqlalchemy import create_engine

# Connect to SQL Server
def create_sqlalchemy_engine(server, database, driver):
    try:
        connection_string = f"mssql+pyodbc://@{server}/{database}?driver={driver}&trusted_connection=yes"
        conn = create_engine(connection_string)
        return conn
    except Exception as e:
        print(f"Error connecting to SQL Server: {e}")
        return None

# Get Database Status
def get_db_status(conn):
    query = "SELECT name, state_desc FROM sys.databases"
    return pd.read_sql_query(query, conn)

# Check SQL Services Status using psutil
def get_sql_services():
    services_list = []
    for service in psutil.win_service_iter():
        service_name = service.name()
        if service_name.startswith("MSSQL$") or service_name == "MSSQLSERVER":
            services_list.append({
                "Service Name": service_name,
                "Display Name": service.display_name(),
                "Status": service.status().capitalize(),
                "Startup Type": service.start_type().capitalize()
            })
        elif service_name.startswith("SQLAgent$") or service_name == "SQLSERVERAGENT":
            services_list.append({
                "Service Name": service_name,
                "Display Name": service.display_name(),
                "Status": service.status().capitalize(),
                "Startup Type": service.start_type().capitalize()
            })
    return pd.DataFrame(services_list)

# Disk Information
def check_disk_space():
    partitions = psutil.disk_partitions()
    drives_list = []
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            drives_list.append({
                "Drive": partition.device,
                "Total Space (GB)": f"{usage.total / (1024**3):.2f}",
                "Free Space (GB)": f"{usage.free / (1024**3):.2f}",
                "Used Space (GB)": f"{usage.used / (1024**3):.2f}",
                "Usage (%)": f"{usage.percent}%"
            })
        except PermissionError:
            continue
    return pd.DataFrame(drives_list)

# Generate HTML Report
def generate_html_report(db_status, services_df, drives_df):
    html_content = """
    <html>
    <head>
        <title>Server Health Report</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #ffffff; }
            .container { width: 90%; margin: auto; padding: 20px; }
            .header { text-align: center; background-color: #333; color: white; padding: 10px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 10px; text-align: left; border: 1px solid #ddd; }
            th { background-color: #444; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            .status-running { color: green; font-weight: bold; }
            .status-stopped { color: red; font-weight: bold; }
            .online { color: green; font-weight: bold; }
            .offline { color: red; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Server Health Report</h1>
            </div>
            
            <h2>Database Status</h2>
            <table>
                <tr><th>Database Name</th><th>Status</th></tr>
    """
    # Add database status rows
    for index, row in db_status.iterrows():
        status_class = "online" if row['state_desc'] == "ONLINE" else "offline"
        html_content += f"""
        <tr>
            <td>{row['name']}</td>
            <td class="{status_class}">{row['state_desc']}</td>
        </tr>
        """
    
    # Add SQL services status
    html_content += """
            </table>
            <h2>SQL Services Status</h2>
            <table>
                <tr><th>Service Name</th><th>Display Name</th><th>Startup Type</th><th>Status</th></tr>
    """
    for index, row in services_df.iterrows():
        status_class = "status-running" if row['Status'] == "Running" else "status-stopped"
        html_content += f"""
        <tr>
            <td>{row['Service Name']}</td>
            <td>{row['Display Name']}</td>
            <td>{row['Startup Type']}</td>
            <td class="{status_class}">{row['Status']}</td>
        </tr>
        """

    # Add Disk Space Information
    html_content += """
            </table>
            <h2>Disk Space Information</h2>
            <table>
                <tr><th>Drive</th><th>Total Space (GB)</th><th>Free Space (GB)</th><th>Used Space (GB)</th><th>Usage (%)</th></tr>
    """
    for index, row in drives_df.iterrows():
        html_content += f"""
        <tr>
            <td>{row['Drive']}</td>
            <td>{row['Total Space (GB)']}</td>
            <td>{row['Free Space (GB)']}</td>
            <td>{row['Used Space (GB)']}</td>
            <td>{row['Usage (%)']}</td>
        </tr>
        """
    
    html_content += """
            </table>
        </div>
    </body>
    </html>
    """

    # Write to HTML file
    with open("server_health_report.html", "w") as file:
        file.write(html_content)
    print("HTML report generated: server_health_report.html")

# Main Function
if __name__ == "__main__":
    server = 'WIN-O2Q4BM3O2QL'
    database = 'master'
    driver = 'ODBC Driver 17 for SQL Server'
    
    # Connect to SQL Server
    connection = create_sqlalchemy_engine(server, database, driver)
    
    if connection:
        db_status = get_db_status(connection)
        services_df = get_sql_services()
        drives_df = check_disk_space()
        generate_html_report(db_status, services_df, drives_df)
    else:
        print("Failed to connect to the SQL Server.")
