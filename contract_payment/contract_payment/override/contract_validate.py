
import frappe
from frappe import _


def validate_amount(doc, method):
    if not doc.contract_payment or doc.is_new():
        return
    amount = 0
    for i in doc.contract_dues:
        amount = amount + i.amount
    if int(amount) != int(doc.amount):
        frappe.throw(_("Contract Dues total {0} must be equl total amount {1}".format(doc.amount, amount)))



