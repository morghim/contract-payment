
import frappe
from frappe import _
from .contract import update_contract_dues

def on_update(doc, method):
    """
    this method for update Contract Dues to is paid
    """
    if not doc.party_type in ('Supplier', 'Customer'):
        return 
    if not frappe.get_value(doc.party_type, doc.party_name, 'is_contract_payment'):
        return 
    if doc.docstatus == 1:
        for d in doc.get("references"):
            doct = frappe.get_doc(d.reference_doctype, d.reference_name)
            update_contract_dues(d.reference_doctype, doct)

        




