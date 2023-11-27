// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Resume', {
	// refresh: function(frm) {

	// }

	// if(frm.doc.placement_company){
	// 	// For departments
	// 	frappe.model.with_doc("Placement Company", frm.doc.placement_company, function() {
	// 		var tabletransfer= frappe.model.get_doc("Placement Company", frm.doc.placement_company)
	// 		frm.clear_table("for_department");	
	// 		$.each(tabletransfer.belong_to_department, function(index, row){
	// 			var d = frm.add_child("for_department");
	// 			d.department = row.department;
	// 			frm.refresh_field("for_department");

	// 		});
	// 	});
	// 	// For sectors
	// 	frappe.model.with_doc("Placement Company", frm.doc.placement_company, function() {
	// 		var tabletransfer= frappe.model.get_doc("Placement Company", frm.doc.placement_company)
	// 		frm.clear_table("for_sectors");	
	// 		$.each(tabletransfer.sector_of_work, function(index, row){
	// 			var d = frm.add_child("for_sectors");
	// 			d.sector = row.sector_name;
	// 			frm.refresh_field("for_sectors");

	// 		});
	// 	});
	// } else{
	// 	frm.clear_table("for_department");
	// 	frm.clear_table("for_sectors");
	// 	frm.refresh();
	// 	frm.refresh_field("eligible_student")
	// }


	id: function(frm){
		if(frm.doc.id){
			frappe.model.with_doc("Student", frm.doc.id, function(){
				var tabletransfer = frappe.model.get_doc("Student", frm.doc.id)
				frm.clear_table("experience_details_table")
				$.each(tabletransfer.experience_detail, function(index, row){
					var d = frm.add_child("experience_details_table")
					d.company_name = row.company_name
					d.job_profile = row.job_profile
					d.job_type = row.job_type
					d.job_start_date = row.job_start_date
					d.job_end_date = row.job_end_date					
					frm.refresh_field("experience_details_table");
				})
			})

			
			// location
			frappe.call({
				method : 'wsc.wsc.doctype.resume.resume.get_location',
				args: {
					student_id : frm.doc.id
				},
				callback : function(result){
					frm.set_value('location', result.message)
				}
			})

			// Current education

			frappe.model.with_doc("Student", frm.doc.id, function(){
				var tabletransfer = frappe.model.get_doc("Student", frm.doc.id)
				frm.clear_table("current_education_details")
				$.each(tabletransfer.current_education, function(index, row){
					var d = frm.add_child("current_education_details")
					d.programs = row.programs
					d.semester = row.semesters
					d.academic_year = row.academic_year
					d.academic_term = row.academic_term
					frm.refresh_field("current_education_details");
				})
			})

			// Previous education

			frappe.model.with_doc("Student", frm.doc.id, function(){
				var tabletransfer = frappe.model.get_doc("Student", frm.doc.id)
				frm.clear_table("previous_education_details")
				$.each(tabletransfer.education_details, function(index, row){
					var d = frm.add_child("previous_education_details")
					d.qualification = row.qualification
					d.institute = row.institute
					d.board = row.board
					d.percentagecgpa = row.percentagecgpa
					d.score = row.score			
					d.year_of_completion = row.year_of_completion
					frm.refresh_field("previous_education_details");
				})
			})
		}
		else{
			frm.clear_table("experience_details_table");
			frm.clear_table("current_education_details");
			frm.clear_table("previous_education_details");
			frm.refresh()
		}
	}
});
