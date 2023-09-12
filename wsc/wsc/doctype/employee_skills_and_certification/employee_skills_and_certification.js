// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Skills and Certification', {
	refresh: function(frm) {
		
		if(!frm.is_new()){
            frappe.call({
        
                method: 'wsc.wsc.doctype.employee_skills_and_certification.employee_skills_and_certification.is_verified_user',
                args: {
                    docname: frm.doc.name
                },
                
                callback: function(r) {
                   
                    if (r.message===false) {
                    
                        $('.actions-btn-group').prop('hidden', true);

                    }
                }
                
            });
        }
	},
});
frappe.ui.form.on('Employee Skills and Certification', {
employee: function(frm) {
frappe.call({
	method: 'wsc.wsc.doctype.employee_skills_and_certification.employee_skills_and_certification.get_skill',

	args: {
		employee: frm.doc.employee
	},
	callback: function(response) {
		if (response.message) {
			frappe.model.clear_table(frm.doc, 'skill_sets');
			
			(response.message).forEach(element => {
				var row = frm.add_child("skill_sets")
				row.skill_name=element.skill_name
			
				row.from_date = element.from_date
				row.to_date=element.to_date
				row.duration=element.duration

				row.description=element.description
				row.documentif_any=element.documentif_any
				
			});
			frm.refresh();
			frm.refresh_field("skill_sets")
			
		}
	}
});
frappe.call({
	method: 'wsc.wsc.doctype.employee_skills_and_certification.employee_skills_and_certification.get_certification',

	args: {
		employee: frm.doc.employee
	},
	callback: function(response) {
		if (response.message) {
			frappe.model.clear_table(frm.doc, 'professional_certification');
			
			(response.message).forEach(element => {
				var row = frm.add_child("professional_certification")
				row.certificate_name=element.certificate_name
			
				row.duration = element.duration
				row.from_date=element.from_date
				row.to_date=element.to_date

				row.certification_authority=element.certification_authority
				row.place=element.place
				row.document=element.document
				
			});
			frm.refresh();
			frm.refresh_field("professional_certification")
			
		}
	}
});
}
});
