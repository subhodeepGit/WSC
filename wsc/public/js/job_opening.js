
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
    }
});