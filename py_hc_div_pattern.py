import pandas
import datetime
import pyodbc
import psutil
import pandas as pd
from sqlalchemy import create_engine

# SQL Server connection details
server = 'WIN-O2Q4BM3O2QL'
database = 'master'
#username = 'ashok'

#connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"

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
    
    # Generate the HTML content with your custom stylesheet
    html_content = f"""
    <html>
    <head>
        <title>Database Health Check Report</title>
        <style>
            body {{background-color:#ffffff;}}
            .container {{width:90%; margin:auto; margin-top:20px;background-color:#999999;overflow:hidden; box-shadow: 10px 10px;padding-bottom:25px;}}
            .headerbox {{width:auto; padding:10px;padding-bottom:0px;background-color:#595659;vertical-align: center;}}
            .main {{background-color: #f9f9f9;padding: 20px;float: right;width: 70%;}}
            .left {{background-color: #999999;margin:5px;padding: 5px;float:left; width: 20%; }}
            .TABLE1 {{width:auto;font:0.8em/145% Segoe UI,helvetica,Segoe UI,Segoe UI;padding-bottom:10px;}}
            TABLE {{width:100%;border-width: 0px;border-style: solid;border-color: black;font:0.8em/145% Segoe UI,helvetica,Segoe UI,Segoe UI;padding: 2px;}}
            TH {{border-width: 1px;padding: 2px;border-style: solid;border-color: black;background-color:#007DB8;}}
            TD {{border-width: 1px;padding: 2px;border-style: solid;border-color: black;vertical-align: left;}}
            tr:nth-child(odd) {{ background-color:#F2F2F2;}}
            tr:nth-child(even) {{ background-color:#DDDDDD;}}
            .p1 {{font:15px; font-family:Segoe UI,helvetica,Segoe UI,Segoe UI;}}
            .footer {{clear:center;width:auto;padding:20px;font:0.9em/145% Segoe UI;margin:5px; text-align:center;vertical-align: center;}}
            .lefttable, td, th {{border: 0px;text-align: left;vertical-align: center;font:0.9em/145% Segoe UI,helvetica,Segoe UI,Segoe UI;}}
            .lefttable {{width: 100%;border-collapse: collapse;font:0.9em/145% Segoe UI,helvetica,Segoe UI,Segoe UI;}}
            .h4 {{color:black;}}
            @media screen and (max-width: 800px) {{.left, .main{{width: 90%;}}}}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="headerbox">
                <h2 class="h4">Database Health Check Report</h2>
                <p class="p1">Server: {server}, Date: {current_date}</p>
            </div>
            
            <div class="left">
                <h3>Service Status</h3>
                <ul class="lefttable">
                    {"".join([f"<li>{service[0]}: <span style='color:{'green' if service[1] == 'Running' else 'red'};'>{service[1]}</span></li>" for service in service_status])}
                </ul>
            </div>
            
            <div class="main">
                <h3>Database Status</h3>
                <table class="TABLE1">
                    <tr><th>Database</th><th>Status</th><th>Compatibility</th></tr>
                    {"".join([f"<tr><td>{db[0]}</td><td style='color:{'green' if db[1] == 'ONLINE' else 'red'};'>{db[1]}</td><td>{db[2]}</td></tr>" for db in database_status])}
                </table>
                
                <h3>Disk Information</h3>
                <table class="TABLE1">
                    <tr><th>Drive</th><th>Free Space (MB)</th></tr>
                    {"".join([f"<tr><td>{disk[0]}</td><td>{disk[1]}</td></tr>" for disk in disk_info])}
                </table>

                <h3>Top Blockers</h3>
                </table>
                <table class="TABLE1">
                    <tr><th>blocking_session_id</th><th>session_id</th><th>wait_type</th><th>wait_time</th><th>status</th></tr>
                    {"".join([f"<tr><td>{blocker[0]}</td><td>{blocker[1]}</td><td>{blocker[2]}</td><td>{blocker[3]}</td><td>{blocker[4]}</td></tr>" for blocker in top_blockers])}
                </table>

                <h3>Top Running Queries</h3>
                <table class="TABLE1">
                    <tr><th>CPU_MS</th><th>Text</th></tr>
                    {"".join([f"<tr><td>{query[0]}</td><td>{query[1]}</td></tr>" for query in top_queries])}
                </table>
                <table class="TABLE1">
                    <tr><th>index_handle</th><th>database_id</th><th>object_id</th><th>equality_columns</th><th>inequality_columns</th><th>included_columns</th><th>statement</th></tr>
                    {"".join([f"<tr><td>{index[0]}</td><td>{index[1]}</td><td>{index[2]}</td><td>{index[3]}</td><td>{index[4]}</td><td>{index[5]}</td></tr>" for index in missing_indexes])}
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Remove zero-width spaces if any
    html_content = html_content.replace('\u200b', '')

    # Save HTML report with UTF-8 encoding
    with open("database_health_report.html", "w", encoding='utf-8') as file:
        file.write(html_content)
    print("Report generated: database_health_report.html")

# Execute the script
generate_html_report()
