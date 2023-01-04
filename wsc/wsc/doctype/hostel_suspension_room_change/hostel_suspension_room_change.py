# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class HostelSuspensionRoomChange(Document):
	# @frappe.whitelist()
	def before_insert(doc):
		allotment_number=doc.allotment_number
		indisciplinary_actions_id=doc.indisciplinary_actions_id
		info_Room_Change=frappe.db.sql("""SELECT * from `tabHostel Suspension Room Change` where `allotment_number`="%s" and 
											`indisciplinary_actions_id`="%s" and `docstatus`!=2"""%(allotment_number,indisciplinary_actions_id))
		if len(info_Room_Change)==0:	
			if doc.allotment_type=="Hostel suspension":	
				info_al_HSRCH=frappe.db.sql("""SELECT ICRS.name,IA.type_of_suspension 
											from `tabIndisciplinary Complaint Registration Student` ICRS
											JOIN `tabIndisciplinary Actions` IA on IA.name=ICRS.parent
											WHERE ICRS.allotment_number="%s" and ICRS.parent="%s" and IA.type_of_suspension="Hostel suspension" """%(
																						allotment_number,indisciplinary_actions_id))						
				if len(info_al_HSRCH)!=0:
					if doc.preferred_hostel!=doc.hostel:
						pass
					else:
						frappe.throw("Hostel Name should be different")
				else:
					frappe.throw("This allotment No don't belong to the Indisciplinary Actions Id")
			else:
				frappe.throw("Student is not Hostel suspension")
		else:
			frappe.throw("Already student Suspension record updated in Doc no '%s' "%(info_Room_Change[0][0]))




	# @frappe.whitelist()
	def on_submit(doc):
		allotment_number=doc.allotment_number
		indisciplinary_actions_id=doc.indisciplinary_actions_id
		info_Room_Change=frappe.db.sql("""SELECT * from `tabHostel Suspension Room Change` where `allotment_number`="%s" and 
											`indisciplinary_actions_id`="%s" and `docstatus`!=2"""%(allotment_number,indisciplinary_actions_id))
		if len(info_Room_Change)!=0:	
			if doc.allotment_type=="Hostel suspension":	
				info_al_HSRCH=frappe.db.sql("""SELECT ICRS.name,IA.type_of_suspension 
											from `tabIndisciplinary Complaint Registration Student` ICRS
											JOIN `tabIndisciplinary Actions` IA on IA.name=ICRS.parent
											WHERE ICRS.allotment_number="%s" and ICRS.parent="%s" and IA.type_of_suspension="Hostel suspension" """%(
																						allotment_number,indisciplinary_actions_id))																		
				if len(info_al_HSRCH)!=0:
					if doc.preferred_hostel!=doc.hostel:
						preferred_room=doc.preferred_room
						preferred_hostel=doc.preferred_hostel
						Room_no_info=frappe.db.sql("""Select `room_number` from `tabRoom Masters` WHERE `name`="%s" """%(preferred_room))
						Room_no_info=Room_no_info[0][0]
						frappe.db.sql("""UPDATE `tabRoom Allotment` SET `hostel_id`="%s",`room_id`="%s",
										`room_number`="%s" WHERE `name`="%s" """%(preferred_hostel,preferred_room,Room_no_info,allotment_number))
						room_id=preferred_room
						frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`-1 WHERE `name`="%s" """%(room_id))
						room_id=doc.room_no
						frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`+1 WHERE `name`="%s" """%(room_id))
						pass
					else:
						frappe.throw("Hostel Name should be different")

				else:
					frappe.throw("This Allotment No don't belong to the Indisciplinary Actions Id")
			else:
				frappe.throw("Student is not Hostel suspension")
		else:
			frappe.throw("Already student Suspension record updated in Doc no '%s' "%(info_Room_Change[0][0]))
	
	# @frappe.whitelist()
	def on_cancel(doc):
		allotment_number=doc.allotment_number
		#past record
		preferred_room=doc.preferred_room
		#present record
		room_number=doc.room_no
		hostel=doc.hostel
		Room_no_info=frappe.db.sql("""Select `room_number` from `tabRoom Masters` WHERE `name`="%s" """%(room_number))
		Room_no_info=Room_no_info[0][0]


		frappe.db.sql("""UPDATE `tabRoom Allotment` SET `hostel_id`="%s",`room_id`="%s",
						`room_number`="%s" WHERE `name`="%s" """%(hostel,room_number,Room_no_info,allotment_number))
		room_id=room_number
		frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`-1 WHERE `name`="%s" """%(room_id))
		room_id=preferred_room
		frappe.db.sql("""UPDATE `tabRoom Masters` SET `vacancy`=`vacancy`+1 WHERE `name`="%s" """%(room_id))
		pass			

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def ra_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""
		SELECT `allotment_number`,`student`,`student_name` 
			FROM `tabIndisciplinary Complaint Registration Student`
			GROUP BY `allotment_number` 
			HAVING COUNT(*) > 1
	"""
	)	

# SELECT *
# FROM `tabIndisciplinary Complaint Registration Student` as IDCR
# GROUP BY `allotment_number` 
# HAVING COUNT(*) > 1