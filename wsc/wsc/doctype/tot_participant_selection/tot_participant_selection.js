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
	start_date : function(frm){
		if(frm.doc.start_date && frm.doc.end_date){
			if(frm.doc.start_date > frm.doc.end_date){
				frappe.throw("Event Start Date should be Less than Event Start date");
			}
		}
	},
	end_date:function(frm){
		if(frm.doc.start_date && frm.doc.end_date){
			if(frm.doc.end_date < frm.doc.start_date){
				rappe.throw("Event End Date should be Greater than Event Start date");
			}
		}
	}
});

frappe.ui.form.on('Selected Participant', {
	participants_add: function(frm){
		frm.fields_dict['participants'].grid.get_field('participant_id').get_query = function(doc){
			var participants = [];
			$.each(doc.participants, function(idx, val){
				if (val.participant_id) participants.push(val.participant_id);
			});
			return { filters: [['ToT Participant', 'name', 'not in', participants]] };
		};
	}
});