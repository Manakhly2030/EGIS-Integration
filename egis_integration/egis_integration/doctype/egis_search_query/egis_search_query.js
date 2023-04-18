// Copyright (c) 2023, Phamos and contributors
// For license information, please see license.txt

frappe.ui.form.on('EGIS Search Query', {
	// refresh: function(frm) {
	// 	frappe.db.get_doc("EGIS Settings").then(r => {
	// 		frappe.egis_settings = r
	// 	})
	// },
	make_request: function(frm) {
		frappe.call({
			method: "egis_integration.egis_integration.doctype.egis_search_query.egis_search_query.make_request",
			args: {
				search_term: frm.doc.search_term
			},
			callback: function (r){
				console.log("response", JSON.parse(r.message));
			}
		})
	}
});
