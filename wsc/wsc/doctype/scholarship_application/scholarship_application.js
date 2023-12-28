// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Scholarship Application', {
	hide_n_show_child_table_fields(frm){
		var df = frappe.meta.get_docfield("Scholarship Eligibility Paramete","parameter", frm.doc.name);
        df.read_only = 1
		var df = frappe.meta.get_docfield("Scholarship Eligibility Paramete","percentagecgpa", frm.doc.name);
        df.read_only = 1
	},
	before_load: function(frm) {
        frm.trigger("hide_n_show_child_table_fields");
    },
	refresh: function(frm) {
		frm.set_df_property('document_list_tab', 'cannot_add_rows', true);
		frm.set_df_property('scholarship_eligibility_parameter', 'cannot_add_rows', true);
		if (frappe.session.user != "Administrator"){
            if (frappe.user.has_role(["Student"]) && frm.doc.workflow_state=="Sent For Approval"){
            Object.keys(cur_frm.fields_dict).forEach(field=>{
                frm.set_df_property(field,'read_only',1)
            })
        }else if(!frappe.user.has_role(["Student"])){
			Object.keys(cur_frm.fields_dict).forEach(field=>{
                frm.set_df_property(field,'read_only',1)
			})
		}
    } 
	},



	setup:function(frm){
		frm.set_query("scholarship_id", function() {
			return {
				query:"wsc.wsc.doctype.scholarship_application.scholarship_application.valid_scholarship",
				filters: {
					"docstatus": 1,
				}
			}
		})	
	},

	student_id: function(frm) {
		frappe.call({
			method: 'wsc.wsc.doctype.scholarship_application.scholarship_application.calculateAge',
			args: {
				'student_no': frm.doc.student_id,
			},
			callback: function(r) {
				if (!r.exc) {
					frm.set_value("age", r.message);
				}
			},

		})
		frappe.call({
			method: 'wsc.wsc.doctype.scholarship_application.scholarship_application.current_education',
			args: {
				'student_no': frm.doc.student_id,
			},
			callback: function(r) {
				if (r.message) {
					frappe.model.clear_table(frm.doc, 'current_education');
					(r.message).forEach(element => {
						var c = frm.add_child("current_education")
						c.programs=element.programs
						c.semesters=element.semesters
						c.academic_year=element.academic_year
						c.academic_term=element.academic_term
					});
					frm.refresh_field("current_education")
				}
			},

		})
	},
	scholarship_id: function(frm){
		frappe.call({
			method: 'wsc.wsc.doctype.scholarship_application.scholarship_application.eligibility',
			args:{
				"scholarship_id_data":frm.doc.scholarship_id
			},
			callback: function(r) {
				if (r.message){
					frappe.model.clear_table(frm.doc, 'scholarship_eligibility_parameter');
					(r.message).forEach(element => {
						var c = frm.add_child("scholarship_eligibility_parameter")
						c.parameter=element.parameter
						c.percentagecgpa=element.percentagecgpa
					});
					frm.refresh_field("scholarship_eligibility_parameter")
				}
			}
		})
	}
});
