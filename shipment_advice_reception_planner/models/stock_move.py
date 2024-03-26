# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    origin_purchase = fields.Char(
        compute="_compute_origin_purchase", search="_search_origin_purchase"
    )
    quantity_to_split_wizard = fields.Float(
        string="Split Demand", store=False, readonly=False
    )

    @api.depends("purchase_line_id")
    def _compute_origin_purchase(self):
        for move in self:
            if not move.purchase_line_id:
                move.origin_purchase = False
                continue
            purchase = move.purchase_line_id.order_id
            move.origin_purchase = " ".join(
                [
                    origin
                    for origin in [
                        purchase.name,
                        purchase.requisition_id.name,
                    ]
                    if origin
                ]
            )

    def _search_origin_purchase(self, operator, value):
        purchases = self.env["purchase.order"].search(
            ["|", ("name", operator, value), ("origin", operator, value)]
        )
        return [("purchase_line_id", "in", purchases.order_line.ids)]
