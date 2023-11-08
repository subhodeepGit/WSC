import frappe

def validate(self, method):
	for cd in self.items:
		if cd.price_list_rate < 0:
			frappe.throw("Price List Rate for Item cannot be negative")
			
            
	for cd in self.items:
		if cd.discount_percentage < 0:
			frappe.throw("Discount on Price List Rate (%) for Item cannot be negative")
			
	for cd in self.items:
		if cd.discount_amount < 0:
			frappe.throw("Discount Amount for Item cannot be negative")
			
	for cd in self.items:
		if cd.rate < 0:
			frappe.throw("Rate for Item cannot be negative")
			
	for cd in self.items:
		if cd.margin_rate_or_amount < 0:
			frappe.throw("Margin Rate or Amount for Item cannot be negative")
	if self.write_off_amount:
		if self.write_off_amount < 0:
			frappe.throw("Write off Amount cannot be negative")
	
	for cd in self.taxes:
		if cd.rate < 0:
			frappe.throw("Tax Rate cannot be negative")
			
	for cd in self.advances:
		if cd.allocated_amount < 0:
			frappe.throw("Allocated amount cannot be negative")
	for cd in self.payment_schedule:
		if cd.invoice_portion < 0:
			frappe.throw("Invoice Portion cannot be negative")
	for cd in self.payment_schedule:
		if cd.discount < 0:
			frappe.throw("Discount cannot be negative")
	for cd in self.payment_schedule:
		if cd.payment_amount < 0:
			frappe.throw("Payment Amount cannot be negative")
	for cd in self.payment_schedule:
		if cd.paid_amount < 0:
			frappe.throw("Paid Amount cannot be negative")