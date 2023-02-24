import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from wsc.wsc.utils import duplicate_row_validation


class FeeStructure(Document):
    def validate(self):
        self.calculate_total()
        self.calculate_amount()
        self.validate_duplicate_programs()
        validate_academic_year(self)
        validate_semester(self)
        duplicate_row_validation(self, "components", ['fees_category', 'amount'])

    def calculate_total(self):
        """Calculates total amount."""
        self.total_amount = 0
        for d in self.components:
            self.total_amount += d.amount
###################
    def calculate_amount(self):
        for events in self.get("components"):
            events.grand_fee_amount=events.amount
            events.outstanding_fees=events.amount

    def validate_duplicate_programs(self):
        duplicateForm=frappe.get_all("Fee Structure", filters={
            "programs":self.programs,
            "program": self.program,
            "fee_type":self.fee_type,
            "student_category": self.student_category,
            "academic_year":self.academic_year,
            "academic_term": self.academic_term,
            # "name":("!=",self.name)
            "docstatus":1
            
        })
        if duplicateForm:
            frappe.throw(("Same Fee Structure is already exist."))        

def validate_semester(doc):
	if doc.program not in [d.semesters for d in frappe.get_all("Semesters", {'parent':doc.get('programs')},['semesters'])]:
		frappe.throw("Semester <b>'{0}'</b> not belongs to program <b>'{1}'</b>".format(doc.get('program'), doc.get('programs')))

def validate_academic_year(doc):
	if doc.academic_term:
		if doc.academic_term not in [d.name for d in frappe.get_all("Academic Term", {'academic_year':doc.get('academic_year')},['name'])]:
			frappe.throw("Academic Term <b>'{0}'</b> not belongs to academic year <b>'{1}'</b>".format(doc.get('academic_term'), doc.get('academic_year')))


@frappe.whitelist()
def get_courses(program):
    return frappe.db.sql('''select course from `tabProgram Course` where parent = %s and required = 1''', (program), as_dict=1)

@frappe.whitelist()
def get_fee_types():
    types=[]
    for d in frappe.get_all("Fee Type",order_by="name"):
        types.append(d.name)
    return "\n".join([''] + types)

@frappe.whitelist()
def make_fee_schedule(source_name, target_doc=None):
    return get_mapped_doc("Fee Structure", source_name,	{
        "Fee Structure": {
            "doctype": "Fee Schedule",
            "validation": {
                "docstatus": ["=", 1],
            }
        },
        "Fee Component": {
            "doctype": "Fee Component"
        }
    }, target_doc)