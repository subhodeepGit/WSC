frappe.ui.form.on("Job Requisition",{
    // setup: function(frm) {
    //     //     frm.set_query("investigation_cell", function() {
    //     //         return {
    //     //             query: "wsc.wsc.validations.employee_grievance.get_cell",
    //     //             filters: {
    //     //                 "grievance_type": frm.doc.grievance_type
    //     //             }
    //     //         };
    //     //     });
    
    //     //     frm.set_query("investigating_authority", function() {
    //     //         return {
    //     //             query: "wsc.wsc.validations.employee_grievance.get_cell_members",
    //     //             filters: {
    //     //                 "investigation_cell": frm.doc.investigation_cell
    //     //             }
    //     //         };
    //     //     });
    //     //     frm.set_query("resolved_by", function() {
    //     //         return {
    //     //             query: "wsc.wsc.validations.employee_grievance.get_cell_members",
    //     //             filters: {
    //     //                 "investigation_cell": frm.doc.investigation_cell
    //     //             }
    //     //         };
    //     //     });
    //     // },
    
    //     if (!frappe.user.has_role(["HR Admin","HR Manager/CS Officer","COO","Director","CEO","CFO"]) || ! frappe.session.user=="Administrator"){
    //         frm.set_query("requested_by", function() {
    //             return {
    //                 query: "wsc.wsc.doctype.job_requisition.test_query",
    //             };
    //         });
    //     }
    
    // },
    refresh: function(frm) {
        // if (frappe.session.user != "Administrator"){
            if (frm.doc.workflow_state=="Pending Approval from Director Admin" || frm.doc.workflow_state=="Pending Approval from COO" || frm.doc.workflow_state=="Pending Approval From CEO" || frm.doc.workflow_state=="Approved by COO"||frm.doc.workflow_state=="Approved by CEO" || frm.doc.workflow_state=="Rejected by COO" || frm.doc.workflow_state=="Rejected by CEO"){
            Object.keys(cur_frm.fields_dict).forEach(field=>{
                frm.set_df_property(field,'read_only',1)
            })

        }
    // }  
    }
    
})
