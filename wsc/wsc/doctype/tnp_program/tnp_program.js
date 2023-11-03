// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('TnP Program', {
	refresh: function(frm) {
		if(frm.is_new()){
			frm.set_df_property('program_status', 'options', ['Scheduled'])
		}
		else{
			frm.set_df_property('program_status', 'options', ['Scheduled', 'Completed', 'Cancelled'])
		}
	},
	setup: function(frm){
		const date = new Date()
		let year = date.getFullYear()
		let month = String(date.getMonth() + 1).padStart(2,'0')
		let day = String(date.getDate()).padStart(2,'0')
		frm.set_value('current_date', `${year}-${month}-${day}`)
	},
	start_date: function(frm){
		if(frm.doc.end_date && frm.doc.start_date > frm.doc.end_date){
			frappe.throw("Start date cannot be after end date")
		}
		if(frm.doc.start_date < frm.doc.current_date){
			frappe.throw("Start date cannot be before current date")
		}
	},
	end_date : function(frm){
		if(frm.doc.start_date && frm.doc.end_date < frm.doc.start_date){
			frappe.throw("End date cannot be before start date")
		}
		if(frm.doc.end_date < frm.doc.current_date){
			frappe.throw("End date cannot be before current date")
		}
	}
});

// --------------------------------------------------

frappe.ui.form.on('chief coordinators list', {
	chief_coordinators_list_add: function(frm){
		frm.fields_dict['chief_coordinators_list'].grid.get_field('coordinator_id').get_query = function(doc){
			var coordinator_list = [];
			$.each(doc.chief_coordinators_list, function(idx, val){
				if (val.coordinator_id) coordinator_list.push(val.coordinator_id);
			});

			return { filters: [['Employee', 'name', 'not in', coordinator_list]] };
		};
	}
});