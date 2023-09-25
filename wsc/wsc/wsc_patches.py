import frappe

BENCH_PATH = frappe.utils.get_bench_path()

def execute():
    disable_cancel_link()
    add_line_for_po()
    comment_lines_job_applicant()
    comment_lines_list_view()
    add_line_JobApplicant_js()
    grid_rowjs_overrides()

def disable_cancel_link():
    file_path = "{}/{}".format(BENCH_PATH,
                               "apps/frappe/frappe/model/delete_doc.py")
    
    with open(file_path, "r") as file:
        content = file.read()
    
    updated_content = content.replace('Submitted Record cannot be deleted. You must {2} Cancel {3} it first.', 'Submitted Record cannot be deleted. You must Cancel it first.')

    with open(file_path) as f:
        if 'Submitted Record cannot be deleted. You must Cancel it first.' in f.read():
            return
        
    with open(file_path, "w") as file:
        file.write(updated_content)
        print("frappe/frappe/model/delete_doc.py modified Cancel link")


def add_line_for_po():
    file_path = "{}/{}".format(BENCH_PATH,"apps/erpnext/erpnext/public/js/controllers/taxes_and_totals.js")
    with open(file_path, "r") as file:
        content = file.readlines()
    target_line1 = 'flt(me.frm.doc.discount_amount) - tax.total, precision("rounding_adjustment"));'
    new_line1 = """\t\t\t\titem.gst=current_tax_amount;\n"""
    with open(file_path) as f:
        if """item.gst=current_tax_amount;""" in f.read():
            return
    index = -1
    for i, line in enumerate(content):
        if target_line1 in line:
            index = i
            break
    if index != -1:
        content.insert(index + 3, new_line1)
    with open(file_path, "w") as file:
        file.writelines(content)
        print("lines added for taxes and total")

def comment_lines_job_applicant():
    file_path = "{}/{}".format(BENCH_PATH,
                               "apps/hrms/hrms/hr/doctype/job_applicant/job_applicant.py")
    
    lines_to_comment = [
        "def autoname(self):",
        "self.name = self.email_id",
        'if frappe.db.exists("Job Applicant", self.name):',
        'self.name = append_number_if_name_exists("Job Applicant", self.name)'
    ]

    modified_lines = []

    with open(file_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        if line.strip() in lines_to_comment:
            modified_line = "#" + line
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)

    if modified_lines != lines:
        with open(file_path, "w") as file:
            file.writelines(modified_lines)
        print("Commented lines in hrms/hrms/hr/doctype/job_applicant/job_applicant.py")


def comment_lines_list_view():
    file_path = "{}/{}".format(BENCH_PATH,
                               "apps/frappe/frappe/public/js/frappe/list/list_view.js")
    lines_to_comment = [
        "actions_menu_items.push(bulk_assignment());",
        "actions_menu_items.push(bulk_assignment_rule());",
        "actions_menu_items.push(bulk_add_tags());"
    ]

    modified_lines = []

    with open(file_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        if line.strip() in lines_to_comment:
            modified_line = "//" + line
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)

    if modified_lines != lines:
        with open(file_path, "w") as file:
            file.writelines(modified_lines)
        print("Commented lines in apps/frappe/frappe/public/js/frappe/list/list_view.js")


def add_line_JobApplicant_js():
    input_file_path = "{}/{}".format(BENCH_PATH,
                                "apps/hrms/hrms/hr/doctype/job_applicant/job_applicant.js")

    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    target_line = '\t\t\t\t\t\t__("Interview Summary")\n'
    line_to_add = '\t\t\t\t$("div").remove(".form-dashboard-section.custom");\n'

    line_added = False

    for i, line in enumerate(lines):
        if target_line in line:           
            if line_to_add not in lines:
                insert_index = i + 3
                lines.insert(insert_index, line_to_add)
                line_added = True
            break 

    if line_added:
        with open(input_file_path, 'w') as file:
            file.writelines(lines)
        print("Line added in hrms/hrms/hr/doctype/job_applicant/job_applicant.js")


def grid_rowjs_overrides():
    file_path = "{}/{}".format(BENCH_PATH,
                               "apps/frappe/frappe/public/js/frappe/form/grid_row.js")
    
    with open(file_path, "r") as file:
        content = file.read()

    updated_content = content.replace('<div class="hidden-xs edit-grid-row">${__("Edit")}</div>', '<div class="hidden-xs edit-grid-row">${__("View")}</div>')

    with open(file_path) as f:
        if '<div class="hidden-xs edit-grid-row">${__("View")}</div>' in f.read():
            return

    with open(file_path, "w") as file:
        file.write(updated_content)
    print('frappe/frappe/public/js/frappe/form/grid_row.js modified Edit to View')






