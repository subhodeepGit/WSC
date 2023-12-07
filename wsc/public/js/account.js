frappe.ui.form.on('Account', {
    add_toolbar_buttons: function(frm) {
		if(frappe.user.has_role(["Accounts User",,"Accounts Manager","Student"]) && !frappe.user.has_role(["Education Administrator"])){
  			frm.remove_custom_button('Convert to Group','Actions');
              frm.remove_custom_button('Chart of Accounts','View');
        }
	},
  update_account_number: function(frm) {
		var d = new frappe.ui.Dialog({
			title: __('Update Account Number / Name'),
			fields: [
				{
					"label": "Account Name",
					"fieldname": "account_name",
					"fieldtype": "Data",
					"reqd": 1,
					"default": frm.doc.account_name
				},
				{
					"label": "Account Number",
					"fieldname": "account_number",
					"fieldtype": "Data",
					"default": frm.doc.account_number
				}
			],
			primary_action: function() {       
				var data = d.get_values();
				// Validation to check if account_number contains only digits
				var accountNumberPattern = /^\d+$/;
				if (!accountNumberPattern.test(data.account_number)) {
					frappe.throw(__("Account Number should contain only digits."));
					return;
				}

				if(data.account_number === frm.doc.account_number && data.account_name === frm.doc.account_name) {
					d.hide();
					return;
				}
				
				frappe.call({
					method: "erpnext.accounts.doctype.account.account.update_account_number",
					args: {
						account_number: data.account_number,
						account_name: data.account_name,
						name: frm.doc.name
					},
					callback: function(r) {
						if(!r.exc) {
							if(r.message) {
								frappe.set_route("Form", "Account", r.message);
							} else {
								frm.set_value("account_number", data.account_number);
								frm.set_value("account_name", data.account_name);
							}
							d.hide();
						}
					}
				});
			},
			primary_action_label: __('Update')
		});
		d.show();
	}
}
);