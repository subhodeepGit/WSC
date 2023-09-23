// frappe.listview_settings['Student Applicant'] = {
//     refresh: function(listview) {
//         if (!frappe.route_options & frappe.user.has_role(["Applicant"]) && !frappe.user.has_role(["System Manager"])){ 
//             alert("SYSTEM")
//             // $(".filter-selector").hide();
//                frappe.route_options = {
//                 // "owner": ["=", frappe.session.user],
//                 "student_email_id":["=", frappe.session.user]
// 				// "docstatus":1
//             };
     
//         }
//     }
// };
frappe.listview_settings['Student Applicant'] = {
    onload: function(listview) {
   
        if (frappe.user.has_role(["Applicant"]) && !frappe.user.has_role(["System Manager"])){        
            $('.primary-action').hide();
            $('.menu-btn-group').hide();
            if(frappe.route_options){
                frappe.route_options = {
                    "student_email_id": ["=", frappe.session.user]
                };
                $(".filter-selector").hide();
                
            }
        }
    }      
};
//  if not self.owner== frappe.session.user:
      // frappe.route_options = {
            //     "user": ["=", frappe.session.user===("toshiffs@gmail.com")],
            //     filters: [["application_status","=","Clear"]],
            //     "docstatus":1,
            //     "application_status":"Clear"
            // };
 // "user": ["=", frappe.session.user],
                 // "user": ["=", frappe.session.user===("student.applicant@kiss.ac.in")],
                  // filters: [["application_status","=","Clear"]],

    // onload: function(listview) {
    
    //         if (frappe.session.user===("student.applicant@kiss.ac.in")){
    //             alert("hey")
    //             frappe.listview_settings['Student Applicant'] = {
              
    //                 filters: [["application_status","=", "Clear"]],
                   
    //         // $(".filter-selector").hide();
    //             }
    //             alert("hello");
    //         }
    //         if (frappe.session.user===("student.applicant@kiss.ac.in")){
    //             alert("heiiiy")
    //             $(".filter-selector").hide();
    //         }
    //     }
    // };
   
    // filters:[["application_status","=", "Clear"]],
    
//     onload: function(listview) {
//         alert("okj")
        
    
//             if (frappe.session.user===("student.applicant@kiss.ac.in")){
//                 filters:[["application_status","=", "Clear"]]
//                 // alert("oksdasj")
//             // $(".filter-selector").hide();
//                 // }
//             }
//             alert("hello")
//             if (frappe.session.user===("student.applicant@kiss.ac.in")){
//                 $(".filter-selector").hide();
//             }
//         }
//     // }
// };

// onload: function(listview) {
//     if (!frappe.route_options & frappe.user.has_role(["Student Applicant"]) && !frappe.user.has_role(["System Manager"])){ 
//         $(".filter-selector").hide();
//         frappe.route_options = {
//             "user": ["=", frappe.session.user===("student.applicant@kiss.ac.in")],
//             "docstatus":1,
//             "application_status":"Clear"
//         };
//     }
// }
// };
