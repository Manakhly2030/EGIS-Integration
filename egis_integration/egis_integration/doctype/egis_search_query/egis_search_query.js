// Copyright (c) 2023, Phamos and contributors
// For license information, please see license.txt

frappe.ui.form.on('EGIS Search Query', {
	refresh: function(frm) {
		// frappe.db.get_doc("EGIS Settings").then(r => {
		// 	frappe.egis_settings = r
		// })
		frm.disable_save();
		frm.set_value("start_row", 1)
	},
	make_request: function(frm) {
		var search_options = get_search_options(frm)

		//validate input
		if (!(Object.keys(search_options).indexOf("ProductGroupId") >= 0 && search_options.ProductGroupId.length == 1)){
			if (frm.doc.search_term.length < 2){
				frappe.msgprint("Search Term must contain at least two characters.", "Invalid input")
				return
			}
		}

		frappe.call({
			method: "egis_integration.egis_integration.doctype.egis_search_query.egis_search_query.make_request",
			args: {
				search_term: frm.doc.search_term,
				search_options: search_options,
				start_row: frm.doc.start_row
			},
			callback: function (r){
				var response = JSON.parse(r.message.replace("&quot;", "'"))
				console.log("response", response);
				if (Object.keys(response).indexOf("ErrorMessage") > 0){
					frappe.msgprint(`An error has occurred:\n${JSON.stringify(response)}`, "Error")
				} else {
					response.Body.Item.forEach(item => {
						var new_row = frm.add_child('response');
						new_row.proprietary_product_number = item.ProductIdentification.ProprietaryProductNumber
						new_row.proprietary_product_description = item.ProductIdentification.ProprietaryProductDescription
						new_row.manufacturer_id = item.ProductIdentification.ManufacturerName["@id"]
						new_row.manufacturer_name = item.ProductIdentification.ManufacturerName["@text"]
						new_row.manufacturer_product_number = item.ProductIdentification.ManufacturerProductNumber
						new_row.global_product_number = item.ProductIdentification.GlobalProductNumber
						new_row.product_group_id = item.ProductIdentification.ProductGroupId
						new_row.purchase_price = item.UnitPrice.PurchasePrice
						new_row.currency_code = item.UnitPrice.CurrencyCode
						new_row.datetime = item.UnitPrice.DateTime
						new_row.recommended_retail_price = item.UnitPrice.RecommendedRetailPrice
						new_row.image_url = item.ImageUrl
					});
					frm.refresh_field('response');
				}
			}
		})
	},
});

var get_search_options = function(frm){
	var search_options = {}
	if (frm.doc.only_active){
		search_options.OnlyActive = frm.doc.only_active
	}
	if (frm.doc.only_stocked){
		search_options.OnlyStocked = frm.doc.only_stocked
	}
	if (frm.doc.only_in_description){
		search_options.MinPrice = frm.doc.only_in_description
	}
	if (frm.doc.min_price){
		search_options.MinPrice = frm.doc.min_price
	}
	if (frm.doc.max_price){
		search_options.MaxPrice = frm.doc.max_price
	}
	if (frm.doc.sort_order){
		search_options.Sorting = {
			"SortOrder": frm.doc.sort_order
		}
	}
	if (frm.doc.distributor_name){
		search_options.DistributorName = frm.doc.distributor_name.split(",").map((e) => e.trim()) 
	}
	if (frm.doc.manufacturer_name){
		search_options.ManufacturerName = frm.doc.manufacturer_name.split(",").map((e) => e.trim()) 
	}
	if (frm.doc.product_group_id){
		search_options.ProductGroupId = frm.doc.product_group_id.split(",").map((e) => e.trim()) 
	}
	return search_options
}