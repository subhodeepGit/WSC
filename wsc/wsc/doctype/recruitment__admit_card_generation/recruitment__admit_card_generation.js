// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Recruitment  Admit Card Generation', {
	
	
	

	exam_declaration: function(frm) {
        frappe.call({
            method: "wsc.wsc.doctype.recruitment__admit_card_generation.recruitment__admit_card_generation.fetch_applicants",
            args: {
                docname: frm.doc.exam_declaration
            },
            callback: function(response) {
                if (response.message) {
                    frm.set_df_property('applicant_number', 'options', response.message);
                }
            }
        });
    },
	applicant_number: function(frm) {
        frappe.call({
            method: "wsc.wsc.doctype.recruitment__admit_card_generation.recruitment__admit_card_generation.get_applicant_details",
            args: {
                applicant_number: frm.doc.applicant_number
            },
            callback: function(response) {
                if (response.message) {
					frm.set_value('applicant_name', response.message.applicant_name);
					frm.set_value('applicant_mail', response.message.applicant_email);
				}
            }
        });
    },


});

