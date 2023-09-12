# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from datetime import datetime, timedelta,timedelta
from wsc.wsc.utils import get_courses_by_semester

class ParticipantGroup(Document):
	def validate(self):
		dupicate_student_group_chk(self)
		self.calculate_total_hours()
		self.trainer_ck()
		dulicate_trainer_chk(self)
		class_scheduling_date_validation(self)
		re_scheduling_chk(self)
		class_scheduling_ovelaping_chk(self)
		tot_class_schedule(self)
		cancel_class(self)


	def calculate_total_hours(self):
		for d in self.get("classes"):
			if d.to_time and d.from_time:
				d.duration = datetime.strptime(d.to_time, '%H:%M:%S') - datetime.strptime(d.from_time, '%H:%M:%S')
				if d.duration < timedelta(0):
					frappe.throw("Duration of the class can't be negative for the line no <b>%s</b>"%(d.idx))

	def trainer_ck(self):
		flag="No"
		for t in self.get("instructor"):
			flag="Yes"
			break
		if flag=="No":
			frappe.throw("Please Provide Trainers Details")		


def cancel_class(self):
	participant_group_id=self.name
	module_name=self.course
	for t in self.get('classes'):
		if t.is_canceled==1:
			re_scheduled_data=frappe.get_all('ToT Class Schedule',{
												'participant_group_id':participant_group_id,
												'module_id':module_name,
												'scheduled_date':t.scheduled_date,
												'from_time':t.from_time,
												"to_time":t.to_time,
												'room_name':t.room_name,
												},['name'])
			
			for j in re_scheduled_data:
				doc=frappe.get_doc('ToT Class Schedule',j['name'])
				doc.is_canceled=1
				doc.save()


	data=frappe.get_all("Participant Group",{"name":self.name})
	if data:
		doc_before_save = self.get_doc_before_save()
		old_object=doc_before_save.get("classes")
		for t in self.get('classes'):
			if t.is_scheduled==1:
				if t.is_canceled==0:
					for j in old_object:
						if t.name==j.name and t.is_canceled!=j.is_canceled:
							re_scheduled_data=frappe.get_all('ToT Class Schedule',{
													'participant_group_id':participant_group_id,
													'module_id':module_name,
													'scheduled_date':t.scheduled_date,
													'from_time':t.from_time,
													"to_time":t.to_time,
													'room_name':t.room_name,
													},['name'])
							for k in re_scheduled_data:	
								doc=frappe.get_doc('ToT Class Schedule',k['name'])
								doc.is_canceled=0
								doc.save()



def re_scheduling_chk(self):
	present_object=self.get("classes")
	data=frappe.get_all("Participant Group",{"name":self.name})
	if data:
		doc_before_save = self.get_doc_before_save()
		old_object=doc_before_save.get("classes")
		for p in present_object:
			if p.re_scheduled==1:
				for o in old_object:
					if p.name==o.name:
						if p.scheduled_date==o.scheduled_date and p.room_name==o.room_name and p.from_time==o.from_time and p.to_time==p.to_time:  
							frappe.throw("<b>No change found in the the Class Rescheduling for line no:- %s </b>"%(p.idx))

def tot_class_schedule(self):
	for d in self.get("classes"):
		if d.is_scheduled!=1:
			if d.re_scheduled!=1:
				for t in self.get('instructor'):
					parent_doc = frappe.new_doc("ToT Class Schedule")
					parent_doc.participant_group_id = self.name
					parent_doc.academic_year = self.academic_year
					parent_doc.academic_term = self.academic_term
					parent_doc.course_name = self.program
					parent_doc.module_id = self.course
					parent_doc.module_name = self.module_name
					parent_doc.scheduled_date = d.scheduled_date
					parent_doc.room_number = d.room_number
					parent_doc.room_name = d.room_name
					parent_doc.from_time = d.from_time
					parent_doc.to_time = d.to_time
					parent_doc.duration = d.duration
					parent_doc.trainers=t.instructors
					parent_doc.save()
				d.is_scheduled=1
		if d.re_scheduled==1 and d.is_scheduled==1:
			participant_group_id=self.name
			module_name=self.course
			old_data=[]
			doc_before_save = self.get_doc_before_save()
			for t in doc_before_save.get('classes'):
				if t.idx==d.idx:
					a={}
					a['scheduled_date']=t.scheduled_date
					a['room_name']=t.room_number 
					a['from_time']=t.from_time
					a['to_time']=t.to_time
					a['name']=t.name
					# a['idx']=
					old_data.append(a)
			for t in old_data:
				for j in self.get('instructor'):
					re_scheduled_data=frappe.get_all('ToT Class Schedule',{
														'participant_group_id':participant_group_id,
														'module_id':module_name,
														'scheduled_date':t['scheduled_date'],
														'from_time':t['from_time'],
														"to_time":t['to_time'],
														'room_number':t['room_name'],
														'trainers':j.instructors
														},['name'])
					for k in re_scheduled_data:
						doc=frappe.get_doc('ToT Class Schedule',k['name'])
						doc.scheduled_date=d.scheduled_date
						doc.from_time=d.from_time
						doc.to_time=d.to_time
						doc.duration=d.duration
						doc.room_number=d.room_number
						doc.re_scheduled=1
						doc.save()
			d.re_scheduled=0

def class_scheduling_date_validation(self):
	####################### data time validation of the scheduling
	classes=[]
	for t in self.get('classes'):
		for j in self.get('classes'):
			if t.scheduled_date==j.scheduled_date and t.name!=j.name and t.room_name!=j.room_name:
				t_from_time=datetime.strptime(t.from_time, "%H:%M:%S")
				t_to_time=datetime.strptime(t.to_time, "%H:%M:%S") 
				j_from_time=datetime.strptime(j.from_time,"%H:%M:%S")
				j_to_time=datetime.strptime(j.to_time, "%H:%M:%S")
				#### from time check
				if j_from_time<=t_from_time<=j_to_time:
					frappe.throw("class schedule Overlapping in line No %s and %s "%(t.idx,j.idx))
				##### to Time check
				if j_from_time<=t_to_time<=j_to_time:
					frappe.throw("class schedule Overlapping in line No %s and %s "%(t.idx,j.idx))
	######################### End of data time validation of the scheduling


@frappe.whitelist()
def participant(doctype, txt, searchfield, start, page_len, filters):
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields = " or ".join("TP."+field + " like %(txt)s" for field in searchfields)
	participant_group_id=filters.get('participant_group_id')
	participant_details = frappe.db.sql(""" SELECT TP.name 
											FROM `tabParticipant Table` as PT
											JOIN `tabToT Participant` as TP on TP.name=PT.participant
											where (TP.{key} like %(txt)s or {scond}) and
													PT.parent = '{participant_group_id}'
											""".format(
												**{
												"key": searchfield,
												"scond": searchfields,
												"participant_group_id":participant_group_id
											}),{"txt": "%%%s%%" % txt, "start": start, "page_len": page_len})
	return participant_details
				# t1 =datetime.strptime(d.from_time, "%H:%M:%S")
				# t2 = datetime.strptime(d.to_time, "%H:%M:%S")
				# delta = t2 - t1
				# ms = delta.total_seconds()/60
				# d.duration=round(ms,2)
				# if d.duration<=0:
				# 	idx=d.idx
				# 	frappe.throw(f"Time Duration can't be <b>Negative or Zero</b> for the line no <b><i>{idx}</i></b>")


def class_scheduling_ovelaping_chk(self):
	tot_start_date=self.tot_start_date
	tot_end_date=self.tot_end_date 
	error_list=[]
	for t in self.get('classes'):
		date_string = t.scheduled_date # Replace with your date string
		date_format = "%Y-%m-%d"
		parsed_date = datetime.strptime(date_string, date_format).date()
		if tot_start_date<=parsed_date <=tot_end_date:
			pass
		else:
			error_list.append(t.idx)
	if error_list:
		frappe.throw("<b>Class Schedule is beyond TOT period</b>")



def dupicate_student_group_chk(self):
	data=frappe.get_all("Participant Group",{"participant_enrollment_id":self.participant_enrollment_id,
				     "course":self.course,"disabled":0,"docstatus":0},['name'])
	flag="No"
	for t in data:
		if t['name']==self.name:
			flag="Yes"
	if flag=="No":
		if data:
			frappe.throw("Participant Group Already Present")


def dulicate_trainer_chk(self):
	trainer_list=[]
	for t in self.get('instructor'):
		trainer_list.append(t.instructors)

	mylist =trainer_list
	myset = set(mylist)
	if len(mylist) != len(myset):
		frappe.throw("Duplicates Record found in the Trainer List")





@frappe.whitelist()
def get_enrollment_details(enrollment_id):
	if(enrollment_id == ''):
		return ['','','', '']
	else:
		enrollment_details = frappe.db.sql(""" SELECT  academic_year, academic_term, programs, semester FROM `tabToT Participant Enrollment` WHERE name = '%s'"""%(enrollment_id), as_dict=1)
		# modules = frappe.db.sql(""" SELECT course FROM `tabProgram Course` WHERE parent = '%s'"""%(enrollment_details[0]['programs']))
		return [enrollment_details[0]['academic_year'], enrollment_details[0]['academic_term'], enrollment_details[0]['programs'], enrollment_details[0]['semester']]

@frappe.whitelist()
def get_module_name(module_id):
	if(module_id == ''):
		return ''
	else:
		data = frappe.db.sql(""" SELECT course_name FROM `tabCourse` WHERE name = '%s'"""%(module_id), as_dict =1)
		return data[0]['course_name']

@frappe.whitelist()
def get_participants(enrollment_id = None):
	if(enrollment_id == None):
		pass
	else:
		data = frappe.get_all("Reported Participant", filters = [['parent', '=', enrollment_id], ['is_reported', '=', 1]], fields =['participant', 'participant_name'])
		return data