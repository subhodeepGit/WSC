frappe.ui.form.on('Employee Separation', {
    refresh: function(frm) {
        if(!frm.is_new()){
            frappe.call({
                method:'wsc.wsc.validations.employee_separation.is_verified_user',
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
    department: function(frm){
        frappe.call({
        method: 'wsc.wsc.validations.employee_separation.depart_head',
     args:{
        department: frm.doc.department
             },
        callback: function(result){
            if (result.message) {
                var dept_head = result.message;
                frm.set_value('department_head',dept_head)
          }
        
      },
   
      }); 
    }
});  
      

    