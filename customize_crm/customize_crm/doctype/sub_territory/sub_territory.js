// Copyright (c) 2021, Tech Station and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sub Territory', {
	refresh: function(frm) {
		frm.set_query('parent_territory', function() {
			return {
				filters: {
					enabled: 1,
					is_group: 1
				}
			};
		});	
	}
});
