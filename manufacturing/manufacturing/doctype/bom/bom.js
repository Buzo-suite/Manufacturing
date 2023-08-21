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
	item: function(frm) {
		console.log("Hello");
		frm.fields_dict['items'].grid.get_field('item').get_query = function(doc, cdt, cdn) {
            var d = frm.doc.item;
			var existing_items = [];

            $.each(doc.items || [], function(i, item) {
               if (item.item !== d) {
                  existing_items.push(item.item);
            }
        });
            return {
                filters: [
                    ['Item', 'name', '!=', d],
					['Item', 'name', 'not in', existing_items]
                ]
            };
        };
    }
});

frappe.ui.form.on("BOM Item","qty",(frm,cdt,cdn)=>{
	let child_table = locals[cdt][cdn];
	let calculate_amount = flt(child_table.qty * child_table.rate);
	//console.log('hello',child_table.qty * child_table.rate);
	child_table.amount = calculate_amount;
	frm.refresh_field('amount');
});
