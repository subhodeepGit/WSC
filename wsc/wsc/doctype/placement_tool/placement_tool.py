# # Copyright (c) 2023, SOUL Limited and contributors
# # For license information, please see license.txt


import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class PlacementTool(Document):
    def validate(self):
        for d in self.get('student_list'):
            print(d.ref_no)
            frappe.set_value('Placement Drive Application', d.ref_no, 'status', d.shortlisting_status)

        if self.round_status == 'Scheduling Of Round':
            frappe.db.sql(""" UPDATE `tabRounds of Placement` SET round_status = 'Scheduled' WHERE parent = '%s' and round_name = '%s' """%(self.placement_drive_name, self.round_of_placement))
        elif self.round_status == 'Round Result Declaration':
            frappe.db.sql(""" UPDATE `tabRounds of Placement` SET round_status = 'Result Declared' WHERE parent = '%s' and round_name = '%s' """%(self.placement_drive_name, self.round_of_placement))
            
        for d in self.get('student_list'):
                print(d.student_name)
                result = frappe.new_doc('Selection Round')
                result.student_name = d.student_name
                result.student_no = d.student_no
                result.program_name = d.program_name
                result.academic_year = d.academic_year
                result.semesters = d.semesters
                result.company_name = self.company_name
                result.placement_batch_year = self.placement_batch_year
                result.placement_drive_name = self.placement_drive_name
                result.round_of_placement = self.round_of_placement
                result.scheduled_date_of_round = self.scheduled_date_of_round
                result.save()
                result.submit()

    
@frappe.whitelist()
def get_drive_names(company_name):
    data = frappe.db.sql(""" SELECT title FROM `tabPlacement Drive` WHERE placement_company = '%s'"""%(company_name))
    return data

@frappe.whitelist()
def get_placement_round_names(self, drive_name, round_status):
    all_round_names = frappe.db.sql(""" SELECT idx, round_name FROM `tabRounds of Placement` WHERE parent = '%s' ORDER BY idx ASC """ %(drive_name))
    rounds_scheduled = frappe.db.sql(""" SELECT idx, round_name FROM `tabRounds of Placement` WHERE parent = '%s' AND round_status = 'Scheduled' ORDER BY idx ASC"""%(drive_name))
    rounds_not_scheduled = frappe.db.sql(""" SELECT idx, round_name FROM `tabRounds of Placement` WHERE parent = '%s' AND round_status = 'Not Scheduled' ORDER BY idx ASC"""%(drive_name))
    rounds_result_declared = frappe.db.sql(""" SELECT idx, round_name FROM `tabRounds of Placement` WHERE parent = '%s' AND round_status = 'Result Declared' ORDER BY idx ASC"""%(drive_name))
    if(round_status == 'Scheduling Of Round'):
        if(len(rounds_not_scheduled) == 0):
            return 'all rounds have been scheduled'
        elif(len(rounds_not_scheduled) > 0):
            return rounds_not_scheduled[0][1]
    elif(round_status == 'Round Result Declaration'):
        if(len(rounds_scheduled) == 0):
            return 'No rounds have been scheduled'
        elif(len(rounds_result_declared) == len(all_round_names)):
            return 'All results have been declared'
        elif(len(rounds_scheduled) > 0):
            return rounds_scheduled[0][1]

@frappe.whitelist()
def get_round_details(doc, drive_name, round_name):
    data = frappe.get_all('Rounds of Placement', filters = [['parent','=',drive_name],['round_name','=',round_name]],fields=['date','reporting_time'])
    scheduled_date_of_round=data[0]['date']
    scheduled_time_of_round=data[0]['reporting_time']
    return [scheduled_date_of_round,scheduled_time_of_round]

@frappe.whitelist()
def get_students(drive_name):
    fil = []
    fil.append(['placement_drive', '=', drive_name])
    fil.append(['status', 'in',['Applied','Shortlisted']])
    fil.append(['docstatus','=',1])
    student_data = frappe.get_all('Placement Drive Application', filters=fil, fields=['name', 'student','student_name'])
    for t in student_data:
        data = frappe.get_all('Current Educational Details',{'parent':t['student'], 'parenttype':'student'},['programs','semesters', 'academic_year'])
        t['programs'] = data[0]['programs']
        t['semesters'] = data[0]['semesters']
        t['academic_year'] = data[0]['academic_year']
    return student_data