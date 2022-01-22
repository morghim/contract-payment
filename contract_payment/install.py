import frappe
from frappe.model.document import Document
from frappe import _


def after_install():
    """
    this function for add item group contracts
    """
    item_group = frappe.get_doc({
                        'doctype': 'Item Group',
                        'item_group_name': 'contracts',
                        'is_contract_group': True 
                    })

    item_group.insert()