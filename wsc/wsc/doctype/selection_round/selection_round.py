# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SelectionRound(Document):
    def on_cancel(self):
        validate_cancel(self)
        pass

@frappe.whitelist()
def validate_cancel(self):
    # parameters
    placement_drive_id = self.placement_drive_name
    application_id = self.application_id
    appliction_status = self.application_status
    current_round_name = self.round_of_placement
    current_round_status = self.drive_round_status


    # delete if not needed

    print('\n\n\n')
    print(placement_drive_id)
    print(application_id)
    print(appliction_status)
    print(current_round_name)
    print(current_round_status)
    print('\n\n\n')

    round_count = frappe.db.sql(""" SELECT COUNT(*) FROM `tabRounds of Placement` WHERE parent = '%s'"""%(placement_drive_id))
    current_round_details = frappe.db.sql(""" SELECT idx FROM `tabRounds of Placement` WHERE parent = '%s' AND round_name = '%s'"""%(placement_drive_id, current_round_name))
    current_round_idx = current_round_details[0][0]
    
    # delete if not needed
    print('\n\n\n')
    print(current_round_name)
    print(current_round_idx)
    print('\n\n\n')

    if(round_count[0][0] == 1):
        if(current_round_status == 'Scheduling Of Round'):
            result_record_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` WHERE docstatus = '1' AND placement_drive_name = '%s' AND round_of_placement = '%s' AND application_id = '%s'"""%(placement_drive_id, current_round_name, application_id))
            if(result_record_status[0][0] > 0):
                # record cannot be deleted before the result record is deleted
                print('Kindly delete the result record first')
                pass
            else:
                # updating student application
                frappe.set_value('Placement Drive Application', application_id, 'status', 'Applied')
            pass
        elif(current_round_status == 'Round Result Declaration'):
            # updating student application
            frappe.set_value('Placement Drive Application', application_id, 'status', 'Applied')
            pass
        pass
    elif(round_count[0][0] > 1):
        print('\n\n\n')
        print('multiple rounds')
        print('\n\n\n')
        # checking round idx
        if(current_round_idx == 1):
            # first round
            print('\n\n\n')
            print('first round')
            print('\n\n\n')
            next_round_idx = current_round_idx + 1
            next_round_name = frappe.db.sql(""" SELECT round_name FROM `tabRounds of Placement` WHERE parent = '%s' AND idx = '%s'"""%(placement_drive_id, next_round_idx))
            next_round_name = next_round_name[0][0]
            result_record_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` WHERE docstatus = '1' AND placement_drive_name = '%s' AND round_of_placement = '%s' AND application_id = '%s'"""%(placement_drive_id, next_round_name, application_id))
            if(result_record_status[0][0] > 0):
                frappe.throw('Kindly cancel records of the next round before cancelling this record')
            else:
                print('\n\n\n')
                print('next round records are not present and update student application status with applied')
                print('\n\n\n')
                if(current_round_status == 'Scheduling Of Round'):
                    result_record_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` WHERE docstatus = '1' AND placement_drive_name = '%s' AND round_of_placement = '%s' AND application_id = '%s'"""%(placement_drive_id, current_round_name, application_id))
                    if(result_record_status[0][0] > 0):
                        # record cannot be deleted before the result record is deleted
                        print('Kindly delete the result record first')
                        pass
                    else:
                        # updating student application
                        frappe.set_value('Placement Drive Application', application_id, 'status', 'Applied')
                    pass
                elif(current_round_status == 'Round Result Declaration'):
                    # updating student application
                    frappe.set_value('Placement Drive Application', application_id, 'status', 'Applied')
        elif(current_round_idx == round_count):
            # last round
            pass
        else:
            # intermediate round
            pass
        pass

    # dont delete till after completion of test
    frappe.throw("end")

# @frappe.whitelist()
# def validate_cancel(self):
#     # get parameters
#     placement_drive_id = self.placement_drive_name
#     application_id = self.application_id
#     application_status = self.application_status
#     round_name = self.round_of_placement
#     round_status = self.drive_round_status

#     # counting rounds
#     round_count = frappe.db.sql(""" SELECT COUNT(*) FROM `tabRounds of Placement` WHERE parent = '%s'"""%(placement_drive_id))
#     # if round count is 1
#     if(round_count[0][0] == 1):
#         if(round_status == 'Scheduling Of Round'):
#             check_result_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` WHERE placement_drive_name = '%s' AND application_id = '%s' AND drive_round_status = 'Round Result Declaration' AND docstatus = '1'"""%(placement_drive_id,application_id))
#             if(check_result_status[0][0] > 0):
#                 frappe.throw("Kindly delete the result record for this applicant before cancelling this record")
#     elif(round_count[0][0] > 1):
#         get_round_idx = frappe.db.sql(""" """)
#         if(get_round_idx[0][0] == 1):
#             next_round_idx = get_round_idx[0][0] + 1
#             next_round_name = frappe.db.sql(""" """)
#             next_round_status = frappe.db.sql(""" """)
#             if(next_round_status[0][0] > 0):
#                 frappe.throw("Kindly delete records of the next round before cancelling this record")
#             else:
#                 if(round_status == 'Scheduling Of Round'):
#                     check_result_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` WHERE placement_drive_name = '%s' AND application_id = '%s' AND drive_round_status = 'Round Result Declaration' AND docstatus = '1'"""%(placement_drive_id,application_id))
#                     if(check_result_status[0][0] > 0):
#                         frappe.throw("Kindly delete the result record for this applicant before cancelling this record")
#         elif(get_round_idx[0][0] == round_count):
#             prev_round_idx = get_round_idx[0][0] - 1
#             if(round_status == "Scheduling Of Round"):
#                 check_result_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` WHERE placement_drive_name = '%s' AND application_id = '%s' AND drive_round_status = 'Round Result Declaration' AND docstatus = '1'"""%(placement_drive_id,application_id))
#                 if(check_result_status[0][0] > 0):
#                     frappe.throw("Kindly delete the result record for this applicant before cancelling this record")
#                 pass
#             else:
#                 pass
#             pass
#         else:
#             next_round_idx = get_round_idx[0][0] + 1
#             prev_round_idx = get_round_idx[0][0] - 1
#             pass
#         pass
#     pass