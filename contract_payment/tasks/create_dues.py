import frappe
from frappe import _
from frappe.utils import today



def create_dues():
    """
    this function create dues for all contract if setting check automtic
    """
	
    is_creat_dues_auto = frappe.db.get_single_value("Contract Payment Settings", "auto_create_dues") 

    if not is_creat_dues_auto:
        return 
    contract_dues = frappe.get_list(
        "Contract Dues", filters={"date_dues": today()}, fields=["*"]
    )
    for d in contract_dues:
        parent_doc = frappe.get_doc('Contract', d['parent'])
        if parent_doc.docstatus != 1:
            return
        if parent_doc.party_type == 'Supplier':
            parent_doc.create_purchase_invoice()
        if parent_doc.party_type == 'Customer':
            parent_doc.create_sales_invoice()


