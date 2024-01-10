import frappe

def validate(doc, metyhod):
    
    if not doc.bank_account_no.isdigit():
        frappe.throw("Invalid Account No.")
    if len(str(doc.bank_account_no)) > 20:
        frappe.throw("Account No. should not have more than 20 digits.")
    if not doc.bank_name.isalpha():
        frappe.throw("Bank Name can only contains alphabets.")
    if len(str(doc.bank_name)) > 20:
        frappe.throw("Bank Name is too large.")
    if doc.earnings:
        for i in doc.earnings:
            if i.amount < 0:
                frappe.throw("Earning amount can not be less than 0")
            if len(str(i.amount)) > 12:
                frappe.throw("Earning amount is too large.")
        ee = []
        for i in doc.earnings:
            ee.append(i.salary_component)
        for i in range(len(ee)-1):
            for j in range(i+1, len(ee)):
                if ee[i] == ee[j]:
                    frappe.throw("One type of Salary Component should be only once.")
    if doc.deductions:
        for j in doc.deductions:
            if j.amount < 0:
                frappe.throw("Deduction amount can not be less than 0")
            if len(str(j.amount)) > 12:
                frappe.throw("Deduction amount is too high.")
        dd = []
        for i in doc.deductions:
            dd.append(i.salary_component)
        for i in range(len(dd)-1):
            for j in range(i+1, len(dd)):
                if dd[i] == dd[j]:
                    frappe.throw("One type of Salary Component should be only once.")