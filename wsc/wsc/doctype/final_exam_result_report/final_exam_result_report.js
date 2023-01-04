// Copyright (c) 2023, SOUL Limited and Contributors
// For license information, please see license.txt

frappe.ui.form.on('Final Exam Result Report', {
	refresh:function(frm){
		frm.disable_save();
		let html_values=cur_frm.fields_dict.report.wrapper;
		var final_exam_result={};
			final_exam_result["rows"]={};
			final_exam_result["academic_year"]=frm.doc.academic_year;
			final_exam_result["academic_term"]=frm.doc.academic_term;
			final_exam_result["programs"]=frm.doc.programs;
			final_exam_result["semester"]=frm.doc.semester;
			if(cur_frm.doc.students){
				(cur_frm.doc.students).forEach(resp => {
					var row={};
					row['student']=resp.student;
					row['roll_no']=resp.roll_no;
					row['registration_number']=resp.registration_number;

					final_exam_result['rows'][resp.student]=row;
				})
			}
	},
	
	setup: function(frm) {
		frm.set_query("programs", function () {
			return {
				filters: [
					["Programs", "program_grade", "=", frm.doc.program_grade],
				]
			}
		});
	
		frm.set_query("academic_term", function() {
			return {
				filters: {
					"academic_year":frm.doc.academic_year,
				}
			};
		});
		frm.set_query('semester', function() {
			return {
				filters: {
					"programs":frm.doc.programs
				}
			};
		});
	},

	academic_year:function(frm){
		frm.trigger("show_report");
	},
	academic_term:function(frm){
		frm.trigger("show_report");
	},
	programs:function(frm){
		frm.trigger("show_report");
	},
	semester:function(frm){
		frm.trigger("show_report");
	},
	show_report:function(frm){
		frm.doc.students=[];
		$(frm.fields_dict.report.wrapper).empty();
		if(frm.doc.academic_year && frm.doc.academic_term && frm.doc.programs && frm.doc.semester) {
			frappe.call({
				method: "get_student_allocations",
				doc:frm.doc,
				callback: function(r) {
					if (r.message) {
						// alert(JSON.stringify(r.message["studnet"]))
						// alert(JSON.stringify(r.message["assessment_result"]))
						$(frm.fields_dict.report.wrapper).empty();
						frm.doc.students=r.message;
						if ((Object.keys(r.message["studnet"]).length) != 0){
							var result_table = $(frappe.render_template('final_exam_result_report', {
								frm: frm,
								students: r.message["studnet"],
								course:r.message["course"],
								assessment_criteria:r.message["assessment_criteria"],
								total_credit:r.message["total_credit"],
								assessment_result:r.message["assessment_result"],
								evaluation_result:r.message["evaluation_result"],
								assessment_criteria_head:r.message["assessment_criteria_head"],
							}));
							result_table.appendTo(frm.fields_dict.report.wrapper);
						}
					}
				}
			});
		}
		// ----------Excel Download with CDN----------------
		// if(frm.doc.academic_year && frm.doc.academic_term && frm.doc.programs && frm.doc.semester) {			
		// 	frm.add_custom_button(__("Export Excel"), function(type, fn, dl) {
		// 			var elt = document.getElementById('tbl_exporttable_to_xls');
		// 			var wb = XLSX.utils.table_to_book(elt, { sheet: "sheet1" });
		// 			return dl ?
		// 				XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }) :
		// 				XLSX.writeFile(wb, fn || ('Final Exam Result Report.' + (type || 'xlsx')));

		// 	});
		// }
		// ----------Excel Download without CDN----------------
		if(frm.doc.academic_year && frm.doc.academic_term && frm.doc.programs && frm.doc.semester) {		
			frm.add_custom_button(__("Export Excel"), function(filename = 'Final Exam Result Report') {
				// var downloadLink;
				// var dataType = 'application/vnd.ms-excel';
				// var tableSelect = document.getElementById('tbl_exporttable_to_xls');
				// var tableHTML = tableSelect.outerHTML.replace(/ /g, '%20');
				// // Specify file name
				// filename = filename?filename+'.xls':'excel_data.xls';
				// // Create download link element
				// downloadLink = document.createElement("a");			
				// document.body.appendChild(downloadLink);				
				// if(navigator.msSaveOrOpenBlob){
				// 	var blob = new Blob(['\ufeff', tableHTML], {
				// 		type: dataType
				// 	});
				// 	navigator.msSaveOrOpenBlob( blob, filename);
				// }else{
				// 	// Create a link to the file
				// 	downloadLink.href = 'data:' + dataType + ', ' + tableHTML;				
				// 	// Setting the file name
				// 	downloadLink.download = filename;					
				// 	//triggering the function
				// 	downloadLink.click();
				// }


				var a = document.createElement('a');
                var postfix = 'KISS'
                //getting data from our div that contains the HTML table
                var data_type = 'data:application/vnd.ms-excel';
                var table_div = document.getElementById('tbl_exporttable_to_xls');
                var table_html = table_div.outerHTML.replace(/ /g, '%20');
                a.href = data_type + ', ' + table_html;
                //setting the file name
                a.download = 'exam_result_report_' + postfix + '.xls';
                //triggering the function
                a.click();
			});
		}
	},
});
