# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView


class ChecksManagerMailerSendAction(BrowserView):

    def __call__(self):
        """
        We need to send notification mail to signup sheet 'managers' only if
        some address is specified in the mailer.
        We want just check if managers has set the field. If they fill it
        wrongly PFG will follow it's standard behaviour.
        """
        recipient = self.context.getRecipient_email()
        #just strip the string 'cause bool(' ') return True
        recipient.strip()
        if recipient:
            return True
        return False
