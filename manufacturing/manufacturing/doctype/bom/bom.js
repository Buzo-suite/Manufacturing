// Copyright (c) 2023, Buzosuite and contributors
// For license information, please see license.txt

frappe.ui.form.on("BOM", {
	refresh(frm) {
        frm.set_query('item', (doc)=>{
			return{
				filters: {
					"item_group": "Finished-product"
				}
			}
		})
	},
});

frappe.ui.form.on("BOM Item","qty",(frm,cdt,cdn)=>{
	let child_table = locals[cdt][cdn];
	let calculate_amount = flt(child_table.qty * child_table.rate);
	console.log('hello',child_table.qty * child_table.rate);
	child_table.amount = calculate_amount;
	frm.refresh_field('amount');
});
