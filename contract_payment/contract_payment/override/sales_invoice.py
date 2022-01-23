import frappe
from frappe import _
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice



def validate_sales_invoice(doc, method):
    """
    this validation for stop create purchase invoice for supplier is check as contract payment

    if settings stop create purchase invoice for supplier 
    """
    stop_create_s_invoice = frappe.db.get_single_value("Contract Payment Settings", "stop_create_s_invoice")
    if not stop_create_s_invoice:
        return 
    customer = frappe.get_doc("Customer", doc.customer)
    if not customer.is_contract_payment:
        return 
    if not doc.is_contract_payment_invoice:
        frappe.throw(_("Need to check is contract payment invoice and select contract for this customer"))
    
        
