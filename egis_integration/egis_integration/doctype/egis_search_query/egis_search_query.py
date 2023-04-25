# Copyright (c) 2023, Phamos and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
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

	response = requests.post(endpoint, json=payload, headers=headers)

	response = response.text
	# response = """{
	# 	"Header": {
	# 		"TotalResults": "6",
	# 		"FirstResult": "3",
	# 		"LastResult": "6"
	# 	},
	# 	"Body": {
	# 		"Item": [
	# 			{
	# 				"ProductIdentification": {
	# 					"ProprietaryProductNumber": "PCS6092716",
	# 					"ProprietaryProductDescription": "BENQ SW270C 68,58cm (27&quot;)",
	# 					"ManufacturerName": {
	# 						"@id": "52",
	# 						"@text": "BENQ"
	# 					},
	# 					"ManufacturerProductNumber": "9H.LHTLB.QBE",
	# 					"GlobalProductNumber": "4718755078392",
	# 					"ProductGroupId": "6704"
	# 				},
	# 				"UnitPrice": {
	# 					"PurchasePrice": "665.90",
	# 					"CurrencyCode": "EUR",
	# 					"DateTime": "2020-01-24T08:21:00",
	# 					"RecommendedRetailPrice": ""
	# 				},
	# 				"ImageUrl": ""
	# 			},
	# 			{
	# 				"ProductIdentification": {
	# 					"ProprietaryProductNumber": "PCS5580690",
	# 					"ProprietaryProductDescription": "BENQ PD2720U 68,6cm (27&quot;)",
	# 					"ManufacturerName": {
	# 					"@id": "52",
	# 					"@text": "BENQ"
	# 					},
	# 					"ManufacturerProductNumber": "9H.LHKLA.TBE",
	# 					"GlobalProductNumber": "4718755076701",
	# 					"ProductGroupId": "6704"
	# 				},
	# 				"UnitPrice": {
	# 					"PurchasePrice": "730.39",
	# 					"CurrencyCode": "EUR",
	# 					"DateTime": "2020-01-24T08:59:00",
	# 					"RecommendedRetailPrice": ""
	# 				},
	# 				"ImageUrl": ""
	# 			},
	# 			{
	# 				"ProductIdentification": {
	# 					"ProprietaryProductNumber": "PCS6092722",
	# 					"ProprietaryProductDescription": "LENOVO Legion Y27gq-25 68,6cm (27&quot;)",
	# 					"ManufacturerName": {
	# 					"@id": "2181",
	# 					"@text": "LENOVO"
	# 					},
	# 					"ManufacturerProductNumber": "65EDGAC1EU",
	# 					"GlobalProductNumber": "0193386422730",
	# 					"ProductGroupId": "6704"
	# 				},
	# 				"UnitPrice": {
	# 					"PurchasePrice": "789.78",
	# 					"CurrencyCode": "EUR",
	# 					"DateTime": "2020-01-24T10:15:00",
	# 					"RecommendedRetailPrice": ""
	# 				},
	# 				"ImageUrl": ""
	# 			}
	# 		]
	# 	}
	# }"""

	response_json = json.loads(response)
	for item in response_json["Body"]["Item"]:
		item_code = item["ProductIdentification"]["ProprietaryProductNumber"]
		item_exists = 0
		if frappe.db.exists("Item", item_code):
			item_exists = 1
		item["item_exists"] = item_exists

	return json.dumps(response_json)

@frappe.whitelist()
def import_items(items):
	items = json.loads(items)
	for item in items:
		brand = item.get("manufacturer_name")
		if not frappe.db.exists("Brand", brand):
			brand = frappe.get_doc({
				"doctype": "Brand",
				"brand": brand,
				"id": item.get("manufacturer_id")
			})
			brand.insert()
		item_group = item.get("product_group_id")
		if not frappe.db.exists("Item Group", item_group):
			item_group = frappe.get_doc({
				"doctype": "Item Group",
				"parent_item_group": "EGIS", #TODO: this should be better
				"item_group_name": item_group
			})
			item_group.insert()
			item_group = item_group.name
		item_doc = frappe.new_doc("Item")
		item_doc.item_code = item.get("proprietary_product_number")
		item_doc.item_name = item.get("proprietary_product_description")
		item_doc.description = item.get("proprietary_product_description")
		item_doc.item_group = item_group
		item_doc.brand = item.get("manufacturer_name")
		item_doc.manufacturer_product_number = item.get("manufacturer_product_number")
		item_doc.global_product_number = item.get("global_product_number")
		item_doc.website_image = item.get("image_url")
		if item.get("recommended_retail_price"):
			item_doc.standard_rate = flt(item.get("recommended_retail_price"))
		item_doc.default_currency = item.get("currency_code")
		item_doc.save()

		if item.get("purchase_price"):
			frappe.get_doc({
				"doctype": "Item Price",
				"item_code": item_doc.name,
				"price_list": "Standard Buying", # TODO maybe we should have this set on EGIS Settings
				"price_list_rate": flt(item.get("purchase_price"))
			}).insert()