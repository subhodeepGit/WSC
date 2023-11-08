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
	for cd in self.items:
		if cd.margin_rate_or_amount < 0:
			frappe.throw("Margin Rate or Amount for Item cannot be negative")
	
	for cd in self.taxes:
		if cd.rate < 0:
			frappe.throw("Tax Rate cannot be negative")