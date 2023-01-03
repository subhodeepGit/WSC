// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Download Student Passport Photo', {
	refresh(frm){
        

        frm.set_df_property('document_details', 'cannot_add_rows', true);
        frm.set_df_property('document_details', 'cannot_delete_rows', true);
	},

	student_application_number:function(frm){
		frappe.call({
			method: "wsc.wsc.doctype.download_student_passport_photo.download_student_passport_photo.student_passport_photo",
			args: {
				student_applicant:frm.doc.student_application_number
			},
		
			callback: function(r) { 
				if(r.message){
					frappe.model.clear_table(frm.doc, 'document_details');
					(r.message).forEach(element => {
						var c = frm.add_child("document_details")
						c.applicant_number=element.name
						c.student_name=element.title
						c.file=element.passport_photo
					});
				}
				frm.refresh();
				frm.refresh_field("document_details")
				
			},
		}); 
		frm.fields_dict["document_details"].grid.add_custom_button(__('Download Documents'), 
		function() {
			let selected = frm.get_selected();
			// alert(JSON.stringify(selected));
			let sel = selected["document_details"];
		for (var i = 0; i < cur_frm.doc.document_details.length; i++) {
			if (cur_frm.doc.document_details[i].file) {
			const data = cur_frm.doc.document_details[i].file;
			const app_no = cur_frm.doc.document_details[i].student_name;
			const a = document.createElement('a');
			a.href = data;
			a.download = data.split('/').pop();
			a.setAttribute('download', app_no);
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);
			}
		}
		
	}); 
},

	setup: function(frm) {
		frm.set_query("stream", function(){
			return{
				filters:{
					"is_group":1,
					"is_stream": 1
				}
			}
		});
		// frm.set_query("programs", function() {
        //     return {
        //         filters: {
        //             // "program_grade":frm.doc.program_grades,
		// 			"department":frm.doc.stream
        //         }
        //     };
        // });
		// frm.fields_dict['program_priority'].grid.get_field('programs').get_query = function(doc, cdt, cdn) {
		frm.set_query("programs", function() {	
            return {   
                query: 'wsc.wsc.doctype.student_applicant.filter_programs_by_department', 
                filters:{
                    "department":frm.doc.stream,
                    "program_grade":frm.doc.program_grades
                }
            }
			
        });
		frm.set_query("program_priorty_2", function() {
            return {   
                query: 'wsc.wsc.doctype.student_applicant.filter_programs_by_department', 
                filters:{
                    "department":frm.doc.stream,
                    "program_grade":frm.doc.program_grades
                }
            }
			
        });
		frm.set_query("program_priorty_3", function() {
            return {   
                query: 'wsc.wsc.doctype.student_applicant.filter_programs_by_department', 
                filters:{
                    "department":frm.doc.stream,
                    "program_grade":frm.doc.program_grades
                }
				
            }
			
        });
	},
	generate_passport_photo(frm){
        if (frm.doc.academic_year && frm.doc.programs){
            frappe.call({
                method: "wsc.wsc.doctype.download_student_passport_photo.download_student_passport_photo.generate_passport_photo",
                args: {
					// student_applicant:frm.doc.reference_name,
                    academic_year:frm.doc.academic_year,
                    department:frm.doc.stream,
                    program_grade:frm.doc.program_grades,
					programs:frm.doc.programs,
					application_status:frm.doc.application_status,
					have_you_approved_the_selected_program:frm.doc.have_you_approved_the_selected_program
                },
            
                callback: function(r) { 
                    if(r.message){
                        frappe.model.clear_table(frm.doc, 'document_details');
                        (r.message).forEach(element => {
                            var c = frm.add_child("document_details")
                            c.applicant_number=element.name
                            c.student_name=element.title
                            c.file=element.passport_photo
                        });
                    }
                    frm.refresh();
                    frm.refresh_field("document_details")
                } 
                
            }); 
			frm.fields_dict["document_details"].grid.add_custom_button(__('Download Documents'), 

			function() {
				var urls = [];
				var stud_names = [];
				let selected = frm.get_selected();
				// alert(JSON.stringify(selected));
				let sel = selected["document_details"];
				// alert(sel);
				for (var i = 0; i < cur_frm.doc.document_details.length; i++) {
					// alert(cur_frm.doc.student_photos[i].name)
					for (var j = 0; j < sel.length; j++) {
						if(sel[j]==cur_frm.doc.document_details[i].name){
							const data = cur_frm.doc.document_details[i].file;
							const student_name = cur_frm.doc.document_details[i].student_name;
							// alert(cur_frm.doc.student_photos[i].name)
							const a = document.createElement('a');
							a.href = data;
							urls.push(a.href);
							stud_names.push(student_name)
						}
					}
				}
				var interval = setInterval(download, 400, urls);

				function download(urls) {
				var url = urls.pop();
				var stud_name = stud_names.pop();

				var a = document.createElement("a");
				a.setAttribute('href', url);
				a.setAttribute('download', stud_name);
				a.setAttribute('target', '_blank');
				a.click();

				if (urls.length == 0) {
					clearInterval(interval);
				}
				}
			});
			frm.fields_dict["document_details"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
		}

        else if (frm.doc.academic_year && frm.doc.program_priorty_2){
            frappe.call({
                method: "wsc.wsc.doctype.download_student_passport_photo.download_student_passport_photo.generate_passport_photo2",
                args: {
					// student_applicant:frm.doc.reference_name,
                    academic_year:frm.doc.academic_year,
                    department:frm.doc.stream,
                    program_grade:frm.doc.program_grades,
					programs:frm.doc.program_priorty_2,
					application_status:frm.doc.application_status,
					have_you_approved_the_selected_program:frm.doc.have_you_approved_the_selected_program
                },
            
                callback: function(r) { 
                    if(r.message){
                        frappe.model.clear_table(frm.doc, 'document_details');
                        (r.message).forEach(element => {
                            var c = frm.add_child("document_details")
                            c.applicant_number=element.name
                            c.student_name=element.title
                            c.file=element.passport_photo
							c.programs=element.programs
                        });
                    }
                    frm.refresh();
                    frm.refresh_field("document_details")
                } 
                
            }); 
			frm.fields_dict["document_details"].grid.add_custom_button(__('Download Documents'), 

			function() {
				let selected = frm.get_selected();
				// alert(JSON.stringify(selected));
				let sel = selected["document_details"];
				// alert(sel);
				for (var i = 0; i < cur_frm.doc.document_details.length; i++) {
					// alert(cur_frm.doc.student_photos[i].name)
					for (var j = 0; j < sel.length; j++) {
						if(sel[j]==cur_frm.doc.document_details[i].name){
							const data = cur_frm.doc.document_details[i].file;
							const app_no = cur_frm.doc.document_details[i].student_name;
							// alert(cur_frm.doc.student_photos[i].name)
							const a = document.createElement('a');
							a.href = data;
							a.download = data.split('/').pop();
							a.setAttribute('download', app_no);
							document.body.appendChild(a);
							a.click();
							document.body.removeChild(a);
						}
					}
				}

			});
			frm.fields_dict["document_details"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
		}
		else if (frm.doc.academic_year && frm.doc.program_priorty_3){
            frappe.call({
                method: "wsc.wsc.doctype.download_student_passport_photo.download_student_passport_photo.generate_passport_photo3",
                args: {
					// student_applicant:frm.doc.reference_name,
                    academic_year:frm.doc.academic_year,
                    department:frm.doc.stream,
                    program_grade:frm.doc.program_grades,
					programs:frm.doc.program_priorty_3,
					application_status:frm.doc.application_status,
					have_you_approved_the_selected_program:frm.doc.have_you_approved_the_selected_program
                },
            
                callback: function(r) { 
                    if(r.message){	
                        frappe.model.clear_table(frm.doc, 'document_details');
                        (r.message).forEach(element => {
                            var c = frm.add_child("document_details")
                            c.applicant_number=element.name
                            c.student_name=element.title
                            c.file=element.passport_photo
							c.programs=element.programs
                        });
                    }
                    frm.refresh();
                    frm.refresh_field("document_details")
                } 
                
            }); 
			frm.fields_dict["document_details"].grid.add_custom_button(__('Download Documents'), 

			function() {
				let selected = frm.get_selected();
				// alert(JSON.stringify(selected));
				let sel = selected["document_details"];
				// alert(sel);
				for (var i = 0; i < cur_frm.doc.document_details.length; i++) {
					// alert(cur_frm.doc.student_photos[i].name)
					for (var j = 0; j < sel.length; j++) {
						if(sel[j]==cur_frm.doc.document_details[i].name){
							const data = cur_frm.doc.document_details[i].file;
							const app_no = cur_frm.doc.document_details[i].student_name;
							// alert(cur_frm.doc.student_photos[i].name)
							const a = document.createElement('a');
							a.href = data;
							a.download = data.split('/').pop();
							a.setAttribute('download', app_no);
							document.body.appendChild(a);
							a.click();
							document.body.removeChild(a);
						}
					}
				}

			});
			frm.fields_dict["document_details"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
		}
		else{}
	},
});