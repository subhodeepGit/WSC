// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Internship Drive', {
	refresh: function(frm) {
		frm.set_df_property('for_departments', 'cannot_add_rows', true)
		frm.set_df_property('for_departments', 'cannot_delete_rows', true)
		frm.set_df_property('for_sectors', 'cannot_add_rows', true)
		frm.set_df_property('for_sectors', 'cannot_delete_rows', true)
		frm.set_query('internship_company', function(){
			return{
				filters:{
					'visitor' : 'Internship',
					'black_list' : 0
				}
			}
		})
	},
	setup: function(frm){
		frm.set_query("semester","for_programs", function(frm, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
				filters: {
					"programs" :d.programs
				}
			};
		});
		const date = new Date()
		let year = date.getFullYear()
		let month = String(date.getMonth() + 1).padStart(2,'0')
		let day = String(date.getDate()).padStart(2,'0')
		frm.set_value('current_date', `${year}-${month}-${day}`)
	},
	internship_company: function(frm){
		if(frm.doc.internship_company){
			// For departments
			frappe.model.with_doc("Placement Company", frm.doc.internship_company, function() {
                var tabletransfer= frappe.model.get_doc("Placement Company", frm.doc.internship_company)
                frm.clear_table("for_department");	
                $.each(tabletransfer.belong_to_department, function(index, row){
                    var d = frm.add_child("for_departments");
                    d.department = row.department;
                    frm.refresh_field("for_departments");

                });
            });
			// For sectors
			frappe.model.with_doc("Placement Company", frm.doc.internship_company, function() {
                var tabletransfer= frappe.model.get_doc("Placement Company", frm.doc.internship_company)
                frm.clear_table("for_sectors");	
                $.each(tabletransfer.sector_of_work, function(index, row){
                    var d = frm.add_child("for_sectors");
                    d.sector = row.sector_name;
                    frm.refresh_field("for_sectors");

                });
            });
        } else{
			frm.clear_table("for_departments");
			frm.clear_table("for_sectors");
			frm.refresh();
			frm.refresh_field("eligible_student")
		}
	},
	// -----------------------------------------------
	application_start_date: function(frm){
		if(frm.doc.application_end_date){
			if(frm.doc.application_start_date > frm.doc.application_end_date){
				frm.set_value('application_start_date', 0)
				frappe.throw('Application start date should be before application end date')
			}
			else if(frm.doc.application_start_date < frm.doc.current_date){
				frm.set_value('application_start_date', 0)
				frappe.throw('Application start date should either be before the end date and either today or a future date')
			}
		}
		else if(frm.doc.application_start_date < frm.doc.current_date){
			frm.set_value('application_start_date', 0)
			frappe.throw('Application start date should either be today or a future date')
		}
	},
	application_end_date: function(frm){
		if(frm.doc.application_start_date){
			if(frm.doc.application_end_date < frm.doc.application_start_date){
				frm.set_value('application_end_date', 0)
				frappe.throw('Application end date should be after application start date')
			}
			else if(frm.doc.application_end_date < frm.doc.current_date){
				frm.set_value('application_end_date', 0)
				frappe.throw('Application date should be on or after application start date')
			}
		}
		else if(frm.doc.application_end_date < frm.doc.current_date){
			frm.set_value('application_end_date', 0)
			frappe.throw('Application end date should either be today or a future date')
		}
	},
	// ----------------
	// application_start_date: function(frm) {
    //     frm.fields_dict.application_end_date.datepicker.update({
    //         minDate: frm.doc.application_start_date ? new Date(frm.doc.application_start_date) : null
    //     });
    // },

    // application_end_date: function(frm) {
    //     frm.fields_dict.application_start_date.datepicker.update({
    //         maxDate: frm.doc.application_end_date ? new Date(frm.doc.application_end_date) : null
    //     });
    // },
	// application_start_date: function(frm){
	// 	if(frm.doc.application_start_date < frm.doc.current_date){
	// 		frappe.throw('Start date cannot be before current date')
	// 	}
	// },
	// application_end_date:function(frm){
	// 	if(frm.doc.application_start_date && frm.doc.application_end_date){
	// 		if(frm.doc.application_end_date < frm.doc.application_start_date){
	// 			frappe.throw("Application End Date should be Greater than Application Start date");
	// 		}
	// 	}
	// },
});
