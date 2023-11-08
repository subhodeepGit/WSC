// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('ToT Participant Selection', {
	course_type: function(frm){
		frm.set_query('course', function(){
			return{
				filters:{
					'program_grade' : frm.doc.course_type,
					'is_tot' : 1
				}
			}
		})
	},
	setup:function(frm){
        frm.set_query("course_type", function() {
            return {
                filters: {
                    "is_short_term_course":"Yes"
                }
            };
        });
	},
	course: function(frm){
		if(frm.doc.course){
			frappe.call({
				method: 'wsc.wsc.doctype.tot_participant_selection.tot_participant_selection.get_semester',
				args:{
					course: frm.doc.course,
				},
				callback: function(r) {
					frm.set_value('semester', r.message);
					// frm.refresh_field("student_list")
				}		
			})
		}
	},
	academic_year: function(frm){
		if(frm.doc.academic_year){
			frappe.call({
				method: 'wsc.wsc.doctype.tot_participant_selection.tot_participant_selection.get_academic_term',
				args:{
					academic_year: frm.doc.academic_year,
				},
				callback: function(r) {
					frm.set_value('academic_term', r.message);
					// frm.refresh_field("student_list")
				}		
			})
		}
	},
	// start_date : function(frm){
	// 	if(frm.doc.start_date && frm.doc.end_date){
	// 		if(frm.doc.start_date > frm.doc.end_date){
	// 			frappe.throw("Event Start Date should be Less than Event Start date");
	// 		}
	// 	}
	// },
	// end_date:function(frm){
	// 	if(frm.doc.start_date && frm.doc.end_date){
	// 		if(frm.doc.end_date < frm.doc.start_date){
	// 			rappe.throw("Event End Date should be Greater than Event Start date");
	// 		}
	// 	}
	// }
	start_date: function(frm) {
        // set minimum To Date equal to From Date
        frm.fields_dict.end_date.datepicker.update({
            minDate: frm.doc.start_date ? new Date(frm.doc.start_date) : null
        });
    },

	end_date: function(frm) {
        // set maximum From Date equal to To Date
        frm.fields_dict.start_date.datepicker.update({
            maxDate: frm.doc.end_date ? new Date(frm.doc.end_date) : null
        });
    },
});

frappe.ui.form.on('Selected Participant', {
	participants_add: function(frm){
		frm.fields_dict['participants'].grid.get_field('participant_id').get_query = function(doc){
			var participants = [];
			$.each(doc.participants, function(idx, val){
				if (val.participant_id) participants.push(val.participant_id);
			});
			return { filters: [['ToT Participant', 'name', 'not in', participants],
								['ToT Participant','enabled','=',1]
							] };
		};
	}
});