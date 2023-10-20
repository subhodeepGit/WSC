// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rank Card Master', {
	setup:function(frm){
		frm.set_query("entrance_exam_declaration", function() {
            return {
                query: "wsc.wsc.doctype.rank_card_master.rank_card_master.ra_query"
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
					"is_group":0,
	                // "is_stream": 1
	            }
	        }
	    })
	}
});
