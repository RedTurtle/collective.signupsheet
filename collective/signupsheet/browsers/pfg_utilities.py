# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from Acquisition import aq_inner, aq_parent
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
from zope.component import getMultiAdapter


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

    def set_registrant_title(self):
        """
        This method create title for registrant object.
        Try to take name and then surname; if we are missing both of them, as
        last try to get email.

        BBB This method need some explanation!
        This view is needed 'cause we want a callable to put in the 'Dynamic title'
        field in FormSaveData2ContentAdapter.

        Following the rules in the registrant workflow from original signupsheet,
        object's owner can't do anything on the registrant object out of the 'new'
        state.

        When we create a new registrant we need to move it from a new state, and
        then a reindex try to update registrant data in the catalog.

        So we need to have this view Public; but in this way we could call it by
        url in the browser and this is bad.

        Trying to secure it I added a check over the authenticator field in the
        form.

        But uwosh.pfg.d2d create registrant using a newSecurityManager, so when
        anonymous subscribe the form, the authenticator token in the form is
        generated considering anonymous user. Due to the new security managers
        the verify method work on a different user, so the verify method return
        false. So in the method I try to validate the authenticator, and if it
        fails, I try to check if the current user (the one used by uwosh) has
        permission to modify the adapter
        """
        authenticator = getMultiAdapter(
                                    (self.context, self.request),
                                    name=u"authenticator"
                                   )
        if not authenticator.verify():
            member = self.context.portal_membership.getAuthenticatedMember()
            adapter = aq_parent(aq_inner(self.context))
            if not member.has_permission('Modify portal content', adapter):
                raise Unauthorized("This method could be called only by the form")
        title = self.context.title
        if title:
            return title
        else:
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
