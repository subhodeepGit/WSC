import frappe

def validate(doc, method):
    if doc.base and doc.variable:
        if doc.base < 0 or doc.variable < 0:
            frappe.throw("Base / Variable Amount can not be less than 0.")
        if len(str(doc.base)) > 12 or len(str(doc.variable)) > 12:
            frappe.throw("Base / Variable Amount is too high.")
    if doc.payroll_cost_centers:
        cc = []
        for i in doc.payroll_cost_centers:
            cc.append(i.cost_center)
        for i in range(len(cc)-1):
            for j in range(i+1, len(cc)):
                if cc[i] == cc[j]:
                    frappe.throw("Cost Centers can not be same.")