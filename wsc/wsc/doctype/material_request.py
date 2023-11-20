import frappe
from frappe import _
import json
from frappe.model.document import Document
from wsc.wsc.notification.custom_notification import purchase_requisition_raised, received_in_inventory, received_by_department, workflow_wating_approval

@frappe.whitelist()
def workflow_notification(self,method):
    # Workflow Notification code start
    user_id = frappe.db.get_list("Employee",{"department":self.department},["user_id"])
    user_ids = [entry['user_id'] for entry in user_id]
    
    # if (self.material_request_type == "Material Transfer" or self.material_request_type == "Material Issue") and self.workflow_state == "Submit":
    #     receipient_name = frappe.db.get_all('User',{'name':('in', user_ids),'role_profile_name':'Requisitioner'},['name'])   
    #     workflow_wating_approval(self,receipient_name)

    if (self. material_request_type == "Material Transfer" or self. material_request_type == "Material Issue" )and self.workflow_state == "Submit":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Dy. Director'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif (self. material_request_type == "Material Transfer" or self. material_request_type == "Material Issue") and self.workflow_state == "Approved by Dy, Director":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Director'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif (self. material_request_type == "Material Transfer" or self. material_request_type == "Material Issue") and self.workflow_state == "Approved by Director":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Purchase Manager-MM'},['name']) 
        workflow_wating_approval(self, receipient_name)

    elif (self. material_request_type == "Material Transfer" or self. material_request_type == "Material Issue" )and self.workflow_state == "Approved by Purchase Manager":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'GM-Procurement & Contract Management'},['name'])  
        workflow_wating_approval(self, receipient_name)

    elif (self. material_request_type == "Material Transfer" or self. material_request_type == "Material Issue") and self.workflow_state == "Approved by GM-Procurement & Contract Management":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Stock Manager- MM'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif self.material_request_type == "Purchase" and frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Board of Directors' },['authority']) == 'Board of Directors' and frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Board of Directors' },['full_power']) == 1 and self.workflow_state == "Submit": 
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Board of Directors'},['name'])
        workflow_wating_approval(self, receipient_name)

    elif self.material_request_type == "Purchase" and frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Director' },['authority']) == 'Director' and frappe.db.get_value('Authorization Hierarchy',{'parent':frappe.db.get_value('Material Request Item', {'parent': self.name},['item_group']), 'authority':'Director' },['full_power']) == 1 and self.workflow_state == "Submit":
        receipient_name = frappe.db.get_list('User',{'name':('in', user_ids),'role_profile_name':'Director'},['name'])
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

def validate(self,method):
    
    if self.workflow_state == "Approved by Director":
        purchase_requisition_raised(self)
    
    if self.status == "Received":
        received_in_inventory(self)

    if self.status == "Issued" or self.status == "Transferred":
        received_by_department(self)

@frappe.whitelist()
def get_next_state(doc):
        doc = json.loads(doc)
        authorisation_workflow = {}

        full_power_authority=frappe.get_all("Authorization Hierarchy", {"parent" : frappe.db.get_value('Material Request Item', {'parent': doc["name"]},['item_group']), "full_power" : 1}, ["authority", "full_power", "from_amount", "to_amount"])

        authority_amount_range = frappe.get_all("Authorization Hierarchy", {"parent" : frappe.db.get_value('Material Request Item', {'parent': doc["name"]},['item_group']), "from_amount" : ("<=", doc["grand_total"]), "to_amount" : (">=", doc["grand_total"])}, ["authority", "full_power", "from_amount", "to_amount"])

        if authority_amount_range:
            authority_greater_amount_range = frappe.get_all("Authorization Hierarchy", {"parent" : frappe.db.get_value('Material Request Item', {'parent': doc["name"]},['item_group']), "from_amount" : (">=", authority_amount_range[0]["to_amount"])}, ["authority", "full_power", "from_amount", "to_amount"])
            if authority_greater_amount_range:
                authorisation_workflow=authority_amount_range
            else:
                authorisation_workflow=authority_amount_range+full_power_authority
        else:
            authorisation_workflow=full_power_authority
        
        next_state_workflow = frappe.get_all("Workflow Transition", {"parent" : "Purchase Requisition Workflow","state":doc["workflow_state"]}, ["state", "next_state", "allowed"])
        
        all_allowed = set()
        if next_state_workflow:
            for i in range(len(next_state_workflow)):
                all_allowed.add(next_state_workflow[i]["allowed"])
            all_allowed = list(all_allowed)
        if all_allowed:
            count = 0
            for entry in authorisation_workflow:
                if entry['authority'] in all_allowed:
                    count += 1
                if count >= 1:
                    return False
            if count == 0:
                return True
            return True
        else:
            return True