import frappe
from frappe import _
from erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool import get_bank_transactions
from erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool import get_linked_payments


@frappe.whitelist()
def auto_reconcile_vouchers(
    bank_account=None,
    from_date=None,
    to_date=None,
    filter_by_reference_date=None,
    from_reference_date=None,
    to_reference_date=None,
):
    frappe.flags.auto_reconcile_vouchers = True
    document_types = ["payment_entry", "journal_entry"]
    bank_transactions = get_bank_transactions(bank_account)
    matched_transactions = []
    transaction_doc = None

    for transaction in bank_transactions:
        linked_payments = get_linked_payments(
            transaction.name,
            document_types,
            from_date,
            to_date,
            filter_by_reference_date,
            from_reference_date,
            to_reference_date,
        )
        vouchers = []
        for r in linked_payments:
            vouchers.append(
                {
                    "payment_doctype": r[1],
                    "payment_name": r[2],
                    "amount": r[4],
                }
            )

        transaction_doc = frappe.get_doc("Bank Transaction", transaction.name)
        account = frappe.db.get_value("Bank Account", transaction_doc.bank_account, "account")
        matched_transactions_count = 0

        for voucher in vouchers:
            gl_entry = frappe.db.get_value(
                "GL Entry",
                dict(
                    account=account, voucher_type=voucher["payment_doctype"], voucher_no=voucher["payment_name"]
                ),
                ["credit", "debit"],
                as_dict=1,
            )
            gl_amount, transaction_amount = (
                (gl_entry.credit, transaction_doc.deposit)
                if gl_entry.credit > 0
                else (gl_entry.debit, transaction_doc.withdrawal)
            )
            allocated_amount = gl_amount if gl_amount >= transaction_amount else transaction_amount
            transaction_doc.append(
                "payment_entries",
                {
                    "payment_document": voucher["payment_doctype"],
                    "payment_entry": voucher["payment_name"],
                    "allocated_amount": allocated_amount,
                },
            )
            matched_transactions.append(str(transaction_doc.name))
            matched_transactions_count += 1

        transaction_doc.save()
        transaction_doc.update_allocations()

    matched_transactions_count = len(set(matched_transactions))
    if matched_transactions_count == 0:
        frappe.msgprint(_("No matching references found for auto reconciliation"))
    elif matched_transactions_count == 1:
        frappe.msgprint(_("{0} transaction is reconciled").format(matched_transactions_count))
    else:
        frappe.msgprint(_("{0} transactions are reconciled").format(matched_transactions_count))

    frappe.flags.auto_reconcile_vouchers = False
    if transaction_doc:
        return frappe.get_doc("Bank Transaction", transaction_doc.name)
    else:
        return None