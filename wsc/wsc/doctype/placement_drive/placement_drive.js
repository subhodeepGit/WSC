// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Placement Drive', {
	get_students: function(frm){
		if(!frm.is_new()){
			let body = JSON.stringify({
				academic_year:frm.doc.academic_year,
				academic_term:frm.doc.academic_term,
				placement_drive_for:frm.doc.placement_drive_for,
				required_cgpa:frm.doc.current_cgpapercentage,
				backlog:frm.doc.active_backlog,
				program:frm.doc.for_programs,
				eligibility_criteria:frm.doc.eligibility_criteria
			})
			// console.log(body)
			frappe.call({
				method: 'wsc.wsc.doctype.placement_drive.placement_drive.get_eligibility',
				args: {
					'body':body
				},
				callback: function(result){
					const res = Object.values(result)
					const values = Object.values(res[0])
					if(values[0].length !== 0){
						let r = values[0]
						frappe.model.clear_table(frm.doc, 'eligible_student');
						values.forEach(r => {
							let c =frm.add_child('eligible_student')
							c.student_doctype_name= r[0].parent
							c.student_name = r[0].student_name
							c.program_enrollment = r[0].programs
							c.academic_year = r[0].academic_year
						})
						frm.refresh();
						frm.refresh_field("eligible_student")	
					} else {
						alert("No Eligible Students found")
						frappe.model.clear_table(frm.doc, 'eligible_student');
						frm.refresh();
						frm.refresh_field("eligible_student")
					}
				}
			})
		}
		
	},
	setup:function(frm){
		frm.set_query("programs","for_programs", function() {
			var dept_list= []
			$.each(frm.doc.for_department, function(index, row){
                dept_list.push(row.department);
	        });
			return {
				filters: {
					"department":  ['in', dept_list]
				}
			};
		});
		frm.set_query("semester","for_programs", function(frm, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
				filters: {
					"programs" :d.programs
				}
			};
		});
		frm.set_query("academic_term", function() {
            return {
                filters: {
                    "academic_year":frm.doc.academic_year
                }
            };
        });
		frm.set_query("placement_company" , function(){
			return{
				filters:{
					"black_list":0
				}
			}
		})
	},
	placement_company:function(frm){
		if(frm.doc.placement_company){
			frappe.model.with_doc("Placement Company", frm.doc.placement_company, function() {
                var tabletransfer= frappe.model.get_doc("Placement Company", frm.doc.placement_company)
                frm.clear_table("for_department");	
                $.each(tabletransfer.belong_to_department, function(index, row){
                    var d = frm.add_child("for_department");
                    d.department = row.department;
                    frm.refresh_field("for_department");
                });
            });
        } else{
			frm.clear_table("for_department");
			frm.refresh();
			frm.refresh_field("eligible_student")
		}
	},
	application_end_date:function(frm){
		if(frm.doc.application_start_date && frm.doc.application_end_date){
			if(frm.doc.application_end_date < frm.doc.application_start_date){
				frappe.throw("Application End Date should be Greater than Application Start date");
			}
		}
	},
	refresh:function(frm){
		if(!frm.is_new()){
			frm.set_df_property('get_students' , 'hidden' , 0)
		}
		else{
			frm.set_df_property('get_students' , 'hidden' , 1)
		}
		if(frm.doc.docstatus==1){
			frm.set_df_property('get_students' , 'hidden' , 1)
		}
		frm.set_df_property("authorized_signature", "cannot_add_rows", true);
	},
	before_submit:function(frm){
		if(frm.doc.eligible_student.length === 0){
			frm.set_df_property("eligible_student" , 'reqd' , 1)
			frm.refresh()
		} else {
			frm.set_df_property("eligible_student" , 'reqd' , 0)
			frm.refresh()
		}
	}
});
