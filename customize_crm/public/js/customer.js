frappe.ui.form.on('Customer', {
	refresh(frm) {
		frm.set_df_property('mobile_no_0',  'reqd', 1);
		frm.set_query('sub_territory', function() {
			return {
				filters: {
					parent_territory: frm.doc.territory,
					enabled: 1
				}
			};
		});

		frm.set_query('territory', function() {
			return {
				filters: {
					enabled: 1,
					is_group: 1
				}
			};
		});	
	},
	territory(frm) {
		frm.set_value('sub_territory','');	
	},
	onload_post_render: function(frm) {
		frm.set_value('reason_for_view','User Did Not Update Notes');
		let d = new frappe.ui.Dialog({
			title: 'Add Comment',
			fields: [
			{
				label: 'Add a reason to view this customer profile',
				fieldname: 'reason',
				fieldtype: 'Small Text',
				reqd: 1,
				description: "(If you do not write any notes here, a note will be written automatically that the <b>" +frappe.session.user+ "</b> did not follow the terms)"
			}
			],
			primary_action_label: 'Submit',
			primary_action(values) {
				frm.set_value('reason_for_view',values.reason);
				frm.save();
			d.hide();
				frm.save();
			}
			});
		d.show();
	},
	after_save(frm) {
		if(frm.doc.create_todo){
		    frm.set_value("date","");
		    frm.set_value("assign_to","");
		    frm.set_value("note","");
		    frm.set_value("create_todo",0);
		    frm.save();
		}
	}
});