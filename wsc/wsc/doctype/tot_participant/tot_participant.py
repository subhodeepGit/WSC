# Copyright (c) 2023, SOUL Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ToTParticipant(Document):
    def validate(self):
            self.participant_name = " ".join(
			filter(None, [self.first_name, self.middle_name, self.last_name])
		)