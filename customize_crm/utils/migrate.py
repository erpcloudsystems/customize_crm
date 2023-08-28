import frappe
import json
BENCH_PATH = frappe.utils.get_bench_path()

def after_migrate():
	add_lines_in_quick()
	replace_import_file()
	create_role()

def add_lines_in_quick():
	target_file_path = "{}/{}".format(BENCH_PATH, "apps/erpnext/erpnext/public/js/utils/customer_quick_entry.js")
	source_file_path = "{}/{}".format(BENCH_PATH, "apps/customize_crm/customize_crm/public/js/customer_quick_entry.js")
	open(target_file_path, 'w').close()

	with open(source_file_path) as f:
		with open(target_file_path, "w") as f1:
			for line in f:
				f1.write(line)

	print("Override Custom Quick Entry Js")

def replace_import_file():
	target_file_path = "{}/{}".format(BENCH_PATH, "apps/frappe/frappe/modules/import_file.py")
	source_file_path = "{}/{}".format(BENCH_PATH, "apps/customize_crm/customize_crm/utils/import_file.py")
	open(target_file_path, 'w').close()

	with open(source_file_path) as f:
		with open(target_file_path, "w") as f1:
			for line in f:
				f1.write(line)

	print("Override import_file in frappe")	


def create_role():
	if not frappe.db.exists("Role", "Lead Manager"):
		create_role_name=frappe.new_doc("Role")
		create_role_name.role_name="Lead Manager"
		create_role_name.insert(ignore_mandatory=True)