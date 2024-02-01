import frappe

def validate(self, method):
    for t in self.percentages:
        if t.percentage_allocation<=0:
            frappe.throw("Percentage Allocation can't be -ve or Zero for the Month of <b>%s</b>"%(t.month))