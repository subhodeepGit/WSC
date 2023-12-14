frappe.ui.form.on("Bank Reconciliation Tool", {
    from_reference_date(frm){
        if(frm.doc.from_reference_date>frm.doc.to_reference_date){
            frappe.throw("<b>From Reference Date</b> can not greater than <b>To Reference Date</b>")
        }
    },
    to_reference_date(frm){
        if(frm.doc.from_reference_date>frm.doc.to_reference_date){
            frappe.throw("<b>From Reference Date</b> can not greater than <b>To Reference Date</b>")
        }
    },
    bank_statement_from_date(frm){
        if(frm.doc.bank_statement_from_date>frm.doc.bank_statement_to_date){
            frappe.throw("<b>From Date</b> can not greater than <b>To Date</b>")
        }
    },
    bank_statement_to_date(frm){
        if(frm.doc.bank_statement_from_date>frm.doc.bank_statement_to_date){
            frappe.throw("<b>From Date</b> can not greater than <b>To Date</b>")
        }
    }
})