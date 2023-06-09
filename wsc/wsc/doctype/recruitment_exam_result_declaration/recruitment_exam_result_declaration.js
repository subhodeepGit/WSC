// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Recruitment Exam Result Declaration', {
	setup(frm){
		frm.set_query("job_applicant_id",function(){
			return{
				filters:{
					"job_title":frm.doc.job_opening
				}
			}
		});
},

	});

