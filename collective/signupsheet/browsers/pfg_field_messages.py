# -*- condign: utf-8 -*-
from Products.Five.browser import BrowserView
from collective.signupsheet import signupsheetMessageFactory as _
from Acquisition import aq_parent, aq_inner
import zope.i18n


class PfgFieldMessages(BrowserView):

    def user_mailer_subject(self):
        """
        this method return the subject for user's subscription mail
        """

        sstitle = aq_parent(aq_inner(self.context)).Title()
        translator = zope.i18n.translate
        msg = translator(_(u"mailer_registration_subject_overrides",
                           default=u"Your registration for ${title} has been received",
                           mapping={'title': sstitle}),
                        context=self.context.REQUEST,)
        return msg

    def manager_mailer_subject(self):
        """
        this method return the subject for manager's subscription mail
        """
        sstitle = aq_parent(aq_inner(self.context)).Title()
        translator = zope.i18n.translate
        msg = translator(_(u"mailer_registration_subject_overrides_manager",
                           default=u"Notification: New registration for ${title} has been received",
                           mapping={'title': sstitle}),
                        context=self.context.REQUEST)
        return msg
