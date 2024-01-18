import frappe
from frappe.desk.reportview import get_match_cond
from frappe import _


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_program_courses(doctype, txt, searchfield, start, page_len, filters):
	if not filters.get("program"):
		frappe.msgprint(_("Please select a Program first."))
		return []

	return frappe.db.sql(
		"""select course, course_name from `tabProgram Course`
		where  parent = %(program)s 
		order by
			if(locate(%(_txt)s, course), locate(%(_txt)s, course), 99999),
			idx desc,
			`tabProgram Course`.course asc
		limit {start}, {page_len}""".format(
			match_cond=get_match_cond(doctype), start=start, page_len=page_len
		),
		{
			"txt": "%{0}%".format(txt),
			"_txt": txt.replace("%", ""),
			"program": filters["program"],
		},
	)