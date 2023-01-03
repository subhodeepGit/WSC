// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Fees Receivable"] = {
	"filters": [
	{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"report_date",
			"label": __("Posting Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
	// 	{
	// 		"fieldname":"finance_book",
	// 		"label": __("Finance Book"),
	// 		"fieldtype": "Link",
	// 		"options": "Finance Book"
	// 	},
	// 	{
	// 		"fieldname":"cost_center",
	// 		"label": __("Cost Center"),
	// 		"fieldtype": "Link",
	// 		"options": "Cost Center",
	// 		get_query: () => {
	// 			var company = frappe.query_report.get_filter_value('company');
	// 			return {
	// 				filters: {
	// 					'company': company
	// 				}
	// 			};
	// 		}
	// 	},
		{
			"fieldname":"student",
			"label": __("Student"),
			"fieldtype": "Link",
			"options": "Student",
			on_change: () => {
				var student = frappe.query_report.get_filter_value('student');
				var company = frappe.query_report.get_filter_value('company');
				if (student) {
					frappe.db.get_value('Student', student, ["tax_id", "student_name", "payment_terms"], function(value) {
						frappe.query_report.set_filter_value('tax_id', value["tax_id"]);
						frappe.query_report.set_filter_value('student_name', value["student_name"]);
						frappe.query_report.set_filter_value('payment_terms', value["payment_terms"]);
					});

					// frappe.db.get_value('Customer Credit Limit', {'parent': customer, 'company': company},
					// 	["credit_limit"], function(value) {
					// 	if (value) {
					// 		frappe.query_report.set_filter_value('credit_limit', value["credit_limit"]);
					// 	}
					// }, "Customer");
				} else {
					frappe.query_report.set_filter_value('tax_id', "");
					frappe.query_report.set_filter_value('student_name', "");
					// frappe.query_report.set_filter_value('credit_limit', "");
					frappe.query_report.set_filter_value('payment_terms', "");
				}
			}
		},
		{
			"fieldname":"ageing_based_on",
			"label": __("Ageing Based On"),
			"fieldtype": "Select",
			"options": 'Posting Date\nDue Date',
			"default": "Due Date"
		},
		{
			"fieldname":"range1",
			"label": __("Ageing Range 1"),
			"fieldtype": "Int",
			"default": "30",
			"reqd": 1
		},
		{
			"fieldname":"range2",
			"label": __("Ageing Range 2"),
			"fieldtype": "Int",
			"default": "60",
			"reqd": 1
		},
		{
			"fieldname":"range3",
			"label": __("Ageing Range 3"),
			"fieldtype": "Int",
			"default": "90",
			"reqd": 1
		},
		{
			"fieldname":"range4",
			"label": __("Ageing Range 4"),
			"fieldtype": "Int",
			"default": "120",
			"reqd": 1
		},
		// {
	// 		"fieldname":"customer_group",
	// 		"label": __("Customer Group"),
	// 		"fieldtype": "Link",
	// 		"options": "Customer Group"
	// 	},
	// 	{
	// 		"fieldname":"payment_terms_template",
	// 		"label": __("Payment Terms Template"),
	// 		"fieldtype": "Link",
	// 		"options": "Payment Terms Template"
	// 	},
	// 	{
	// 		"fieldname":"sales_partner",
	// 		"label": __("Sales Partner"),
	// 		"fieldtype": "Link",
	// 		"options": "Sales Partner"
	// 	},
	// 	{
	// 		"fieldname":"sales_person",
	// 		"label": __("Sales Person"),
	// 		"fieldtype": "Link",
	// 		"options": "Sales Person"
	// 	},
	// 	{
	// 		"fieldname":"territory",
	// 		"label": __("Territory"),
	// 		"fieldtype": "Link",
	// 		"options": "Territory"
	// 	},
		{
			"fieldname": "group_by_student",
			"label": __("Group By Student"),
			"fieldtype": "Check"
		},
	// 	{
	// 		"fieldname":"based_on_payment_terms",
	// 		"label": __("Based On Payment Terms"),
	// 		"fieldtype": "Check",
	// 	},
	// 	{
	// 		"fieldname":"show_future_payments",
	// 		"label": __("Show Future Payments"),
	// 		"fieldtype": "Check",
	// 	},
	// 	{
	// 		"fieldname":"show_delivery_notes",
	// 		"label": __("Show Linked Delivery Notes"),
	// 		"fieldtype": "Check",
	// 	},
	// 	{
	// 		"fieldname":"show_sales_person",
	// 		"label": __("Show Sales Person"),
	// 		"fieldtype": "Check",
	// 	},
		{
			"fieldname":"tax_id",
			"label": __("Tax Id"),
			"fieldtype": "Data",
			"hidden": 1
		},
		{
			"fieldname":"student_name",
			"label": __("Student Name"),
			"fieldtype": "Data",
			"hidden": 1
		},
		{
			"fieldname":"payment_terms",
			"label": __("Payment Tems"),
			"fieldtype": "Data",
			"hidden": 1
		},
	// 	{
	// 		"fieldname":"credit_limit",
	// 		"label": __("Credit Limit"),
	// 		"fieldtype": "Currency",
	// 		"hidden": 1
	// 	}

	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.bold) {
			value = value.bold();

		}
		return value;
	},

};
