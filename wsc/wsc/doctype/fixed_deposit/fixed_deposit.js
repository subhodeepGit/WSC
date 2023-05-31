// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fixed Deposit', {
	maturity_date: function(frm) {
		// alert(frm.doc.fd_start_date)
		// alert(frm.doc.maturity_date)

		var startDateObj = new Date(frm.doc.fd_start_date);
  		var endDateObj = new Date(frm.doc.maturity_date);

		var dateDifference = endDateObj - startDateObj;

		var days = Math.floor(dateDifference / (1000 * 60 * 60 * 24));

		var years = Math.floor(days / 365);
		var months = Math.floor((days % 365) / 30);
		days = days % 30;
		var tenure = years + " years " + months + " months " + days + " days"

		// alert(tenure) 
		frm.set_value('fd_tenure', tenure)
		
	},
	fd_start_date: function(frm) {
		// alert(frm.doc.fd_start_date)
		// alert(frm.doc.maturity_date)

		var startDateObj = new Date(frm.doc.fd_start_date);
  		var endDateObj = new Date(frm.doc.maturity_date);

		var dateDifference = endDateObj - startDateObj;

		var days = Math.floor(dateDifference / (1000 * 60 * 60 * 24));

		// var years = Math.floor(days / 365);
		// var months = Math.floor((days % 365) / 30);
		var months = Math.floor(days / 30); // Assuming each month has 30 days
		var years = Math.floor(months / 12);
		days %= 30;
		months %= 12;
		var tenure = years + " years " + months + " months " + days + " days"

		// alert(tenure) 
		if (tenure != "NaN years NaN months NaN days"){
		frm.set_value('fd_tenure', tenure)
		}
	}
});
