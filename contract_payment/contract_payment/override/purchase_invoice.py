import frappe
from frappe import _
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice



def validate_purchase_invoice(doc, method):
    """
    this validation for stop create purchase invoice for supplier is check as contract payment

    if settings stop create purchase invoice for supplier 
    """
    stop_create_p_invoice = frappe.db.get_single_value("Contract Payment Settings", "stop_create_p_invoice")
    if not stop_create_p_invoice:
        return 
    supplier = frappe.get_doc("Supplier", doc.supplier)
    if not supplier.is_contract_payment:
        return 
    if not doc.is_contract_payment_invoice:
        frappe.throw(_("Need to check is contract payment invoice and select contract for this supplier"))
    
        
