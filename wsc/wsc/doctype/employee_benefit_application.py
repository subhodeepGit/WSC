import frappe

def validate(doc,method):
    if doc.employee_benefits:
        print(doc.employee_benefits)
        for i in doc.employee_benefits:
            print(i)
            if i.amount<0:
                frappe.throw("Amount should not be less than 0")