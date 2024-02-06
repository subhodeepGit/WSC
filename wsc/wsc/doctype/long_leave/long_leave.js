// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Long Leave', {
	setup: function (frm) {
		frm.set_query("allotment_number", function() {
			return {
				query: "wsc.wsc.doctype.room_change.room_change.ra_query"
			};
		});
		// frm.set_value('data_11', 'Problem not Resolved')
	},
	medium_of_communicatinon: function(frm){
		if(frm.doc.medium_of_communicatinon=="Telephone"){
			frm.set_value("email_attachment", "");
			frm.set_value("email_id", "");
			frm.set_value("address_line_1", "");
			frm.set_value("address_line_2", "");
			frm.set_value("pincode", "");
			frm.set_value("city", "");
			frm.set_value("state", "");
			frm.set_value("letter_attacmnent", "");
        }else if(frm.doc.medium_of_communicatinon=="Email"){
			frm.set_value("phone_no", "");
			frm.set_value("address_line_1", "");
			frm.set_value("address_line_2", "");
			frm.set_value("pincode", "");
			frm.set_value("city", "");
			frm.set_value("state", "");
			frm.set_value("letter_attacmnent", "");
        }
		else if(frm.doc.medium_of_communicatinon=="Postal"){
			frm.set_value("phone_no", "");
			frm.set_value("email_attachment", "");
			frm.set_value("email_id", "");
        }else{
			frm.set_value("phone_no", "");
			frm.set_value("email_attachment", "");
			frm.set_value("email_id", "");
			frm.set_value("address_line_1", "");
			frm.set_value("address_line_2", "");
			frm.set_value("pincode", "");
			frm.set_value("city", "");
			frm.set_value("state", "");
			frm.set_value("letter_attacmnent", "");
        }
	},
	medium_of_communicatinon_from_student: function(frm){
		if(frm.doc.medium_of_communicatinon_from_student=="Telephone"){
			frm.set_value("email", "");
			frm.set_value("address_line_1_student", "");
			frm.set_value("address_line_2_student", "");
			frm.set_value("pincode_student", "");
			frm.set_value("city_student", "");
			frm.set_value("state_student", "");
			frm.set_value("letter_attacmnent_student", "");
        }else if(frm.doc.medium_of_communicatinon_from_student=="Email"){
			frm.set_value("communication_phone_no", "");
			frm.set_value("address_line_1_student", "");
			frm.set_value("address_line_2_student", "");
			frm.set_value("pincode_student", "");
			frm.set_value("city_student", "");
			frm.set_value("state_student", "");
			frm.set_value("letter_attacmnent_student", "");
        }
		else if(frm.doc.medium_of_communicatinon_from_student=="Postal"){
			frm.set_value("communication_phone_no", "");
			frm.set_value("email", "");
        }else{
			frm.set_value("communication_phone_no", "");
			frm.set_value("email", "");
			frm.set_value("address_line_1_student", "");
			frm.set_value("address_line_2_student", "");
			frm.set_value("pincode_student", "");
			frm.set_value("city_student", "");
			frm.set_value("state_student", "");
			frm.set_value("letter_attacmnent_student", "");
        }
	}
});
