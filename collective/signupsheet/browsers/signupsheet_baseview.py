# BBB cancella
# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.CMFPlone.i18nl10n import utranslate


class SignupSheetBaseView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getSignupStatus(self, nextstatus=0):
        """Returns the status of the SignupSheet container"""
        status = ''
        event_size = self.context.getEventsize()
        waitlist_size = self.context.getWaitlist_size()
        # BBB non avremo degli oggetti registrant all'interno. Vedere come gestire con d2c
        current_size = len(self.context.contentIds(filter={'portal_type': 'Registrant'}))
        max_size = event_size + waitlist_size

        if current_size + nextstatus <= event_size:
            status = 'open'
        elif max_size - current_size <= waitlist_size:
            status = 'waitlist'

        if current_size >= max_size:
            status = 'full'

        if max_size == 0:
            status = 'open'

        return status

    def getSignupMessage(self):
        """ returns signup message for signupsheet_view """
        if self.getSignupStatus(nextstatus=1) == 'open':
            msg = utranslate(msgid='sign_up',
                             default='Sign up!',
                             context=self,
                             domain="signupsheet")
        else:
            msg = utranslate(msgid='sign_up_for_waitinglist',
                             default='Signup for waiting list',
                             context=self,
                             domain="signupsheet")
        return msg

    def getSeatsLeft(self):
        return self.context.getEventsize() + self.context.getWaitlist_size()
        #BBB togliere gli oggetti già creati - len(self.objectIds())
