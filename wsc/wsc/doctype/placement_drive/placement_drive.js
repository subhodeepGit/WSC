// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Placement Drive', {
	refresh: function(frm){
		frm.set_query('placement_company', function(){
			return{
				filters:[
					['visitor' ,"!=", 'Internship'],
					['black_list', "=", '0']
				]
			}
		})
		if(!frm.is_new()){
			frm.set_df_property('get_students' , 'hidden' , 0)
			frm.set_df_property('tentative_joining_date' , 'hidden' , 0)
		}
		else{
			frm.set_df_property('get_students' , 'hidden' , 1)
			frm.set_df_property('tentative_joining_date' , 'hidden' , 1)
		}
		if(frm.doc.docstatus==1){
			frm.set_df_property('get_students' , 'hidden' , 1)
			frm.set_df_property('tentative_joining_date' , 'hidden' , 1)
		}
		frm.set_df_property("authorized_signature", "cannot_add_rows", true);
	},

	setup: function(frm){
		const date = new Date()
		let year = date.getFullYear()
		let month = String(date.getMonth() + 1).padStart(2,'0')
		let day = String(date.getDate()).padStart(2,'0')
		frm.set_value('current_date', `${year}-${month}-${day}`)

		// sector filter
		frm.set_query("sector_of_work", function() {
			var sector_list= []
			$.each(frm.doc.for_sectors, function(index, row){
                sector_list.push(row.sector);
	        });
			return {
				filters: {
					"sector_name":  ['in', sector_list]
				}
			};
		});
		// course
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
				filters:[
					["black_list", "=", "0"],
					["visitor", "!=", "Internship"]
				]
			}
		})
	},
	before_submit:function(frm){
		if(frm.doc.eligible_student.length === 0){
			frm.set_df_property("eligible_student" , 'reqd' , 1)
			frm.refresh()
		} else {
			frm.set_df_property("eligible_student" , 'reqd' , 0)
			frm.refresh()
		}
	},
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
				frappe.throw('Application end date should be after application end date')
			}
			else if(frm.doc.application_end_date < frm.doc.current_date){
				frm.set_value('application_end_date', 0)
				frappe.throw('Application end date should be after application start date')
			}
		}
		else if(frm.doc.application_end_date < frm.doc.current_date){
			frm.set_value('application_end_date', 0)
			frappe.throw('Application end date should either be today or a future date')
		}
	},
	placement_company:function(frm){
		if(frm.doc.placement_company){
			// For departments
			frappe.model.with_doc("Placement Company", frm.doc.placement_company, function() {
                var tabletransfer= frappe.model.get_doc("Placement Company", frm.doc.placement_company)
                frm.clear_table("for_department");	
                $.each(tabletransfer.belong_to_department, function(index, row){
                    var d = frm.add_child("for_department");
                    d.department = row.department;
                    frm.refresh_field("for_department");

                });
            });
			// For sectors
			frappe.model.with_doc("Placement Company", frm.doc.placement_company, function() {
                var tabletransfer= frappe.model.get_doc("Placement Company", frm.doc.placement_company)
                frm.clear_table("for_sectors");	
                $.each(tabletransfer.sector_of_work, function(index, row){
                    var d = frm.add_child("for_sectors");
                    d.sector = row.sector_name;
                    frm.refresh_field("for_sectors");

                });
            });
        } else{
			frm.clear_table("for_department");
			frm.clear_table("for_sectors");
			frm.refresh();
			frm.refresh_field("eligible_student")
		}
	},
	ctc: function(frm){
		if(isNaN(frm.doc.ctc)){
			frm.set_value("ctc", '0')
			frappe.throw('value needs to be a positive number')
		}
		else if(frm.doc.ctc < 0){
			frm.set_value("ctc", '0')
			frappe.throw('value needs to be a positive number')
		}
	},
	get_students: function(frm){
		if(!frm.is_new()){
			let body = JSON.stringify({
				name: frm.doc.name,
				academic_year:frm.doc.academic_year,
				academic_term:frm.doc.academic_term,
				placement_drive_for:frm.doc.placement_drive_for,
				required_cgpa:frm.doc.current_cgpapercentage,
				backlog:frm.doc.active_backlog,
				program:frm.doc.for_programs,
				eligibility_criteria:frm.doc.eligibility_criteria
			})
			frappe.call({
				method: 'wsc.wsc.doctype.placement_drive.placement_drive.get_eligibility',
				args: {
					'body':body
				},
				callback: function(result){
					if(result.message.length !== 0){
						frappe.model.clear_table(frm.doc, 'eligible_student');
						result.message.forEach(i => {
							
							let c =frm.add_child('eligible_student')
							c.student_doctype_name = i.parent
							c.student_name = i.student_name
							c.program_enrollment = i.programs
							c.academic_year = i.academic_year
						})
						frm.refresh();
						frm.refresh_field("eligible_student")	
						frm.save()
					} else {
						alert("No Eligible Students found")
						frappe.model.clear_table(frm.doc, 'eligible_student');
						frm.refresh();
						frm.refresh_field("eligible_student")
					}
				}
			})
		}
		
	}	
});

frappe.ui.form.on('Eligibility Criteria', {
	percentage:function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	frm.doc.eligibility_criteria.forEach(function(d){ 
		if(d.percentage < 0){
			d.percentage = 0;
		}
	});
  }
});

frappe.ui.form.on('Rounds of Placement', {
	date:function(frm, cdt, cdn){
	var d = locals[cdt][cdn];
	frm.doc.rounds_of_placement_table.forEach(function(d){ 
		if(d.date <= frm.doc.application_end_date){
			d.date = ''
			alert("Round date cannot be before application end date")
		}
	});
  }
});

frappe.ui.form.on('Placement Designations', {
	designations_position_add: function(frm){
		frm.fields_dict['designations_position'].grid.get_field('designation').get_query = function(doc){
			var designations = [];
			$.each(doc.designations_position, function(idx, val){
				if (val.designation) designations.push(val.designation);
			});
			return { filters: [['Designation', 'name', 'not in', designations]] };
		};
	}
});