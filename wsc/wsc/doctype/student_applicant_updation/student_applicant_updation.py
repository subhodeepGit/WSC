# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class StudentApplicantUpdation(Document):
	
	def validate(doc):
		validate_pin_code(doc)
		mobile_number_validation(doc)
		email_validation(doc)
		  
	@frappe.whitelist()
	def update_student_applicant(self):
		
		frappe.db.sql("""
			UPDATE `tabStudent Applicant` 
			SET 
				first_name = "{first_name}" , middle_name  = "{middle_name}" , last_name = "{last_name}" ,
				student_category  = "{student_category}" ,
				academic_year = "{academic_year}" , academic_term = "{academic_term}" ,
				department = "{department}" , program_grade = "{program_grade}" ,
				room_type = "{room_type}" , sharing = "{sharing}" ,
				date_of_birth = "{date_of_birth}" , gender = "{gender}" , religion = "{religion}" ,
				blood_group = "{blood_group}" , nationality = "{nationality}" ,
				student_email_id = "{student_email_id}" , student_mobile_number = "{student_mobile_number}" ,
				physically_disabled = "{physically_disabled}" , award_winner = "{award_winner}" ,
				states =  "{states}" , districts = "{districts}" , blocks = "{blocks}" , post_office = "{post_office}" ,
				address_line_i = "{address_line_i}" , address_line_ii = "{address_line_ii}" , pin_code = "{pin_code}" ,
				fathers_name = "{fathers_name}", fathers_contact_number = "{fathers_contact_number}" ,qualification = "{qualification}" ,
				fathers_occupation = "{fathers_occupation}" , father_annual_income = "{father_annual_income}" ,
				mothers_name = "{mothers_name}" , mothers_contact_number = "{mothers_contact_number}" , mothers_qualification = "{mothers_qualification}" ,
				mothers_occupation  = "{mothers_occupation}" , mother_annual_income = "{mother_annual_income}" ,
				local_guardians_name = "{local_guardians_name}" , local_guardian_contact_no = "{local_guardian_contact_no}" , relation_with_student = "{relation_with_student}" ,
				local_guardian_occupation = "{local_guardian_occupation}" , local_guardian_address = "{local_guardian_address}"
			WHERE name = "{applicant_id}"
		""".format(applicant_id = self.student_applicant,
					first_name = self.first_name , middle_name  = self.middle_name, last_name = self.last_name ,
					student_category  = self.student_category,
					academic_year = self.academic_year , academic_term = self.academic_term ,
					department = self.department , program_grade = self.course_type ,
					room_type = self.room_type , sharing = self.sharing ,
					date_of_birth = self.date_of_birth , gender = self.gender , religion = self.religion ,
					blood_group = self.blood_group , nationality = self.nationality ,
					student_email_id = self.student_email_address , student_mobile_number = self.student_mobile_number ,
					physically_disabled = self.physically_disabled , award_winner = self.award_winner ,
					states =  self.state , districts = self.district , blocks = self.block, post_office = self.post_office ,
					address_line_i = self.address_line_1 , address_line_ii = self.address_line_2 , pin_code = self.pincode ,
					fathers_name = self.fathers_name, fathers_contact_number = self.fathers_contact_number , qualification = self.fathers_qualification ,
					fathers_occupation = self.fathers_occupation , father_annual_income = self.fathers_annual_income ,
					mothers_name = self.mothers_name , mothers_contact_number = self.mothers_contact_number , mothers_qualification = self.mothers_qualification ,
					mothers_occupation  = self.mothers_occupation , mother_annual_income = self.mothers_annual_income ,
					local_guardians_name = self.local_guardians_name , local_guardian_contact_no = self.local_guardian_contact_no , relation_with_student = self.relation_with_student , 
					local_guardian_occupation = self.local_guardian_occupation , local_guardian_address = self.local_guardian_address
			))

		## For Course Preference
		for i in self.course_preferences:
			frappe.db.sql("""
				UPDATE `tabProgram Priority`
				SET
				 	programs = "{program}"
				WHERE parent = "{applicant_id}"
			""".format(program = i.programs , applicant_id = self.student_applicant))

		## Education Qualifications
		for j in self.education_qualifications_details:
			frappe.db.sql("""
				UPDATE `tabEducation Qualifications Details`
				SET 
					qualification = "{qualification}",
					institute = "{institute}",
					board = "{board}",
					percentage_cgpa = "{percentage_cgpa}",
					total_marks = "{total_marks}",
					earned_marks = "{earned_marks}" ,
					year_of_completion = "{year_of_completion}" ,
					mandatory = "{mandatory}" ,
					admission_percentage = "{admission_percentage}"
				WHERE parent = "{applicant_id}"
			""".format(applicant_id = self.student_applicant , 
			  			qualification = j.qualification ,
						board = j.board , 
						percentage_cgpa = j.percentage_cgpa ,
						total_marks = j.total_marks , 
						earned_marks = j.earned_marks ,
						year_of_completion = j.year_of_completion ,
						mandatory = j.mandatory ,
						admission_percentage = j.admission_percentage
					))
		
		if self.physically_disabled == 1:
			for k in self.disable_type:
				frappe.db.sql("""
					UPDATE `tabPhysically Disabled`
				  	SET
				  		disability_type = "{disability_type}" ,
				  		percentage_of_disability = "{percentage_of_disability}" ,
				  		attach_disability_certificate = "{attach_disability_certificate}"
				  	WHERE parent = "{applicant_id}"
				""".format(applicant_id = self.student_applicant , 
							disability_type = k.disability_type , 
							percentage_of_disability = k.percentage_of_disability ,
							attach_disability_certificate = k.attach_disability_certificate
						))
		
		if self.physically_disabled == 1:
			for l in self.awards_winner_list:
				frappe.db.sql("""
					UPDATE `tabAwards List`
				  	SET
				  		awards = "{awards}" ,
				  		won_in_year = "{won_in_year}" ,
				  	WHERE parent = "{applicant_id}"
				""".format(applicant_id = self.student_applicant , 
							disability_type = l.awards , 
							percentage_of_disability = l.won_in_year ,
						))

def validate_pin_code(doc):
    # try:
		if doc.pin_code:

			if len(doc.pin_code)<6:
				frappe.throw("Field <b>Pincode</b> must be 6 Digits")
			if len(doc.pin_code)>6:
				frappe.throw("Field <b>Pincode</b> must be 6 Digits")

def mobile_number_validation(doc):

		if doc.student_mobile_number:
			if not (doc.student_mobile_number).isdigit():
				frappe.throw("Field <b>Mobile Number</b> Accept Digits Only")
			if len(doc.student_mobile_number)>10:
				frappe.throw("Field <b>Mobile Number</b> must be 10 Digits")
			if len(doc.student_mobile_number)<10:
				frappe.throw("Field <b>Mobile Number</b> must be 10 Digits")
			
		if doc.local_guardian_contact_no:
		
			if not (doc.local_guardian_contact_no).isdigit():
				frappe.throw("Field <b>Local Guardian Contact Number</b> Accept Digits Only")
			if len(doc.local_guardian_contact_no)<10:
				frappe.throw("Field <b>Local Guardian Contact Number</b> must be 10 Digits")
			if len(doc.local_guardian_contact_no)>10:
				frappe.throw("Field <b>Local Guardian Contact Number</b> must be 10 Digits")


		if doc.fathers_contact_number:
			
			if not (doc.fathers_contact_number).isdigit():
				frappe.throw("Field <b>Father's Contact Number</b> Accept Digits Only")
			if len(doc.fathers_contact_number)<10:
				frappe.throw("Field <b>Father's Contact Number</b> must be 10 Digits")
			if len(doc.fathers_contact_number)>10:
				frappe.throw("Field <b>Father's Contact Number</b> must be 10 Digits")

		if doc.mothers_contact_number:
			
			if not (doc.mothers_contact_number).isdigit():
				frappe.throw("Field <b>Mother's Contact Number</b> Accept Digits Only")
			if len(doc.mothers_contact_number)<10:
				frappe.throw("Field <b>Mother's Contact Number</b> must be 10 Digits")
			if len(doc.mothers_contact_number)>10:
				frappe.throw("Field <b>Mother's Contact Number</b> must be 10 Digits")
	
def email_validation(doc):
		for stu_app in frappe.get_all("Student Applicant",{"student_email_id":doc.student_email_id,"docstatus":("!=",2),"name":("!=",doc.name)}):
			frappe.throw("<b>Email ID</b> already Exist <b><a href='/app/student-applicant/{0}' target='_blank'>{0}</a></b>".format(stu_app.name))			
		

# caste_category ,
@frappe.whitelist()
def applicant_data(applicant_id):
	
	data = []
	applicant_data = frappe.db.sql("""
		SELECT 
			first_name , middle_name , last_name ,
			student_category ,
			academic_year , academic_term ,
			department , program_grade ,
			room_type , sharing ,
			date_of_birth , gender , religion ,
			blood_group , nationality ,
			student_email_id AS student_email_address, student_mobile_number ,
			physically_disabled , award_winner ,
			states AS state , districts AS district, blocks AS block, post_office , address_line_i AS address_line_1 , address_line_ii AS address_line_2 , pin_code AS pincode,
			fathers_name , fathers_contact_number , qualification AS fathers_qualification, fathers_occupation , father_annual_income ,
			mothers_name , mothers_contact_number , mothers_qualification , mothers_occupation , mother_annual_income ,
			local_guardians_name , local_guardian_contact_no , relation_with_student , local_guardian_occupation , local_guardian_address 
		FROM `tabStudent Applicant` 
		WHERE name = "{applicant_id}"
	""".format(applicant_id = applicant_id), as_dict=1)

	education_qualification = frappe.db.sql("""
		SELECT 
			qualification ,
			institute ,
			board ,
			percentage_cgpa ,
			total_marks ,
			earned_marks ,
			year_of_completion ,
			mandatory ,
			admission_percentage 
		FROM `tabEducation Qualifications Details` 
		WHERE parent = '{applicant_id}'
	""".format(applicant_id = applicant_id) , as_dict=1)

	course_preference = frappe.db.sql("""
		SELECT 
			programs 
		FROM `tabProgram Priority` 
		WHERE parent = '{applicant_id}'
	""".format(applicant_id = applicant_id) , as_dict=1)

	physical_disability = []
	if applicant_data[0]['physically_disabled'] == 1:
		physical_disability = frappe.db.sql("""
			SELECT 
				disability_type ,
				percentage_of_disability ,
				attach_disability_certificate
			FROM `tabPhysically Disabled` 
			WHERE parent = '{applicant_id}'
		""".format(applicant_id = applicant_id) , as_dict=1)

	award_winner_list = []
	if applicant_data[0]['award_winner'] == 1:
		award_winner_list = frappe.db.sql("""
			SELECT
				parent ,
				awards ,
				won_in_year 
			FROM `tabAwards List` 
			WHERE parent = '{applicant_id}'
		""".format(applicant_id = applicant_id) , as_dict=1)
	
	print(course_preference)
	data.append(applicant_data)  #0
	data.append(education_qualification) #1
	data.append(course_preference) #2
	data.append(physical_disability) #3
	data.append(award_winner_list) #4

	
	return data