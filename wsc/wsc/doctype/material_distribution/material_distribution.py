# Copyright (c) 2023, SOUL Limited and Contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MaterialDistribution(Document):
    # @frappe.whitelist()
    def on_submit(doc):
        for row in doc.materials_allotment:
            if row.mandatory_materials and not row.material_applicability_check:
                frappe.throw("Please check Material Applicability for Mandatory materials")

    def validate(doc):
        allotment_number=doc.allotment_number
        info=frappe.db.sql("""SELECT `name`,`allotment_number`,`docstatus` FROM `tabMaterial Distribution` WHERE `allotment_number`="%s" and `docstatus`!=2"""%\
                            (allotment_number))				
        if len(info)==0:
            pass
        elif len(info)==1 and info[0][2]==0:
            pass
        else:
            frappe.throw("Material already provided to the Student")

@frappe.whitelist()
def fetch_material(server_date):
    distribution_master = frappe.get_all(
        "Material Distribution Master",
        filters={
            "start_date": ["<=", server_date],
            "end_date": [">=", server_date]
        },
        fields=["name"]
    )
    if distribution_master:
        material_distribution_components = frappe.get_all(
            "Material Distribution Components",
            filters={
                "parent": distribution_master[0].name
            },
            fields=["materials", "mandatory_materials"],
            as_list=True,
        )
        if material_distribution_components:
                materials_records = []
                for component in material_distribution_components:
                    material = component[0]
                    mandatory_material = component[1]
                    materials_records.append({
                        "material": material,
                        "mandatory_material": mandatory_material
                    })
                return materials_records
        else:
            frappe.msgprint("No Material Distribution Component record found for the today date.")
    else:
        frappe.msgprint("No Material Distribution Master record found for the today date.")
    return []
                        
