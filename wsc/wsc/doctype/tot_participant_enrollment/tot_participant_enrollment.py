# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ToTParticipantEnrollment(Document):
	# def validate(self):
		# self.create_participant()
		# self.make_participant()
	def on_submit(self):
			self.create_participant()
	def create_participant(self):
		self.db_set("participant_creation_status", "In Process")
		frappe.publish_realtime("tot_participant_enrollment_progress",
			{"progress": "0", "reload": 1}, user=frappe.session.user)

		total_records = len(self.get("participant_list"))
		if total_records > 41:
			frappe.msgprint(_(''' Records will be created in the background.
				In case of any error the error message will be updated in the Schedule.'''))
			frappe.enqueue(make_participant, queue='default', timeout=6000, event='make_participant',
				tot_participant_enrollment=self.name)

		else:
			# print("\n\n\make_participant")
			make_participant(self.name)
	
	@frappe.whitelist()
	def enroll_participant(self):
		self.db_set("participant_enrollment_status", "In Process")
		frappe.publish_realtime("tot_participant_enrollment_progress",
			{"progress": "0", "reload": 1}, user=frappe.session.user)

		total_records = len(self.get("participant_list"))
		if total_records > 41:
			frappe.msgprint(_(''' Records will be created in the background.
				In case of any error the error message will be updated in the Schedule.'''))
			frappe.enqueue(make_enrollment, queue='default', timeout=6000, event='make_enrollment',
				tot_participant_enrollment=self.name)

		else:
			make_enrollment(self.name)

def make_participant(tot_participant_enrollment):
	# print("\n\n\nPART")
	doc = frappe.get_doc("ToT Participant Enrollment", tot_participant_enrollment)
	error = False
	total_records = len(doc.get("participant_list"))
	created_records = 0
	created_records += 1
	if not total_records:
		frappe.throw(_("Please Create Participant Selection Record First"))
	for d in doc.get("participant_list",{'is_reported':1}):
		print("\n\n\n\n\n\n\n\nParticipant",d.is_reported,d.participant)
		result=frappe.new_doc("Student")
		result.first_name=d.first_name
		result.middle_name=d.middle_name
		result.last_name=d.last_name
		result.student_email_id=d.email_address
		check_duplicate_student = frappe.get_all("Student",{'student_email_id':d.email_address},['student_email_id'])
		# print("\n\n\ncheck_duplicate_student",check_duplicate_student)
		if(check_duplicate_student):
			X=check_duplicate_student
			print("\n\nX",X)
			Y=list(X[0].values())
			print("\n\nY",Y)
			print("\n\n\nEmail",Y[0])
			if Y[0]==d.email_address:
				pass
					# frappe.throw("Email Id should be unique")
		else:
			result.save()
			created_records += 1
			frappe.msgprint("Record Created")
			frappe.publish_realtime("tot_participant_enrollment_progress", {"progress": str(int(created_records * 100/total_records)),"current":str(created_records),"total":str(total_records)}, user=frappe.session.user)
			frappe.db.set_value("ToT Participant Enrollment", tot_participant_enrollment, "participant_creation_status", "Successful")
			frappe.publish_realtime("tot_participant_enrollment_progress",
			{"progress": "100", "reload": 1}, user=frappe.session.user)


def make_enrollment(tot_participant_enrollment):
	doc = frappe.get_doc("ToT Participant Enrollment", tot_participant_enrollment)
	error = False
	total_records = len(doc.get("participant_list"))
	created_records = 0
	if not total_records:
		frappe.throw(_("Please Create Participant Record First"))
	
	for d in doc.get("participant_list",{'is_reported':1}):
		for stud in frappe.get_all("Student",{"student_email_id":d.email_address},['name']):
			print("\n\n\nStudent",stud.name)
			result=frappe.new_doc("Program Enrollment")
			result.student=stud.name
			for data in frappe.get_all("ToT Participant Selection",{"name":doc.tot_participant_selection_id},['participant_selection_date']):
				result.programs=doc.programs
				result.program=doc.semester
				result.academic_year=doc.academic_year
				result.academic_term=doc.academic_term
				result.enrollment_date=data.participant_selection_date
				result.student_batch_name=doc.tot_participant_batch
				result.is_tot=1
				result.save()
				result.submit()
				created_records += 1
			frappe.msgprint("Record Created")
		frappe.publish_realtime("tot_participant_enrollment_progress", {"progress": str(int(created_records * 100/total_records)),"current":str(created_records),"total":str(total_records)}, user=frappe.session.user)
		frappe.db.set_value("ToT Participant Enrollment", tot_participant_enrollment, "participant_enrollment_status", "Successful")
		frappe.publish_realtime("tot_participant_enrollment_progress",
		{"progress": "100", "reload": 1}, user=frappe.session.user)




@frappe.whitelist()
def get_participants(participant_selection_id):
    participant_list=frappe.get_all("Selected Participant",{'parent':participant_selection_id},['participant_id','participant_name','hrms_id','district','mobile_number','email_address'])
    return participant_list