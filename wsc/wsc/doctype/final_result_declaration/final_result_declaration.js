
frappe.ui.form.on('Final Result Declaration', {
	
	setup: function(frm) {

		// frm.fields_dict.item.grid.wrapper.on('mouseover', 'input[data-fieldname="result_declaration_student"][data-doctype="Result Declaration Student"]', function() {
		// 	// alert("event::" + e.type);
		// 	var d = frappe.get_(cdt, cdn)
		// 	var d = locals[cdt][cdn];
		// 	alert(cur_frm.get_field("student").grid.grid_rows[0].doc.student);
		// 	alert(cur_frm.get_field("student_name").grid.grid_rows[0].doc.student_name);
		// });
		// frm.fields_dict.item.grid.wrapper.on('mouseover', 'input[data-fieldname="last_purchase_price"][data-doctype="Pre Purchase Order Item"]', function(e) {
		// 	alert("event::" + e.type);
		// 	//var d = frappe.get_(cdt, cdn)
		// 	//var d = locals[cdt][cdn];
		// 	alert(cur_frm.get_field("item").grid.grid_rows[0].doc.last_supplier);
		// 	alert(cur_frm.get_field("item").grid.grid_rows[0].doc.po_number);
		// });

// }
		// document.write("Hey there");

		$("[data-fieldname=programs]").mouseover(function(){
			$("input[data-fieldname='programs']").tooltip({
				// ["data-fieldname=frm.doc.programs"]
				// title: __('programs'),
				title: __(frm.doc.programs)
			});
			// console.log(frm.doc.programs);
		  });

		$("[data-fieldname=semester]").mouseover(function(){
			$("input[data-fieldname='semester']").tooltip({
				// ["data-fieldname=frm.doc.programs"]
				// title: __('programs'),
				title: __(frm.doc.semester)
			});
			// console.log(frm.doc.programs);
		  });
		// $("[data-fieldname=programs]").mouseover(function(){
		// 	$("input[data-fieldname='programs']").tooltip({
		// 		title: __(frm.doc.programs)
		// 	});
		//   });
		// $("[data-fieldname='semester']").mouseover(function(){
		// 	// frm.doc.semester
		// 	$("input[data-fieldname='semester']").css("background-color", "lightgreen");
		// 	// $("input[data-fieldname='semester']").tooltip(frm.doc.semester)
		// 	console.log(frm.doc.semester);
		// })

frm.set_query("programs", function () {
	return {
		filters: [
			["Programs", "program_grade", "=", frm.doc.program_grade],
		]
	}
});
frm.set_query('semester', function(doc) {
	return {
		filters: {
			"programs":frm.doc.programs
		}
	};
});
frm.set_query("academic_term", function() {
	return {
		filters: {
			"academic_year":frm.doc.academic_year
		}
	};
});
},
refresh:function(frm){
if (!frm.doc.__islocal){
	frm.add_custom_button(__('Create Exam Assessment Result'), function() {
		frappe.call({
			method: 'make_exam_assessment_result',
			doc: frm.doc,
			callback: function() {
				frm.refresh();
			}
		});
	}).addClass('btn-primary');;
}

},
onload:function(frm){
frappe.realtime.on('final_result_declaration_progress', function(data) {
	if (data.reload && data.reload === 1) {
		frm.reload_doc();
	}
	if (data.progress && frm.doc.result_creation_status === 'In Process' && data.current && data.total) {
		cur_frm.dashboard.show_progress('Result Creation Status',data.progress+'%',__('Created Exam Assessment Result {0} of {1}', [data.current,data.total]))
	}
});
},
get_students:function(frm){
frm.clear_table("result_declaration_student");
frappe.call({
	method: "wsc.wsc.doctype.final_result_declaration.final_result_declaration.get_enroll_students",
	args: {
		programs: frm.doc.programs,
		semester: frm.doc.semester,
		academic_year: frm.doc.academic_year,
		academic_term: frm.doc.academic_term
	},
	callback: function(r) { 
		(r.message).forEach(element => {
			var row = frm.add_child("result_declaration_student")
			row.student=element.name
			row.student_name=element.student_name
			row.completion_status=element.completion_status
		});
		frm.refresh_field("result_declaration_student")
		frm.set_value("total_enrolled_student",(r.message).length)
	} 
	
});  
}
});
// frappe.ui.form.on('Result Declaration Student', {
// 	onload: function(frm) {
// 		alert("ell")
// 		$("[data-fieldname=student_name]").mouseover(function(){
// 			$("input[data-fieldname='student_name']").tooltip({
// 				// ["data-fieldname=frm.doc.programs"]
// 				title: __('student_name'),
// 				// title: __(data.student)
// 			});
// 			console.log("student_name");
// 		  });
// 	}
// });
frappe.ui.form.on("Result Declaration Student",'student', function(frm, cdt, cdn) {
var d = locals[cdt][cdn];
// var a=0
$("[data-fieldname=d.student_name]").mouseover(function(){
$("input[data-fieldname=d.student_name]").tooltip({
// ["data-fieldname=frm.doc.programs"]
title: __('d.student_name'),
// title: __(data.student)
});
console.log(frm.student_name);
});
// if (d.student_name){
//     a=frm.doc.program_priority.length;
//     frm.set_value("count_programs", a);
//     if(a>=3){
//         frm.set_df_property('program_priority', 'cannot_add_rows', true);
//         frm.set_df_property('program_priority', 'cannot_delete_rows', true); 
//         // frm.set_df_property('program_priority', 'cannot_insert_below', true); 
//     }
// }
});

// frappe.ui.form.on(cur_frm.result_declaration_student, {
// 	'onload_post_render': function(frm, cdt, cdn) {
// 		alert("hey you kiwi2")
// 		frm.fields_dict.item.grid.wrapper.on('mouseover', 'input[data-fieldname="result_declaration_student"][data-doctype="Result Declaration Student"]', function() {
// 		alert("event::" + e.type);
// 			alert("hey you king")
// 			$("[data-fieldname=cur_frm.get_field('student')]").mouseover(function(){
// 				$("input[data-fieldname=cur_frm.get_field('student')]").tooltip({
// 					// ["data-fieldname=frm.doc.programs"]
// 					// title: __('programs'),
// 					title: __("esult_declaration_student")
// 				});
// 				console.log("programs");
// 			});
// 		})
// 	}
// });