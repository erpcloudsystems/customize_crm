from __future__ import unicode_literals
import frappe
from erpnext.crm.doctype.lead.lead import Lead

class CustomLead(Lead):
    def create_contact(self):
        pass