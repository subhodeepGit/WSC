// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Placement Drive Application', {
	// refresh: function(frm) {

	// }
	setup:function(frm){
		frm.set_query("placement_drive", function() {
			return {
				query:"wsc.wsc.doctype.placement_drive_application.placement_drive_application.get_placement_drive",
				filters: {
					"docstatus": 1,
					"student":frm.doc.student
				}
			};
		});
		frm.set_query('resume', function(){
			return{
				filters: {
					"id":frm.doc.student
				}
			}
		})
		frm.set_query("current_semester", function() {
			return {
				filters: {
					"programs":frm.doc.programs
				}
			};
		});
	},
	student:function(frm){
		if(frm.doc.student){
			frappe.model.with_doc("Student", frm.doc.student, function() {
                var tabletransfer= frappe.model.get_doc("Student", frm.doc.student)
                // frm.clear_table("educational_details");
                // $.each(tabletransfer.education_details, function(index, row){
                //     var d = frm.add_child("educational_details");
                //     d.qualification = row.qualification;
                //     d.institute = row.institute;
                //     d.board = row.board;
                //     d.score = row.score;
				// 	d.percentage = row.percentage;
                //     d.year_of_completion = row.year_of_completion;
                //     frm.refresh_field("educational_details");
                // });
                $.each(tabletransfer.current_education, function(index, row){
                    frm.doc.programs = row.programs;
                    frm.doc.current_semester = row.semesters;
                    frm.refresh_field("programs");
                    frm.refresh_field("current_semester");
                });
            });
        }
		else{

			frm.set_value('programs', '')
			frm.set_value('current_semester', '')
			frm.refresh_field("programs");
			frm.refresh_field("current_semester");
			
		}
	},
	placement_drive:function(frm){
		if(frm.doc.placement_drive){
			frappe.db.get_value("Placement Drive", {'name':frm.doc.placement_drive, "docstatus":1},'process_of_placement', resp => {
				console.log(resp);
				frm.set_value("eligibility_details",resp.process_of_placement)
			})
			frm.refresh_field("eligibility_details");
		}
	},
	status:function(frm){
		if(frm.doc.status){
			frappe.call({
				method: "wsc.wsc.notification.custom_notification.placement_drive_application_submit",
                args:{
                	'doc':frm.doc
                },
				callback: function(r) { 
					if(r.message){
						frappe.msgprint("Mail sent to student")
					}
				} 
			});
		}
	},
	resume: function(frm){
		if(frm.doc.resume){
			// experience child table
			frappe.model.with_doc("Resume", frm.doc.resume, function(){
				var tabletransfer = frappe.model.get_doc("Resume", frm.doc.resume)
				frm.clear_table("experience_details")
				$.each(tabletransfer.experience_details_table, function(index, row){
					var d = frm.add_child("experience_details")
					d.company_name = row.company_name
					d.job_profile = row.job_profile
					d.job_type = row.job_type
					d.job_start_date = row.job_start_date
					d.job_end_date = row.job_end_date			
					d.job_location = row.job_location
					d.work_description = row.work_description
					frm.refresh_field("experience_details");
				})
			})
			// current educational details table
			frappe.model.with_doc("Resume", frm.doc.resume, function(){
				var tabletransfer = frappe.model.get_doc("Resume", frm.doc.resume)
				frm.clear_table("educational_details")
				$.each(tabletransfer.current_education_details, function(index, row){
					var d = frm.add_child("educational_details")
					d.programs = row.programs
					d.semester = row.semester
					d.academic_year = row.academic_year
					d.academic_term = row.academic_term
					d.academic_term = row.academic_term
					d.institute = row.institute
					d.location = row.location
					frm.refresh_field("educational_details");
				})
			})
			// previous education details table
			frappe.model.with_doc("Resume", frm.doc.resume, function(){
				var tabletransfer = frappe.model.get_doc("Resume", frm.doc.resume)
				frm.clear_table("previous_education_details")
				$.each(tabletransfer.previous_education_details, function(index, row){
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
			// Technical skills
			frappe.model.with_doc("Resume", frm.doc.resume, function(){
				var tabletransfer = frappe.model.get_doc("Resume", frm.doc.resume)
				frm.clear_table("technical_skills")
				$.each(tabletransfer.technical_skills, function(index, row){
					var d = frm.add_child("technical_skills")
					d.skill = row.skill
					frm.refresh_field("technical_skills");
				})
			})
			// non technical skills
			frappe.model.with_doc("Resume", frm.doc.resume, function(){
				var tabletransfer = frappe.model.get_doc("Resume", frm.doc.resume)
				frm.clear_table("non_technical_skills")
				$.each(tabletransfer.non_technical_skills, function(index, row){
					var d = frm.add_child("non_technical_skills")
					d.skill = row.skill
					frm.refresh_field("non_technical_skills");
				})
			})
			// languages
			frappe.model.with_doc("Resume", frm.doc.resume, function(){
				var tabletransfer = frappe.model.get_doc("Resume", frm.doc.resume)
				frm.clear_table("languages")
				$.each(tabletransfer.languages, function(index, row){
					var d = frm.add_child("languages")
					d.language = row.language
					frm.refresh_field("languages");
				})
			})
		}
		else{
			frm.clear_table("experience_details");
			frm.clear_table("educational_details");
			frm.clear_table("previous_education_details");
			frm.refresh_field("technical_skills");
			frm.refresh_field("non-technical_skills");
			frm.refresh_field("languages");
			frm.refresh();
		}
	}
});
