frappe.listview_settings['Lead'] = {
	onload: function(listview) {
		// if(frappe.user.has_role("System Manager")){
		//    listview.page.add_menu_item(__("Migrate Changes With Old App"), function() {
		// 	frappe.confirm(
		// 			'It will take some time to Refelect. Are You Sure ?',
		// 			function(){
		// 						frappe.call({
		// 							method: "customize_crm.hook.lead.migrate",
		// 							callback: function(r) {
		// 									console.log(r)
	 	// 									   frappe.msgprint("Migrated Successfully")
		// 									}
		// 							});
		// 					},
		// 			function(){
		// 						show_alert('Thanks!')
		// 					}
		// 	)
		//   })
		// }
		// if(frappe.user.has_role("System Manager")){
		//    listview.page.add_menu_item(__("Check Number Converted"), function() {
		// 	frappe.confirm(
		// 			'That it takes some time should not implement any other operation before the end of examination and treatment',
		// 			function(){
		// 						frappe.call({
		// 							method: "customize_crm.hook.lead.convert_numbers",
		// 							callback: function(r) {
	 	// 									   frappe.msgprint("Lead Converted Successfully")
		// 									}
		// 							});
		// 					},
		// 			function(){
		// 						show_alert('Thanks for continue here!')
		// 					}
		// 	)
		//   })
		// }
		listview.page.add_menu_item(__("Search Customer/Lead"), function() {
			var d = new frappe.ui.Dialog({
					'title':"Advanced Lead Search",
					'fields': [

								{
									'fieldname': 'search_type',
									'fieldtype': 'Select',
									'options':'Phone\nIdentification\nPassport',
									'label': __('Search Type')
								},
								{
									'fieldname': 'search_data',
									'fieldtype': 'Data',
									'label': __('Search Data')
								},
								{
									'fieldname': 'search',
									'fieldtype':'Button',
									'label': __('Search'),
							click: () => {
									let search_type = d.fields_dict.search_type.value;
									let search_data = d.fields_dict.search_data.value;
									frappe.call({
										method: "customize_crm.hook.lead.get_search_data",
										args: {
											search_type:search_type,
											search_data:search_data,
										},
										callback: function(r) {
	 										   if (!r.exc) {
											console.log(r)
													var batches = d.fields_dict.batches;
											if(batches) {
												batches.grid.df.data = r.message.result;
												batches.grid.refresh();
											}
									   }
									}
								});
							}
						},
								{'fieldname': 'break','fieldtype':'Section Break','label': __('Results')},
								{'fieldname': 'batches', 'fieldtype': 'Table', 'label': __('Customer Details'),
							fields: [
									{
										'fieldtype': 'Link',
										'read_only': 1,
										'fieldname': 'document_type',
										'label': __('Doctype'),
										'options':'DocType'
									},
									{
										'fieldtype': 'Dynamic Link',
										'fieldname': 'customer',
										'label': __('Customer'),
										'in_list_view': 1,
										'options':'document_type',
										'read_only':1
									},
									{
										'fieldtype': 'Link',
										'read_only': 1,
										'fieldname': 'company',
										'label': __('Company'),
										'in_list_view': 1,
									}
								],
								in_place_edit: true,
								data: [{'idx':1,'customer':'','company':''}],
								get_data: function () {
								return this.data;
						},
				}
			],
		});
			d.show();
		});
	}
};