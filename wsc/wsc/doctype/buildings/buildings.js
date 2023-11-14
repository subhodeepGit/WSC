// Copyright (c) 2022, SOUL Limited and contributors
// For license information, please see license.txt

////To filter districts based on the selected state link field
// frappe.ui.form.on('Buildings', {
// 	 function(frm) {
// 		frm.set_query("districts", function() {
// 			return {
// 				 filters: {
// 				   "state":frm.doc.state
// 				 }
// 			 };
// 		 });
// 	}
// });

//To fetch only those buildings which are between start and end date of the Land with respect to today’s date
frappe.ui.form.on("Buildings", {
	setup: function(frm) {
		frm.set_query("plot_number", function() {
			return {
                query: "wsc.wsc.doctype.buildings.buildings.room_type_query",
			}
		});
        frm.set_query("block", function() {
            return {
                filters: [
                    ["Blocks","districts","=",frm.doc.district]
                ]
            }; 
        });

        frm.set_query("district", function() {
            return {
                filters: [
                    ["Districts","state","=",frm.doc.state]
                ]
            };
        });
	},
    state: function(frm) {
        frm.set_value("district","")
        frm.set_value("block","")
    },
    district: function(frm) {
        frm.set_value("block","")
    },
});

// frm.set_query("land_plot_number","land_details", function(_doc, cdt, cdn) {
//     var d = locals[cdt][cdn];
//     return {
//         filters: {
//             'company': d.company,
//             'account_type': d.account_type = 'Receivable',
//             'is_group': d.is_group = 0
//         }
//     };
// });
frappe.ui.form.on("Buildings", {
    setup: function(frm){
        frm.set_query("land_plot_number","land_details", function(_doc, cdt, cdn) {
            var d = locals[cdt][cdn];
            return {
                query: "wsc.wsc.doctype.buildings.buildings.room_type_query",
                // filters: {
                //     'company': d.company,
                //     'account_type': d.account_type = 'Receivable',
                //     'is_group': d.is_group = 0
                // }
            };
        });
    }
})

// To validate end date is not before start date
frappe.ui.form.on("Buildings", {
    start_date: function(frm) {
        frm.fields_dict.end_date.datepicker.update({
            minDate: frm.doc.start_date ? new Date(frm.doc.start_date) : null
        });
    },

    end_date: function(frm) {
        frm.fields_dict.start_date.datepicker.update({
            maxDate: frm.doc.end_date ? new Date(frm.doc.end_date) : null
        });
    },
});


frappe.ui.form.on('Land Details', {
	land_details_add: function(frm){
		frm.fields_dict['land_details'].grid.get_field('land_plot_number').get_query = function(doc){
			var land_list = [];
			if(!doc.__islocal) land_list.push(doc.name);
			$.each(doc.land_details, function(idx, val){
				if (val.land_plot_number) land_list.push(val.land_plot_number);
			});
			return { filters: [['Land', 'name', 'not in', land_list]] };
		};
	}
});