import frappe

def validate_format_length_lead(doc):
	# Validate Phone
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Phone'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Phone'})
		if doc.phone_no and len(doc.phone_no) != country_format.formatting:
			frappe.throw('Phone Number Formatting Not Matching With Required Format')

	# Validate Mobile No
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Mobile No'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Mobile No'})
		if doc.mobile_no_0 and len(doc.mobile_no_0) != country_format.formatting:
			frappe.throw('Mobile Number Formatting Not Matching With Required Format')

	# Validate Emergency Mobile No
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Emergency Mobile No'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Emergency Mobile No'})
		if doc.mobile_no_1 and len(doc.mobile_no_1) != country_format.formatting:
			frappe.throw('Emergency Mobile Number Formatting Not Matching With Required Format')

	# Validate Whatsapp
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Whatsapp'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Whatsapp'})
		if doc.whatsapp and len(doc.whatsapp) != country_format.formatting:
			frappe.throw('Whatsapp Number Formatting Not Matching With Required Format')

	# Validate Telegram
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Telegram'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Telegram'})
		if doc.telegram and len(doc.telegram) != country_format.formatting:
			frappe.throw('Telegram Number Formatting Not Matching With Required Format')

########################################################################################################

def validate_format_length_customer(doc):
	# Validate Phone
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.nationality_1,'contact_type':'Phone'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.nationality_1,'contact_type':'Phone'})
		if doc.phone_no and len(doc.phone_no) != country_format.formatting:
			frappe.throw('Phone Number Formatting Not Matching With Required Format')

	# Validate Mobile No
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.nationality_1,'contact_type':'Mobile No'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.nationality_1,'contact_type':'Mobile No'})
		if doc.mobile_no_0 and len(doc.mobile_no_0) != country_format.formatting:
			frappe.throw('Mobile Number Formatting Not Matching With Required Format')

	# Validate Emergency Mobile No
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.nationality_1,'contact_type':'Emergency Mobile No'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.nationality_1,'contact_type':'Emergency Mobile No'})
		if doc.mobile_no_1 and len(doc.mobile_no_1) != country_format.formatting:
			frappe.throw('Emergency Mobile Number Formatting Not Matching With Required Format')

	# Validate Whatsapp
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.nationality_1,'contact_type':'Whatsapp'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.nationality_1,'contact_type':'Whatsapp'})
		if doc.whatsapp and len(doc.whatsapp) != country_format.formatting:
			frappe.throw('Whatsapp Number Formatting Not Matching With Required Format')

	# Validate Telegram
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.nationality_1,'contact_type':'Telegram'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.nationality_1,'contact_type':'Telegram'})
		if doc.telegram_1 and len(doc.telegram_1) != country_format.formatting:
			frappe.throw('Telegram Number Formatting Not Matching With Required Format')

########################################################################################################

def validate_format_length_contact(doc):
	# Validate Phone
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Phone'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Phone'})
		if doc.phone and len(doc.phone) != country_format.formatting:
			frappe.throw('Phone Number Formatting Not Matching With Required Format')

	# Validate Mobile No
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Mobile No'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Mobile No'})
		if doc.mobile_no and len(doc.mobile_no) != country_format.formatting:
			frappe.throw('Mobile Number Formatting Not Matching With Required Format')

	# Validate Emergency Mobile No
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Emergency Mobile No'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Emergency Mobile No'})
		if doc.mobile_no_1 and len(doc.mobile_no_1) != country_format.formatting:
			frappe.throw('Emergency Mobile Number Formatting Not Matching With Required Format')

	# Validate Whatsapp
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Whatsapp'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Whatsapp'})
		if doc.whatsapp and len(doc.whatsapp) != country_format.formatting:
			frappe.throw('Whatsapp Number Formatting Not Matching With Required Format')

	# Validate Telegram
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Telegram'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.nationality,'contact_type':'Telegram'})
		if doc.telegram and len(doc.telegram) != country_format.formatting:
			frappe.throw('Telegram Number Formatting Not Matching With Required Format')

def validate_format_length_or(doc):
	# Validate Phone
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.country,'contact_type':'Phone'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.country,'contact_type':'Phone'})
		if doc.phone and len(doc.phone) != country_format.formatting:
			frappe.throw('Phone Number Formatting Not Matching With Required Format')

	# Validate Mobile No
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.country,'contact_type':'Mobile No'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.country,'contact_type':'Mobile No'})
		if doc.mobile_no and len(doc.mobile_no) != country_format.formatting:
			frappe.throw('Mobile Number Formatting Not Matching With Required Format')

	# Validate Emergency Mobile No
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.country,'contact_type':'Emergency Mobile No'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.country,'contact_type':'Emergency Mobile No'})
		if doc.mobile_no_1 and len(doc.mobile_no_1) != country_format.formatting:
			frappe.throw('Emergency Mobile Number Formatting Not Matching With Required Format')

	# Validate Whatsapp
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.country,'contact_type':'Whatsapp'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.country,'contact_type':'Whatsapp'})
		if doc.watsapp and len(doc.watsapp) != country_format.formatting:
			frappe.throw('Whatsapp Number Formatting Not Matching With Required Format')

	# Validate Telegram
	if frappe.db.exists('Format Contact Number Table',{'parent':doc.country,'contact_type':'Telegram'}):
		country_format = frappe.get_doc('Format Contact Number Table',{'parent':doc.country,'contact_type':'Telegram'})
		if doc.telegram and len(doc.telegram) != country_format.formatting:
			frappe.throw('Telegram Number Formatting Not Matching With Required Format')			