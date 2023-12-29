// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Dynamic Workflow', {
    refresh: function(frm) {
        if (!frm.doc.__islocal) {
            frappe.call({
                method: 'wsc.wsc.doctype.dynamic_workflow.dynamic_workflow.get_approvers',
                args: {
                    "employee": frm.doc.employee
                },
                callback: function(r) {
                    if (r.message) {
                        var currentApprover = null;
                        var previousApprover = null;
                        var nextApprover = null;
                        var hasLevel1Approver = r.message.some(function(row){
                            return row.role==="Level 1"
                        });
                        
                        var hasLevel2Approver = r.message.some(function(row){
                            return row.role==="Level 2"
                        });
                        if (frm.doc.docstatus === 1 && frm.doc.document_status=="Pending") {
            
                            if (hasLevel1Approver){
                                var level1Approver=r.message.find(function(row){
                                        return row.role==="Level 1"
                
                                })
                            if(frappe.session.user===level1Approver.user_id){
                                frm.add_custom_button(__("Approve"), function() {
                                if(hasLevel2Approver){
                                    frm.set_value("document_status", "Approved by "+ level1Approver.employee_name+"("+level1Approver.designation+")");
                                    frm.save("Update")
                                    frm.save("Submit");
                                    frm.page.clear_primary_action();
                                    frm.page.clear_secondary_action();
                                }else{
                                    frm.set_value("document_status", "Approved");
                                    frm.save("Update")
                                    frm.save("Submit");
                                    frm.page.clear_primary_action();
                                    frm.page.clear_secondary_action();
                                }
                            }, 'Actions');
    
                                frm.add_custom_button(__("Reject"), function() {
                                    if(hasLevel2Approver){
                                        frm.set_value("document_status", "Rejected by "+ level1Approver.employee_name+"("+level1Approver.designation+")");
                                        frm.save("Update")
                                        frm.save("Submit");
                                        frm.page.clear_primary_action();
                                        frm.page.clear_secondary_action();
                                    }else{
                                        frm.set_value("document_status", "Rejected");
                                        frm.save("Update")
                                        frm.save("Submit");
                                        frm.page.clear_primary_action();
                                        frm.page.clear_secondary_action();
                                    }
                                    
                
                                }, 'Actions');
                            }
                            }
                        }

                        

                        for (var i = 2; i <= 10; i++) {
                            var currentRole = "Level " + i;
                            var hasApprover = r.message.some(function(row) {
                                return row.role === currentRole;
                            });

                            if (hasApprover) {
                                currentApprover = r.message.find(function(row) {
                                    return row.role === currentRole;
                                });

                                // Skip checking previous approver for Level 1
                                
                                var previousRole = "Level " + (i - 1);
                                var hasPreviousApprover = r.message.some(function(row) {
                                    return row.role === previousRole;
                                });

                                if (hasPreviousApprover) {
                                    previousApprover = r.message.find(function(row) {
                                        return row.role === previousRole;
                                    });
                                }
                                

                                var nextRole = "Level " + (i + 1);
                                var hasNextApprover = r.message.some(function(row) {
                                    return row.role === nextRole;
                                });

                                if (frm.doc.docstatus === 1 && frappe.session.user === currentApprover.user_id &&
                                     frm.doc.document_status === "Approved by " + previousApprover.employee_name + "(" + previousApprover.designation + ")") {

                                    frm.add_custom_button(__("Approve"), function() {
                                        if (hasNextApprover) {
                                            frm.set_value("document_status", "Approved by " + currentApprover.employee_name + "(" + currentApprover.designation + ")");
                                        } else {
                                            frm.set_value("document_status", "Approved");
                                        }

                                        frm.save("Update");
                                        frm.save("Submit");
                                        frm.page.clear_primary_action();
                                        frm.page.clear_secondary_action();
                                    }, 'Actions');

                                    frm.add_custom_button(__("Reject"), function() {
                                        if (hasNextApprover) {

                                            frm.set_value("document_status", "Rejected by " + currentApprover.employee_name + "(" + currentApprover.designation + ")");
                                        } else {
                                            frm.set_value("document_status", "Rejected");
                                        }

                                        frm.save("Update");
                                        frm.save("Submit");
                                        frm.page.clear_primary_action();
                                        frm.page.clear_secondary_action();
                                    }, 'Actions');

                                    break; // exit loop if a current approver is found
                                }
                            }
                        }
                    }
                }
            });
        }
    }
});



               






