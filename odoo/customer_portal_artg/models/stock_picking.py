from odoo.addons.customer_portal_artg.tools.date_shift import date_shift

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def get_shifted_date(self, scheduled_date=None):
        """
        test
        """
        scheduled_date = scheduled_date and scheduled_date or self.scheduled_date.date()
        if scheduled_date:
            scheduled_date = date_shift(scheduled_date)
        return scheduled_date
