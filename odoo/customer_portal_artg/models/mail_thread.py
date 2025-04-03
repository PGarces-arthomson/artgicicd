from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.returns("mail.message", lambda value: value.id)
    def message_post(self, **kwargs):
        """
        test
        """
        if kwargs.get("message_type") == "notification" and self.env.user.share:
            # Prevent notification from Portal User.
            return
        return super().message_post(**kwargs)
