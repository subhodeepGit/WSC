import frappe
from frappe import _
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import purchase_requisition_raised, received_in_inventory, received_by_department, workflow_wating_approval

def validate(self,method):
    if self.workflow_state == "Approved by Director":
        purchase_requisition_raised(self)
    
    if self.status == "Received":
        received_in_inventory(self)

    if self.status == "Issued" or self.status == "Transferred":
        received_by_department(self)

    # Workflow Notification code start
    user_id = frappe.db.get_list("Employee",{"department":self.department},["user_id"])
    user_ids = [entry['user_id'] for entry in user_id]

    if self. material_request_type == "Material Transfer" or self. material_request_type == "Material Issue" and self.workflow_state == "Submit":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Course Manager'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif self. material_request_type == "Material Transfer" or self. material_request_type == "Material Issue" and self.workflow_state == "Approved by Course Manager":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Dy. Director'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif self. material_request_type == "Material Transfer" or self. material_request_type == "Material Issue" and self.workflow_state == "Approved by Dy, Director":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Director'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif self. material_request_type == "Material Transfer" or self. material_request_type == "Material Issue" and self.workflow_state == "Approved by Director":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Purchase Manager-MM'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif self. material_request_type == "Material Transfer" or self. material_request_type == "Material Issue" and self.workflow_state == "Approved by Purchase Manager":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'GM-Procurement & Contract Management'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif self.material_request_type == "Purchase" and frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Board of Directors' },['authority']) == 'Board of Directors' and frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Board of Directors' },['full_power']) == 1 and self.workflow_state == "Submit": 
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Board of Directors'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif self.material_request_type == "Purchase" and frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Director' },['authority']) == 'Director' and frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Director' },['full_power']) == 1 and self.workflow_state == "Submit":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Directors'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif self.material_request_type == "Purchase" and frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Dy. Principal' },['authority']) == 'Dy. Principal' and frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Dy. Principal' },['full_power']) == 1 and self.workflow_state == "Approved by Director":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Dy. Principal'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif self.material_request_type == "Purchase" and frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Principal' },['authority']) == 'Principal' and frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Principal' },['full_power']) == 1 and self.workflow_state == "Submit":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Principal'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif self.material_request_type == "Purchase" and frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'CEO' },['authority']) == 'CEO' and frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'CEO' },['full_power']) == 1 and self.workflow_state == "Approved by Principal":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'CEO'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif (self.material_request_type == "Purchase" and (frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Principal' },['authority']) == 'Principal')) and ((frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Principal' },['full_power']) == 1) or (self.grand_total <= frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Principal' },['to_amount']) and self.grand_total >= frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Principal' },['from_amount']))) and self.workflow_state == "Submit":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Principal'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif (self.material_request_type == "Purchase" and (frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'CEO' },['authority']) == 'CEO')) and ((frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'CEO' },['full_power']) == 1) or (self.grand_total <= frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'CEO' },['to_amount']) and self.grand_total >= frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'CEO' },['from_amount']))) and self.workflow_state == "Approved by Principal":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'CEO'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif (self.material_request_type == "Purchase" and (frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Board of Directors' },['authority']) == 'Board of Directors')) and ((frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Board of Directors' },['full_power']) == 1) or (self.grand_total <= frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Board of Directors' },['to_amount']) and self.grand_total >= frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Board of Directors' },['from_amount']))) and self.workflow_state == "Approved by CEO":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Board of Directors'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif (self.material_request_type == "Purchase" and (frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Director' },['authority']) == 'Director')) and ((frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Director' },['full_power']) == 1) or (self.grand_total <= frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Director' },['to_amount']) and self.grand_total >= frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Director' },['from_amount']))) and  self.workflow_state == "Submit":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Director'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif (self.material_request_type == "Purchase" and (frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Dy. Principal' },['authority']) == 'Dy. Principal')) and ((frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Dy. Principal' },['full_power']) == 1) or (self.grand_total <= frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Dy. Principal' },['to_amount']) and self.grand_total >= frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Dy. Principal' },['from_amount']))) and  self.workflow_state == "Approved by Director":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Dy. Principal'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif (self.material_request_type == "Purchase" and (frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Principal' },['authority']) == 'Principal')) and ((frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Principal' },['full_power']) == 1) or (self.grand_total <= frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Principal' },['to_amount']) and self.grand_total >= frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Principal' },['from_amount']))) and  self.workflow_state == "Approved by Dy. Principal":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Principal'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif (self.material_request_type == "Purchase" and (frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Dy. Principal' },['authority']) == 'Dy. Principal')) and ((frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Dy. Principal' },['full_power']) == 1) or (self.grand_total <= frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Dy. Principal' },['to_amount']) and self.grand_total >= frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Dy. Principal' },['from_amount']))) and  self.workflow_state == "Submit":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Dy. Principal'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif (self.material_request_type == "Purchase" and (frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'CEO' },['authority']) == 'CEO')) and ((frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'CEO' },['full_power']) == 1) or (self.grand_total <= frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'CEO' },['to_amount']) and self.grand_total >= frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'CEO' },['from_amount']))) and  self.workflow_state == "Submit":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'CEO'},['name'])
        workflow_wating_approval(self, receipient_name)
    # Workflow Notification code Ends