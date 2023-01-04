import frappe

@frappe.whitelist()
def get_fee_components(hostel_fee_structure):
    if hostel_fee_structure:
        fees = frappe.get_all("Fee Component", fields=["fees_category", "description", "amount","receivable_account",
                                                    "income_account","grand_fee_amount","outstanding_fees","waiver_type","percentage","waiver_amount",
                                                    "total_waiver_amount"] , 
                                                filters={"parent": hostel_fee_structure}, order_by= "idx asc")
        return fees