frappe.ui.form.on('Leave Application', {
refresh: function(frm) {
    var reporting_authority_email = ""; 

    
        if (frm.doc.reporting_authority_email) {
            reporting_authority_email = frm.doc.reporting_authority_email;
        }
    if (frm.doc.status==="Open" && frappe.session.user===reporting_authority_email) {
		frm.add_custom_button(__("Forwarded to Approving Authority"), function() {
			frm.set_value("current_status", "Forwarded to Approving Authority")
			frm.save_or_update();

		}, 'Actions');
        
	}
	var leave_approver = ""; 

    
        if (frm.doc.leave_approver) {
            leave_approver = frm.doc.leave_approver;
        }
	if (frm.doc.current_status==="Forwarded to Approving Authority" && frappe.session.user===leave_approver) {
		frm.add_custom_button(__("Approve"), function() {
			frm.set_value("status", "Approved");
            frm.set_value("current_status","Approved")
			frm.save_or_update();

		}, 'Actions');

		frm.add_custom_button(__("Reject"), function() {
			frm.set_value("status", "Rejected");
            frm.set_value("current_status", "Rejected");
			frm.save_or_update();
		}, 'Actions');
	}
   
    frm.set_df_property('status', 'options', ['Open','Approved','Rejected','Cancelled','Forwarded to Approving Authority']);
    
},   
  
});
frappe.ui.form.on('Leave Application', {
    refresh: function(frm) {
      
        if (frappe.session.user !== frm.doc.leave_approver) {
			$('.secondary-action').prop('hidden', true);
        }
    },
    // refresh: function(frm) {
    //     if (frappe.session.user !== frm.doc.leave_approver) {
    //         frm.disable_save();
    //     } else {
    //         frm.enable_save();
    //     }
    // }
});

    