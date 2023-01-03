// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Document Manager',"student_application_number",function(frm)  {
    
	frappe.model.with_doc("Student Applicant", frm.doc.student_application_number,
	function() {
		var tabletransfer= frappe.model.get_doc("Student Applicant", frm.doc.student_application_number);
        cur_frm.doc.documents = "";
        cur_frm.refresh_field("documents");
        $.each(tabletransfer.document_list, function(index, row){
            var d = frappe.model.add_child(cur_frm.doc, "Document List", "documents");
            d.document_name = row.document_name;
            d.mandatory = row.mandatory;
            d.attach = row.attach;
            cur_frm.refresh_field("documents");
        });
	});

});

frappe.ui.form.on('Document Manager', {

    setup: function(frm) {
        frm.set_query("stream", function(){
            return{
                filters:{
                    "is_group":1,
                    "is_stream": 1
                }
            }
        });
        frm.set_query("program_priority_1", function() {	
            return {   
				
                query: 'wsc.wsc.doctype.document_manager.document_manager.filter_programs_by_department', 
                filters:{
                    "department":frm.doc.stream,
                    "program_grade":frm.doc.program_grades
                }
            }
			
        });
		frm.set_query("program_priority_2", function() {
            return {   
                query: 'wsc.wsc.doctype.document_manager.document_manager.filter_programs_by_department', 
                filters:{
                    "department":frm.doc.stream,
                    "program_grade":frm.doc.program_grades
                }
            }
			
        });
		frm.set_query("program_priority_3", function() {
            return {   
                query: 'wsc.wsc.doctype.document_manager.document_manager.filter_programs_by_department', 
                filters:{
                    "department":frm.doc.stream,
                    "program_grade":frm.doc.program_grades
                }
				
            }
			
        });
    },
    refresh(frm){
        frm.set_df_property('document_details', 'cannot_add_rows', true);
        frm.set_df_property('document_details', 'cannot_delete_rows', true);
    },
    stream:function(frm){
		frm.trigger("document_name")
	},
	program_grades:function(frm){
		frm.trigger("document_name")
	},
	get_student_data(frm){
        if (frm.doc.document_name && frm.doc.academic_year && frm.doc.program_priority_1){
            frappe.call({
                method: "wsc.wsc.doctype.document_manager.document_manager.get_documents1",
                args: {
                    document_name: frm.doc.document_name,
                    academic_year:frm.doc.academic_year,
                    department:frm.doc.stream,
                    program_grade:frm.doc.program_grades,
                    programs:frm.doc.program_priority_1,
                    application_status:frm.doc.application_status
                },
            
                callback: function(r) { 
                    if(r.message){
                        frappe.model.clear_table(frm.doc, 'document_details');
                        (r.message).forEach(element => {
                            var c = frm.add_child("document_details")
                            c.applicant_number=element.parent
                            c.file=element.attach
                            c.mandatory=element.mandatory
                        });
                    }
                    frm.refresh();
                    frm.refresh_field("document_details")
                } 
                
            }); 
        }
        if (frm.doc.document_name && frm.doc.academic_year && frm.doc.program_priority_2){
            frappe.call({
                method: "wsc.wsc.doctype.document_manager.document_manager.get_documents2",
                args: {
                    document_name: frm.doc.document_name,
                    academic_year:frm.doc.academic_year,
                    department:frm.doc.stream,
                    program_grade:frm.doc.program_grades,
                    programs:frm.doc.program_priority_2,
                    application_status:frm.doc.application_status
                },
            
                callback: function(r) { 
                    if(r.message){
                        frappe.model.clear_table(frm.doc, 'document_details');
                        (r.message).forEach(element => {
                            var c = frm.add_child("document_details")
                            c.applicant_number=element.parent
                            c.file=element.attach
                            c.mandatory=element.mandatory
                        });
                    }
                    frm.refresh();
                    frm.refresh_field("document_details")
                } 
                
            }); 
        }
        if (frm.doc.document_name && frm.doc.academic_year && frm.doc.program_priority_3){
            frappe.call({
                method: "wsc.wsc.doctype.document_manager.document_manager.get_documents3",
                args: {
                    document_name: frm.doc.document_name,
                    academic_year:frm.doc.academic_year,
                    department:frm.doc.stream,
                    program_grade:frm.doc.program_grades,
                    programs:frm.doc.program_priority_3,
                    application_status:frm.doc.application_status
                },
            
                callback: function(r) { 
                    if(r.message){
                        frappe.model.clear_table(frm.doc, 'document_details');
                        (r.message).forEach(element => {
                            var c = frm.add_child("document_details")
                            c.applicant_number=element.parent
                            c.file=element.attach
                            c.mandatory=element.mandatory
                        });
                    }
                    frm.refresh();
                    frm.refresh_field("document_details")
                } 
                
            }); 
        }
    },
    refresh(frm) {
		frm.fields_dict["document_details"].grid.add_custom_button(__('Download Documents'), 
			function() {
                let selected = frm.get_selected();
                // alert(JSON.stringify(selected));
                let sel = selected["document_details"];
                // alert(sel);
                for (var i = 0; i < cur_frm.doc.document_details.length; i++) {
                    // alert(cur_frm.doc.student_photos[i].name)
                    for (var j = 0; j < sel.length; j++) {
                        if(sel[j]==cur_frm.doc.document_details[i].name){
                            const data = cur_frm.doc.document_details[i].file;
                            const app_no = cur_frm.doc.document_details[i].applicant_number;
                            // alert(cur_frm.doc.student_photos[i].name)
                            const a = document.createElement('a');
                            a.href = data;
                            a.download = data.split('/').pop();
                            a.setAttribute('download', app_no);
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                        }
                    }
                    }
	
        });
        frm.fields_dict["document_details"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
        
        frm.fields_dict["documents"].grid.add_custom_button(__('Download Documents'), 
        function() {
            for (var i = 0; i < cur_frm.doc.documents.length; i++) {
                if (cur_frm.doc.documents[i].attach) {
                const data = cur_frm.doc.documents[i].attach;
                // const roll = cur_frm.doc.document_details[i].student_roll_number;
                const a = document.createElement('a');
                a.href = data;
                a.download = data.split('/').pop();
                // a.setAttribute('download', roll);
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                }
                }
    });
    frm.fields_dict["documents"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
	}
});