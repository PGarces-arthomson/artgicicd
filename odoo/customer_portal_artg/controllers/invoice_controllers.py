from collections import OrderedDict

from odoo.addons.account.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.http import request
from odoo.osv.expression import OR

from odoo import _, http


class InvoicePortal(CustomerPortal):

    def _get_invoice_search_domain(self, search_in, search):
        """
        asdasd
        """
        search_domain = []
        if search_in == "inv_number":
            search_domain.append([("name", "ilike", search)])

        if search_in == "csr":
            user_ids = (
                request.env["res.users"].sudo().search([("name", "ilike", search)])
            )
            search_domain.append([("user_id", "in", user_ids.ids)])

        if search_in == "customer_po":
            search_domain.append([("ref", "ilike", search)])

        return OR(search_domain)

    def _invoice_searchbar_inputs(self):
        """
        asdasd
        """
        values = {
            "inv_number": {
                "input": "inv_number",
                "label": _("Search by INV #"),
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

    @http.route(
        ["/my/invoices", "/my/invoices/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_invoices(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="customer_po",
        **kw  # pylint: disable=W0613
    ):
        """
        asdasd
        """

        values = self._prepare_portal_layout_values()
        invoice = request.env["account.move"]
        domain = self._get_invoices_domain()

        searchbar_inputs = self._invoice_searchbar_inputs()
        searchbar_sortings = {
            "date": {"label": _("Date"), "order": "invoice_date desc"},
            "duedate": {"label": _("Due Date"), "order": "invoice_date_due desc"},
            "name": {"label": _("Reference"), "order": "name desc"},
            "state": {"label": _("Status"), "order": "state"},
        }
        # default sort by order
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]

        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
            "invoices": {
                "label": _("Invoices"),
                "domain": [("move_type", "in", ("out_invoice", "out_refund"))],
            },
            "bills": {
                "label": _("Bills"),
                "domain": [("move_type", "in", ("in_invoice", "in_refund"))],
            },
        }
        # default filter by value
        if not filterby:
            filterby = "all"
        domain += searchbar_filters[filterby]["domain"]

        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]

        # search
        if search and search_in:
            domain += self._get_invoice_search_domain(search_in, search)

        # count for pager
        invoice_count = invoice.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/invoices",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "search_in": search_in,
                "search": search,
            },
            total=invoice_count,
            page=page,
            step=self._items_per_page,
        )
        # content according to pager and archive selected
        invoices = invoice.search(
            domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )
        request.session["my_invoices_history"] = invoices.ids[:100]

        sorted_searchbar_filters = OrderedDict(sorted(searchbar_filters.items()))
        values.update(
            {
                "date_begin": date_begin,
                "date_end": date_end,
                "invoices": invoices,
                "page_name": "invoice",
                "pager": pager,
                "default_url": "/my/invoices",
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
                "searchbar_filters": sorted_searchbar_filters,
                "filterby": filterby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
            }
        )
        return request.render("account.portal_my_invoices", values)
