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
        if (/[^A-Za-z\s]/.test(frm.doc.name_of_beneficiary) && frm.doc.name_of_beneficiary!="") {
          frm.set_value('name_of_beneficiary',"");  
          frappe.throw(__('Name of Beneficiary is not valid'));
          return;
        }
      },
    // bank_guarantee_number: function(frm){
    //     if (/[/^\d+$/]/.test(cur_frm.doc.bank_guarantee_number) && frm.doc.bank_guarantee_number!="") {
    //         frm.set_value('bank_guarantee_number',""); 
    //         frappe.throw(__('Bank Guarantee Number is not valid'));
    //         return;
    //       }
    //   },
    bank_guarantee_number:function(frm){
		var accountNumberPattern = /^\d+$/;
		if (!accountNumberPattern.test(frm.doc.bank_guarantee_number) && frm.doc.bank_guarantee_number!="") {
			frm.set_value('bank_guarantee_number',"");
			frappe.throw(__("Bank Guarantee Number should contain only digits."));

			return;
		}
	},
    fixed_deposit_number: function(frm){
        var accountNumberPattern = /^\d+$/;
        if (!accountNumberPattern.test(frm.doc.fixed_deposit_number) && frm.doc.fixed_deposit_number!="") {
            frm.set_value('fixed_deposit_number',""); 
            frappe.throw(__("Fixed Deposit Number should contain only digits."));
            return;
        }
      }
}
);