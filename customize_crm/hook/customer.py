import frappe
import json
from frappe import msgprint, throw, _
import re
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, get_url, get_datetime
from customize_crm.utils.number_format_validate import validate_format_length_customer

def validate(doc, method):
	# Validate Formatting
	if doc.nationality_1:
		validate_format_length_customer(doc)

	# Validate String
	pattern = re.compile("[A-Za-z]+")
	if any(chr.isdigit() for chr in doc.customer_name):
		throw(_("Customer Name Should Only Consist of Alphabets"))

	if doc.phone_no and doc.phone_no in [doc.mobile_no_0,doc.mobile_no_1,doc.whatsapp,doc.telegram_1]:
		frappe.throw(_("This Phone Number is already in use in this form"))

	if doc.mobile_no_0 and doc.mobile_no_0 in [doc.phone_no,doc.mobile_no_1,doc.whatsapp,doc.telegram_1]:
		frappe.throw(_("This Mobile Number is already in use in this form"))

	if doc.mobile_no_1 and doc.mobile_no_1 in [doc.mobile_no_0,doc.phone_no,doc.whatsapp,doc.telegram_1]:
		frappe.throw(_("Emergency Mobile Number is already in use in this form"))

	if doc.whatsapp and doc.whatsapp in [doc.mobile_no_0,doc.mobile_no_1,doc.phone_no]:
		frappe.throw(_("Whatsapp Number is already in use in this form"))

	if doc.telegram_1 and doc.telegram_1 in [doc.mobile_no_0,doc.mobile_no_1,doc.phone_no]:
		frappe.throw(_("Telegram Number is already in use in this form"))

	try:
		if doc.phone_no:
			int(str(doc.phone_no))
		if doc.mobile_no_0:
			int(str(doc.mobile_no_0))
		if doc.mobile_no_1:
			int(str(doc.mobile_no_1))
		if doc.whatsapp:
			int(str(doc.whatsapp))
		if doc.telegram_1:
			int(str(doc.telegram_1))

	except ValueError:
		frappe.throw("Contact number added in string type. Please change it to integer.")	

	# Validate Contact Digit Limit

	phone_no_digit = frappe.db.get_value('Format Contact Number Table',{'parent':doc.nationality_1,'contact_type':'Phone'},'formatting')
	mobile_no_digit = frappe.db.get_value('Format Contact Number Table',{'parent':doc.nationality_1,'contact_type':'Mobile No'},'formatting')
	emergency_no_digit = frappe.db.get_value('Format Contact Number Table',{'parent':doc.nationality_1,'contact_type':'Emergency Mobile No'},'formatting')
	whatsapp_no_digit = frappe.db.get_value('Format Contact Number Table',{'parent':doc.nationality_1,'contact_type':'Whatsapp'},'formatting')
	telegram_no_digit = frappe.db.get_value('Format Contact Number Table',{'parent':doc.nationality_1,'contact_type':'Telegram'},'formatting')

	if phone_no_digit and doc.phone_no:
		if len(doc.phone_no) > phone_no_digit:
			frappe.throw(_("Phone No Length Should not be more then <b>{0}</b> digit").format(phone_no_digit))

	if mobile_no_digit and doc.mobile_no_0:
		if len(doc.mobile_no_0) > mobile_no_digit:
			frappe.throw(_("Mobile No Length Should not be more then <b>{0}</b> digit").format(mobile_no_digit))

	if emergency_no_digit and doc.mobile_no_1:
		if len(doc.mobile_no_1) > emergency_no_digit:
			frappe.throw(_("Emergency No Length Should not be more then <b>{0}</b> digit").format(emergency_no_digit))

	if whatsapp_no_digit and doc.whatsapp:
		if len(doc.whatsapp) > whatsapp_no_digit:
			frappe.throw(_("Whatsapp No Length Should not be more then <b>{0}</b> digit").format(whatsapp_no_digit))

	if telegram_no_digit and doc.telegram_1:
		if len(doc.telegram_1) > telegram_no_digit:
			frappe.throw(_("Telegram No Length Should not be more then <b>{0}</b> digit").format(telegram_no_digit))
	
	# Validation for Phone Number

	if doc.phone_no and (doc.is_new() or not doc.is_new()) and not doc.lead_name:
		contact_id = get_contact_id(doc.name,doc.phone_no,doc.company)
		if contact_id:
			url = get_url("/app/contact/{0}").format(contact_id)
			frappe.throw(_("Phone Number Already Registered In Contact <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,contact_id,doc.company))

		lead_id = get_lead_id(doc.name,doc.phone_no,doc.company)
		if lead_id:
			url = get_url(("/app/lead/{0}").format(lead_id))
			frappe.throw(_("Phone Number Already Registered In Lead <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,lead_id,doc.company))

	# Validation for Mobile Number

	if doc.mobile_no_0 and (doc.is_new() or not doc.is_new()) and not doc.lead_name:
		contact_id = get_contact_id(doc.name,doc.mobile_no_0,doc.company)
		if contact_id:
			url = get_url("/app/contact/{0}").format(contact_id)
			frappe.throw(_("Mobile Number Already Registered In Contact <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,contact_id,doc.company))

		lead_id = get_lead_id(doc.name,doc.mobile_no_0,doc.company)
		if lead_id:
			url = get_url(("/app/lead/{0}").format(lead_id))
			frappe.throw(_("Mobile Number Already Registered In Lead <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,lead_id,doc.company))

	# Validation for Mobile Number 1

	if doc.mobile_no_1 and (doc.is_new() or not doc.is_new()) and not doc.lead_name:
		contact_id = get_contact_id(doc.name,doc.mobile_no_1,doc.company)
		if contact_id:
			url = get_url("/app/contact/{0}").format(contact_id)
			frappe.throw(_("Emergency Mobile Number Already Registered In Contact <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,contact_id,doc.company))

		lead_id = get_lead_id(doc.name,doc.mobile_no_1,doc.company)
		if lead_id:
			url = get_url(("/app/lead/{0}").format(lead_id))
			frappe.throw(_("Emergency Mobile Number Already Registered In Lead <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,lead_id,doc.company))

	# Validation for Whatsapp Number

	if doc.whatsapp and (doc.is_new() or not doc.is_new()) and not doc.lead_name:
		contact_id = get_contact_id(doc.name,doc.whatsapp,doc.company)
		if contact_id:
			url = get_url("/app/contact/{0}").format(contact_id)
			frappe.throw(_("Whatsapp Number Already Registered In Contact <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,contact_id,doc.company))

		lead_id = get_lead_id(doc.name,doc.whatsapp,doc.company)
		if lead_id:
			url = get_url(("/app/lead/{0}").format(lead_id))
			frappe.throw(_("Whatsapp Number Already Registered In Lead <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,lead_id,doc.company))

	# Validation for Telegram

	if doc.telegram_1 and (doc.is_new() or not doc.is_new()) and not doc.lead_name:
		contact_id = get_contact_id(doc.name,doc.telegram_1,doc.company)
		if contact_id:
			url = get_url("/app/contact/{0}").format(contact_id)
			frappe.throw(_("Telegram Number Already Registered In Contact <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,contact_id,doc.company))

		lead_id = get_lead_id(doc.name,doc.telegram_1,doc.company)
		if lead_id:
			url = get_url(("/app/lead/{0}").format(lead_id))
			frappe.throw(_("Telegram Number Already Registered In Lead <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,lead_id,doc.company))

	# Validation For NIN

	if doc.national_identification_number_1 and (doc.is_new() or not doc.is_new()) and not doc.lead_name:
		ninumber = frappe.db.sql("""select name from `tabLead` where name != '{lead_name}' and 
			national_identification_number = '{ni_number}';"""
			.format(
				lead_name = doc.name,
				ni_number = doc.national_identification_number_1
			),as_dict = True)

		if ninumber:
			url = get_url(("/app/lead/{0}").format(ninumber[0].name))
			frappe.throw(_("National Identification Number Already Registered In Lead <b><a href={0}>{1}</a></b>").format(url,ninumber[0].name))

		ninumber = frappe.db.sql("""select name from `tabCustomer` where name != '{lead_name}' and 
			national_identification_number_1 = '{ni_number}';"""
			.format(
				lead_name = doc.name,
				ni_number = doc.national_identification_number_1
			),as_dict = True)

		if ninumber:
			url = get_url(("/app/customer/{0}").format(ninumber[0].name))
			frappe.throw(_("National Identification Number Already Registered In Customer <b><a href={0}>{1}</a></b>").format(url,ninumber[0].name))

	# Validation For Passport Number

	if doc.passport_number_1 and (doc.is_new() or not doc.is_new()) and not doc.lead_name:
		ppnumber = frappe.db.sql("""select name from `tabLead` where name != '{lead_name}' and 
			passport_number = '{passport_number}';"""
			.format(
				lead_name = doc.name,
				passport_number = doc.passport_number_1
			),as_dict = True)

		if ppnumber:
			url = get_url(("/app/lead/{0}").format(ppnumber[0].name))
			frappe.throw(_("Passport Number Already Registered In Lead <b><a href={0}>{1}</a></b>").format(url,ppnumber[0].name))

		ppnumber = frappe.db.sql("""select name from `tabCustomer` where name != '{lead_name}' and 
			passport_number_1 = '{passport_number}';"""
			.format(
				lead_name = doc.name,
				passport_number = doc.passport_number_1
			),as_dict = True)

		if ppnumber:
			url = get_url(("/app/customer/{0}").format(ppnumber[0].name))
			frappe.throw(_("Passport Number Already Registered In Customer <b><a href={0}>{1}</a></b>").format(url,ppnumber[0].name))

	if doc.create_todo:
		perm = frappe.get_doc({
		"doctype": "ToDo",
		"owner": doc.assign_to,
		"date": doc.date,
		"description": doc.note,
		"reference_type": "Customer",
		"reference_name": doc.name,
		"assigned_by": frappe.session.user
		})
		perm.insert(ignore_permissions=True,ignore_mandatory = True)
		perm.save()
		frappe.msgprint("ToDo Created")

	update_customer_view_tracked(doc)

@frappe.whitelist(allow_guest=True)
def update_customer_view_tracked(doc):
	track = frappe.get_doc({
	"doctype": "Customer Profile Viewed",
	"viewed_by_user": frappe.session.user,
	"customer": doc.name,
	"timestamp_of_view": get_datetime(),
	"viewers_notes": doc.reason_for_view or 'User Did Not Update Notes',
	})
	track.insert(ignore_permissions=True,ignore_mandatory = True)
	track.save()

@frappe.whitelist()
def get_contact_id(customer,contact_number,company):
	contact_id = frappe.db.sql("""select con.name as name from `tabDynamic Link` dl, `tabContact` con
		where dl.parent = con.name and dl.link_doctype = 'Customer' and (phone = {contact_number} or mobile_no = {contact_number}
		or mobile_no_1 = {contact_number} or whatsapp = {contact_number} or telegram = {contact_number}) 
		and dl.link_name != '{customer}' and company = '{company}';"""
		.format(
			customer = customer,
			contact_number = contact_number,
			company = company
		),as_dict = True)

	return contact_id[0].name if contact_id else False

@frappe.whitelist()
def get_lead_id(lead_id,contact_number,company):
	lead_id = frappe.db.sql("""select name from `tabLead` where name != '{lead_name}' and (phone_no = {contact_number} or 
		mobile_no_0 = {contact_number} or mobile_no_1 = {contact_number} or whatsapp = {contact_number} or 
		telegram = {contact_number}) and company = '{company}';"""
		.format(
			lead_name = lead_id,
			contact_number = contact_number,
			company = company
		),as_dict = True)

	return lead_id[0].name if lead_id else False

@frappe.whitelist(allow_guest=True)
def createContact(doc,method):
	doc.created_by = frappe.session.user
	doc.save()

	if doc.address_line:
		address = frappe.get_doc({
		"doctype": "Address",
		"address_line1": doc.address_line,
		"city": doc.city_town,
		"street": doc.street,
		"country": doc.country,
		"territory": doc.territory,
		"sub_territory": doc.sub_territory,
		"pincode": doc.postal_code,
		"telegram": doc.telegram_1,
		"house_number": doc.house_number,
		"apartment_number": doc.apartment_number,
		"floor": doc.floor,
		"way_to_climb": doc.way_to_climb,
		"number_of_stairs": doc.number_of_stairs,
		"special_marque": doc.special_marque,
		'links': [{
			'link_doctype': doc.doctype,
			'link_name': doc.name
		}]
		})
		address.insert(ignore_permissions=True,ignore_mandatory = True)
		address.save()
		frappe.msgprint("Address Created")

	phone_nos = []
	email_ids = []
	if doc.phone_no:
		phone_nos.append({'phone':doc.phone_no,'is_primary_phone': 1})
	if doc.mobile_no_0:
		phone_nos.append({'phone':doc.mobile_no_0,'is_primary_mobile_no': 1})
	if doc.email_add:
		email_ids.append({'email_id': doc.email_add,'is_primary': 1})

	contact = frappe.get_doc({
		"doctype": "Contact",
		"first_name": doc.name,
		"lead": doc.lead_name,
		"preferred_method_of_communication": doc.preferred_method_of_communication,
		"mobile_no_1": doc.mobile_no_1,
		"whatsapp": doc.whatsapp,
		"telegram": doc.telegram_1,
		'is_primary_contact': 1,
		'company': doc.company,
		'nationality': doc.nationality_1,
		"contact": 1,
		'email_ids': email_ids,
		'phone_nos': phone_nos,
		'links': [{
				'link_doctype': doc.doctype,
				'link_name': doc.name
			}]
	})
	contact.insert(ignore_permissions=True,ignore_mandatory = True)
	contact.save()
	frappe.msgprint("Contact Created")

@frappe.whitelist()
def get_search_data(search_type = '',search_data=''):
	if search_type == "Identification":
		lead = frappe.db.sql("""select name,company from `tabLead` where 
		national_identification_number = {}""".format(search_data))
		contact = frappe.db.sql("""select customer_name,docstatus from `tabCustomer` 
		where national_identification_number_1 = {}""".format(search_data))

	elif search_type == "Passport":
		lead = frappe.db.sql("""select name,company from `tabLead` where passport_number = {}""".format(search_data))
		contact = frappe.db.sql("""select customer_name,docstatus from 
		`tabCustomer` where passport_number_1 = {}""".format(search_data))

	elif search_type == "Phone":
		contact = frappe.db.sql("""select dl.link_title,ct.company from `tabDynamic Link` dl inner join 
		`tabContact` ct on  ct.name = dl.parent where phone = {0} or mobile_no = {0} or mobile_no_1 = {0}""".format(search_data))
		lead = frappe.db.sql("""select name,company from `tabLead` where phone_no = {0} or 
		mobile_no_0 = {0} or mobile_no_1 = {0}""".format(search_data))

	search_result = []
	for data in lead:
		search_result.append({'idx':1,'document_type':'Lead','customer':data[0],'company':data[1]})

	for data in contact:
		search_result.append({'idx':2,'document_type':'Contact','customer':data[0],'company':data[1]})

	return {'result':search_result}	