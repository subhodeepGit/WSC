import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today


class AppointmentLetter(Document):
	def validate(self):
		if self.appointment_date:
			if (self.appointment_date) < today():
				frappe.throw("Appointment Date cannot be a past date.")