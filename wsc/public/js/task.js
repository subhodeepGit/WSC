// frappe.ui.form.on("Task", {
	
// 	onload: function (frm) {
//         frm.clear_table("depends_on")

// 		frappe.call({
//             method: 'wsc.wsc.doctype.task.dependency_task',
//             args: {
//               // Pass any arguments to the server method
//               docname: frm.doc.name
//             },
// 			callback: function(r) {
//                 (r.message).forEach(element => {
//                     var row = frm.add_child("depends_on")
//                     // alert(element[0].name)
//                     row.task=element[0].name
//                     // row.employee_name=element.employee_name
//                     // row.user_id = element.user_id
//                     // row.designation= element.designation
//                     // row.department = element.designation
//                 });
//                 frm.refresh_field("depends_on");
                
//             }
// 		});
//     }
// })
frappe.ui.form.on("Task", {
  onload: function (frm) {
      

      if (!frm.doc.__islocal) {
        frm.clear_table("depends_on");
          frappe.call({
              method: 'wsc.wsc.doctype.task.dependency_task',
              args: {
                  // Pass any arguments to the server method
                  docname: frm.doc.name
              },
              callback: function (r) {
                  (r.message).forEach(element => {
                      var row = frm.add_child("depends_on");
                      row.task = element[0].name;
                      // Add other fields as needed
                  });
                  frm.refresh_field("depends_on");
              }
          });
      }
  }
});
