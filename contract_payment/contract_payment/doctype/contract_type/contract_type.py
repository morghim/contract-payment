# Copyright (c) 2021, Ibrahim Morghim and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
class ContractType(Document):

	@frappe.whitelist()
	def create_item(self):
		"""
		this method for create item
		"""
		item = frappe.get_doc({
					'doctype': 'Item',
					'item_name': self.name1,
					'item_code': self.name1,
					'item_group': self.get_contract_item_group(),
					'is_purchase_item': True,
					'is_sales_item': True,
					'is_stock_item': False,
					'include_item_in_manufacturing': False
				})
		item.item_defaults = None
		item.insert()
		self.item = item.name
		frappe.msgprint(_('item created successfuly'))


	def get_contract_item_group(self):
		"""
		this method for get contract item group
		"""
		item_group = frappe.get_list('Item Group', filters={'is_contract_group': True})
		if item_group:
			return item_group[0].name
		return None 