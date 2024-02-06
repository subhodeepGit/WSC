import frappe

@frappe.whitelist()
def getChartData():
    return([25,28,29,30])