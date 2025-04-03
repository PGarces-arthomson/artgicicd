from odoo.addons.customer_portal_artg.tools.date_shift import date_shift

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_deliveries(self):
        """
        test
        """
        self.ensure_one()

        pickings = self.picking_ids.filtered(
            lambda x: x.state not in ["draft", "cancel"]
            and (
                x.picking_type_code == "outgoing"
                or (
                    x.picking_type_code == "incoming"
                    and x.location_id.usage == "transit"
                    and x.location_dest_id.usage == "customer"
                )
            )
        )
        deliveries = pickings.filtered(lambda x: x.picking_type_code == "outgoing")

        dropship = pickings.filtered(
            lambda x: x.picking_type_code == "incoming"
        ).move_lines.move_orig_ids.picking_id
        dropship_deliveries = dropship.filtered(
            lambda x: x.state not in ["draft", "cancel"]
            and x.picking_type_code == "outgoing"
        )

        return deliveries + dropship_deliveries


class SalesOrderLine(models.Model):
    _inherit = "sale.order.line"

    def get_latest_delivery_date(self):
        """
        test
        """
        self.ensure_one()
        delivery_date = False
        outgoing_moves = self.move_ids.filtered(
            lambda move: move.picking_id
            and move.picking_id.state not in ["draft", "cancel"]
            and (
                move.picking_id.picking_type_code == "outgoing"
                or (
                    move.picking_id.picking_type_code == "incoming"
                    and move.picking_id.picking_type_code == "incoming"
                    and move.picking_id.location_id.usage == "transit"
                    and move.picking_id.location_dest_id.usage == "customer"
                    and move.picking_id.state not in ["draft", "cancel"]
                )
            )
        )

        if outgoing_moves:
            delivery_date = outgoing_moves.sorted(key=lambda mv: mv.date, reverse=True)[
                0
            ].date.date()

            if delivery_date:
                delivery_date = date_shift(delivery_date)

        return delivery_date
