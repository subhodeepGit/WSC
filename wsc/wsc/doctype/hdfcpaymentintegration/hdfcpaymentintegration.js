// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

//Created By :Rupali_Bhatta : 17-07-2023
frappe.ui.form.on("HdfcPaymentIntegration", {
	refresh: function (frm) {
		var hdfcButton = frm.add_custom_button("By HDFC", function () {
			
			frappe.call({
				
				method: "wsc.wsc.doctype.hdfcpaymentintegration.hdfcpaymentintegration.login",
				args: {
					party_name: frm.doc.name1,
					roll_no: frm.doc.roll_no,
					amount: frm.doc.amount,
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

					window.open("https://test.ccavenue.com/transaction/transaction.do?command=initiateTransaction" + "&access_code=" + access_code + "&encRequest=" + encRequest);
                } else if (isProd) {
                    
					window.open("https://ccavenue.com/transaction/transaction.do?command=initiateTransaction" + "&access_code=" + access_code + "&encRequest=" + encRequest);
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



frappe.ui.form.on('HdfcPaymentIntegration', {
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
frappe.ui.form.on("HdfcPaymentIntegration", "refresh", function (frm) {
	frm.set_df_property("amount", "read_only", frm.is_new() ? 0 : 1);
	frm.set_df_property("name1", "read_only", frm.is_new() ? 0 : 1);
	frm.set_df_property("roll_no", "read_only", frm.is_new() ? 0 : 1);
});








