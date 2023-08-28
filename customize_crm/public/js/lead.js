frappe.ui.form.on('Lead', {
	refresh(frm) {
		frm.set_query('sub_territory', function() {
			return {
				filters: {
					parent_territory: frm.doc.territory_name,
					enabled: 1
				}
			};
		});

		frm.set_query('territory_name', function() {
			return {
				filters: {
					enabled: 1,
					is_group: 1
				}
			};
		});		
	},
	territory_name(frm) {
		frm.set_value('sub_territory','');	
	}
});

erpnext.LeadController = frappe.ui.form.Controller.extend({

	setup: function () {
		this.frm.make_methods = {
			'Quotation': () => erpnext.utils.create_new_doc('Quotation', {
				'quotation_to': this.frm.doc.doctype,
				'party_name': this.frm.doc.name
			}),
			'Opportunity': () => erpnext.utils.create_new_doc('Opportunity', {
				'opportunity_from': this.frm.doc.doctype,
				'party_name': this.frm.doc.name
			})
		}

		this.frm.fields_dict.customer.get_query = function (doc, cdt, cdn) {
			return { query: "erpnext.controllers.queries.customer_query" }
		}

		this.frm.toggle_reqd("lead_name", !this.frm.doc.organization_lead);
	},

	onload: function () {
		if (cur_frm.fields_dict.lead_owner.df.options.match(/^User/)) {
			cur_frm.fields_dict.lead_owner.get_query = function (doc, cdt, cdn) {
				return { query: "frappe.core.doctype.user.user.user_query" }
			}
		}

		if (cur_frm.fields_dict.contact_by.df.options.match(/^User/)) {
			cur_frm.fields_dict.contact_by.get_query = function (doc, cdt, cdn) {
				return { query: "frappe.core.doctype.user.user.user_query" }
			}
		}
	},

	refresh: function () {
		var doc = this.frm.doc;
		erpnext.toggle_naming_series();
		frappe.dynamic_link = { doc: doc, fieldname: 'name', doctype: 'Lead' }

		if(!doc.__islocal && doc.__onload && !doc.__onload.is_customer && doc.status != "Converted") {
			let user=frappe.session.user;

			if(frappe.user.has_role("Lead Manager") || user == doc.lead_owner){
				this.frm.set_df_property('lead_owner', 'read_only', 0);
				this.frm.add_custom_button(__("Make Customer"), this.create_customer_new, __('Create'));
			}
			else{
				this.frm.set_df_property('lead_owner', 'read_only', 1);
			}
			this.frm.add_custom_button(__("Opportunity"), this.create_opportunity, __('Create'));
			this.frm.add_custom_button(__("Quotation"), this.make_quotation, __('Create'));
		}

		if (!this.frm.doc.__islocal) {
			frappe.contacts.render_address_and_contact(cur_frm);
		} else {
			frappe.contacts.clear_address_and_contact(cur_frm);
		}
	},
	create_customer: function () {
		frappe.model.open_mapped_doc({
			method: "erpnext.crm.doctype.lead.lead.make_customer",
			frm: cur_frm
		})
	},

	create_opportunity: function () {
		frappe.model.open_mapped_doc({
			method: "erpnext.crm.doctype.lead.lead.make_opportunity",
			frm: cur_frm
		})
	},

	make_quotation: function () {
		frappe.model.open_mapped_doc({
			method: "erpnext.crm.doctype.lead.lead.make_quotation",
			frm: cur_frm
		})
	},

	organization_lead: function () {
		this.frm.toggle_reqd("lead_name", !this.frm.doc.organization_lead);
		this.frm.toggle_reqd("company_name", this.frm.doc.organization_lead);
	},

	company_name: function () {
		if (this.frm.doc.organization_lead == 1) {
			this.frm.set_value("lead_name", this.frm.doc.company_name);
		}
	},

	contact_date: function () {
		if (this.frm.doc.contact_date) {
			let d = moment(this.frm.doc.contact_date);
			d.add(1, "hours");
			this.frm.set_value("ends_on", d.format(frappe.defaultDatetimeFormat));
		}
	},
	create_customer_new : function(){
		var frm = cur_frm;
		console.log(frm.doc)
		frappe.call({
		    method: "customize_crm.hook.lead.createCustomer",
		    args: {lead:frm.doc},
		    callback: function(r) {
		    }
		})

	}
})

$.extend(cur_frm.cscript, new erpnext.LeadController({ frm: cur_frm }));

frappe.ui.form.on('Lead', {
	validate(frm) {
		frm.set_value("mobile_no",frm.doc.mobile_no_0);
	}
});