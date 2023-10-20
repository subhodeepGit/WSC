// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('TnP Event', {
	refresh: function(frm) {
		if(frm.is_new()){
			frm.set_df_property('event_status', 'options', ['Scheduled'])
		}
		else{
			frm.set_df_property('event_status', 'options', ['Scheduled', 'Completed', 'Cancelled'])
		}
		frm.set_query('select_program', function(){
			return{
				filters:{
					'program_status' : 'Scheduled',
				}
			}
		})
	},
	setup: function(frm){
		const date = new Date()
		let year = date.getFullYear()
		let month = String(date.getMonth() + 1).padStart(2,'0')
		let day = String(date.getDate()).padStart(2,'0')
		frm.set_value('current_date', `${year}-${month}-${day}`)
	},
	in_a_program : function(frm){
		if(frm.doc.in_a_program == 0){
			frm.set_value('select_program', '')
			frm.set_value('program_name', '')
		}
	},
	program_start_date: function(frm){
		if(frm.doc.event_start_date && frm.doc.event_start_date < frm.doc.program_start_date){
			frappe.throw("Event start date cannot be before program start date")
		}
		if(frm.doc.event_end_date && frm.doc.event_end_date < frm.doc.program_start_date){
			frappe.throw("Event end date cannot be before program start date")
		}
	},
	program_end_date: function(frm){
		if(frm.doc.event_start_date && frm.doc.event_start_date > frm.doc.program_end_date){
			frappe.throw("Event start date cannot be after program end date")
		}
		if(frm.doc.event_end_date && frm.doc.event_end_date > frm.doc.program_end_date){
			frappe.throw("Event end date cannot be after of program end date")
		}
	},
	event_start_date: function(frm){
		if(frm.doc.program_start_date && frm.doc.program_end_date && frm.doc.event_start_date){
			if(frm.doc.event_start_date < frm.doc.program_start_date || frm.doc.event_start_date > frm.doc.program_end_date){
				frappe.throw("Event start date cannot be outside of Program dates")
			}
		}
		if(frm.doc.event_start_date && frm.doc.event_start_date > frm.doc.event_end_date){
			frappe.throw("Event start date cannot be after event end date")
		}
		if(frm.doc.event_start_date < frm.doc.current_date){
			frappe.throw('Start date cannot be before current date')
		}
	},
	event_end_date: function(frm){
		if(frm.doc.event_end_date && frm.doc.program_end_date && frm.doc.program_start_date){
			if(frm.doc.event_end_date < frm.doc.program_start_date || frm.doc.event_end_date > frm.doc.program_end_date){
				frappe.throw("Event end date cannot be outside of Program dates")
			}
		}
		if(frm.doc.event_end_date < frm.doc.event_start_date){
			frappe.throw("Event end date cannot be before event start date")
		}
		if(frm.doc.event_end_date < frm.doc.current_date){
			frappe.throw('End date cannot be before current date')
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