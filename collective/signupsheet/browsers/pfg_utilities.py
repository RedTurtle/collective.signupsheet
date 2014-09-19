# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr


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
    """
    This class is a set of pfg utilities used to get values, default values,
    overrides and so on.
    """

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
        """
        generate the default name for the form field
        """
        mtool = getToolByName(self, 'portal_membership')
        if mtool.isAnonymousUser():
            return ''
        member = mtool.getAuthenticatedMember()
        return self._get_first_last_member_name(member)[0]

    def default_surname_value(self):
        """
        generate the default surnamename for the form field
        """
        mtool = getToolByName(self, 'portal_membership')
        if mtool.isAnonymousUser():
            return ''
        member = mtool.getAuthenticatedMember()
        return self._get_first_last_member_name(member)[1]

    def default_email_value(self):
        """
        get the default email for the form field
        """
        member = getToolByName(self, 'portal_membership').getAuthenticatedMember()
        return member.getProperty('email') or ''


class PfgPublicFormUtilities(BrowserView):

    def get_registrant_title(self):
        """
        This method create title for registrant object.
        Try to take name and then surname; if we are missing both of them, as
        last try to get email.
        """
        if self.context.portal_type == 'registrant':
            fullname = []
            if shasattr(self.context, 'name'):
                fullname.append(self.context.getField('name').get(self.context))
            if shasattr(self.context, 'surname'):
                fullname.append(self.context.getField('surname').get(self.context))
            #If we don't have both name and surname (maybe those field has been
            # deleted) we perform a last try with email. Then will use object id
            #as default title
            if not fullname and shasattr(self.context, 'email'):
                fullname.append(self.context.getField('email').get(self.context))
            return ' '.join(fullname)
