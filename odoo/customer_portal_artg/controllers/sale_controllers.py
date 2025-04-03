from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.http import request
from odoo.osv.expression import OR

from odoo import _, http


class SalePortal(CustomerPortal):

    def _get_sale_search_domain(self, search_in, search):
        search_domain = []
        if search_in == "so_number":
            search_domain.append([("name", "ilike", search)])

        if search_in == "csr":
            user_ids = (
                request.env["res.users"].sudo().search(["&", ("name", "ilike", search)])
            )
            search_domain.append([("user_id", "in", user_ids.ids)])

        if search_in == "customer_po":
            search_domain.append([("client_order_ref", "ilike", search)])

        return OR(search_domain)

    def _sale_searchbar_inputs(self):
        values = {
            "so_number": {
                "input": "so_number",
                "label": _("Search by SO#"),
                "order": 1,
            },
            "csr": {"input": "csr", "label": _("Search by CSR"), "order": 2},
            "customer_po": {
                "input": "customer_po",
                "label": _("Search by Customer PO"),
                "order": 3,
            },
        }
        return dict(sorted(values.items(), key=lambda item: item[1]["order"]))

    def _prepare_orders_domain(self, partner):
        # IMPORTANT: Do no super this! this is an intentional override!
        # the base method searches for message_partner_ids instead on the
        # partner.
        # issue case: A sales order was assigned to a wrong customer and was
        # assigned to the correct one; the initial creation links the wrong
        # customer to the message followers
        return [
            "|",
            ("partner_id", "child_of", partner.commercial_partner_id.id),
            ("partner_id", "=", partner.commercial_partner_id.id),
            ("state", "in", ["sale", "done"]),
        ]

    @http.route(
        ["/my/orders", "/my/orders/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_orders(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        search=None,
        search_in="customer_po",
        **kw  # # pylint: disable=W0613
    ):
        """
        Test docstring
        """
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        sale_order = request.env["sale.order"]

        domain = self._prepare_orders_domain(partner)

        searchbar_sortings = self._get_sale_searchbar_sortings()
        searchbar_inputs = self._sale_searchbar_inputs()

        # default sortby order
        if not sortby:
            sortby = "date"
        sort_order = searchbar_sortings[sortby]["order"]

        if date_begin and date_end:
            domain += [("date_order", ">=", date_begin), ("date_order", "<=", date_end)]

        # search
        if search and search_in:
            domain += self._get_sale_search_domain(search_in, search)
        # count for pager
        order_count = sale_order.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/orders",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "search_in": search_in,
                "search": search,
            },
            total=order_count,
            page=page,
            step=self._items_per_page,
        )
        # content according to pager
        orders = sale_order.search(
            domain, order=sort_order, limit=self._items_per_page, offset=pager["offset"]
        )

        request.session["my_orders_history"] = orders.ids[:100]

        values.update(
            {
                "date_begin": date_begin,
                "date_end": date_end,
                "orders": orders,
                "page_name": "order",
                "pager": pager,
                "default_url": "/my/orders",
                "searchbar_sortings": searchbar_sortings,
                "searchbar_inputs": searchbar_inputs,
                "sortby": sortby,
                "search_in": search_in,
            }
        )
        return request.render("sale.portal_my_orders", values)

    # def _stock_picking_check_access(self, picking_id, access_token=None):
    #     import pdb; pdb.set_trace()
