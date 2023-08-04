// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Re-engagement', {
	new_contract_start_date(frm) {
        frm.fields_dict.new_contract_end_date.datepicker.update({
            minDate: frm.doc.new_contract_start_date ? new Date(frm.doc.new_contract_start_date) : null
        });
    },

    new_contract_end_date(frm) {
        frm.fields_dict.new_contract_start_date.datepicker.update({
            maxDate: frm.doc.new_contract_end_date ? new Date(frm.doc.new_contract_end_date) : null
        });
    },
	refresh: function(frm) {
		frm.set_query("employee", function () {
			return {
				filters:{
					"Status":"Active",
				}
			};
		})
	}
});
