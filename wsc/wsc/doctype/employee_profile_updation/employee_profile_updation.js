// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Profile Updation', {
	refresh: function(frm) {
		
		if(!frm.is_new()){
            frappe.call({
                // wsc.wsc.doctype.employee_reengagement.employee_reengagement.isrfp
                method: 'wsc.wsc.doctype.employee_profile_updation.employee_profile_updation.is_verified_user',
                args: {
                    docname: frm.doc.name
                },
                
                callback: function(r) {
                    // alert(r)
                    if (r.message===false) {
                        // alert(r.message)
                        // $('.page-header-actions-block .btn btn-primary btn-sm, .page-header-actions-block .btn-default').addClass('hidden');
                        $('.actions-btn-group').prop('hidden', true);

                    }
                }
                
            });
        }
	},
	employee: function(frm) {
        // Get the selected employee

        // Fetch the employees details based on the selected employee
        frappe.call({
            method: 'wsc.wsc.doctype.employee_profile_updation.employee_profile_updation.get_employee_details',
            args: {
                employee: frm.doc.employee
            },
            callback: function(r) {
                if (r.message) {
                    // alert(r.message)
                    frm.set_value("employee_name",r.message['employee_name']);
                    frm.set_value("department",r.message['department']);
                    frm.set_value("designation",r.message['designation']);
                    frm.set_value("branch",r.message['branch']);
                    frm.set_value("employment_type",r.message['employment_type']);
                    frm.set_value("date_of_birth",r.message['date_of_birth']);
                    frm.set_value("employee_number",r.message['employee_number']);
                    frm.set_value("user_id",r.message['user_id']);
                    frm.set_value("reporting_authority",r.message['reports_to']);
                    frm.set_value("reporting_auth_id",r.message['reporting_authority_email']);
                    frm.set_value("blood_group",r.message['blood_group']);
                    frm.set_value("gender",r.message['gender']);
                    
                }
				
            }
			
        });
		frappe.call({
            method: 'wsc.wsc.doctype.employee_profile_updation.employee_profile_updation.get_hr_mail',
            callback: function(response) {
                if (response.message) {
                    frm.set_value('hr_id', response.message);
                }
            }
        });
		frappe.call({
            method: 'wsc.wsc.doctype.employee_profile_updation.employee_profile_updation.get_education',
            args: {
                employee: frm.doc.employee
            },
			callback: function(response) {
                if (response.message) {
					frappe.model.clear_table(frm.doc, 'education');
					// alert(response.message)
					(response.message).forEach(element => {
						var row = frm.add_child("education")
						row.qualification=element.qualification
						// alert(element.school_univ)
						row.school_univ = element.school_univ
						row.level=element.level
						row.year_of_passing=element.year_of_passing

						row.class_per=element.class_per
						
						// row.registration_number = element.permanant_registration_number
					});
					frm.refresh();
                	frm.refresh_field("education")
					// frm.refresh_field("employee_education");
					// frm.save();
					// frm.set_value("total_enrolled_student",(r.message).length)
                }
            }
        });
		frappe.call({
            method: 'wsc.wsc.doctype.employee_profile_updation.employee_profile_updation.get_family_background',
            args: {
                employee: frm.doc.employee
            },
			callback: function(response) {
                if (response.message) {
					// alert(response.message)
					frappe.model.clear_table(frm.doc, 'family');

					(response.message).forEach(element => {
						var row = frm.add_child("family")
						row.name1=element.name1
						// alert(element.school_univ)
						row.relation = element.relation
						row.occupation=element.occupation
						row.gender=element.gender

						row.contact=element.contact
						
						// row.registration_number = element.permanant_registration_number
					});
					frm.refresh();
                	frm.refresh_field("family")
					// frm.refresh_field("employee_education");
					// frm.save();
					// frm.set_value("total_enrolled_student",(r.message).length)
                }
            }
        });
		frappe.call({
            method: 'wsc.wsc.doctype.employee_profile_updation.employee_profile_updation.addr_contact',
            args: {
                employee: frm.doc.employee
            },
            callback: function(response) {
                if (response.message) {
                    frm.set_value('current_address', response.message["current_address"]);
					frm.set_value('permanent_address', response.message["permanent_address"]);
					frm.set_value('mobile', response.message["cell_number"]);
					frm.set_value('emergency_contact', response.message["emergency_phone_number"]);
					frm.set_value('emergency_contact_name', response.message["person_to_be_contacted"]);
					frm.set_value('personal_email', response.message["personal_email"]);
					frm.set_value('relation', response.message["relation"]);
                }
            }
        });
    }
});
