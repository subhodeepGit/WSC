// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Placement Company', {
	refresh: function(frm) {
		frappe.dynamic_link = { doc: frm.doc, fieldname: 'name', doctype: 'Placement Company' }

		frm.toggle_display(['address_html','contact_html'], !frm.doc.__islocal);

		if (frm.doc.__islocal) {
			frappe.contacts.clear_address_and_contact(frm);
		}
		else {
			frappe.contacts.render_address_and_contact(frm);
		}
	},
	refresh: function(frm){
		if (!frm.doc.__islocal)	{
		if(frm.doc.black_list!=1){
			if(frm.doc.visitor == 'Internship'){
				frm.add_custom_button(__("Internship Drive"), function() {
					frappe.model.open_mapped_doc({
						method: "wsc.wsc.doctype.placement_company.placement_company.create_internship_drive",
						frm: frm,
					});
				}, __('Create'))
			}
			else{
				frm.add_custom_button(__("Placement Drive"), function() {
					frappe.model.open_mapped_doc({
						method: "wsc.wsc.doctype.placement_company.placement_company.create_placement_drive",
						frm: frm,
					});
				}, __('Create'))
			}
		
	}
	}
	} ,
	setup(frm) {
        frm.set_query("department","belong_to_department", function() {
			return {
				filters: {
					"is_stream":0
				}
			};
		});
		frm.set_query("sector" , function(){
			return{
				filters:{
					"blacklist_sector":0
				}
			}
		})
    } 
});

// ------------------------------------------------------------------------------------

frappe.ui.form.on('sector of work', {
	sector_of_work_add: function(frm){
		frm.fields_dict['sector_of_work'].grid.get_field('sector_name').get_query = function(doc){
			var sector_of_work = [];
			$.each(doc.sector_of_work, function(idx, val){
				if (val.sector_name) sector_of_work.push(val.sector_name);
			});

			return { filters: [['Sector', 'name', 'not in', sector_of_work]] };
		};
	}
});

frappe.ui.form.on('Placement Department', {
	belong_to_department_add: function(frm){
		frm.fields_dict['belong_to_department'].grid.get_field('department').get_query = function(doc){
			var departmentName = [];
			$.each(doc.belong_to_department, function(idx, val){
				if (val.department) departmentName.push(val.department);
			});

			return { filters: [['Department', 'name', 'not in', departmentName]] };
		};
	}
});