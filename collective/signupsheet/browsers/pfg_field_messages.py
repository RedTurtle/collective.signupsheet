# -*- condign: utf-8 -*-

from Acquisition import aq_parent, aq_inner
from Products.Five.browser import BrowserView
from collective.signupsheet import signupsheetMessageFactory as _
from zope.i18n import translate


class PfgFieldMessages(BrowserView):

    def user_mailer_subject(self):
        """
        this method return the subject for user's subscription mail
        """
        context = self.context
        sstitle = aq_parent(aq_inner(context)).Title()
        return translate(_(u"mailer_registration_subject_overrides",
                           default=u"Your registration for ${title} has been received",
                           mapping={'title': sstitle.decode('utf-8')}),
                         context=context.REQUEST,)

    def manager_mailer_subject(self):
        """
        this method return the subject for manager's subscription mail
        """
        context = self.context
        sstitle = aq_parent(aq_inner(context)).Title()
        return translate(_(u"mailer_registration_subject_overrides_manager",
                           default=u"Notification: New registration for ${title} has been received",
                           mapping={'title': sstitle.decode('utf-8')}),
                         context=context.REQUEST)
