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
// frappe.ui.form.on('OnlinePayment', {
// 	refresh: function (frm) {
// 		var hdfcButton = frm.add_custom_button("By HDFC", function () {
// 			// alert(window.location.href)	
// 			frappe.call({

// 				method: "wsc.wsc.doctype.onlinepayment.onlinepayment.login",
// 				args: {
// 					party_name: frm.doc.party,
// 					roll_no: frm.doc.roll_no,
// 					amount: frm.doc.paying_amount,
// 					order_id: frm.doc.name,
// 					url: window.location.href

// 				},
// 				callback: function (r) {

// 					var encRequest = r.message["encRequest"];					
// 					var access_code = r.message["accessCode"];					
// 					var baseUrl = r.message["baseUrl"];	
// 					alert(r.message)
// 					alert(baseUrl)			

// 					var isLocalhost = baseUrl.includes("http");					
//                     var isProd = baseUrl.includes("https");


// 				if (isLocalhost) {  

// 					window.location.href="https://test.ccavenue.com/transaction/transaction.do?command=initiateTransaction" + "&access_code=" + access_code + "&encRequest=" + encRequest;
//                 } else if (isProd) {

// 					window.location.href="https://ccavenue.com/transaction/transaction.do?command=initiateTransaction" + "&access_code=" + access_code + "&encRequest=" + encRequest;
//                 } else {

//                     // window.open("https://test.ccavenue.com/transaction/transaction.do?command=initiateTransaction" + "&access_code=" + access_code + "&encRequest=" + encRequest);
// 					alert("Invalid Request. Please contact administrator.");
//                 }



// 				}
// 			});
// 		}, "Online Payment");

// 		hdfcButton.css({ 'color': 'black', 'background-color': 'white', 'font-weight': 'normal' });

// 		var axisButton = frm.add_custom_button("By Axis", function () {
// 			// HAve to add the logic for Axis payment here

// 			alert("axisButton clicked")
// 		}, "Online Payment");

// 		axisButton.css({ 'color': 'black', 'background-color': 'white', 'font-weight': 'normal' });
// 	}
// });

frappe.ui.form.on('OnlinePayment', {
    refresh: function (frm) {
        frm.add_custom_button(__('By HDFC Payment Gateway <img src="data:image/png;base64,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B3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fBP/xHLPrHP/3xfgl6FOhRo0fBP/mnLPpnP/3xfgl6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiTHhV6FOhRo0eBHm3So0KPAj1q9CjQo016VOhRoEeNHgV6tEmPCj0K9KjRo0CPNulRoUeBHjV6FOjRJj0q9CjQo0aPAj3apEeFHgV61OhRoEeb9KjQo0CPGj0K9GiT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UaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhRoEeNHgEHehToUaNHwIEeBXrU6BFwoEeBHjV6BBzoUaBHjR4BB3oU6FGjR8CBHgV61OgRcKBHgR41egQc6FGgR40eAQd6FOhRo0fAgR4FetToEXCgR4EeNXoEHOhR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" alt="HDFC" style="width: 30px; height: 30px;">'), function () {
            frappe.call({
                method: "wsc.wsc.doctype.onlinepayment.onlinepayment.open_gateway",
                args: {
                    party_name: frm.doc.party_name,
                    roll_no: frm.doc.roll_no,
                    amount: frm.doc.paying_amount,
                    order_id: frm.doc.name,
                    url: window.location.href,
                    gw_provider: "hdfc"
                },
                callback: function (r) {
                    if (r.message) {
                        var encRequest = r.message["encRequest"];
                        var access_code = r.message["accessCode"];
                        var is_prod = r.message["is_prod"];
                        // alert(is_prod)
                        // alert(encRequest)
                        // alert(access_code)


                        if (is_prod == 1) {
                            // alert("1")
                            // window.location.href = "https://test.ccavenue.com/transaction/transaction.do?command=initiateTransaction" + "&access_code=" + access_code + "&encRequest=" + encRequest;

                            window.location.href = "https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction" + "&access_code=" + access_code + "&encRequest=" + encRequest;

                        } else {
                            // alert("2")

                            window.location.href = "https://test.ccavenue.com/transaction/transaction.do?command=initiateTransaction" + "&access_code=" + access_code + "&encRequest=" + encRequest;

                        }
                    } else {
                        alert("No response data received.");
                    }
                }
            });
        }, __('Click here for Online Payment'));

        frm.page.wrapper.find('button:contains("Click here for Online Payment")').addClass('btn-primary');

        // hdfcButton.css({ 'color': 'black', 'background-color': 'white', 'font-weight': 'normal' });

        // var axisButton = frm.add_custom_button("By Axis", function () {
        //     // HAve to add the logic for Axis payment here

        //     alert("axisButton clicked")
        // }, "Online Payment");

        // axisButton.css({ 'color': 'black', 'background-color': 'white', 'font-weight': 'normal' });
    }
});

frappe.ui.form.on('OnlinePayment', {
    refresh(frm) {

        if (frm.is_new() && frm.doc.docstatus === 0) {
            // frm.remove_custom_button('Online Payment');
            frm.remove_custom_button('By HDFC Payment Gateway', 'Click here for Online Payment');
            frm.remove_custom_button('By Axis', 'Click here for Online Payment');
        }

        if (!frm.is_new() && frm.doc.docstatus === 0) {
            $('.primary-action').prop('disabled', true);
        }

        if (!frm.is_new() && frm.doc.docstatus === 1) {
            // frm.remove_custom_button('Online Payment');
            frm.remove_custom_button('By HDFC Payment Gateway', 'Click here for Online Payment');
            frm.remove_custom_button('By Axis', 'Click here for Online Payment');
        }
        if (!frm.is_new() && frm.doc.docstatus === 0 && frm.doc.transaction_id != undefined) {
            $('.primary-action').prop('disabled', false);

            if (!frm.is_new() && frm.doc.docstatus === 0 && frm.doc.transaction_status != undefined) {
                // frm.remove_custom_button('Online Payment');
                frm.remove_custom_button('By HDFC Payment Gateway', 'Click here for Online Payment');
                frm.remove_custom_button('By Axis', 'Click here for Online Payment');
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








