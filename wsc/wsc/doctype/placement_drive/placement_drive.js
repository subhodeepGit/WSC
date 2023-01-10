// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Placement Drive', {
	// refresh: function(frm) {

	// 	// console.log(frm.doc.doc_status)
	// 	if(frm.doc.docstatus == 1 ){
	// 		frm.add_custom_button('Eligible Students' , () => {
	// 			console.log("click")
	// 			frappe.call({
	// 				method: 'wsc.wsc.doctype.placement_drive.placement_drive.get_eligibility',
	// 				args: {
	// 					'name': frm.doc.name,
	// 				},
	// 			})
				
	// 		})
	// 	}
	// } , 

	get_students: function(frm){
		// console.log(frm.doc.placement_company , frm.doc.academic_year , frm.doc.academic_term)
		frappe.call({
			method: 'wsc.wsc.doctype.placement_drive.placement_drive.get_eligibility',
			args: {
				'name': frm.doc.name,
				'academic_year':frm.doc.academic_year,
				'academic_term':frm.doc.academic_term,
				'placement_drive_for':frm.doc.placement_drive_for
			},
		})
		
	},
	setup:function(frm){
		frm.set_query("programs","for_programs", function() {
			var dept_list= []
			$.each(frm.doc.for_department, function(index, row){
                dept_list.push(row.department);
	        });
			return {
				filters: {
					"department":  ['in', dept_list]
				}
			};
		});
		frm.set_query("semester","for_programs", function(frm, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
				filters: {
					"programs" :d.programs
				}
			};
		});
		frm.set_query("academic_term", function() {
            return {
                filters: {
                    "academic_year":frm.doc.academic_year
                }
            };
        });
	},
	placement_company:function(frm){
		if(frm.doc.placement_company){
			frappe.model.with_doc("Placement Company", frm.doc.placement_company, function() {
                var tabletransfer= frappe.model.get_doc("Placement Company", frm.doc.placement_company)
                frm.clear_table("for_department");
                $.each(tabletransfer.belong_to_department, function(index, row){
                    var d = frm.add_child("for_department");
                    d.department = row.department;
                    frm.refresh_field("for_department");
                });
            });
        }
	},
	application_end_date:function(frm){
		if(frm.doc.application_start_date && frm.doc.application_end_date){
			if(frm.doc.application_end_date < frm.doc.application_start_date){
				frappe.throw("Application End Date should be Greater than Application Start date");
			}
		}
	},
	// before_save:function(frm){
	// 	var result = {}
	// 	var classes = [];
	// 	var marks = [];
	// 	for (var i = 0; i < frm.doc.eligibility_criteria.length; i++) {
	// 		classes.push(frm.doc.eligibility_criteria[i].class)  
	// 		marks.push(frm.doc.eligibility_criteria[i].percentage)
	// 	}

	// 	// console.log(classes , marks)
	// 	result.class = classes
	// 	result.marks = marks
	// 	// console.log(1)
	// 	// frm.add_custom_button("Get Student")
	// }
});
