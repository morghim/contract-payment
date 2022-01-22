// Copyright (c) 2021, Ibrahim Morghim and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contract', {
	refresh: function(frm) {
		frm.events.create_buttons(frm);
		frm.events.create_sale_invoice_button(frm);
		frm.events.create_purchase_invoice_button(frm);
		frm.events.create_salary_slip_button(frm);
		frm.events.make_qurey(frm);


	},
	create_item: function(frm){
		
	},
	create_buttons: function(frm){
		if(!frm.is_new() && frm.doc.contract_payment){
            console.log("is created button");
			frm.add_custom_button(__('Calculate Benfites'), function(){
				frm.events.calculate_benfites(frm);
			},
			
			__("Actions"));
		}
		
	},
    calculate_benfites: function(frm){
        frm.call({
            doc: frm.doc,
            method: "calculate_dues",
        }).then((r) => {
        });
    },
    contract_payment: function(frm){
        frm.refresh()
    },
	create_sale_invoice_button: function(frm){
		if(!frm.is_new() && frm.doc.contract_payment && frm.doc.docstatus === 1){

		if(frm.doc.party_type === 'Customer'){
			frm.add_custom_button(__('Create Sale Invoice'), function(){
				frm.events.create_invoice(frm);
			},
			
			__("Actions"));
		}
	}
	},
	create_invoice: function(frm){
		frm.call({
            doc: frm.doc,
            method: "create_sales_invoice",
        }).then((r) => {
        });
	},
	party_type: function(frm){
		frm.refresh()
	},
	create_purchase_invoice_button: function(frm){
		if(!frm.is_new() && frm.doc.contract_payment && frm.doc.docstatus === 1){

			if(frm.doc.party_type === 'Supplier'){
				frm.add_custom_button(__('Create Purchase Invoice'), function(){
					frm.events.create_purchase_invoice(frm);
				},
				
				__("Actions"));
			}
		}

	},
	create_purchase_invoice: function(frm){
		frm.call({
            doc: frm.doc,
            method: "create_purchase_invoice",
        }).then((r) => {
        });

	},
	create_salary_slip_button: function(frm){
		if(!frm.is_new() && frm.doc.contract_payment && frm.doc.docstatus === 1){

			if(frm.doc.party_type === 'Employee'){
				frm.add_custom_button(__('Create Salary Slip'), function(){
					frm.events.create_salary_slip(frm);
				},
				
				__("Actions"));
			}
		}



	},
	create_salary_slip: function(frm){

		frm.call({
            doc: frm.doc,
            method: "create_salary_slips",
        }).then((r) => {
        });



	},
	make_qurey: function(frm){
		if(frm.doc.contract_payment){

			frm.set_query("party_name", function() {
				return {
					filters: {
						"is_contract_payment": 1
					}
				};
			});

		}
		else{
			frm.set_query("party_name", function() {
				return {
					filters: {
					}
				};
			});

		}
	
	}


});
