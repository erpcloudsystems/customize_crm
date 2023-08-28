import frappe
import json
from frappe import msgprint, throw, _
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, get_url
from customize_crm.utils.number_format_validate import validate_format_length_contact

def validate(doc, method):
	# Validate Formatting
	if doc.nationality:
		validate_format_length_contact(doc)

	if doc.phone and doc.phone in [doc.mobile_no,doc.mobile_no_1,doc.whatsapp,doc.telegram]:
		frappe.throw(_("This Phone Number is already in use in this form"))

	if doc.mobile_no and doc.mobile_no in [doc.phone,doc.mobile_no_1,doc.whatsapp,doc.telegram]:
		frappe.throw(_("This Mobile Number is already in use in this form"))

	if doc.mobile_no_1 and doc.mobile_no_1 in [doc.mobile_no,doc.phone,doc.whatsapp,doc.telegram]:
		frappe.throw(_("Emergency Mobile Number is already in use in this form"))

	if doc.whatsapp and doc.whatsapp in [doc.mobile_no,doc.mobile_no_1,doc.phone]:
		frappe.throw(_("Whatsapp Number is already in use in this form"))

	if doc.telegram and doc.telegram in [doc.mobile_no,doc.mobile_no_1,doc.phone]:
		frappe.throw(_("Telegram Number is already in use in this form"))

	try:
		if doc.phone:
			int(str(doc.phone))
		if doc.mobile_no:
			int(str(doc.mobile_no))
		if doc.mobile_no_1:
			int(str(doc.mobile_no_1))
		if doc.whatsapp:
			int(str(doc.whatsapp))
		if doc.telegram:
			int(str(doc.telegram))

	except ValueError:
		frappe.throw("Contact number added in string type. Please change it to integer.")
	
	# Validate Contact Digit Limit

	phone_no_digit = frappe.db.get_value('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Phone'},'formatting')
	mobile_no_digit = frappe.db.get_value('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Mobile No'},'formatting')
	emergency_no_digit = frappe.db.get_value('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Emergency Mobile No'},'formatting')
	whatsapp_no_digit = frappe.db.get_value('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Whatsapp'},'formatting')
	telegram_no_digit = frappe.db.get_value('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Telegram'},'formatting')

	if phone_no_digit and doc.phone:
		if len(doc.phone) > phone_no_digit:
			frappe.throw(_("Phone No Length Should not be more then <b>{0}</b> digit").format(phone_no_digit))

	if mobile_no_digit and doc.mobile_no:
		if len(doc.mobile_no) > mobile_no_digit:
			frappe.throw(_("Mobile No Length Should not be more then <b>{0}</b> digit").format(mobile_no_digit))

	if emergency_no_digit and doc.mobile_no_1:
		if len(doc.mobile_no_1) > emergency_no_digit:
			frappe.throw(_("Emergency No Length Should not be more then <b>{0}</b> digit").format(emergency_no_digit))

	if whatsapp_no_digit and doc.whatsapp:
		if len(doc.whatsapp) > whatsapp_no_digit:
			frappe.throw(_("Whatsapp No Length Should not be more then <b>{0}</b> digit").format(whatsapp_no_digit))

	if telegram_no_digit and doc.telegram:
		if len(doc.telegram) > telegram_no_digit:
			frappe.throw(_("Telegram No Length Should not be more then <b>{0}</b> digit").format(telegram_no_digit))

	# Validation for Phone Number

	if doc.phone and (doc.is_new() or not doc.is_new()):
		customer_id = get_customer_id(doc.first_name,doc.phone,doc.company)
		if customer_id:
			url = get_url("/app/customer/{0}").format(customer_id)
			frappe.throw(_("Phone Number Already Registered In Customer <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,customer_id,doc.company))
			
		contact_id = get_contact_id(doc.name,doc.phone,doc.company,doc.lead)
		if contact_id:
			url = get_url("/app/contact/{0}").format(contact_id)
			frappe.throw(_("Phone Number Already Registered In Contact <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,contact_id,doc.company))

		lead_id = get_lead_id(doc.phone,doc.company,doc.lead)
		if lead_id:
			url = get_url(("/app/lead/{0}").format(lead_id))
			frappe.throw(_("Phone Number Already Registered In Lead <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,lead_id,doc.company))

	# Validation for Mobile Number

	if doc.mobile_no and (doc.is_new() or not doc.is_new()):
		customer_id = get_customer_id(doc.first_name,doc.mobile_no,doc.company)
		if customer_id:
			url = get_url("/app/customer/{0}").format(customer_id)
			frappe.throw(_("Mobile Number Already Registered In Customer <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,customer_id,doc.company))
			
		contact_id = get_contact_id(doc.name,doc.mobile_no,doc.company,doc.lead)
		if contact_id:
			url = get_url("/app/contact/{0}").format(contact_id)
			frappe.throw(_("Mobile Number Already Registered In Contact <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,contact_id,doc.company))

		lead_id = get_lead_id(doc.mobile_no,doc.company,doc.lead)
		if lead_id:
			url = get_url(("/app/lead/{0}").format(lead_id))
			frappe.throw(_("Mobile Number Already Registered In Lead <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,lead_id,doc.company))

	# Validation for Mobile Number 1

	if doc.mobile_no_1 and (doc.is_new() or not doc.is_new()):
		customer_id = get_customer_id(doc.first_name,doc.mobile_no_1,doc.company)
		if customer_id:
			url = get_url("/app/customer/{0}").format(customer_id)
			frappe.throw(_("Emergency Mobile Number Already Registered In Customer <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,customer_id,doc.company))

		contact_id = get_contact_id(doc.name,doc.mobile_no_1,doc.company,doc.lead)
		if contact_id:
			url = get_url("/app/contact/{0}").format(contact_id)
			frappe.throw(_("Emergency Mobile Number Already Registered In Contact <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,contact_id,doc.company))

		lead_id = get_lead_id(doc.mobile_no_1,doc.company,doc.lead)
		if lead_id:
			url = get_url(("/app/lead/{0}").format(lead_id))
			frappe.throw(_("Emergency Mobile Number Already Registered In Lead <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,lead_id,doc.company))

	# Validation for Whatsapp Number

	if doc.whatsapp and (doc.is_new() or not doc.is_new()):
		customer_id = get_customer_id(doc.first_name,doc.whatsapp,doc.company)
		if customer_id:
			url = get_url("/app/customer/{0}").format(customer_id)
			frappe.throw(_("Whatsapp Number Already Registered In Customer <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,customer_id,doc.company))

		contact_id = get_contact_id(doc.name,doc.whatsapp,doc.company,doc.lead)
		if contact_id:
			url = get_url("/app/contact/{0}").format(contact_id)
			frappe.throw(_("Whatsapp Number Already Registered In Contact <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,contact_id,doc.company))

		lead_id = get_lead_id(doc.whatsapp,doc.company,doc.lead)
		if lead_id:
			url = get_url(("/app/lead/{0}").format(lead_id))
			frappe.throw(_("Whatsapp Number Already Registered In Lead <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,lead_id,doc.company))

	# Validation for Telegram

	if doc.telegram and (doc.is_new() or not doc.is_new()):
		customer_id = get_customer_id(doc.first_name,doc.telegram,doc.company)
		if customer_id:
			url = get_url("/app/customer/{0}").format(customer_id)
			frappe.throw(_("Telegram Number Already Registered In Customer <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,customer_id,doc.company))

		contact_id = get_contact_id(doc.name,doc.telegram,doc.company,doc.lead)
		if contact_id:
			url = get_url("/app/contact/{0}").format(contact_id)
			frappe.throw(_("Telegram Number Already Registered In Contact <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,contact_id,doc.company))

		lead_id = get_lead_id(doc.telegram,doc.company,doc.lead)
		if lead_id:
			url = get_url(("/app/lead/{0}").format(lead_id))
			frappe.throw(_("Telegram Number Already Registered In Lead <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,lead_id,doc.company))

@frappe.whitelist()
def get_customer_id(customer,contact_number,company):
	customer_id = frappe.db.sql("""select name from `tabCustomer` where (phone_no = {contact_number} or 
		mobile_no_0 = {contact_number} or mobile_no_1 = {contact_number} or whatsapp = {contact_number} or 
		telegram_1 = {contact_number}) and name != '{customer}' and company = '{company}';"""
		.format(
			contact_number = contact_number,
			customer = customer,
			company = company
		),as_dict = True)

	return customer_id[0].name if customer_id else False

@frappe.whitelist()
def get_contact_id(contact_name,contact_number,company,lead):
	contact_id = frappe.db.sql("""select name from `tabContact` where name != '{contact_name}' and (phone = {contact_number} or 
		mobile_no = {contact_number} or mobile_no_1 = {contact_number} or whatsapp = {contact_number} or 
		telegram = {contact_number}) and company = '{company}' and lead != '{lead}';"""
		.format(
			contact_name = contact_name,
			contact_number = contact_number,
			company = company,
			lead = lead
		),as_dict = True)

	return contact_id[0].name if contact_id else False

@frappe.whitelist()
def get_lead_id(contact_number,company,lead):
	lead_id = frappe.db.sql("""select name from `tabLead` where (phone_no = {contact_number} or 
		mobile_no_0 = {contact_number} or mobile_no_1 = {contact_number} or whatsapp = {contact_number} or 
		telegram = {contact_number}) and company = '{company}' and name != '{lead}';"""
		.format(
			contact_number = contact_number,
			company = company,
			lead = lead
		),as_dict = True)

	return lead_id[0].name if lead_id else False