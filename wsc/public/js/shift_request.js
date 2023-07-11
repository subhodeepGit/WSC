frappe.ui.form.on('Shift Request', {
    refresh: function(frm) {
        frappe.call({
            method: 'wsc.wsc.validations.shift_request.get_hr_mail',
            callback: function(r) {
                if (r.message) {
                    var hr_mail = r.message;
                    frm.set_value('hr_mail', hr_mail);
                
                }
            }
        });
    }   
});




