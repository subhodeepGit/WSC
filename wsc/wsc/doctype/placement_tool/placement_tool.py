# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc



class PlacementTool(Document):
	@frappe.whitelist()
	def schedule_round(self):
		if(self.round_status == 'Scheduling Of Round'):
			status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` WHERE placement_drive_name = '%s' AND round_of_placement = '%s' """%(self.placement_drive_name, self.round_of_placement))
			data = frappe.db.sql(""" SELECT round_name from `tabRounds of Placement` where parent="%s" ORDER BY idx ASC"""%(self.placement_drive_name))
			data = data[-1]
			print('\n\n\n\n', status[0][0],'\n\n\n\n')
			if(status[0][0] == 0):
				for d in self.get('student_list'):
					result = frappe.new_doc('Selection Round')
					result.student_name = d.student_name
					result.student_no = d.student_no
					result.program_name = d.program_name
					result.academic_year = d.academic_year
					result.semesters = d.semesters
					result.company_name = self.company_name
					result.placement_batch_year = self.placement_batch_year
					result.drive_title = self.drive_title
					result.placement_drive_name = self.placement_drive_name					
					result.round_of_placement = self.round_of_placement				
					result.scheduled_date_of_round = self.scheduled_date_of_round
					if(data == self.round_of_placement):
						result.shortlisting_status = 'Interview scheduled'
					else:
						result.shortlisting_status = d.shortlisting_status
					result.save()
					result.submit()
				frappe.db.sql(""" UPDATE `tabRounds of Placement` SET round_status = 'Round Scheduled' WHERE parent = '%s' and round_name = '%s' """%(self.placement_drive_name, self.round_of_placement))
			elif(status[0][0] > 0):
				print('\n\n\n\n Record already exists \n\n\n\n')
		elif(self.round_status == 'Round Result Declaration'):
			print('\n\n\n\n','Elif','\n\n\n\n')
			for d in self.get('student_list'):
				frappe.db.sql(""" UPDATE `tabSelection Round` SET shortlisting_status = '%s' WHERE student_no='%s' AND placement_drive_name = '%s' AND placement_batch_year='%s' AND round_of_placement = '%s'"""%(d.shortlisting_status, d.student_no,self.placement_drive_name, self.placement_batch_year, self.round_of_placement))
				frappe.db.sql(""" UPDATE `tabPlacement Drive Application` SET status = '%s' WHERE student = '%s' AND placement_drive = '%s' """%(d.shortlisting_status, d.student_no, self.placement_drive_name))
				frappe.db.sql(""" UPDATE `tabApplied Companies` SET round_status = '%s' WHERE parent = '%s' AND drive_title = '%s' """%(d.shortlisting_status, d.student_no, self.drive_title))


@frappe.whitelist()
def get_student(drive_name):
    print(drive_name)
    fil = []
    fil.append(['placement_drive', '=', drive_name])
    fil.append(['status', 'in',['Applied','Shortlisted']])
    fil.append(['docstatus','=',1])
    # student_data = frappe.get_all('Placement Drive Application', [['placement_drive', '=', drive_name],['status', '=','Applied']], ['student','name', 'student_name'])
    student_data = frappe.get_all('Placement Drive Application', filters=fil, fields=['student','name','student_name'])
    print(student_data)
    for t in student_data:
        data = frappe.get_all('Current Educational Details',{'parent':t['student'], 'parenttype':'student'},['programs','semesters', 'academic_year'])
        t['programs'] = data[0]['programs']
        t['semesters'] = data[0]['semesters']
        t['academic_year'] = data[0]['academic_year']
    return student_data

@frappe.whitelist()
def get_date_of_round(doc, drive_name, round_name):
	data = frappe.db.sql(""" SELECT date , reporting_time from `tabRounds of Placement` where parent = '%s' AND round_name = '%s'"""%(drive_name, round_name))
	return data

@frappe.whitelist()
def get_title(company_name):
	data = frappe.db.sql(""" SELECT title FROM `tabPlacement Drive` where placement_company = '%s' """%(company_name))
	return data

@frappe.whitelist()
def get_rounds_of_placement(self,drive_name=None,round_status=None):
	print('echo')
	all_round_names = frappe.db.sql(""" SELECT idx, round_name FROM `tabRounds of Placement` WHERE parent = '%s' ORDER BY idx ASC"""%(self.placement_drive_name))
	rounds_not_scheduled = frappe.db.sql(""" SELECT idx, round_name FROM `tabRounds of Placement` WHERE parent = '%s' AND round_status = 'Not Scheduled' ORDER BY idx ASC"""%(self.placement_drive_name))
	rounds_scheduled = frappe.db.sql(""" SELECT idx, round_name FROM `tabRounds of Placement` WHERE parent = '%s' AND round_status = 'Scheduled' ORDER BY idx """%(self.placement_drive_name))
	
	previous_round = rounds_scheduled[0]
	previous_round_idx = previous_round[0]
	previous_round_name = previous_round[1]
	
	current_round = rounds_not_scheduled[0]
	current_round_idx = current_round[0]
	current_round_name = current_round[1]

	current_round_scheduling_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` parent = '%s' AND round_of_placement = '%s' AND round_status = 'scheduled'"""%(self.placement_drive_name, current_round_name))

	if(self.round_status == 'Scheduling Of Round'):
		if(current_round_idx == 1):
			if(current_round_scheduling_status[0][0] == 0):
				return current_round_name
		elif(current_round_idx > 1):
			if(current_round_scheduling_status[0][0] == 0):
				previous_round_result_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` parent = '%s' AND round_of_placement = '%s' AND round_status = 'result declared'"""%(self.placement_drive_name, previous_round_name))
				if(previous_round_result_status > 0):
					return current_round_name
	elif(self.round_status == 'Round Result Declaration'):
		if(current_round_scheduling_status[0][0] > 1):
			current_round_result_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` parent = '%s' AND round_of_placement = '%s' AND round_status = 'result declared'"""%(self.placement_drive_name, current_round_name))
			previous_round_result_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` parent = '%s' AND round_of_placement = '%s' AND round_status = 'result declared'"""%(self.placement_drive_name, previous_round_name))
			if(current_round_idx == 1):
				if(current_round_result_status[0][0] == 0):
					if(current_round_scheduling_status[0][0] > 0):
						return current_round_name
			elif(current_round_idx > 1):
				if(current_round_result_status[0][0] == 0):
					if(current_round_scheduling_status[0][0] > 1):
						previous_round_result_status = frappe.db.sql(""" SELECT COUNT(*) FROM `tabSelection Round` parent = '%s' AND round_of_placement = '%s' AND round_status = 'result declared'"""%(self.placement_drive_name, previous_round_name))
						if(previous_round_result_status[0][0] > 0):
							return current_round_name
