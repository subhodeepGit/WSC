frappe.ui.form.on('Placement tool', {
    refresh: function(frm){
        frm.disable_save();
        frm.set_df_property('student_list', 'cannot_add_rows', true);
        frm.set_df_property('student_list', 'cannot_delete_rows', true);

        frm.set_query('placement_drive_name', function(){
            return{
                filters:{
                    'placement_company': frm.doc.company_name,
                    'academic_year' : frm.doc.placement_batch_year
                }
            }
        })
        if(!frm.doc.__isLocal){
            frm.add_custom_button(__('Schedule Round'), function(){
                frappe.call({
                    method: 'schedule_round',
                    doc: frm.doc
                })
            }).addClass('btn-primary')
        }
    },
    placement_drive_name: function(frm){
        frappe.call({
            method: 'wsc.wsc.doctype.placement_tool.placement_tool.get_placement_rounds',
            args:{
                drive_name: frm.doc.placement_drive_name
            },
            callback: function(result){
                let arr = [];
                for(let x in result.message){
                    arr.push(result.message[x]);
                }
                frm.set_df_property('round_of_placement', 'options', arr)
            }
        })
    },
    round_of_placement: function(frm){
        frappe.call({
            method:'wsc.wsc.doctype.placement_tool.placement_tool.get_date_of_round',
            args:{
                doc:frm.doc,
                drive_name: frm.doc.placement_drive_name,
                round_name: frm.doc.round_of_placement
            },
            callback: function(result){
                frm.set_value('scheduled_date_of_round', result.message[0])
            }
        })
    },
    get_eligible_students_list: function(frm){
        frappe.call({
            method: 'wsc.wsc.doctype.placement_tool.placement_tool.get_eligible_students',
            args:{
                drive_name: frm.doc.placement_drive_name
            },
            callback:function(result){
                if(result.message){
                    frappe.model.clear_table(frm.doc, 'student_list');
                    result.message.forEach(elements => {
                        var childTable = frm.add_child('student_list');
                        childTable.ref_no = element.name
                        childTable.student_no = element.student
                        childTable.student_name = element.student_name
                        childTable.program_name = element.programs
                        childTable.academic_year = element.academic_year
                        childTable.semesters = element.semesters
                    })
                }
                frm.refresh()
                frm.refresh_field('student_list')
            }
        })
    }
})