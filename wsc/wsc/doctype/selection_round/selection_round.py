# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SelectionRound(Document):
    def on_cancel(self):
        validate_cancel(self)


@frappe.whitelist()
def validate_cancel(self):
    placement_drive_id = self.placement_drive_name
    application_id = self.application_id
    application_status = self.application_status
    current_round_name = self.round_of_placement
    current_round_status = self.drive_round_status
    drive_round_count = frappe.db.sql(""" SELECT COUNT(*) FROM `tabRounds of Placement` WHERE parent = '%s'"""%(placement_drive_id))
    current_round_idx = frappe.db.sql(""" SELECT idx FROM `tabRounds of Placement` WHERE parent = '%s' AND round_name = '%s'"""%(placement_drive_id, current_round_name))
    current_round_result_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` WHERE docstatus = '1' AND drive_round_status = 'Round Result Declaration' AND placement_drive_name = '%s' AND round_of_placement = '%s' AND application_id = '%s'"""%(placement_drive_id, current_round_name, application_id))
    drive_round_count = drive_round_count[0][0]
    current_round_idx = current_round_idx[0][0]
    current_round_result_status = current_round_result_status[0][0]
    placement_drive_blocklist = frappe.db.sql("""SELECT blocklist_id FROM `tabPlacement Drive` WHERE name = '%s'"""%(placement_drive_id))

    if(application_status == 'Hired'):
        parent_doc = frappe.get_doc('Placement Blocked Student', placement_drive_blocklist)
        for d in parent_doc.blocked_student:
            if(d.student == self.student_no):
                d.delete()

    if(drive_round_count == 1):
        if(current_round_status == 'Scheduling Of Round'):
            if(current_round_result_status == 0):
                frappe.set_value('Placement Drive Application', application_id, 'status', 'Applied')
            elif(current_round_result_status > 0):
                frappe.throw('Kindly cancel the result record for this round before cancelling this record')
        elif(current_round_status == 'Round Result Declaration'):
            current_round_scheduling_status = frappe.db.sql(""" SELECT application_status FROM `tabSelection Round` WHERE docstatus = '1' AND drive_round_status = 'Scheduling Of Round' AND placement_drive_name = '%s' AND round_of_placement = '%s' AND application_id = '%s'"""%(placement_drive_id, current_round_name, application_id))
            frappe.set_value('Placement Drive Application', application_id, 'status', current_round_scheduling_status[0][0])
    elif(drive_round_count > 1):
        if(current_round_idx == 1):
            next_round_idx = current_round_idx + 1
            next_round_details = frappe.db.sql(""" SELECT round_name FROM `tabRounds of Placement` WHERE parent = '%s' AND idx = '%s'"""%(placement_drive_id, next_round_idx))
            next_round_name = next_round_details[0][0]
            next_round_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` WHERE docstatus = '1' AND placement_drive_name = '%s' AND round_of_placement = '%s' AND application_id = '%s'"""%(placement_drive_id, next_round_name, application_id))
            next_round_status = next_round_status[0][0]

            if(next_round_status == 0):
                if(current_round_status == 'Scheduling Of Round'):
                    if(current_round_result_status == 0):
                        frappe.set_value('Placement Drive Application', application_id, 'status', 'Applied')
                    elif(current_round_result_status > 0):
                        frappe.throw('Kindly cancel the result record for this round before cancelling this record')
                elif(current_round_status == 'Round Result Declaration'):
                    current_round_scheduling_status = frappe.db.sql(""" SELECT application_status FROM `tabSelection Round` WHERE docstatus = '1' AND drive_round_status = 'Scheduling Of Round' AND placement_drive_name = '%s' AND round_of_placement = '%s' AND application_id = '%s'"""%(placement_drive_id, current_round_name, application_id))
                    frappe.set_value('Placement Drive Application', application_id, 'status', current_round_scheduling_status[0][0])
            elif(next_round_status > 0):
                frappe.throw('Kindly cancel the records for the next round before cancelling this record')
        elif(current_round_idx == drive_round_count):
            prev_round_idx = current_round_idx - 1
            prev_round_name = frappe.db.sql(""" SELECT round_name FROM `tabRounds of Placement` WHERE parent = '%s' AND idx = '%s'"""%(placement_drive_id, prev_round_idx))
            prev_round_name = prev_round_name[0][0]
            prev_result_record_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` WHERE docstatus = '1' AND placement_drive_name = '%s' AND round_of_placement = '%s' AND application_id = '%s' AND drive_round_status = 'Round Result Declaration'"""%(placement_drive_id, prev_round_name, application_id))
            prev_result_record_status = prev_result_record_status[0][0]
            prev_schedule_record_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` WHERE docstatus = '1' AND placement_drive_name = '%s' AND round_of_placement = '%s' AND application_id = '%s' AND drive_round_status = 'Scheduling Of Round'"""%(placement_drive_id, prev_round_name, application_id))
            prev_schedule_record_status = prev_schedule_record_status[0][0]
            
            if(current_round_status == 'Scheduling Of Round'):
                prev_application_status = frappe.db.sql(""" SELECT application_status FROM `tabSelection Round` WHERE docstatus = '1' AND drive_round_status = 'Round Result Declaration' AND placement_drive_name = '%s' AND round_of_placement = '%s' AND application_id = '%s'"""%(placement_drive_id, prev_round_name, application_id))
                if(current_round_result_status == 0):
                    if(prev_result_record_status > 0):
                        frappe.set_value('Placement Drive Application', application_id, 'status', prev_application_status[0][0])
                    elif(prev_schedule_record_status > 0):
                        frappe.set_value('Placement Drive Application', application_id, 'status', prev_application_status[0][0])                    
                elif(current_round_result_status > 0):
                    frappe.throw('Kindly cancel the next document before cancelling this document')
            elif(current_round_status == 'Round Result Declaration'):
                current_round_scheduling_status = frappe.db.sql(""" SELECT application_status FROM `tabSelection Round` WHERE docstatus = '1' AND drive_round_status = 'Scheduling Of Round' AND placement_drive_name = '%s' AND round_of_placement = '%s' AND application_id = '%s' AND drive_round_status = 'Scheduling Of Round'"""%(placement_drive_id, current_round_name, application_id))
                frappe.set_value('Placement Drive Application', application_id, 'status', current_round_scheduling_status[0][0])
        else:
            next_round_idx = current_round_idx + 1
            next_round_details = frappe.db.sql(""" SELECT round_name FROM `tabRounds of Placement` WHERE parent = '%s' AND idx = '%s'"""%(placement_drive_id, next_round_idx))
            next_round_name = next_round_details[0][0]
            next_round_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` WHERE docstatus = '1' AND placement_drive_name = '%s' AND round_of_placement = '%s' AND application_id = '%s'"""%(placement_drive_id, next_round_name, application_id))
            next_round_status = next_round_status[0][0]

            prev_round_idx = current_round_idx -1
            prev_round_name = frappe.db.sql(""" SELECT round_name FROM `tabRounds of Placement` WHERE parent = '%s' AND idx = '%s'"""%(placement_drive_id, next_round_idx))
            prev_round_name = prev_round_name[0][0]
            prev_result_record_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` WHERE docstatus = '1' AND placement_drive_name = '%s' AND round_of_placement = '%s' AND application_id = '%s' AND drive_round_status = 'Round Result Declaration'"""%(placement_drive_id, prev_round_name, application_id))
            prev_result_record_status = prev_result_record_status[0][0]
            prev_schedule_record_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` WHERE docstatus = '1' AND placement_drive_name = '%s' AND round_of_placement = '%s' AND application_id = '%s' AND drive_round_status = 'Scheduling Of Round'"""%(placement_drive_id, prev_round_name, application_id))
            prev_schedule_record_status = prev_schedule_record_status[0][0]
            
            current_round_scheduling_status = frappe.db.sql(""" SELECT application_status FROM `tabSelection Round` WHERE docstatus = '1' AND drive_round_status = 'Scheduling Of Round' AND placement_drive_name = '%s' AND round_of_placement = '%s' AND application_id = '%s' AND drive_round_status = 'Scheduling Of Round'"""%(placement_drive_id, current_round_name, application_id))
            prev_round_result_status = frappe.db.sql(""" SELECT application_status FROM `tabSelection Round` WHERE docstatus = '1' AND drive_round_status = 'Round Result Declaration' AND placement_drive_name = '%s' AND round_of_placement = '%s' AND application_id = '%s' AND drive_round_status = 'Scheduling Of Round'"""%(placement_drive_id, prev_round_name, application_id))

            if(next_round_status == 0):
                if(current_round_status == 'Scheduling Of Round'):
                    if(current_round_result_status == 0):
                        frappe.set_value('Placement Drive Application', application_id, 'status', prev_round_result_status[0][0])
                    elif(current_round_result_status > 0):
                        frappe.throw('Kindly cancel the result record of the current round first')
                elif(current_round_status == 'Round Result Declaration'):
                   frappe.set_value('Placement Drive Application', application_id, 'status', current_round_scheduling_status[0][0])
            elif(next_round_status > 0):
                frappe.throw('Kindly cancel record of the next round before cancelling this record')