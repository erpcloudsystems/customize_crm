# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "customize_crm"
app_title = "Customize Crm"
app_publisher = "Tech Station"
app_description = "App for Custom CRM"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "dev"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/customize_crm/css/customize_crm.css"
# app_include_js = "/assets/customize_crm/js/customize_crm.js"

# include js, css files in header of web template
# web_include_css = "/assets/customize_crm/css/customize_crm.css"
# web_include_js = "/assets/customize_crm/js/customize_crm.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Lead" : "public/js/lead.js",
	"Customer":"public/js/customer.js",
	"Address":"public/js/address.js"
}
doctype_list_js = {
	"Lead" : "public/js/lead_list.js",
	"Customer":"public/js/customer_list.js"
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "customize_crm.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "customize_crm.install.before_install"
# after_install = "customize_crm.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "customize_crm.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Lead": {
			"validate":"customize_crm.hook.lead.validate"
		},
	# "Project": {
	# 		"validate":"customize_crm.hook.lead.update_record"
	# 	},
	# "Sales Order": {
	# 		"validate":"customize_crm.hook.lead.update_customer_record"
	# 	},
 	"Customer": {
		"after_insert":"customize_crm.hook.customer.createContact",
		"validate":"customize_crm.hook.customer.validate"
	},
	"Contact": {
			"validate":"customize_crm.hook.contact.validate"
	}
}

fixtures = [
	{
		"doctype": "Property Setter",
		"filters": [
			[
				"name",
				"in",
				[
			# Address Property
			"Address-address_line2-hidden",
			"Address-address_line1-label",

			# Lead Property
			"Lead-territory-hidden",
			"Lead-address_html-hidden",
			"Lead-address_desc-hidden",
			"Lead-contact_info-label",
			"Lead-phone-hidden",
			"Lead-mobile_no-hidden",
			"Lead-salutation-hidden",
			"Lead-lead_owner-label",
			"Lead-address_title-hidden",
			"Lead-address_line1-hidden",
			"Lead-address_line2-hidden",
			"Lead-city-hidden",
			"Lead-address_info-label",
			"Lead-county-hidden",
			"Lead-state-hidden",
			"Lead-pincode-hidden",
			"Lead-fax-hidden",
			"Lead-website-hidden",
			"Lead-company-reqd",
			"Lead-contact_html-hidden",

			# Issue Property
			"Issue-subject-in_standard_filter",
			"Issue-customer-in_standard_filter",
			"Issue-raised_by-in_list_view",
			"Issue-priority-in_list_view",
			"Issue-customer-in_list_view",

			# Customer Property
			"Customer-territory-reqd"
		]
	   ]
	]
		},
	{
		"doctype": "Custom Field",
		"filters": [
			[
				"name",
				"in",
				[
			# Customer Custom Field
			"Customer-note",
			"Customer-assign_to",
			"Customer-date",
			"Customer-create_todo",
			"Customer-contact_created",
			"Customer-created_by",
			"Customer-passport_number_1",
			"Customer-national_identification_number_1",
			"Customer-national_identity",
			"Customer-country",
			"Customer-state",
			"Customer-date_of_birth_1",
			"Customer-column_break_21",
			"Customer-nationality_1",
			"Customer-column_break_30",
			"Customer-address_line",
			"Customer-primary_address_detail",
			"Customer-telegram_1",
			"Customer-whatsapp",
			"Customer-column_break_23",
			"Customer-phone_no",
			"Customer-mobile_no_0",
			"Customer-mobile_no_1",
			"Customer-preferred_method_of_communication",
			"Customer-primary_contact_detail",
			"Customer-special_marque",
			"Customer-number_of_stairs",
			"Customer-way_to_climb",
			"Customer-floor",
			"Customer-apartment_number",
			"Customer-house_number",
			"Customer-street",
			"Customer-city_town",
			"Customer-postal_code",
			"Customer-email_add",
			"Customer-fax",
			"Customer-company",
			"Customer-sub_territory",
			"Customer-phone_to_contact",
			"Customer-reason_for_view",

			# Lead Custom Field
			"Lead-preferred_method_of_communication",
			"Lead-mobile_no_0",
			"Lead-mobile_no_1",
			"Lead-column_break_57",
			"Lead-whatsapp",
			"Lead-telegram",
			"Lead-customer_group",
			"Lead-territory_name",
			"Lead-nationality",
			"Lead-date_of_birth",
			"Lead-national_identification_number",
			"Lead-passport_number",
			"Lead-phone_no",
			"Lead-address_line",
			"Lead-city_town",
			"Lead-street",
			"Lead-postal_code",
			"Lead-column_break_52",
			"Lead-house_number",
			"Lead-apartment_number",
			"Lead-floor",
			"Lead-special_marque",
			"Lead-way_to_climb",
			"Lead-number_of_stairs",
			"Contact-sub_contact",
			"Lead-sub_territory",
			"Lead-formatting",

			# Contact Custom Field
			"Contact-preferred_method_of_communication",
			"Contact-mobile_no_1",
			"Contact-whatsapp",
			"Contact-telegram",
			"Contact-column_break_27",
			"Contact-lead",
			"Contact-column_break_38",
			"Contact-company",
			"Contact-nationality",

			# Address Custom Field
			"Address-special_marque",
			"Address-number_of_stairs",
			"Address-way_to_climb",
			"Address-floor",
			"Address-apartment_number",
			"Address-house_number",
			"Address-street",
			"Address-territory",
			"Address-sub_territory",

			# Issue Custom Field
			"Issue-territory",
			"Issue-assign_to",

			# Territory Custom Field
			"Territory-shipping_fee",
			"Territory-collection_fee",
			"Territory-shipping_days",
			"Territory-available_working_days_for_shipping",
			"Territory-maximum_order_limit",
			"Territory-enabled",
			"Territory-section_break_1",
				]
			]
		]
	}
]

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"customize_crm.tasks.all"
# 	],
# 	"daily": [
# 		"customize_crm.tasks.daily"
# 	],
# 	"hourly": [
# 		"customize_crm.tasks.hourly"
# 	],
# 	"weekly": [
# 		"customize_crm.tasks.weekly"
# 	]
# 	"monthly": [
# 		"customize_crm.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "customize_crm.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "customize_crm.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "customize_crm.task.get_dashboard_data"
# }

override_doctype_class = {
	"Lead": "customize_crm.override.lead.CustomLead"
}

after_migrate = "customize_crm.utils.migrate.after_migrate"