// Copyright (c) 2023, SOUL Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Seminar Info Details For TnP', {
	// refresh: function(frm) {

	// }
	// date:function(frm){
	// 	console.log(1)
	// 	if(1){

	// 	}
	// },
	validate: function(frm){
		// frm.toggle_display('topic_name',1)
		frappe.call({
		method: 'wsc.wsc.doctype.seminar_info_details_for_tnp.seminar_info_details_for_tnp.get_data',
		args: {
			'topic': frm.doc.topic,
			'date':frm.doc.date,
			
		},callback(result){
			const res = Object.values(result)
			// console.log(res[0][1][0]);
			// console.log(Object.values(res[0][1][0]));
			const instructor_data = Object.values(res[0][0])
			const student_data = Object.values(res[0][1])

			frappe.model.clear_table(frm.doc, 'student_attending_seminar');
			for(const i in student_data){
				console.log(student_data[i].parent);
				
				let c = frm.add_child('student_attending_seminar')
				c.academic_year = student_data[i].academic_year
				c.department = student_data[i].department
				c.activities = student_data[i].activities
				c.duration = student_data[i].duration
				c.description = student_data[i].description
				c.date = student_data[i].date
				c.student_id = student_data[i].parent
			}

			frappe.model.clear_table(frm.doc, 'instructor_attending_or_giving_seminar');
			for(const i in instructor_data){
				console.log(instructor_data[i].parent);
				
				let c = frm.add_child('instructor_attending_or_giving_seminar')
				c.academic_year = instructor_data[i].academic_year
				c.department = instructor_data[i].department
				c.activities = instructor_data[i].activities
				c.duration = instructor_data[i].duration
				c.description = instructor_data[i].description
				c.date = instructor_data[i].date
				c.instructor_name = instructor_data[i].parent
			}
		}
	})
	frm.refresh();
	frm.refresh_field("student_attending_seminar")
	}
});
