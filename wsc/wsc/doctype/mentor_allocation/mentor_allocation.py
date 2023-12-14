# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe import msgprint, _
from wsc.wsc.utils import duplicate_row_validation
from wsc.wsc.notification.custom_notification import mentor_allocation_submit

class MentorAllocation(Document):
    def validate(self):
        validate_allocation_from_to(self)
        duplicate_row_validation(self, "mentee_list", ['student', "student_name"])

    def on_submit(self):
        existed_stud_grp = frappe.db.get_list("Student Group", {'mentor_allocation':self.name},'name')
        if len([d.name for d in existed_stud_grp]) == 0:
            create_student_group(self)
        else:
            update_student_group(self, existed_stud_grp)
        mentor_allocation_submit(self)
        
    def on_cancel(self):
        existed_stud_grp = frappe.db.get_list("Student Group", {'mentor_allocation':self.name,'disabled':0},'name')
        for s in existed_stud_grp:
            sg_doc = frappe.get_doc('Student Group', s.get('name'))
            sg_doc.disabled = 1
            sg_doc.save()
            msgprint(_("Student Group <b>'{0}'</b> disabled.".format(s.get('name'))))

@frappe.whitelist()
def get_students(doctype, txt, searchfield, start, page_len, filters):
    list_student=filters[0]
    fil=""
    if list_student[3]:
        if len(list_student[3])==1:
            fil="  st.name <> '%s' and "%(list_student[3][0])
        else:
            fil=" st.name Not IN  %s and "%(str(tuple(list_student[3])))      
    # return frappe.db.sql("""
    #                             Select 
    #                                     distinct(st.name) as student, st.student_name as student_name ,st.roll_no as roll_no
    #                             from `tabCurrent Educational Details` ced 
    #                             left join `tabStudent` st on st.name=ced.parent 
    #                             where enabled=1 and (st.name LIKE %(txt)s or st.student_name LIKE %(txt)s) and ced.programs='{0}'""".format(filters.get("programs")),dict(txt="%{}%".format(txt))) 
    return frappe.db.sql("""
                            Select 
                                    distinct(st.name) as student, st.student_name as student_name ,st.roll_no as roll_no
                            from `tabCurrent Educational Details` ced 
                            left join `tabStudent` st on st.name=ced.parent 
                            where enabled=1 and {1} (st.name LIKE %(txt)s or st.student_name LIKE %(txt)s) and ced.programs='{0}'""".format(filters[1][3],fil),dict(txt="%{}%".format(txt))) 

def validate_allocation_from_to(doc):
    if doc.allocation_from and doc.allocation_to and doc.allocation_from > doc.allocation_to:
        frappe.throw("Allocation to <b>'{0}'</b> Should be Greater than Allocation from  <b>'{1}'</b> ".format( doc.allocation_to, doc.allocation_from))

def create_student_group(self):
    count = 1 
    mentor_cnt = [m.get('inst_cnt') for m in frappe.db.sql("""SELECT count(mentor_name) as inst_cnt
    from `tabStudent Group` where mentor_name='{0}'""".format(self.mentor), as_dict=1)]
    sg_doc = frappe.new_doc('Student Group')
    sg_doc.academic_year=self.academic_year
    sg_doc.group_based_on = "Mentor-Mentee"
    sg_doc.mentor_allocation = self.name
    if len(mentor_cnt) > 0 :
        count = mentor_cnt[0] + 1
    sg_doc.student_group_name = self.mentor_name + " Mentor-Mentee Group " + str(count)
    sg_doc.mentor_name=self.mentor
    for stud in self.mentee_list:
        s_row = sg_doc.append('students', {})
        s_row.student = stud.student
        s_row.student_name = stud.student_name

    sg_doc.save()
    sg_doc.reload()
    msgprint(_("Student Group created successfully."))
 
def update_student_group(self, existed_stud_grp):
    for s in existed_stud_grp:
        sg_doc = frappe.get_doc('Student Group', s.get('name'))
        sg_doc.disabled = 0
        sg_doc.mentor_allocation = self.name
        for stud in self.mentee_list:
            s_row = sg_doc.append('students', {})
            s_row.student = stud.student
            s_row.student_name = stud.student_name
        sg_doc.save()
        msgprint(_("Student Group <b>'{0}'</b> updated successfully.".format(s.get('name'))))

@frappe.whitelist()
def create_course_schedulling_tool(source_name, target_doc=None):
    doclist = get_mapped_doc("Mentor Allocation", source_name,  {
        "Mentor Allocation": {
            "doctype": "Course Scheduling Tool",
            "field_map": {
                "mentor":"instructor",
                "mentor_name":"instructor_name"
            },
        },
    }, target_doc)

    return doclist

