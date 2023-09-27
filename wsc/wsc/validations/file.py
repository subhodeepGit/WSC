import frappe
import os
from frappe.utils import get_files_path


def validate(doc,method):
    file_size(doc)
    
def file_size(doc):
    # public_file_path = frappe.get_site_path('public', 'files', file_name) #./erp.soulunileaders.com/public/files/logo.png
    flag_session="No"
    if frappe.session.user!="Administrator":
        for t in frappe.get_roles(frappe.session.user):
            if t=="Student" or t=="Applicant" or t=="Provisionally admitted":
                flag_session="Yes"
    if flag_session=="Yes":
        base_path = os.path.realpath(get_files_path(is_private=doc.is_private))
        file_name=doc.file_url.split("/")[-1] 
        localFile = base_path+'/'+file_name 
        url=localFile 
        ext=os.path.splitext(url)
        extstr=ext[1] 
        ext_list=[".jpg",".jpeg",".jfif",".pjpeg",".pjp",".png",".pdf"]
        flag="No"
        for t in ext_list:
            if t==extstr:
                flag="Yes"
                file_size = os.path.getsize(url)
                if file_size > 200000:
                    os.remove(url)
                    return frappe.throw("Image Size cannot exceed 200KB. Please upload an Image of smaller size.")
        if flag=="No":
            os.remove(url)
            frappe.throw("File Type is not Allowed")        

