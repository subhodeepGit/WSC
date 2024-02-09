import frappe

@frappe.whitelist()
def getCardData():
    return([25,28,29,30,89,95])


@frappe.whitelist()
def getChartData():
    return([25,28,29,30,89,95])

@frappe.whitelist()
def getTableData():
    return([25,28,29,30,89,95])