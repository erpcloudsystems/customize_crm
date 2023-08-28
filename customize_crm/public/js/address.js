frappe.ui.form.on('Address', {
	refresh(frm) {
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
	}
});