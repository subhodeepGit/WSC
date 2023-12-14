frappe.ui.form.on('Bank Guarantee', {
    onload: function(frm) {
        frm.set_query('reference_document', function() {
            return {
                filters: {
                    'name': 'Purchase Order'
                }
            };
        });
    },
    name_of_beneficiary: function(frm) {
        if (/[^A-Za-z\s]/.test(cur_frm.doc.name_of_beneficiary)) {
          frappe.throw(__('Name of Beneficiary is not valid'));
          return;
        }
      },
    bank_guarantee_number: function(frm){
        if (/[^A-Za-z0-9-]/.test(cur_frm.doc.bank_guarantee_number)) {
            frappe.throw(__('Bank Guarantee Number is not valid'));
            return;
          }
      },
    fixed_deposit_number: function(frm){
        var accountNumberPattern = /^\d+$/;
        if (!accountNumberPattern.test(frm.doc.fixed_deposit_number)) {
            frappe.throw(__("Fixed Deposit Number should contain only digits."));
            return;
        }
      }
}
);