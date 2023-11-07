
frappe.ui.form.on('Job Opening', {
    validate: function(frm) {
        var round_names = [];
        var duplicate_round_names = [];

        frm.doc.job_selection_round.forEach(function(job_selection_round) {
            var round_name = job_selection_round.name_of_rounds.toLowerCase(); 

            if (round_name && round_names.includes(round_name)) {
                duplicate_round_names.push(round_name);
            } else {
                round_names.push(round_name);
            }
        });

        if (duplicate_round_names.length > 0) {
            var error_message = 'Duplicate Round Name found: ' + duplicate_round_names.join(', ');
            frappe.throw(error_message);
            validated = false;
        }
    },
    
});
frappe.ui.form.on("Job Selection Round", "name_of_rounds", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    var a=0
    // if (d.programs && frappe.user.has_role(["Student Applicant"])){
        a=frm.doc.job_selection_round.length;
        frm.set_value("count_rows", a);
        if(a>=frm.doc.number_of_selection_round){
            // alert("number_of_selection_round")
            // alert(frm.doc.number_of_selection_round)
            frm.set_df_property('job_selection_round', 'cannot_add_rows', true);
            frm.set_df_property('job_selection_round', 'cannot_delete_rows', true);
            // frm.set_df_property('program_priority', 'cannot_insert_below', true);
        }
    // }
});