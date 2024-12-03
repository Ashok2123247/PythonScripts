import pyodbc
import datetime

# SQL Server connection details
server = 'your_server'
database = 'master'
username = 'your_username'
password = 'your_password'

connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

def fetch_data(query):
    """Fetch data from the database using the provided query."""
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

def check_service_status():
    """Get SQL Server and Agent service status."""
    query = """
    SELECT servicename, status_desc = 
    CASE status 
        WHEN 4 THEN 'Running'
        ELSE 'Stopped'
    END
    FROM sys.dm_server_services;
    """
    return fetch_data(query)

def get_database_status():
    """Retrieve database status with compatibility level."""
    query = """
    SELECT name, state_desc, compatibility_level 
    FROM sys.databases;
    """
    return fetch_data(query)

def get_disk_info():
    """Retrieve disk space information."""
    query = """
    EXEC xp_fixeddrives;
    """
    return fetch_data(query)

def get_top_blockers():
    """Retrieve top blocking sessions."""
    query = """
    SELECT blocking_session_id, session_id, wait_type, wait_time, status
    FROM sys.dm_exec_requests
    WHERE blocking_session_id > 0;
    """
    return fetch_data(query)

def get_top_queries():
    """Get top CPU-consuming queries."""
    query = """
    SELECT TOP 5 total_worker_time/1000 AS CPU_MS, text
    FROM sys.dm_exec_query_stats
    CROSS APPLY sys.dm_exec_sql_text(sql_handle)
    ORDER BY total_worker_time DESC;
    """
    return fetch_data(query)

def get_missing_indexes():
    """Retrieve missing indexes details."""
    query = """
    SELECT * FROM sys.dm_db_missing_index_details;
    """
    return fetch_data(query)

def generate_html_report():
    """Generate HTML report based on the collected data."""
    service_status = check_service_status()
    database_status = get_database_status()
    disk_info = get_disk_info()
    top_blockers = get_top_blockers()
    top_queries = get_top_queries()
    missing_indexes = get_missing_indexes()
    
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html_content = f"""
    <html>
    <head>
        <title>Database Health Check Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .container {{ display: flex; flex-direction: column; }}
            .header {{ text-align: center; font-size: 24px; padding: 10px; }}
            .section {{ border: 2px solid black; padding: 10px; margin: 10px; }}
            .panel-container {{ display: flex; justify-content: space-around; }}
            .panel {{ width: 30%; padding: 10px; border: 2px solid black; }}
            .green {{ color: green; }}
            .red {{ color: red; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                Database Health Check Report<br>
                Server: {server}, Date: {current_date}
            </div>
            
            <div class="panel-container">
                <!-- Service Status -->
                <div class="panel">
                    <h3>Service Status</h3>
                    <ul>
                        {"".join([f"<li>{service[0]}: <span class='{('green' if service[1] == 'Running' else 'red')}'>{service[1]}</span></li>" for service in service_status])}
                    </ul>
                </div>
                
                <!-- Database Status -->
                <div class="panel">
                    <h3>Database Status</h3>
                    <table border="1">
                        <tr><th>Database</th><th>Status</th><th>Compatibility</th></tr>
                        {"".join([f"<tr><td>{db[0]}</td><td class='{('green' if db[1] == 'ONLINE' else 'red')}'>{db[1]}</td><td>{db[2]}</td></tr>" for db in database_status])}
                    </table>
                </div>
                
                <!-- Disk Info -->
                <div class="panel">
                    <h3>Disk Information</h3>
                    <ul>
                        {"".join([f"<li>Drive {disk[0]}: {disk[1]} MB free</li>" for disk in disk_info])}
                    </ul>
                </div>
            </div>
            
            <!-- Top Blockers, Queries, and Missing Indexes -->
            <div class="section">
                <h3>Top Blockers</h3>
                <ul>
                    {"".join([f"<li>Session {block[1]} blocking {block[0]}: {block[2]}, {block[4]}</li>" for block in top_blockers])}
                </ul>
                
                <h3>Top Running Queries</h3>
                <ul>
                    {"".join([f"<li>CPU Time: {query[0]} ms - {query[1]}</li>" for query in top_queries])}
                </ul>
                
                <h3>Missing Indexes</h3>
                <ul>
                    {"".join([f"<li>{index}</li>" for index in missing_indexes])}
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Save HTML report
    with open("database_health_report.html", "w") as file:
        file.write(html_content)
    print("Report generated: database_health_report.html")

# Execute the script
generate_html_report()
