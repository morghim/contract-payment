import frappe
from erpnext.crm.doctype.contract.contract import Contract
from frappe import _
import datetime
from dateutil import parser
import calendar

from erpnext.payroll.doctype.payroll_entry.payroll_entry import (
    create_salary_slips_for_employees,
)

from frappe.utils import (
    add_days,
    add_months,
    cint,
    date_diff,
    flt,
    get_datetime,
    get_last_day,
    getdate,
    month_diff,
    nowdate,
    today,
    get_link_to_form,
)
from numpy import pad


class CustomContract(Contract):
    """
    this class override for contract
    """

    @frappe.whitelist()
    def calculate_dues(self):
        """
        this function for make Contract Dues
        """
        self.contract_dues = None

        if not self.start_date or not self.end_date:
            frappe.msgprint(_("You need add start and end date"))
            return
        if self.dues_period_ == "Monthly":
            self.creat_dues_month()
        else:
            self.creat_dues_yearly()

    def creat_dues_month(self):
        """
        pass
        """
        start_date = parser.parse(self.start_date)
        end_date = parser.parse(self.end_date)
        num_months = (
            (end_date.year - start_date.year) * 12
            + (end_date.month - start_date.month)
            + 1
        )
        dues_date = add_days(
            start_date, calendar.monthrange(start_date.year, start_date.month)[1]
        )
        amount = self.amount / num_months
        if self.party_type == "Employee":
            end_dues_date = add_days(
                dues_date,
                calendar.monthrange(dues_date.year, dues_date.month)[1],
            )
            amount = self.get_employee_dues(dues_date, end_dues_date)
        for i in range(num_months):

            cont_benf = {
                "date_dues": dues_date.date(),
                "amount": amount,
            }
            self.append("contract_dues", cont_benf)
            dues_date = add_days(
                dues_date, calendar.monthrange(dues_date.year, dues_date.month)[1]
            )

    def creat_dues_yearly(self):
        """
        pass
        """
        start_date = parser.parse(self.start_date)
        end_date = parser.parse(self.end_date)
        num_years = (end_date.year - start_date.year) + 1
        dues_date = add_days(
            start_date, self.get_days(start_date, add_months(start_date, 12))
        )

        amount = self.amount / num_years
        if self.party_type == "Employee":
            end_dues_date = add_days(
                dues_date, self.get_days(dues_date, add_months(dues_date, 12))
            )
            amount = self.get_employee_dues(dues_date, end_dues_date)
            if not amount:
                frappe.msgprint(_("Please add salary structer for employee"))
                return
        for i in range(num_years):

            cont_benf = {
                "date_dues": dues_date.date(),
                "amount": amount,
            }
            self.append("contract_dues", cont_benf)
            dues_date = add_days(
                dues_date, self.get_days(dues_date, add_months(dues_date, 12))
            )

    def get_days(self, from_date, to_date):
        date_diff = to_date - from_date
        return date_diff.days

    def create_employee_dues(self):
        amount = self.get_employee_dues

    @frappe.whitelist()
    def create_sales_invoice(self, today=False):
        contract = frappe.get_doc("Contract Type", self.contract_type)
        item = frappe.get_doc("Item", contract.item)
        income_account = frappe.db.get_value(
            "Company", self.company, ["default_income_account"]
        )
        due = self.get_unpaid_dues(today_=today)
        invoice = frappe.get_doc(
            {
                "doctype": "Sales Invoice",
                "customer": self.party_name,
                "due_date": due.date_dues,
                "is_contract_payment_invoice": True,
                "contract": self.name,
                "company": self.company,
            }
        )
        invoice.append(
            "items",
            {
                "item": item,
                "item_name": item.item_name,
                "qty": 1,
                "conversion_factor": 1,
                "rate": due.amount,
                "description": item.name,
                "uom": item.stock_uom,
                "income_account": income_account,
            },
        )
        invoice.insert()
        submit_after_create = frappe.db.get_single_value(
            "Contract Payment Settings", "submit_p_invoice"
        )
        if submit_after_create:
            invoice.submit()

        link = get_link_to_form("Sales Invoice", invoice.name)
        frappe.msgprint(_("invoice created successfuly {0}".format(link)))

    @frappe.whitelist()
    def create_purchase_invoice(self, today=False):
        """
        this for make purchaase invoice
        """
        contract = frappe.get_doc("Contract Type", self.contract_type)
        item = frappe.get_doc("Item", contract.item)
        expense_account = frappe.db.get_value(
            "Company", self.company, ["default_expense_account"]
        )
        due = self.get_unpaid_dues(today_=today)
        invoice = frappe.get_doc(
            {
                "doctype": "Purchase Invoice",
                "supplier": self.party_name,
                "due_date": due.date_dues,
                "is_contract_payment_invoice": True,
                "contract": self.name,
                "comapny": self.company,
            }
        )
        invoice.append(
            "items",
            {
                "item": item,
                "item_name": item.item_name,
                "qty": 1,
                "conversion_factor": 1,
                "rate": due.amount,
                "description": item.name,
                "uom": item.stock_uom,
                "expense_account": expense_account,
            },
        )
        invoice.insert()
        submit_after_create = frappe.db.get_single_value(
            "Contract Payment Settings", "submit_p_invoice"
        )
        if submit_after_create:
            invoice.submit()

        link = get_link_to_form("Purchase Invoice", invoice.name)
        frappe.msgprint(_("purchase invoice created successfuly {0}".format(link)))

    def get_employee_dues(self, start_date, end_date):
        salary_slip = frappe.get_doc(
            {
                "doctype": "Salary Slip",
                "is_payment_contract_salary_slip": True,
                "employee": self.party_name,
                "contract": self.name,
                "company": self.company,
                "start_date": start_date,
                "end_date": end_date,
            }
        )
        salary_slip.validate()
        return salary_slip.gross_pay

    @frappe.whitelist()
    def create_salary_slips(self):
        """
        Creates salary slip for selected employees if already not created
        """
        dues_date = self.get_unpaid_dues.date_dues
        salary_slip = frappe.get_doc(
            {
                "doctype": "Salary Slip",
                "is_payment_contract_salary_slip": True,
                "employee": self.party_name,
                "contract": self.name,
                "company": self.company,
                "start_date": dues_date,
                "end_date": self.get_to_date(dues_date, self.dues_period_),
            }
        )
        salary_slip.insert()
        link = get_link_to_form("Salary Slip", salary_slip.name)
        frappe.msgprint(_("Salary Slip Created Succefully {0}".format(link)))

    def get_to_date(self, start_date, period="Monthly"):
        """
        this function get last date with period
        """
        start_date = get_datetime(start_date)
        if period == "Monthly":
            last_date = add_days(
                start_date, calendar.monthrange(start_date.year, start_date.month)[1]
            )
            return last_date
        elif period == "Yearly":
            last_date = add_days(
                start_date, self.get_days(start_date, add_months(start_date, 12))
            )
            return last_date

    def get_unpaid_dues(self, today_=False):
        for i in self.contract_dues:
            if not i.is_paid:
                if today_:
                    if i.date_dues == today():
                        return i
                    return
                return i
        frappe.msgprint(_("All contract dues is paid"))


def update_contract_dues(doctype, doc):
    contract = doc.contract
    contract_dues = frappe.get_list(
        "Contract Dues", filters={"parent": contract, "is_paid": 0}, fields=["*"]
    )
    paid_amount = doc.total
    for i in contract_dues:
        if paid_amount == 0 or paid_amount < 0:
            break
        if i["is_partial_paid"]:
            i["amount"] = i["amount"] - i["paid_amount"]
        if i["amount"] == paid_amount:
            dues = frappe.get_doc("Contract Dues", i.name)
            dues.is_paid = True
            dues.is_partial_paid = False
            dues.party_type = doctype
            dues.party_name = doc.name
            dues.paid_amount = paid_amount
            dues.save()
            break
        elif i["amount"] > paid_amount:
            dues = frappe.get_doc("Contract Dues", i.name)
            dues.is_partial_paid = True
            dues.party_type = doctype
            dues.party_name = doc.name
            dues.paid_amount = paid_amount
            if i["is_partial_paid"]:
                dues.paid_amount = paid_amount + i["paid_amount"]
            dues.save()
            break
        elif i["amount"] < paid_amount:
            dues = frappe.get_doc("Contract Dues", i.name)
            dues.is_paid = True
            dues.party_type = doctype
            dues.party_name = doc.name
            paid_amount = paid_amount - i["amount"]
            dues.paid_amount = i["amount"]
            dues.save()
