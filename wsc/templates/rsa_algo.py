import frappe
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import pymysql

@frappe.whitelist(allow_guest=True)
def rsa_gen_key():
    private_key=private_key_gen()
    public_key_pem_date=public_key_gen_pem(private_key)
    private_key_pem_date=private_key_gen_pem(private_key)
    sql=""" Insert into `rsa_data` (`public_key_pem_date`,`private_key_pem_date`,`flag`) values ('%s' , '%s',"1")"""%(public_key_pem_date,private_key_pem_date)
    c,conn=my_sql_conn()
    c.execute(sql)
    conn.commit()
    q = """SELECT LAST_INSERT_ID()"""
    c.execute(q)
    j = c.fetchall()
    rsa_No = int(j[0][0])
    c.close()
    return {"public_key_pem_date":public_key_pem_date,"rsa_no":rsa_No}


def private_key_gen():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return private_key

def public_key_gen_pem(private_key):
    public_key_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    return public_key_pem

def private_key_gen_pem(private_key):
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()
    return  private_key_pem


def my_sql_conn():
    conn = pymysql.connect(
    host="localhost",
    user="erpnext",
    password="erp@123",
    database="erpdb"
    )

    c=conn.cursor()
    return c,conn