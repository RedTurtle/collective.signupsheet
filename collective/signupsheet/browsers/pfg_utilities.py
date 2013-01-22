# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName


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


class PfgFormUtilities(BrowserView):

    perm_view_reg_info = "SignupSheet: View Registration Info"

    def check_state_field_is_visible(self):
        pm = getToolByName(self.context, 'portal_membership')
        member = pm.getAuthenticatedMember()
        return member.has_permission(self.perm_view_reg_info, self.context)

    def _get_first_last_member_name(self, member):
        """
        Obtain the first/last member name
        """
        fullname = member.getProperty('fullname') or member.getId() or ''
        elements = fullname.split()

        if len(elements) == 1:
            return (elements[0], '')
        if len(elements) == 2:
            return (elements[0], elements[1])
        return ('', '')

    def default_name_value(self):
        mtool = getToolByName(self, 'portal_membership')
        if mtool.isAnonymousUser():
            return ''
        member = mtool.getAuthenticatedMember()
        return self._get_first_last_member_name(member)[0]

    def default_surname_value(self):
        mtool = getToolByName(self, 'portal_membership')
        if mtool.isAnonymousUser():
            return ''
        member = mtool.getAuthenticatedMember()
        return self._get_first_last_member_name(member)[1]

    def default_email_value(self):
        member = getToolByName(self, 'portal_membership').getAuthenticatedMember()
        return member.getProperty('email') or ''
