cur_frm.add_fetch('course','course_name','course_name');
cur_frm.add_fetch('course','course_code','course_code');
frappe.ui.form.on('Course Enrollment', {
    refresh(frm){
        frm.set_query("course", function() {
            return {
                query: 'wsc.wsc.validations.student_group.filter_courses',
                filters:{
                    "semester":frm.doc.semester,						
                }
                // getdate("year_end_date"):[">="(getdate())]}
            };
        });
        cur_frm.dashboard.hide()
        // frm.set_df_property('credit_distribution', 'cannot_add_rows', true);
        cur_frm.doc.credit_distribution.forEach(data=>{
            var df = frappe.meta.get_docfield("Credit distribution List", "assessment_criteria",data.name);
            df.read_only=1;
        })
        

    },

    // frm.set_query("course", function() {
    //     return {
    //         query:"ed_tec.ed_tec.doctype.course_assessment_result_tool.course_assessment_result_tool.get_courses",
    //         filters: {
    //             "semester":frm.doc.semester
    //             // "exam_declaration":frm.doc.exam_declaration
    //         }
            
    //     };
    // });
    total_course_marks:function(frm){
		(frm.doc.credit_distribution).forEach(data=>{
			var d = locals[data.doctype][data.name];
			d.total_marks=(frm.doc.total_course_marks*(d.weightage/100))
			refresh_field("total_marks", d.name, d.parentfield);	
		})
	},
})

frappe.ui.form.on("Credit distribution List", "weightage", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
	d.total_marks=(frm.doc.total_course_marks*(d.weightage/100))
	refresh_field("total_marks", d.name, d.parentfield);
});