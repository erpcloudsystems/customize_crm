import frappe
import json
from frappe import msgprint, throw, _
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, get_url
from customize_crm.utils.number_format_validate import validate_format_length_lead




def update_record(self,method=None):
	# pass
	# update_item(self)
	get_record=frappe.db.sql(f"""select name from `tabShipping Type` where company='Elsawy' """,as_dict=1)
	if get_record:
		for row in get_record:
			frappe.db.set_value("Shipping Type",row.name,{"company":"Carnielli"})

def update_customer_record(self,method=None):
	# pass
	update_customer(self)

def update_customer(self):
	get_record=frappe.db.sql(f"""select name from `tabCustomer` where disabled=0 limit 20""",as_dict=1)
	frappe.msgprint(str(get_record))
	if get_record:
		for row in get_record:
			new_name = "N -"+row.name
			frappe.rename_doc("Customer", row.name, "N -"+row.name, merge=False)
			# frappe.db.set_value("Item",new_name,{"disabled":0})

def update_item(self):
	get_record=frappe.db.sql(f"""select name from `tabShipping Type` where enabled=1 limit 20""",as_dict=1)
	frappe.msgprint(str(get_record))
	if get_record:
		for row in get_record:
			new_name = "N -"+row.name
			frappe.rename_doc("Item", row.name, "N -"+row.name, merge=False)
			frappe.db.set_value("Item",new_name,{"disabled":0})

def validate(doc, method):
	# Validate Formatting 
	if doc.nationality:
		validate_format_length_lead(doc)

	if doc.phone_no and doc.phone_no in [doc.mobile_no_0,doc.mobile_no_1,doc.whatsapp,doc.telegram]:
		frappe.throw(_("This Phone Number is already in use in this form"))

	if doc.mobile_no_0 and doc.mobile_no_0 in [doc.phone_no,doc.mobile_no_1,doc.whatsapp,doc.telegram]:
		frappe.throw(_("This Mobile Number is already in use in this form"))

	if doc.mobile_no_1 and doc.mobile_no_1 in [doc.mobile_no_0,doc.phone_no,doc.whatsapp,doc.telegram]:
		frappe.throw(_("Emergency Mobile Number is already in use in this form"))

	if doc.whatsapp and doc.whatsapp in [doc.mobile_no_0,doc.mobile_no_1,doc.phone_no]:
		frappe.throw(_("Whatsapp Number is already in use in this form"))

	if doc.telegram and doc.telegram in [doc.mobile_no_0,doc.mobile_no_1,doc.phone_no]:
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

	if telegram_no_digit and doc.telegram:
		if len(doc.telegram) > telegram_no_digit:
			frappe.throw(_("Telegram No Length Should not be more then <b>{0}</b> digit").format(telegram_no_digit))


	# Validation for Phone Number
	
	if doc.phone_no and (doc.is_new() or not doc.is_new()):
		contact_id = get_contact_id(doc.phone_no,doc.company)
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

	if doc.mobile_no_0 and (doc.is_new() or not doc.is_new()):
		contact_id = get_contact_id(doc.mobile_no_0,doc.company)
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

	if doc.mobile_no_1 and (doc.is_new() or not doc.is_new()):
		contact_id = get_contact_id(doc.mobile_no_1,doc.company)
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

	if doc.whatsapp and (doc.is_new() or not doc.is_new()):
		contact_id = get_contact_id(doc.whatsapp,doc.company)
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

	if doc.telegram and (doc.is_new() or not doc.is_new()):
		contact_id = get_contact_id(doc.telegram,doc.company)
		if contact_id:
			url = get_url("/app/contact/{0}").format(contact_id)
			frappe.throw(_("Telegram Number Already Registered In Contact <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,contact_id,doc.company))

		lead_id = get_lead_id(doc.name,doc.telegram,doc.company)
		if lead_id:
			url = get_url(("/app/lead/{0}").format(lead_id))
			frappe.throw(_("Telegram Number Already Registered In Lead <b><a href={0}>{1}</a></b> for the company \
			<b>{2}</b>").format(url,lead_id,doc.company))

	# Validation For NIN

	if doc.national_identification_number and (doc.is_new() or not doc.is_new()):
		ninumber = frappe.db.sql("""select name from `tabLead` where name != '{lead_name}' and 
			national_identification_number = '{ni_number}';"""
			.format(
				lead_name = doc.name,
				ni_number = doc.national_identification_number
			),as_dict = True)

		if ninumber:
			url = get_url(("/app/lead/{0}").format(ninumber[0].name))
			frappe.throw(_("National Identification Number Already Registered In Lead <b><a href={0}>{1}</a></b>").format(url,ninumber[0].name))

		ninumber = frappe.db.sql("""select name from `tabCustomer` where name != '{lead_name}' and 
			national_identification_number_1 = '{ni_number}';"""
			.format(
				lead_name = doc.name,
				ni_number = doc.national_identification_number
			),as_dict = True)

		if ninumber:
			url = get_url(("/app/customer/{0}").format(ninumber[0].name))
			frappe.throw(_("National Identification Number Already Registered In Customer <b><a href={0}>{1}</a></b>").format(url,ninumber[0].name))

	# Validation For Passport Number

	if doc.passport_number and (doc.is_new() or not doc.is_new()):
		ppnumber = frappe.db.sql("""select name from `tabLead` where name != '{lead_name}' and 
			passport_number = '{passport_number}';"""
			.format(
				lead_name = doc.name,
				passport_number = doc.passport_number
			),as_dict = True)

		if ppnumber:
			url = get_url(("/app/lead/{0}").format(ppnumber[0].name))
			frappe.throw(_("Passport Number Already Registered In Lead <b><a href={0}>{1}</a></b>").format(url,ppnumber[0].name))

		ppnumber = frappe.db.sql("""select name from `tabCustomer` where name != '{lead_name}' and 
			passport_number_1 = '{passport_number}';"""
			.format(
				lead_name = doc.name,
				passport_number = doc.passport_number
			),as_dict = True)

		if ppnumber:
			url = get_url(("/app/customer/{0}").format(ppnumber[0].name))
			frappe.throw(_("Passport Number Already Registered In Customer <b><a href={0}>{1}</a></b>").format(url,ppnumber[0].name))

@frappe.whitelist()
def get_contact_id(contact_number,company):
	contact_id = frappe.db.sql("""select name from `tabContact` where (phone = {contact_number} or mobile_no = {contact_number} 
		or mobile_no_1 = {contact_number} or whatsapp = {contact_number} or telegram = {contact_number})
		and company = '{company}';"""
		.format(
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

@frappe.whitelist()
def migrate():
	set = frappe.db.sql("""update `tabLead` set phone_no = phone, mobile_no_0 = mobile_no;""")
	return set

@frappe.whitelist()
def get_search_data(search_type = '',search_data=''):
	if search_type == "Identification":
		lead = frappe.db.sql("""select name,company from `tabLead` where 
		national_identification_number = {}""".format(search_data))
		contact = frappe.db.sql("""select customer_name,docstatus,company from `tabCustomer` 
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

@frappe.whitelist()
def convert_numbers():
	leads = frappe.get_list('Lead', fields=['name','phone_no','mobile_no_0','mobile_no_1','national_identification_number','passport_number','preferred_method_of_communication','whatsapp','telegram'])

	for lead in leads:
		contact = frappe.db.get_values("Contact", filters={'lead':lead.name}, fieldname=["name"])

		if contact:

			contact_doc = frappe.get_doc("Contact",contact[0][0])
			if not contact_doc.national_identification_number:
				contact_doc.national_identification_number = lead.national_identification_number

			if not contact_doc.phone:
				contact_doc.phone = lead.phone_no

			if not contact_doc.mobile_no:
				contact_doc.mobile_no = lead.mobile_no_0

			if not contact_doc.mobile_no_1:
				contact_doc.mobile_no_1 = lead.mobile_no_1

			if not contact_doc.passport_number:
				contact_doc.passport_number = lead.passport_number

			if not contact_doc.whatsapp:
				contact_doc.whatsapp = lead.whatsapp

			if not contact_doc.telegram:
				contact_doc.telegram = lead.telegram

			contact_doc.save()

@frappe.whitelist()
def migrate():
	set = frappe.db.sql("""update `tabLead` set phone_no = phone, mobile_no_0 = mobile_no;""")
	return set

@frappe.whitelist(allow_guest=True)
def createCustomer(lead):
	lead = json.loads(lead)
	customer = frappe.get_doc({
	"doctype": "Customer",
	"customer_name": lead.get("lead_name"),
	"company": lead.get("company"),
	"preferred_method_of_communication": lead.get("preferred_method_of_communication"),
	"mobile_no_1": lead.get("mobile_no_1"),
	"whatsapp": lead.get("whatsapp"),
	"telegram_1": lead.get("telegram"),
	"lead_name": lead.get("name"),
	"customer_group": lead.get("customer_group"),
	"territory": lead.get("territory_name"),
	"sub_territory": lead.get("sub_territory"),
	"phone_no": lead.get("phone_no"),
	"email_add": lead.get("email_id"),
	"email_id": lead.get("email_id"),
	"fax": lead.get("fax"),
	"website": lead.get("website"),
	"mobile_no_0": lead.get("mobile_no_0"),
	"address_line": lead.get("address_line"),
	"city_town": lead.get("city_town"),
	"street": lead.get("street"),
	"country": lead.get("country"),
	"postal_code": lead.get("postal_code"),
	"house_number": lead.get("house_number"),
	"apartment_number": lead.get("apartment_number"),
	"floor": lead.get("floor"),
	"way_to_climb": lead.get("way_to_climb"),
	"number_of_stairs": lead.get("number_of_stairs"),
	"special_marque": lead.get("special_marque"),
	"nationality_1": lead.get("nationality"),
	"date_of_birth_1": lead.get("date_of_birth"),
	"national_identification_number_1": lead.get("national_identification_number"),
	"passport_number_1": lead.get("passport_number"),
	"contact_created": 1
	})
	customer.insert(ignore_permissions=True,ignore_mandatory = True)
	customer.save()
	frappe.msgprint("Customer Created")	