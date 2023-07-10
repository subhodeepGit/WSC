frappe.ui.form.on('Shift Request', {
    refresh: function(frm) {
    //     if (!frm.is_new()) {
    //         frappe.call({
    //             method: 'wsc.wsc.validations.shift_request.is_verified_user',
    //             args: {
    //                 docname: frm.doc.name
    //             },
    //             callback: function(r) {
    //                 if (r.message === false) {
    //                     hideActionButtons();
    //                 } else {
    //                     showActionButtons();
    //                 }
    //             }
    //         });
    //     }
    }
});

// frappe.ui.form.on('Shift Request', {
//     workflow_state: function(frm) {
//         if (frm.doc.workflow_state !== 'Pending for Approval from Reporting Authority') {
//             hideActionButtons();
//         } else {
//             showActionButtons();
//         }
//     }
// });

// function hideActionButtons() {
//     $('.actions-btn-group').prop('hidden', true);
// }

// function showActionButtons() {
//     $('.actions-btn-group').prop('hidden', false);
// }


