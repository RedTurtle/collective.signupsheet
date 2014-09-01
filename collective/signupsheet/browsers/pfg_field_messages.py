# -*- condign: utf-8 -*-

from Acquisition import aq_parent, aq_inner
from Products.Five.browser import BrowserView
from collective.signupsheet import signupsheetMessageFactory as _
from zope.i18n import translate


class PfgFieldMessages(BrowserView):
    # TO BE REMOVED

    def user_mailer_subject(self):
        """
        this method return the subject for user's subscription mail
        """
        context = self.context
        sstitle = aq_parent(aq_inner(context)).Title()
        subject = context.getMsg_subject()
        return subject.replace("${title}",sstitle).decode('utf-8')

    def manager_mailer_subject(self):
        """
        this method return the subject for manager's subscription mail
        """
        context = self.context
        sstitle = aq_parent(aq_inner(context)).Title()
        subject = context.getMsg_subject()
        return subject.replace("${title}",sstitle).decode('utf-8')
