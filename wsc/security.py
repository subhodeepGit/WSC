import frappe

BENCH_PATH = frappe.utils.get_bench_path()

def execute():
    add_line_for_po()

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