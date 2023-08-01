// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Entrance Exam Result Publication', {
	setup:function(frm){
		frm.set_query("academic_term", function() {
			return {
				filters:{
					"academic_year":frm.doc.academic_year
				}
			}
		})
		frm.set_query("department", function(){
	        return{
	            filters:{
	                "is_group":1,
	                "is_stream": 1
	            }
	        }
	    });

		frm.set_query("applicant_id" , function() {
			return {
				filters: {
					"academic_year":frm.doc.academic_year,
					"academic_term":frm.doc.academic_term,
					"department":frm.doc.department
				}
			}
		})
	}
});
