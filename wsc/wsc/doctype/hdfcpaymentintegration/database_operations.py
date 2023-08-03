# database_operations.py

import os
import json
import pymysql
import frappe

def fetch_and_process_data():
    # Fetch username
    username = os.getenv('USER')
    print("Username:", username)

    # Fetch site name
    site_name = frappe.local.site
    print("Current site name:", site_name)

    # Construct site_config.json file path
    file_path = os.path.join("/home", username, "frappe-bench", "sites", site_name, "site_config.json")

    # Read the JSON content from the file
    with open(file_path, "r") as file:
        config_data = json.load(file)

    # Fetch the value of "db_name"
    db_name = config_data["db_name"]
    print("db_name:", db_name)

    # Construct db_name.txt file path
    file_path = os.path.join("/home", username, "frappe-bench", "apps", "wsc", "wsc", "wsc", "doctype", "hdfcpaymentintegration", "db_name.txt")

    # Open the file for writing
    with open(file_path, "w") as file:
        file.write(db_name)

    print("\n\n\n\n")
    print("db_name.txt created and written with db_name:", db_name)

    # Connect to the database and fetch integration data
    try:
        conn = pymysql.connect(
            host="localhost",
            user="hdfctest",
            password="India@1234",
            database=db_name)
        c = conn.cursor()
        return c

    except pymysql.Error as e:
        print("Error connecting to the database:", e)

# Run the fetch_and_process_data function when the file is executed directly
if __name__ == "__main__":
    fetch_and_process_data()
