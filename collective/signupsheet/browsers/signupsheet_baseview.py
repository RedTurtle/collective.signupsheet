# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import getUtility
from collective.signupsheet.interfaces import IGetRegistrants
from collective.signupsheet import signupsheetMessageFactory as _
from collective.signupsheet import config
from AccessControl import getSecurityManager


class SignupSheetBaseView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getSignupStatus(self, nextstatus=0):
        """Returns the status of the SignupSheet container"""
        status = ''
        event_size = self.context.getEventsize()
        waitlist_size = self.context.getWaitlist_size()
        utility = getUtility(IGetRegistrants)
        registrant_folder = utility.get_registrants_folder(self.context)
        if registrant_folder == []:
            current_size = 0
        else:
            current_size = len(registrant_folder.contentIds(filter={'portal_type': 'registrant'}))
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
            msg = _(u'sign_up', default='Sign up!')
        else:
            msg = _(u'sign_up_for_waitinglist', default='Signup for waiting list')
        return msg

    def getSeatsLeft(self):
        registrants = getUtility(IGetRegistrants).get_registrants_brains_anon
        registrants_number = len((registrants(self.context)))
        return self.context.getEventsize() + \
               self.context.getWaitlist_size() - \
               registrants_number

    def check_deadline(self):
        deadline = self.context.getRegistrationDeadline()
        if not deadline:
            return True
        now = DateTime()
        return now < deadline

    def can_subscribe(self):
        """
        Check if subscription is possibile, checking all the logic
        """
        context = self.context
        wtool = getToolByName(context, 'portal_workflow')
        wf_state = wtool.getInfoFor(context, 'review_state')
        if not self.check_deadline():
            return False
        return wf_state in ('earlybird', 'open') or \
               (wf_state=='closed' and self.check_add_registrants_permission())

    def check_add_registrants_permission(self):
        """
        check if you have the permission to create registrants
        """
        sm = getSecurityManager()
        return sm.checkPermission(config.ADD_PERMISSIONS['SignupSheet'], self.context)

    def check_duplicate_registrant(self, form_fields):
        """
        check if the submitted data are already stored in the db
        """
        registrants = getUtility(IGetRegistrants).get_registrants_brains_anon
        registrants = registrants(self.context)
        fields = [x for x in self.context.fgFieldsDisplayList()]
        tot_fields = len(fields)
        for registrant in registrants:
            # I need to do an unrestrictedTraverse because otherwise anonymous
            # users can't get saved registrants
            registrant_obj = self.context.unrestrictedTraverse(
                registrant.getPath())
	    if 'email' in fields:
	        if  str(getattr(registrant_obj, 'email', None)).strip() == str(form_fields.get('email', None)).strip():
                    return True
	    else:
                match = [x for x in fields if str(getattr(registrant_obj, x, None)).strip() == str(form_fields.get(x, None)).strip()]
                if len(match) == tot_fields:
                    return True
        return False
