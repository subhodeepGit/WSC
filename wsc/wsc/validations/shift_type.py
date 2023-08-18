
import frappe

def validate(doc,method):
    if doc.start_time>doc.end_time:
        frappe.throw("Shift Start Time cannot be greater than Shift End Time")
    if doc.begin_check_in_before_shift_start_time:
        if doc.begin_check_in_before_shift_start_time<0 :
            frappe.throw("Threshold time cannot be Negative")
    if doc.working_hours_threshold_for_half_day:
        if doc.working_hours_threshold_for_half_day<0:
            frappe.throw("Threshold time cannot be Negative")
    if doc.working_hours_threshold_for_absent:
        if doc.working_hours_threshold_for_absent<0:
            frappe.throw("Threshold time cannot be Negative")
    if doc.allow_check_out_after_shift_end_time:
        if doc.allow_check_out_after_shift_end_time<0:
            frappe.throw("Threshold time cannot be Negative")
    if doc.late_entry_grace_period:
        if doc.late_entry_grace_period<0:
            frappe.throw('Grace Period cannot be Negative')
    if doc.early_exit_grace_period:
        if doc.early_exit_grace_period<0:
            frappe.throw("Grace Period cannot be Negative")
    