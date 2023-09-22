// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Third Party Attendance Contract', {
	setup: function (frm) {
		frm.set_query("contract", function () {
			return {
				filters: [
					["Contract", "docstatus", "=", 1],
					["Contract", "is_signed", "=", 1],
				]
			}
		});
	},
	end_date: function(frm) {

		const startDate = new Date(frm.doc.start_date);
		const endDate = new Date(frm.doc.end_date);


			const timeDiff = endDate - startDate;

			const daysDiff = Math.ceil(timeDiff / (1000 * 60 * 60 * 24)) + 1;
	
			frm.set_value("total_days", daysDiff)


	}
});
