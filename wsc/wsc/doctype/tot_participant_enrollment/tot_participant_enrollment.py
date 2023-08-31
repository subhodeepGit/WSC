# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class ToTParticipantEnrollment(Document):
	def validate(self):
		data=frappe.get_all("ToT Participant Enrollment",{"tot_participant_selection_id":self.tot_participant_selection_id,"docstatus":1})
		if data:
			frappe.throw("Participant Selection Id is already submitted")

	def on_submit(self):
		participant_count_validation(self)	
		self.create_participant()

	def create_participant(self):
		self.db_set("participant_creation_status", "In Process")
		frappe.publish_realtime("tot_participant_enrollment_progress",
			{"progress": "0", "reload": 1}, user=frappe.session.user)

		total_records = len(self.get("participant_list"))
		if total_records > 50:
			frappe.msgprint(_(''' Records will be created in the background.
				In case of any error the error message will be updated in the Schedule.'''))
			frappe.enqueue(make_participant, queue='default', timeout=6000, event='make_participant',
				tot_participant_enrollment=self.name)

		else:
			make_participant(self.name)

	def on_cancel(self):
		participant_list=[]
		for t in self.get("participant_list"):
			if t.is_reported==1:
				doc=frappe.get_doc("Program Enrollment",t.program_enrollment)
				doc.cancel()
				participant_list.append(t.participant)
				frappe.db.set_value('Reported Participant', t.name, 'program_enrollment',"")

		result=frappe.get_doc("ToT Participant Selection",self.tot_participant_selection_id)
		for t in result.get("participants"):
			for j in participant_list:
				if j==t.participant_id:
					frappe.set_value('Selected Participant',t.name, {
									"reporing_status":"Not Reported",
									"participant_enrollment_no":""
								})	
		frappe.db.sql(""" UPDATE `tabToT Participant Enrollment` SET status="Cancelled" where name="%s" """%(self.name))	




	
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

def participant_count_validation(self):
	count=0
	for t in self.get("participant_list"):
		if t.is_reported==1:
			count=count+1

	if count==0:
		frappe.throw("No Participant has not been repoted. Hence It can't be Submitted")



def make_participant(tot_participant_enrollment):
	doc = frappe.get_doc("ToT Participant Enrollment", tot_participant_enrollment)
	error = False
	total_records = len(doc.get("participant_list"))
	created_records = 0
	created_records += 1
	if not total_records:
		frappe.throw(_("Please Create Participant Selection Record First"))
	for d in doc.get("participant_list",{'is_reported':1}):
		check_duplicate_student = frappe.get_all("Student",{'student_email_id':d.email_address},['student_email_id'])
		if(check_duplicate_student):
			X=check_duplicate_student
			Y=list(X[0].values())
			if Y[0]==d.email_address:
				pass
		else:	
			result=frappe.new_doc("Student")
			result.first_name=d.first_name
			result.middle_name=d.middle_name
			result.last_name=d.last_name
			result.student_email_id=d.email_address
			result.district=d.district
			result.state=d.odisha
			result.pin_code=d.pincode
			result.save()

			student=result.name
			result=frappe.get_doc("ToT Participant",d.participant)
			result.student_no=student
			result.user=d.email_address 
			result.save()

			created_records += 1
			frappe.msgprint("Record Created")
			# frappe.publish_realtime("tot_participant_enrollment_progress", {"progress": str(int(created_records * 100/total_records)),"current":str(created_records),"total":str(total_records)}, user=frappe.session.user)
			# frappe.db.set_value("ToT Participant Enrollment", tot_participant_enrollment, "participant_creation_status", "Successful")
			# frappe.publish_realtime("tot_participant_enrollment_progress",
			# {"progress": "100", "reload": 1}, user=frappe.session.user)	


def make_enrollment(tot_participant_enrollment):
	doc = frappe.get_doc("ToT Participant Enrollment", tot_participant_enrollment)
	error = False
	total_records = len(doc.get("participant_list"))
	created_records = 0
	if not total_records:
		frappe.throw(_("Please Create Participant Record First"))
	
	participant_list=[]
	for d in doc.get("participant_list",{'is_reported':1}):
		for stud in frappe.get_all("Student",{"student_email_id":d.email_address},['name']):
			participant_list.append(d.participant)
			for data in frappe.get_all("ToT Participant Selection",{"name":doc.tot_participant_selection_id},['participant_selection_date']):
				result=frappe.new_doc("Program Enrollment")
				result.student=stud.name
				result.participant=d.participant
				result.programs=doc.programs
				result.program=doc.semester
				result.academic_year=doc.academic_year
				result.academic_term=doc.academic_term
				result.enrollment_date=data.participant_selection_date
				result.student_batch_name=doc.tot_participant_batch
				result.admission_status="Admitted"
				result.is_provisional_admission="No" 
				result.is_tot=1
				for get_course in frappe.get_all("Program Course",{'parent':result.program,'parenttype':'Program'},['course','course_name']):
					result.append("courses",{
					"course":get_course.course,
					"course_name":get_course.course_name,
					})
				result.save()
				result.submit()

				program_enrollment_name=result.name
				frappe.db.set_value('Reported Participant', d.name, 'program_enrollment', program_enrollment_name)


				created_records += 1
			
		# frappe.publish_realtime("tot_participant_enrollment_progress", {"progress": str(int(created_records * 100/total_records)),"current":str(created_records),"total":str(total_records)}, user=frappe.session.user)
		# frappe.db.set_value("ToT Participant Enrollment", tot_participant_enrollment, "participant_enrollment_status", "Successful")
		# frappe.publish_realtime("tot_participant_enrollment_progress",
		# {"progress": "100", "reload": 1}, user=frappe.session.user)

	result=frappe.get_doc("ToT Participant Selection",doc.tot_participant_selection_id)
	for t in result.get("participants"):
		for j in participant_list:
			if j==t.participant_id:
				frappe.set_value('Selected Participant',t.name, {
								"reporing_status":"Repoted",
								"participant_enrollment_no":doc.name
							})

	for t in participant_list:
		data=frappe.get_all("Previous Participation Table",{"parent":t,"participant_selection":doc.tot_participant_selection_id},['name'])
		frappe.set_value("Previous Participation Table",data[0]['name'],'participant_enrollment',doc.name)

	frappe.set_value("ToT Participant Enrollment",tot_participant_enrollment,"status","Completed")	
	frappe.msgprint("Record Created")				




@frappe.whitelist()
def get_participants(participant_selection_id):
    participant_list=frappe.get_all("Selected Participant",{'parent':participant_selection_id,'reporing_status':"Not Reported","docstatus":1},
				    ['participant_id','participant_name','hrms_id','district','mobile_number','email_address','odisha','pincode','is_hostel_required','room_type'],
					order_by="idx asc")
    return participant_list

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def tot_participant_selection_id(doctype, txt, searchfield, start, page_len, filters):

	data=[]
	
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)	

	data=frappe.db.sql("""
		SELECT `name`,`tot_participant_batch` FROM `tabToT Participant Selection` WHERE ({key} like %(txt)s or {scond})  and
		    (`start_date` <= now() AND `end_date` >= now()) 
	""".format(
		**{
			"key": searchfield,
			"scond": searchfields,
		}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	return data