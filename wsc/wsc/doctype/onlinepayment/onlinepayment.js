// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt
frappe.ui.form.on('OnlinePayment', {
	party: function(frm) {
		frappe.call({
			method:"wsc.wsc.doctype.onlinepayment.onlinepayment.get_outstanding_amount",
			args: {
				student: frm.doc.party
			},
			callback: function(r){
				// if(r.message){
					var result = r.message;
					frm.set_value("total_outstanding_amout",result);
					frm.set_value("paying_amount",result);
				// }
			}
		})
	}
});
frappe.ui.form.on('OnlinePayment', {
	refresh: function (frm) {
		var hdfcButton = frm.add_custom_button("By HDFC", function () {
			// alert(window.location.href)	
			frappe.call({
				
				method: "wsc.wsc.doctype.onlinepayment.onlinepayment.login",
				args: {
					party_name: frm.doc.party,
					roll_no: frm.doc.roll_no,
					amount: frm.doc.paying_amount,
					order_id: frm.doc.name,
					url: window.location.href
					
				},
				callback: function (r) {
					
					var encRequest = r.message["encRequest"];					
					var access_code = r.message["accessCode"];					
					var baseUrl = r.message["baseUrl"];	
					// alert(baseUrl)			

					var isLocalhost = baseUrl.includes("http");					
                    var isProd = baseUrl.includes("https");
				

				if (isLocalhost) {  

					window.location.href="https://test.ccavenue.com/transaction/transaction.do?command=initiateTransaction" + "&access_code=" + access_code + "&encRequest=" + encRequest;
                } else if (isProd) {
                    
					window.location.href="https://ccavenue.com/transaction/transaction.do?command=initiateTransaction" + "&access_code=" + access_code + "&encRequest=" + encRequest;
                } else {
                    
                    // window.open("https://test.ccavenue.com/transaction/transaction.do?command=initiateTransaction" + "&access_code=" + access_code + "&encRequest=" + encRequest);
					alert("Invalid Request. Please contact administrator.");
                }

				
				
				}
			});
		}, "Online Payment");

		hdfcButton.css({ 'color': 'black', 'background-color': 'white', 'font-weight': 'normal' });

		var axisButton = frm.add_custom_button("By Axis", function () {
			// HAve to add the logic for Axis payment here
			
			alert("axisButton clicked")
		}, "Online Payment");

		axisButton.css({ 'color': 'black', 'background-color': 'white', 'font-weight': 'normal' });
	}
});



frappe.ui.form.on('OnlinePayment', {
	refresh(frm) {

		if (frm.is_new() && frm.doc.docstatus === 0) {
			// frm.remove_custom_button('Online Payment');
			frm.remove_custom_button('By HDFC', 'Online Payment');
			frm.remove_custom_button('By Axis', 'Online Payment');
		}

		if (!frm.is_new() && frm.doc.docstatus === 0) {
			$('.primary-action').prop('disabled', true);
		}

		if (!frm.is_new() && frm.doc.docstatus === 1) {
			// frm.remove_custom_button('Online Payment');
			frm.remove_custom_button('By HDFC', 'Online Payment');
			frm.remove_custom_button('By Axis', 'Online Payment');
		}
		if (!frm.is_new() && frm.doc.docstatus === 0 && frm.doc.transaction_id != undefined) {
			$('.primary-action').prop('disabled', false);

			if (!frm.is_new() && frm.doc.docstatus === 0 && frm.doc.transaction_status != undefined) {
				// frm.remove_custom_button('Online Payment');
				frm.remove_custom_button('By HDFC', 'Online Payment');
			    frm.remove_custom_button('By Axis', 'Online Payment');
			}
		}

		if (!frm.is_new() && frm.doc.docstatus === 1) {
			frm.page.btn_secondary.hide();
		}

	}
});
frappe.ui.form.on("OnlinePayment", "refresh", function (frm) {
	frm.set_df_property("amount", "read_only", frm.is_new() ? 0 : 1);
	frm.set_df_property("name1", "read_only", frm.is_new() ? 0 : 1);
	frm.set_df_property("roll_no", "read_only", frm.is_new() ? 0 : 1);
});








