// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('TnP Event', {
	refresh: function(frm) {

	},
	in_a_program : function(frm){
		if(frm.doc.in_a_program == 0){
			frm.set_value('select_program', '')
			frm.set_value('program_name', '')
		}
	},
	event_start_date : function(frm){
		if(frm.doc.event_start_date && frm.doc.event_end_date){
			if(frm.doc.event_start_date > frm.doc.event_end_date){
				frappe.throw("Event Start Date should be Less than Event Start date");
			}
		}
		if(frm.doc.event_date && frm.doc.event_start_date){
			if(frm.doc.event_date != frm.doc.event_start_date){
				frappe.throw("Event Date and Event Start Date must be same");
			}
		}
	},
	event_end_date:function(frm){
		if(frm.doc.event_start_date && frm.doc.event_end_date){
			if(frm.doc.event_end_date < frm.doc.event_start_date){
				frappe.throw("Event End Date should be Greater than Event Start date");
			}
		}
	},
	event_date : function(frm){
		frm.set_value('event_start_date', frm.doc.event_date)
		if(frm.doc.event_date && frm.doc.event_start_date){
			if(frm.doc.event_date != frm.doc.event_start_date){
				frappe.throw("Event Date and Event Start Date must be same");
			}
		}
	},
	start_time : function(frm){
		if(frm.doc.start_time && frm.doc.end_time){
			if(frm.doc.start_time > frm.doc.end_time){
				frappe.throw("Event Start Time should be Less than Event Start Time");
			}
		}
	},
	end_time : function(frm){
		if(frm.doc.start_time && frm.doc.end_time){
			if(frm.doc.end_time < frm.doc.start_time){
				frappe.throw("Event End Time should be Greater than Event Start Time");
			}
		}
	},
	select_program : function(frm){
		frappe.call({
			method : 'wsc.wsc.doctype.tnp_event.tnp_event.get_program_name',
			args: {
				program_id : frm.doc.select_program
			},
			callback : function(result){
				frm.set_value('program_name', result.message)
			}
		})
	}
});

// --------------------------------------------------

frappe.ui.form.on('coordinators list', {
	coordinators_list_add: function(frm){
		frm.fields_dict['coordinators_list'].grid.get_field('coordinator_id').get_query = function(doc){
			var coordinator_list = [];
			$.each(doc.coordinators_list, function(idx, val){
				if (val.coordinator_id) coordinator_list.push(val.coordinator_id);
			});

			return { filters: [['Employee', 'name', 'not in', coordinator_list]] };
		};
	}
});