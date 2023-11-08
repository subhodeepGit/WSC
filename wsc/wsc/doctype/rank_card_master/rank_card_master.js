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

frappe.ui.form.on('Ranking Category', {
	ranking_category_add: function(frm){
		frm.fields_dict['ranking_category'].grid.get_field('category_name').get_query = function(doc){
			var ranking_category_list = [];
			$.each(doc.ranking_category, function(idx, val){
				if (val.category_name) ranking_category_list.push(val.category_name);
			});
			return { filters: [['Category', 'name', 'not in', ranking_category_list],
								// ['ToT Participant','enabled','=',1]
							] };
		};
	}
});