// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Entrance Exam Result Publication', {
	setup:function(frm){
		frm.set_query("entrance_exam_declaration", function() {
            return {
                query: "wsc.wsc.doctype.entrance_exam_result_publication.entrance_exam_result_publication.ra_query"
            }
        })

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
		
		frm.set_query("applicant_id" , function(){
			return {
                query: "wsc.wsc.doctype.entrance_exam_result_publication.entrance_exam_result_publication.ra_query3",
				filters:{
					'entrance_exam_declaration':frm.doc.entrance_exam_declaration
				}
            }
		})
	}
});
