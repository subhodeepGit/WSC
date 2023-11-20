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
        var btn_name = 'By HDFC Payment Gateway <img src="/assets/wsc/images/hdfc_logo.png" alt="HDFC" style="width: 30px; height: 30px;">'
        frm.add_custom_button(__(btn_name), function () {
            var formStatus = "Yes"
            if (!frm.is_new()){
                formStatus="No"
            }
            var formProgress=frm.doc.transaction_progress
            frappe.call({
                method: "wsc.wsc.doctype.onlinepayment.onlinepayment.open_gateway",
                args: {
                    party_name: frm.doc.party_name,
                    party: frm.doc.party,
                    amount: frm.doc.paying_amount,
                    order_id: frm.doc.name,
                    url: window.location.href,
                    gw_provider: "hdfc",
                    form_status:formStatus,
                    formProgress:formProgress
                },
                callback: function (r) {
                    if (r.message) {
                        var encRequest = r.message["encRequest"];
                        var access_code = r.message["accessCode"];
                        var is_prod = r.message["is_prod"];
                        if (is_prod == 1) {
                            window.location.href = "https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction" + "&access_code=" + access_code + "&encRequest=" + encRequest;

                        } else {
                            window.location.href = "https://test.ccavenue.com/transaction/transaction.do?command=initiateTransaction" + "&access_code=" + access_code + "&encRequest=" + encRequest;
                        }
                    } else {
                        alert("No response data received.");
                    }
                }
            });
        }, __('Click here for Online Payment'));

        frm.page.wrapper.find('button:contains("Click here for Online Payment")').addClass('btn-primary');


        //#################################### AXIS Button ########################################


        var axis_btn_name = 'By AXIS Payment Gateway &nbsp;&nbsp;<img src="/assets/wsc/images/axis_logo.png" alt="AXIS" style="width: 30px; height: 30px;" >'
        frm.add_custom_button(axis_btn_name, function () {
                var formStatus = "Yes"
                if (!frm.is_new()){
                    formStatus="No"
                }
                var formProgress=frm.doc.transaction_progress
                frappe.call({
                method: "wsc.wsc.doctype.onlinepayment.onlinepayment.open_gateway",
                args: {
                    party_name: frm.doc.party_name,
                    party: frm.doc.party,
                    amount: frm.doc.paying_amount,
                    order_id: frm.doc.name,
                    url: window.location.href,
                    gw_provider: "AXIS",
                    form_status:formStatus,
                    formProgress:formProgress
                },
                
                callback: function (r) {
                    if (r.message) {
                        var encRequest = r.message["encRequest"];
                        var access_code = r.message["accessCode"];
                        var is_prod = r.message["is_prod"];

                        if (is_prod == 1) {
                            window.location.href = "https://secure.ccavenue.com/transaction/transaction.do?command=initiateTransaction" + "&access_code=" + access_code + "&encRequest=" + encRequest;
                        } else {
                            window.location.href = "https://test.ccavenue.com/transaction/transaction.do?command=initiateTransaction" +  "&encRequest=" + encRequest +"&access_code=" + access_code;
                        }
                    } else {
                        alert("No response data received.");
                    }
                }
            });
        }, __('Click here for Online Payment'));

    }
});

frappe.ui.form.on('OnlinePayment', {
    refresh(frm) {
        var btn_name = 'By HDFC Payment Gateway <img src="/assets/wsc/images/hdfc_logo.png" alt="HDFC" style="width: 30px; height: 30px;">'
        var axis_btn_name = 'By AXIS Payment Gateway &nbsp;&nbsp;<img src="/assets/wsc/images/axis_logo.png" alt="AXIS" style="width: 30px; height: 30px;" >'
        if (frm.is_new() && frm.doc.docstatus === 0) {
            frm.remove_custom_button(btn_name, 'Click here for Online Payment');
            frm.remove_custom_button(axis_btn_name, 'Click here for Online Payment');
            frm.set_df_property('declaration', 'hidden', 1);
        }

        if (!frm.is_new() && frm.doc.docstatus === 0) {
            $('.primary-action').prop('disabled', true);
        }

        if (!frm.is_new() && frm.doc.docstatus === 1) {
            frm.remove_custom_button(btn_name, 'Click here for Online Payment');
            frm.remove_custom_button(axis_btn_name, 'Click here for Online Payment');
        }
        if (!frm.is_new() && frm.doc.docstatus === 0 && frm.doc.transaction_id != undefined) {
            $('.primary-action').prop('disabled', false);

            if (!frm.is_new() && frm.doc.docstatus === 0 && frm.doc.transaction_status != undefined) {
                frm.remove_custom_button(btn_name, 'Click here for Online Payment');
                frm.remove_custom_button(axis_btn_name, 'Click here for Online Payment');
            }
        }

        if (!frm.is_new() && frm.doc.docstatus === 1) {
            frm.page.btn_secondary.hide();
            frm.set_df_property('declaration', 'hidden', 0);
        }
        if (frm.doc.docstatus === 0 && frm.doc.transaction_progress === "Initiated") {
            frm.remove_custom_button(btn_name, 'Click here for Online Payment');
            frm.remove_custom_button(axis_btn_name, 'Click here for Online Payment');
        }

    }
});
frappe.ui.form.on("OnlinePayment", "refresh", function (frm) {
    frm.set_df_property("amount", "read_only", frm.is_new() ? 0 : 1);
    frm.set_df_property("name1", "read_only", frm.is_new() ? 0 : 1);
    // frm.set_df_property("roll_no", "read_only", frm.is_new() ? 0 : 1);
});