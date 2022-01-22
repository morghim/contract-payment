// Copyright (c) 2021, Ibrahim Morghim and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contract Type', {
	refresh: function(frm) {
		frm.events.create_buttons(frm);
	},
	create_item: function(frm){
		
	},
	create_buttons: function(frm){
		if(!frm.is_new()){
			frm.add_custom_button(__('Make item for invoice'), function(){
				frm.events.create_item(frm);
				
			}, __("Actions"));
		}
		
	},
	create_item: function(frm){
		frm.call({
			doc: frm.doc,
			method: "create_item",
		}).then((r) => {
		});

	},
});
