
# This module provides features specifically tailored to the
# internal operations and proprietary needs of A.R. Thomson Group Inc.
# It is not intended for public distribution or general use.

# See LICENSE file for full copyright and licensing details.
{
   "name": "ARTG - Customer Portalsss",
   "version": "18.0.0.3.3",
   "summary": "Customer Portal",
   "description": "Customer Portal",
   "author": "A.R. Thomson Group Inc",
   "website": "https://www.arthomson.com/",
   "license": "Other proprietary",
   "category": "A.R. Customization",
   "depends": [
        "sale_stock",
        "purchase",
        "sign",
        "project",
        "hr_timesheet",
        "web_debranding_artg",
        "website_sale",
        ],
   "images": [
        "static/description/banner.gif",
        ],
   "data": [
        "sale_stock",
        "purchase",
        "sign",
        "project",
        "hr_timesheet",
        "web_debranding_artg",
        "website_sale",
        ],
   "assets": {
        "web._assets_primary_variables": [
            "account/static/src/scss/variables.scss",
        ],
        "web.assets_backend": [
            "account/static/src/css/account_bank_and_cash.css",
            "account/static/src/css/account.css",
            "account/static/src/css/tax_totals.css",
            "account/static/src/scss/account_reconciliation.scss",
            "account/static/src/scss/account_journal_dashboard.scss",
            "account/static/src/scss/account_dashboard.scss",
            "account/static/src/scss/account_searchpanel.scss",
            "account/static/src/scss/section_and_note_backend.scss",
            "account/static/src/scss/account_activity.scss",
            "account/static/src/js/account_payment_field.js",
            "account/static/src/js/account_resequence_field.js",
            "account/static/src/js/grouped_view_widget.js",
            "account/static/src/js/mail_activity.js",
            "account/static/src/js/tax_totals.js",
            "account/static/src/js/section_and_note_fields_backend.js",
            "account/static/src/js/tours/account.js",
            "account/static/src/js/bills_upload.js",
            "account/static/src/js/account_selection.js",
        ],
        "web.assets_frontend": [
            "account/static/src/js/account_portal_sidebar.js",
        ],
        "web.assets_tests": [
            "account/static/tests/tours/**/*",
        ],
        "web.assets_qweb": [
            "account/static/src/xml/**/*",
        ],
        },
   "auto_install": False,
   "installable": True,
   "application": False
}
