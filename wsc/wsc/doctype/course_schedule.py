import frappe
from frappe import _
from frappe.model.document import Document
import datetime
from wsc.wsc.utils import duplicate_row_validation
from dateutil import parser

class CourseSchedule(Document):
	def validate(self):
		self.instructor_name = frappe.db.get_value("Instructor", self.instructor, "instructor_name")
		self.set_title()
		self.validate_course()
		self.validate_date()
		self.validate_overlap()
		duplicate_row_validation(self, "student_paper_code", ['student','student_name',])
		validate_course(self)
		validate_instructor(self)
		validate_exam_declaration(self)
		validate_student_for_student_group(self)
		validate_instructor_for_course(self)
		class_scheduled = frappe.db.sql("""Select count(*) from `tabCourse Schedule` where instructor = %s""",self.instructor_name)
		# print("\n\n\n\n\n")
		# print(self.instructor_name)
		# print(class_scheduled[0][0])
		frappe.db.set_value("Instructor",self.instructor_name,"total_scheduled_classes",class_scheduled[0][0]+1)

		# a.s
	def set_title(self):
		"""Set document Title"""
		self.title = self.course + " by " + (self.instructor_name if self.instructor_name else self.instructor)

	def validate_course(self):
		group_based_on, course = frappe.db.get_value("Student Group", self.student_group, ["group_based_on", "course"])
		if group_based_on == "Course":
			self.course = course

	def validate_date(self):
		"""Validates if from_time is greater than to_time"""
		if	parser.parse(str(self.from_time)) > parser.parse(str(self.to_time)):
			frappe.throw(_("From Time cannot be greater than To Time."))

	def validate_overlap(self):
		"""Validates overlap for Student Group, Instructor, Room"""

		from education.education.utils import validate_overlap_for

		#Validate overlapping course schedules.
		if self.student_group:
			validate_overlap_for(self, "Course Schedule", "student_group")

		validate_overlap_for(self, "Course Schedule", "instructor")
		validate_overlap_for(self, "Course Schedule", "room", self.room)

		#validate overlapping assessment schedules.
		if self.student_group:
			validate_overlap_for(self, "Assessment Plan", "student_group")

		validate_overlap_for(self, "Assessment Plan", "room")
		validate_overlap_for(self, "Assessment Plan", "supervisor", self.instructor)

	def on_update(self):
		for pec in frappe.get_all("Program Enrollment Course",{'course':self.course}):
			frappe.db.set_value("Program Enrollment Course",pec.name,'instructor',self.instructor)


def validate_course(doc):
    if not doc.is_exam_schedule and doc.course not in [d.course for d in frappe.get_all("Student Group Instructor",{"parent":doc.get("student_group"),"instructor":doc.get("instructor")},['course'])]:
        frappe.throw("Course <b>'{0}'</b> not belongs to student group <b>'{1}'</b> and instructor <b>'{2}'</b>".format(doc.get('course'), doc.get('student_group'), doc.get('instructor')))

def validate_instructor(doc):
    if not doc.is_exam_schedule and doc.instructor not in [d.instructor for d in frappe.get_all("Student Group Instructor",{"parent":doc.get("student_group")},['instructor'])]:
        frappe.throw("Instructor <b>'{0}'</b> not belongs to student group <b>'{1}'</b> ".format(doc.get('instructor'), doc.get('student_group')))

def validate_exam_declaration(doc):
    ed_list = frappe.db.sql("""SELECT distinct(ed.name) as name from `tabExam Declaration` ed 
    left join `tabExam Courses` c on c.parent=ed.name where c.courses='{0}' and ed.docstatus=1""".format(doc.get("course")), as_dict=1)
    if doc.exam_declaration:
        if doc.exam_declaration not in [d.name for d in ed_list if ed_list]:
            frappe.throw("Exam declaration <b>'{0}'</b> not belongs to course <b>'{1}'</b> ".format(doc.get('exam_declaration'), doc.get('course')))

def validate_student_for_student_group(doc):
    student_list =frappe.db.sql("""SELECT stg.student as student from `tabStudent Group Student` stg 
    left join `tabStudent Group` sg on stg.parent=sg.name where sg.name='{0}' """.format(doc.get("student_group")), as_dict=1)
    for stud in doc.student_paper_code:
        if stud.student not in [s.student for s in student_list]:
            frappe.throw("Student <b>'{0}'</b> not belongs to student group <b>'{1}'</b> ".format(stud.student, doc.get('student_group')))

def validate_instructor_for_course(doc):
    if not doc.is_exam_schedule:
        for i in doc.additional_instructor:
            if i.instructor not in [d.parent for d in frappe.get_all("Instructor Log",{"course":doc.get("course")},['parent'])]:
                frappe.throw("Instructor <b>'{0}'</b> not belongs to course <b>'{1}'</b> ".format(i.instructor, doc.get('course')))

@frappe.whitelist()
def get_exam_declaration_by_course(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""Select distinct(ed.name),ed.exam_name from `tabExam Declaration` ed left join `tabExam Courses` c on c.parent=ed.name where c.courses='{0}' and (ed.name like '%{1}%' or ed.exam_name like '%{1}%')""".format(filters.get("course"),txt))

@frappe.whitelist()
def get_student_by_student_group(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""Select stg.student,stg.student_name from `tabStudent Group Student` stg left join `tabStudent Group` sg on stg.parent=sg.name where sg.name='{0}' and (stg.student like '%{1}%' or stg.student_name like '%{1}%')""".format(filters.get("student_group"),txt))
	

@frappe.whitelist()
def get_courses_from_student_group_semester(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""Select cr.name,cr.course_name,cr.course_code from `tabStudent Group Instructor` stg left join `tabCourse` cr on stg.course=cr.name where (cr.name like '%{0}%' or cr.course_name like '%{0}%' or cr.course_code like '%{0}%') and stg.instructor='{1}'""".format(txt,filters.get("instructor")))
	# course_list=[]
	# for d in frappe.get_all("Student Group Instructor",{"parent":filters.get("student_group"),"instructor":filters.get("instructor"),'course': ['like', '%{}%'.format(txt)]},['course']):
	# 	if d.course:
	# 		course_list.extend(frappe.get_all("Course",{"name":d.course},['name','course_name','course_code'],as_list=1))
	# return course_list

@frappe.whitelist()
def get_course_schedule_events(start, end, filters=None):
	from frappe.desk.calendar import get_event_conditions
	conditions = get_event_conditions("Course Schedule", filters)
	custom_conditions=""
	join_table=""

	if "System Manager" not in frappe.get_roles():
		# for student user
		if "Student" in frappe.get_roles() and "Instructor" not in frappe.get_roles():
			student=frappe.db.get_value("Student",{"student_email_id":frappe.session.user},"name")
			if student:
				join_table="left join `tabStudent Group Student` on `tabCourse Schedule`.student_group=`tabStudent Group Student`.parent"
				custom_conditions=" and `tabStudent Group Student`.student='{0}'".format(student)

		# for instructor user
		if "Instructor" in frappe.get_roles():
			for emp in frappe.get_all("Employee",{"user_id":frappe.session.user_email},"name"):
				for inst in frappe.get_all("Instructor",{"employee":emp.name},"name"):
					join_table="left join `tabStudent Group Instructor` sgi on `tabCourse Schedule`.student_group=`tabStudent Group Instructor`.parent"
					custom_conditions=" and `tabStudent Group Instructor`.instructor='{0}'".format(inst.name)

	# data = frappe.db.sql("""select `tabCourse Schedule`.name, `tabCourse Schedule`.course, `tabCourse Schedule`.course_name,`tabCourse Schedule`.course_code, `tabCourse Schedule`.color,
	# 		timestamp(`tabCourse Schedule`.schedule_date, `tabCourse Schedule`.from_time) as from_datetime,
	# 		timestamp(`tabCourse Schedule`.schedule_date, `tabCourse Schedule`.to_time) as to_datetime,
	# 		`tabCourse Schedule`.room, `tabCourse Schedule`.student_group, 0 as 'allDay'
	# 	from `tabCourse Schedule` 
	# 	{join_table}
	# 	where ( `tabCourse Schedule`.schedule_date between %(start)s and %(end)s ) 
	# 	{conditions}
	# 	{custom_conditions}""".format(join_table=join_table,conditions=conditions,custom_conditions=custom_conditions), {
	# 		"start": start,
	# 		"end": end
	# 		}, as_dict=True, update={"allDay": 0})

	# result=[]
	# for d in data:
	# 	d.update({"course":d.course_code+":"+d.course_name+":"+d.course})
	# 	result.append(d)
	# return result



	data = frappe.db.sql("""select `tabCourse Schedule`.name, `tabCourse Schedule`.course, `tabCourse Schedule`.color,
			timestamp(`tabCourse Schedule`.schedule_date, `tabCourse Schedule`.from_time) as from_datetime,
			timestamp(`tabCourse Schedule`.schedule_date, `tabCourse Schedule`.to_time) as to_datetime,
			`tabCourse Schedule`.room, `tabCourse Schedule`.student_group, 0 as 'allDay'
		from `tabCourse Schedule` 
		{join_table}
		where ( `tabCourse Schedule`.schedule_date between %(start)s and %(end)s ) 
		{conditions}
		{custom_conditions}""".format(join_table=join_table,conditions=conditions,custom_conditions=custom_conditions), {
			"start": start,
			"end": end
			}, as_dict=True, update={"allDay": 0})

	return data
@frappe.whitelist()
def get_instructor(doctype, txt, searchfield, start, page_len, filters):
	student_group=frappe.get_doc("Student Group",filters.get("student_group"))
	if student_group.group_based_on=="Exam Declaration":
		return [(d.instructor,) for d in student_group.get("invigilator_list")]
	else:
		lst = []
		for i in frappe.get_all("Instructor Log",filters={"course":filters.get("course"),'parent': ['like', '%{}%'.format(txt)]},fields=['parent'],order_by="parent"):
			if i.parent not in lst:
				lst.append(i.parent)
		return [(d,) for d in lst]

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_instructor_by_student_group(doctype, txt, searchfield, start, page_len, filters):
	student_group=frappe.get_doc("Student Group",filters.get("student_group"))
	if student_group.group_based_on=="Exam Declaration":
		return [(d.instructor,) for d in student_group.get("invigilator_list")]
	else:
		return frappe.get_all("Student Group Instructor",{"parent":filters.get("student_group"),"instructor": ["like", "%{0}%".format(txt)]},['instructor'],as_list=1)