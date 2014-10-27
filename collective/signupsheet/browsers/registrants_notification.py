# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from collective.signupsheet import signupsheetMessageFactory as _
from collective.signupsheet import pmf
from collective.signupsheet.interfaces import IGetRegistrants
from Products.CMFCore.utils import getToolByName
from uwosh.pfg.d2c.interfaces import IFormSaveData2ContentAdapter
from zope.component import getUtility
from zope.i18n import translate


class RegistrantNotificationView(BrowserView):
    """View for sending email to registrants"""
    
    def __init__(self, context, request):
        super(RegistrantNotificationView, self).__init__(context, request)
        self.errors = {}
    
    def __call__(self, *args, **kwargs):
        if 'form.submitted' in self.request.form.keys():
            self._notify(self.request.form)
        if self.errors:
            plone_utils = getToolByName(self.context, 'plone_utils')
            plone_utils.addPortalMessage(pmf('Please correct the indicated errors.'),
                                         type="error")
        return self.index()
    
    def _notify(self, form):
        context = self.context
        request = self.request
        registrants = form.get('registrants', [])
        subject = form.get('subject', None)
        message = form.get('message', None)
        
        if not registrants:
            self.errors['registrants'] = translate(_('registrants_required',
                                                     default=u"Please, provide at least one registrants"),
                                                   context=request)
        if not subject:
            self.errors['subject'] = translate(_('subject_required',
                                                     default=u"Subject is required. Please provide it"),
                                               context=request)
        if not message:
            self.errors['message'] = translate(_('message_required',
                                                     default=u"Message is required. Please provide it"),
                                               context=request)

        if self.errors:
            return

        parsedMessage = self._parseMessage(message)
        mail_host = getToolByName(context, 'MailHost')
        catalog = getToolByName(context, 'portal_catalog')
        portal = getToolByName(context, 'portal_url').getPortalObject()
        storage = catalog(path='/'.join(context.getPhysicalPath()),
                          object_provides=IFormSaveData2ContentAdapter.__identifier__)
        mailer = getattr(context, 'user_notification_mailer', None)
        mfrom = mailer and mailer.getRecipient_email() or portal.getProperty('email_from_address')
        storage = storage[0].getObject()
        cnt = 0
        for registrant in registrants:
            email = getattr(getattr(storage, registrant, None), 'email', None)
            if email:
                mail_host.secureSend(parsedMessage, mto=email, mfrom=mfrom, subject=subject)
                cnt += 1
        plone_utils = getToolByName(self.context, 'plone_utils')
        plone_utils.addPortalMessage(_('sent_notification_count',
                                       default=u"Message sent to $count registrants",
                                       mapping={'count': cnt}))

    def _parseMessage(self, message):
        context = self.context
        message = message.replace('$title', context.Title())
        message = message.replace('$url', context.absolute_url())
        return message

    def registrants(self):
        utility = getUtility(IGetRegistrants)
        wtool = getToolByName(self.context, 'portal_workflow')
        registrants = utility.get_registrants(self.context)
        results = []
        for registrant in registrants:
            data = dict(id=registrant.id,
                        name=registrant.title_or_id(),
                        email=registrant.email,
                        review_state=wtool.getInfoFor(registrant, 'review_state'))
            results.append(data)
        return results
