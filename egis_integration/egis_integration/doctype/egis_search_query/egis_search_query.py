# Copyright (c) 2023, Phamos and contributors
# For license information, please see license.txt

import frappe
import requests
from frappe.model.document import Document

class EGISSearchQuery(Document):
	pass

@frappe.whitelist()
def make_request(search_term):
	egis_settings = frappe.get_doc("EGIS Settings")
	endpoint = "{}Artikelstamm/SearchQuery".format(egis_settings.url)

	payload = {
		"SearchTerm": search_term, #"tft",
		"SearchOptions": {
			"OnlyActive": "true",
			"OnlyStocked": "true",
			"OnlyInDescription": "true",
			"MinPrice": "100",
			"MaxPrice": "1000",
			"Sorting": {
				"SortOrder": "asc"
			},
			"DistributorName": ["ALSO"]
		},
		"Pagination": {
			"StartRow": "1"
		}
	}

	headers = {
		'accept': '*/*',
		'Ebc-Erp': 'Test ERP',
		'Ebc-Login': egis_settings.user,
		'Ebc-Password': egis_settings.get_password("password"),
		'Content-Type': 'application/json'
	}

	response = requests.post(endpoint, json=payload, headers=headers)

	return response.text
