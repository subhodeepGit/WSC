# database_operations.py

import os
import json
import pymysql
import frappe

def fetch_and_process_data(site_name):
    username = os.getenv('USER')
    # username ='erpnext'
    # Construct the file paths
    site_config_file_path = os.path.join("/home", username, "frappe-bench", "sites", site_name, "site_config.json")
   
    db_name_file_path = os.path.join("/home", username, "frappe-bench", "apps", "wsc", "wsc", "wsc", "doctype", "onlinepayment", "db_name.txt")
  
    try:
        # Read the site configuration
        with open(site_config_file_path, "r") as config_file:
            config_data = json.load(config_file)
        db_name = config_data["db_name"]
        
        
        # Write the db_name to the file
        with open(db_name_file_path, "w") as db_name_file:
            db_name_file.write(db_name)
           
            
        # Connect to the database
        conn = pymysql.connect(
            host="localhost",
            user="integration",
            password="erp@123",
            database=db_name)
        c = conn.cursor()
        return c

    except Exception as e:
        print(f"Error processing data for site {site_name}: {e}")
        return None

if __name__ == "__main__":
    site_names = frappe.get_all("Site", filters={"enabled": 1}, pluck="name")
   
    for site_name in site_names:
        if site_name == "site_name_1":
            # Process data for site_name_1
            cursor = fetch_and_process_data(site_name)
            if cursor:
                
                pass  
        elif site_name == "erp.soulunileaders.com":
            # Process data for site_name_2
            cursor = fetch_and_process_data(site_name)
            if cursor:
              
                pass 
        else:
            # Default data processing for other sites
            cursor = fetch_and_process_data(site_name)
            if cursor:
               
                pass  
