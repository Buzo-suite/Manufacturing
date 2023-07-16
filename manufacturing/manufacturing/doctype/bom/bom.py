# Copyright (c) 2023, Buzosuite and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class BOM(Document):

	def autoname(self):
		# ignore amended documents while calculating current index
		existing_boms = frappe.get_all(
			"BOM", filters={"item": self.item, "amended_from": ["is", "not set"]}, pluck="name"
		)

		if existing_boms:
			index = self.get_next_version_index(existing_boms)
		else:
			index = 1

		prefix = self.doctype
		suffix = "%.3i" % index  # convert index to string (1 -> "001")
		bom_name = f"{prefix}-{self.item}-{suffix}"

		if len(bom_name) <= 140:
			name = bom_name
		else:
			# since max characters for name is 140, remove enough characters from the
			# item name to fit the prefix, suffix and the separators
			truncated_length = 140 - (len(prefix) + len(suffix) + 2)
			truncated_item_name = self.item[:truncated_length]
			# if a partial word is found after truncate, remove the extra characters
			truncated_item_name = truncated_item_name.rsplit(" ", 1)[0]
			name = f"{prefix}-{truncated_item_name}-{suffix}"

		if frappe.db.exists("BOM", name):
			conflicting_bom = frappe.get_doc("BOM", name)

			if conflicting_bom.item != self.item:
				msg = _("A BOM with name {0} already exists for item {1}.").format(
					frappe.bold(name), frappe.bold(conflicting_bom.item)
				)

				frappe.throw(
					_("{0}{1} Did you rename the item? Please contact Administrator / Tech support").format(
						msg, "<br>"
					)
				)

		self.name = name

	def validate(self):
		self.route = frappe.scrub(self.name).replace("_", "-")

		self.update_stock_uom()

	def update_stock_uom(self):

		for m in self.get("items"):

			if m.uom and m.stock_uom:
				m.uom = 2
				m.qty = 2

	# @staticmethod
	# def get_next_version_index(existing_boms: List[str]) -> int:
	# 	# split by "/" and "-"
	# 	delimiters = ["/", "-"]
	# 	pattern = "|".join(map(re.escape, delimiters))
	# 	bom_parts = [re.split(pattern, bom_name) for bom_name in existing_boms]

	# 	# filter out BOMs that do not follow the following formats: BOM/ITEM/001, BOM-ITEM-001
	# 	valid_bom_parts = list(filter(lambda x: len(x) > 1 and x[-1], bom_parts))

	# 	# extract the current index from the BOM parts
	# 	if valid_bom_parts:
	# 		# handle cancelled and submitted documents
	# 		indexes = [cint(part[-1]) for part in valid_bom_parts]
	# 		index = max(indexes) + 1
	# 	else:
	# 		index = 1

	# 	return index				