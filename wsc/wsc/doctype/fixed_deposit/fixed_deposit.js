// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fixed Deposit', {
	refresh: function(frm){
		frm.set_df_property('tenure_days', 'depends_on','eval:doc.interest_payable=="Days"');
		frm.set_df_property('tenurein_months', 'depends_on','eval:doc.interest_payable=="Months"');
		frm.set_df_property('tenurein_weeks', 'depends_on','eval:doc.interest_payable=="Weeks"');
		frm.set_df_property('tenurein_quarter', 'depends_on','eval:doc.interest_payable=="Quarterly"');
		frm.set_df_property('tenuresemi_annually', 'depends_on','eval:doc.interest_payable=="Semi-Annually"');
		frm.set_df_property('tenurein_annually', 'depends_on','eval:doc.interest_payable=="Annually"');
	},

	fd_start_date: function(frm) {
		frm.trigger("calculate_days")
		frm.trigger("calculate_months")
		frm.trigger("calculate_weeks")
		frm.trigger("calculate_quaters")
		frm.trigger("calculate_semiannually")
		frm.trigger("calculate_annually")
	},

	maturity_date: function(frm) {
		frm.trigger("calculate_days")
		frm.trigger("calculate_months")
		frm.trigger("calculate_weeks")
		frm.trigger("calculate_quaters")
		frm.trigger("calculate_semiannually")
		frm.trigger("calculate_annually")
	},

	calculate_days: function(frm) {
		const startDate = new Date(frm.doc.fd_start_date);
		const endDate = new Date(frm.doc.maturity_date);
		const timeDiff = endDate.getTime() - startDate.getTime();
		const days = Math.floor(timeDiff / (1000 * 3600 * 24));
		isNaN(days) ? frm.set_value("tenure_days",'') : frm.set_value("tenure_days",days);
	},

	calculate_months: function(frm){
		const startDate = new Date(frm.doc.fd_start_date);
		const endDate = new Date(frm.doc.maturity_date);
		var months;
		months = (endDate.getFullYear() - startDate.getFullYear()) * 12;
		months -= startDate.getMonth();
		months += endDate.getMonth();
		isNaN(months) ? frm.set_value("tenurein_months",'') : frm.set_value("tenurein_months",months);
	},

	calculate_weeks: function(frm){
		const startDate = new Date(frm.doc.fd_start_date);
		const endDate = new Date(frm.doc.maturity_date);
		var oneDay = 24 * 60 * 60 * 1000; // Number of milliseconds in a day
		var millisecondsDiff = Math.abs(endDate - startDate); // Difference in milliseconds
		var weeks = Math.floor(millisecondsDiff / (7 * oneDay)); // Difference in weeks
		isNaN(weeks) ? frm.set_value("tenurein_weeks",'') : frm.set_value("tenurein_weeks",weeks);
	},

	calculate_quaters: function(frm){
		const startDate = new Date(frm.doc.fd_start_date);
		const endDate = new Date(frm.doc.maturity_date);
		var quarters;
		quarters = (endDate.getFullYear() - startDate.getFullYear()) * 4;
		quarters -= Math.floor(startDate.getMonth() / 3);
		quarters += Math.floor(endDate.getMonth() / 3);  
		isNaN(quarters) ? frm.set_value("tenurein_quarter",'') : frm.set_value("tenurein_quarter",quarters);
	},
	calculate_semiannually: function(frm){
		const startDate = new Date(frm.doc.fd_start_date);
		const endDate = new Date(frm.doc.maturity_date);
		var monthsDiff = (endDate.getFullYear() - startDate.getFullYear()) * 12;
		monthsDiff += endDate.getMonth() - startDate.getMonth();
		var semiAnnually = Math.floor(monthsDiff / 6);
		isNaN(semiAnnually) ? frm.set_value("tenuresemi_annually",'') : frm.set_value("tenuresemi_annually",semiAnnually);
	},

	calculate_annually: function(frm){
		const startDate = new Date(frm.doc.fd_start_date);
		const endDate = new Date(frm.doc.maturity_date);
		var years;
		years = endDate.getFullYear() - startDate.getFullYear();
		if (endDate.getMonth() < startDate.getMonth() || (endDate.getMonth() === startDate.getMonth() && endDate.getDate() < startDate.getDate())) {
		  years--;
		}
		isNaN(years) ? frm.set_value("tenurein_annually",'') : frm.set_value("tenurein_annually",years);
	},

	get_amount:function(frm) {
		frappe.call({
			"method": "wsc.wsc.doctype.fixed_deposit.fixed_deposit.calculate_fd",
			args:{
				fd_amount:frm.doc.fd_amount,
				interest_payable:frm.doc.interest_payable,
				interest_type:frm.doc.interest_type,
				interest_rate:frm.doc.interest_percentage,
				days:frm.doc.tenure_days,
				weeks:frm.doc.tenurein_weeks,
				months:frm.doc.tenurein_months,
				quarterly:frm.doc.tenurein_quarter,
				semi_annually:frm.doc.tenuresemi_annually,
				annually:frm.doc.tenurein_annually

			},
			callback: function(r) {
				if (r.message){
					frm.refresh_field("maturity_amount")
					frm.set_value("maturity_amount",r.message)
					alert(JSON.stringify(r))
			// 		frappe.model.clear_table(frm.doc, 'class_wise_leave');
			// 		(r.message).forEach(element => {
			// 			var c = frm.add_child("class_wise_leave")
			// 			c.class_schedule_id=element.name
			// 			c.module_name=element.course_name
			// 			c.class=element.room_name
			// 			c.schedule_date=element.schedule_date
			// 			c.from_time=element.from_time
			// 			c.to_time=element.to_time
			// 			c.leave_applicability_check=element.check
			// 		});
			// 		frm.refresh_field("class_wise_leave")
				}
			}
		})
	},
});
