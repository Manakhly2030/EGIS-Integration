# Copyright (c) 2023, Phamos and contributors
# For license information, please see license.txt

import frappe
import requests, json
from frappe.model.document import Document

class EGISSearchQuery(Document):
	pass

@frappe.whitelist()
def make_request(search_term, search_options, start_row):
	search_options = json.loads(search_options or {})
	print(search_options, type(search_options))
	egis_settings = frappe.get_doc("EGIS Settings")
	endpoint = "{}Artikelstamm/SearchQuery".format(egis_settings.url)

	payload = {
		"SearchTerm": search_term, #"tft",
		"SearchOptions": search_options,
		"Pagination": {
			"StartRow": start_row
		}
	}
	print(payload)

	headers = {
		'accept': '*/*',
		'Ebc-Erp': 'Test ERP',
		'Ebc-Login': egis_settings.user,
		'Ebc-Password': egis_settings.get_password("password"),
		'Content-Type': 'application/json'
	}

	# response = requests.post(endpoint, json=payload, headers=headers)

	# return response.text
	return """{
		"Header": {
			"TotalResults": "6",
			"FirstResult": "3",
			"LastResult": "6"
		},
		"Body": {
			"Item": [
				{
					"ProductIdentification": {
						"ProprietaryProductNumber": "PCS6092716",
						"ProprietaryProductDescription": "BENQ SW270C 68,58cm (27&quot;)",
						"ManufacturerName": {
							"@id": "52",
							"@text": "BENQ"
						},
						"ManufacturerProductNumber": "9H.LHTLB.QBE",
						"GlobalProductNumber": "4718755078392",
						"ProductGroupId": "6704"
					},
					"UnitPrice": {
						"PurchasePrice": "665.90",
						"CurrencyCode": "EUR",
						"DateTime": "2020-01-24T08:21:00",
						"RecommendedRetailPrice": ""
					},
					"ImageUrl": ""
				},
				{
					"ProductIdentification": {
						"ProprietaryProductNumber": "PCS5580690",
						"ProprietaryProductDescription": "BENQ PD2720U 68,6cm (27&quot;)",
						"ManufacturerName": {
						"@id": "52",
						"@text": "BENQ"
						},
						"ManufacturerProductNumber": "9H.LHKLA.TBE",
						"GlobalProductNumber": "4718755076701",
						"ProductGroupId": "6704"
					},
					"UnitPrice": {
						"PurchasePrice": "730.39",
						"CurrencyCode": "EUR",
						"DateTime": "2020-01-24T08:59:00",
						"RecommendedRetailPrice": ""
					},
					"ImageUrl": ""
				},
				{
					"ProductIdentification": {
						"ProprietaryProductNumber": "PCS6092722",
						"ProprietaryProductDescription": "LENOVO Legion Y27gq-25 68,6cm (27&quot;)",
						"ManufacturerName": {
						"@id": "2181",
						"@text": "LENOVO"
						},
						"ManufacturerProductNumber": "65EDGAC1EU",
						"GlobalProductNumber": "0193386422730",
						"ProductGroupId": "6704"
					},
					"UnitPrice": {
						"PurchasePrice": "789.78",
						"CurrencyCode": "EUR",
						"DateTime": "2020-01-24T10:15:00",
						"RecommendedRetailPrice": ""
					},
					"ImageUrl": ""
				}
			]
		}
	}"""
