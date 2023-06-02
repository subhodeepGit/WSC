// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Recruitment Exam Declaration', {
job_opening: function(frm){
	frappe.call({
	method: 'wsc.wsc.doctype.recruitment_exam_declaration.recruitment_exam_declaration.get_selectionrounds',
 args:{
	job_opening: frm.doc.job_opening
		 },
	callback: function(result){
		// alert(JSON.stringify(result.message))
		console.log(result.message)
		let arr = [];
        for (let i = 0; i < result.message.length; i++) {
          arr.push(result.message[i].name_of_rounds);
        }
        // set_field_options('selection_round','option' ,arr)
        frm.set_df_property('selection_round', 'options', arr);
      }
    });
  },
  
  setup(frm){
	frm.set_query("recruitment_exam_center",function(){
		return{
			filters:{
				"is_active":1
			}
		}
	});
},
get_applicants: function(frm){
	alert("Hello")
	frappe.call({
		method: 'wsc.wsc.doctype.recruitment_exam_declaration.recruitment_exam_declaration.get_job_applicants',
		args:{
			job_opening:frm.doc.job_opening
		},
		callback: function(r) {
			if (r.message) {
			  var applicants = r.message;
	
			  frm.clear_table("applicant_details");
			  for (var i = 0; i < applicants.length; i++) {
				var applicant = applicants[i];
	  
				var row = frappe.model.add_child(frm.doc, "Applicant Detail", "applicant_details");
				row.job_applicant = applicant.name;
				row.applicant_name = applicant.applicant_name;
				row.applicant_mail_id = applicant.email_id;
				
			  }

			  frm.refresh_field("applicant_details");
			}
		  }
	});
},
});


// frappe.ui.form.on('Recruitment Exam Declaration', {
//     validate: function(frm) {
//         frappe.call({
//             method: 'wsc.wsc.doctype.recruitment_exam_declaration.recruitment_exam_declaration.update_job_opening',
//             args: {
//                 name: frm.doc.name
//             },
//             callback: function(result) {
//                 alert(result.message);
//             }
//         });
//     }
// });