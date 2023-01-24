// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Role Permission Tool', {
	refresh: function(frm) {
		frm.set_df_property("role_permission", "cannot_add_rows", true);
		frm.set_df_property("role_permission", "cannot_delete_rows", true);

	}
});
frappe.ui.form.on('Role Permission Tool', {
    module_name: function(frm) {
        frappe.call({
            method: 'wsc.wsc.doctype.role_permission_tool.role_permission_tool.fetch_data',
            args: {
				role:frm.doc.role,
                module_name:frm.doc.module_name,
            },
           callback: function(r) {
                if(r.message){
                    frappe.model.clear_table(frm.doc, 'role_permission');
                    (r.message).forEach(element => {
                        var c = frm.add_child("role_permission")
                        c.doctype_name=element.doctype_list
						c.select = element.select
						c.read = element.read
						c.write = element.write
						c.create = element.create
						c.submittable = element.submittable
						c.can_data = element.can_data
						c.amnd_data = element.amnd_data
						c.eml_data = element.eml_data
						c.del_data = element.del_data
						c.report = element.report
						c.export = element.export
						c.import_data = element.import_data
					 	c.print = element.print
						c.shr_data = element.shr_data
                    });
                }
                frm.refresh();
                frm.refresh_field("role_permission")
            }
        })
    }
});