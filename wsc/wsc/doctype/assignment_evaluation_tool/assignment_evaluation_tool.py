# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe 
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class AssignmentEvaluationTool(Document):
    def on_submit(self):
        check_list = []
        participant_id_list=[]
        for d in self.get('participants_list'):
            if d.participant_id:
                if d.participant_id in check_list:
                    pass
                else:
                    check_list_dict = {}
                    check_list_dict['participant_id']=d.participant_id
                    participant_id_list.append(d.participant_id)
                    check_list_dict['participant_name']=d.participant_name
                    check_list_dict['job_sheet_number']=d.job_sheet_number
                    check_list_dict['job_sheet_name']=d.job_sheet_name
                    check_list_dict['assessment_criteria']=d.assessment_criteria
                    check_list_dict['weightage']=d.weightage
                    check_list_dict['total_marks']=d.total_marks
                    check_list_dict['pass_marks']=d.pass_marks
                    check_list_dict['start_date_and_time']=d.start_date_and_time
                    check_list_dict['end_date_and_time']=d.end_date_and_time
                    check_list_dict['total_duration']=d.total_duration
                    check_list_dict['marks_earned']=d.marks_earned
                    check_list.append(check_list_dict)
        participant_id_list=list(set(participant_id_list))
        for t in participant_id_list:
            doc = frappe.new_doc('Assignment Evaluation')
            doc.assignment_declaration = self.assignment_declaration
            doc.assignment_declaration_start_date = self.assignment_declaration_start_date
            doc.participant_group = self.participant_group
            doc.tot_start_date = self.tot_start_date
            doc.academic_year = self.academic_year
            doc.select_course = self.programs
            doc.module_name = self.module_name
            doc.assignment_declaration_end_date = self.assignment_declaration_end_date
            doc.participant_group_name = self.participant_group_name
            doc.tot_end_date = self.tot_end_date
            doc.academic_term = self.academic_term
            doc.select_module = self.course
            doc.module_code = self.module_code
            doc.instructor_id = self.evaluator_id
            doc.instructor_name = self.evaluator_name
            doc.assessment_component = self.assessment_component
            doc.weightage = self.weightage
            doc.total_marks = self.total_marks
            doc.passing_marks = self.passing_marks
            doc.participant_id=t
            marks_earned=0
            for j in check_list:
                if j['participant_id']==t:
                    marks_earned+=int(j['marks_earned'])
                    doc.append("job_sheet_fetch",{                                     
                            "job_sheet_number": j['job_sheet_number'],                             
                            "job_sheet_name": j['job_sheet_name'],                                   
                            "assessment_criteria": j['assessment_criteria'],                                       
                            "start_date_and_time": j['start_date_and_time'],                                     
                            "total_durationin_hours": j['total_duration'],                                   
                            "pass_marks": j['pass_marks'],                                   
                            "total_marks": j['total_marks'],                           
                            "weightage": j['weightage'],                            
                            "end_date_and_time": j['end_date_and_time'],
                            "marks": j['marks_earned'],                                    
                        })
            doc.marks_earned=marks_earned        
            doc.save()    



@frappe.whitelist()
def get_participants_and_assignments(assignment_declaration = None,participant_group=None,select_assessment_criteria=None):
    qualified_participants = frappe.get_all('Participant List Table', filters = [['parent', '=', assignment_declaration],['qualification_check', '=', 1]], fields = ['participant_id', 'participant_name'])
    credit_details = frappe.get_all('Assignment Declaration', filters = [['name', '=', assignment_declaration]], fields = ['weightage', 'total_marks','pass_marks','select_assessment_criteria'],group_by="select_assessment_criteria")

    assignments = []
    if participant_group != None:
        assignments = frappe.get_all("Assignment",filters=[["participant_group","=",participant_group],["assessment_criteria","=",select_assessment_criteria],["docstatus","=",1],["evaluate","=",1]],fields=['name','assignment_name','assessment_criteria','weightage','total_marks','passing_marks','start_date','end_date','total_duration'],group_by="name")

    participant_assignments = []
    
    if assignments:
        
        for participant in qualified_participants:
            for assignment in assignments:
                participants = {}
                participants['participant_id']=participant['participant_id']
                participants['participant_name']=participant['participant_name']
                participants['name']=assignment['name']
                participants['assignment_name']=assignment['assignment_name']
                participants['assessment_criteria']=assignment['assessment_criteria']
                participants['weightage']=assignment['weightage']
                participants['total_marks']=assignment['total_marks']
                participants['passing_marks']=assignment['passing_marks']
                participants['start_date']=assignment['start_date']
                participants['end_date']=assignment['end_date']
                participants['total_duration']=assignment['total_duration']
                participant_assignments.append(participants)

    else:

        for participant in qualified_participants:
                participants = {}
                participants['participant_id']=participant['participant_id']
                participants['participant_name']=participant['participant_name']
                participants['name']=None
                participants['assignment_name']=None
                participants['assessment_criteria']=credit_details[0]['select_assessment_criteria']
                participants['weightage']=credit_details[0]['weightage']
                participants['total_marks']=credit_details[0]['total_marks']
                participants['passing_marks']=credit_details[0]['pass_marks']
                participants['start_date']=None
                participants['end_date']=None
                participants['total_duration']=None
                participant_assignments.append(participants)
                

    return participant_assignments
    