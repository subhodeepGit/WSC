// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Applicant Updation', {
	refresh:function(frm){
		frm.set_df_property('disable_type' , 'hidden' , 1)
		frm.set_df_property('awards_winner_list' , 'hidden' , 1)
		if(!frm.is_new()){

			frm.add_custom_button(__('Update Student Applicant'), function(){
				// body = JSON.parse(frm.doc)
				frappe.call({
					method: 'update_student_applicant',
					doc:frm.doc	
				})
				// frm.remove_custom_button('Center Select')
			}).addClass('btn-primary');
		}
	},
	setup: function(frm){
		frm.set_query("student_applicant", function() {
			return{
				filters:{
					"docstatus":1
				}
			}
		})
	},
	student_applicant: function(frm){
		frappe.call({
			method:'wsc.wsc.doctype.student_applicant_updation.student_applicant_updation.applicant_data',
			args:{
				'applicant_id':frm.doc.student_applicant,
			}, 
			callback: function(result){
				if(result.message){
					// console.log(result.message[0][0]); //applicant data
					// console.log(result.message[1]); //education_qualification
					// console.log(result.message[2]); //course_preference
					// console.log(result.message[3]); //physical_disability
					// console.log(result.message[4]); //award_winner_list
					
					
					for (const key  in result.message[0][0]){
						console.log(result.message[0][0][key]);
						frm.doc[key] = result.message[0][0][key]
					}   
					// console.log(result.message[0][0][room_type]);
					frappe.model.clear_table(frm.doc, 'education_qualifications_details');
					frappe.model.clear_table(frm.doc, 'course_preferences');
					
					//Educational Qualification
					result.message[1].forEach((i) => {
						// course_preferences
						let c = frm.add_child('education_qualifications_details')
						
						c.qualification = i.qualification// result.message[3].forEach((i) => {
							// 	let 
							// })
						c.institute = i.institute
						c.board = i.board
						c.percentage_cgpa = i.percentage_cgpa
						c.total_marks = i.total_marks
						c.earned_marks = i.earned_marks
						c.year_of_completion = i.year_of_completion
						c.mandatory = i.mandatory
						c.score = i.admission_percentage
					})

					//Course Preference
					result.message[2].forEach((i) => {
						let c = frm.add_child('course_preferences')
						c.programs = i.programs
					})

					if(result.message[0][0].physically_disabled === 1) {
						frm.set_df_property('disable_type' , 'hidden' , 0)
						frappe.model.clear_table(frm.doc, 'disable_type');
						result.message[3].forEach((i) => {
							let c = frm.add_child('disable_type')

							c.disability_type = i.disability_type
							c.percentage_of_disability = i.percentage_of_disability
							c.attach_disability_certificate = i.attach_disability_certificate
						})
					}

					if(result.message[0][0].award_winner === 1) {
						frm.set_df_property('awards_winner_list' , 'hidden' , 0)
						frappe.model.clear_table(frm.doc, 'awards_winner_list');
						result.message[3].forEach((i) => {
							let c = frm.add_child('awards_winner_list')

							c.disability_type = i.disability_type
							c.percentage_of_disability = i.percentage_of_disability
							c.attach_disability_certificate = i.attach_disability_certificate
						})
					}

					frm.refresh()
					frm.refresh_field("education_qualifications_details")
					frm.refresh_field("course_preferences")
					frm.refresh_field("disable_type")
					frm.refresh_field("awards_winner_list")

				}
				
			}
		})
	},
});
