# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements

from collective.signupsheet import signupsheetMessageFactory as _
from collective.signupsheet.interfaces import (ISignupSheet,
                                               ISignupSheetInitializer)

import zope.i18n


INITIAL_MAIL = u"""<html xmlns='http://www.w3.org/1999/xhtml'>\r\n\r\n
<head><title></title></head>\r\n\r\n<body>\r\n<p tal:content='here/getBody_pre |nothing' />
\r\n %s \r\n<dl>\r\n<tal:block repeat='field options/wrappedFields | nothing'>\r\n
<dt tal:content='field/fgField/widget/label' />\r\n
<dd tal:content='structure python:field.htmlValue(request)' />\r\n
</tal:block>\r\n</dl>\r\n<p tal:content='here/getBody_post | nothing' />\r\n
<pre tal:content='here/getBody_footer | nothing' />\r\n</body>\r\n</html>
"""
INITIAL_MAIL_MESSAGE = u"""
Thank you for registering to <tal:title tal:replace='here/aq_inner/aq_parent/Title'/>
"""

MANAGER_MAIL = u"""
<html xmlns='http://www.w3.org/1999/xhtml'>\r\n\r\n<head><title></title></head>
\r\n\r\n<body>\r\n %s \n
\r\n</body>\r\n</html>
"""
MANAGER_MAIL_MESSAGE = """
New registrant registered for <tal:s tal:content=\"here/Title\" />
\nPlease check current registrans: <tal:s tal:content=\"string:${here/absolute_url}/view_registrants\" />
"""


class InitializeSignupSheetForm(object):
    adapts(ISignupSheet)
    implements(ISignupSheetInitializer)

    def __init__(self, context):
        self.form = context

    def form_initializer(self, **kwargs):
        """
        The same as PloneformGen do, but we overrides to create objects we
        are interest on: name, surname, status, email
        """
        self.form.setSubmitLabel(zope.i18n.translate(
                                    _(u'signupsheet_formfolder_signup',
                                      u'Sign up'),
                                 context=self.form.REQUEST))
        self.form.setResetLabel(zope.i18n.translate(
                                    _(u'signupsheet_formfolder_reset',
                                      u'Reset'),
                                 context=self.form.REQUEST))

        oids = self.form.objectIds()
        if not oids:
            member = self.form.portal_membership.getAuthenticatedMember()
            # create a name field
            try:
                self.form.invokeFactory('FormStringField', 'name')
            except:
                print self.form
                print self.form.absolute_url()
                print member.__str__

            obj = self.form['name']
            obj.fgField.__name__ = 'name'

            obj.setTitle(zope.i18n.translate(
                         _(u'signupsheet_namefield_title', u'Your Name'),
                         context=self.form.REQUEST))
            self.form._pfFixup(obj)

            # create a surname field
            self.form.invokeFactory('FormStringField', 'surname')
            obj = self.form['surname']
            obj.fgField.__name__ = 'surname'
            obj.setTitle(zope.i18n.translate(
                        _(u'signupsheet_surnamefield_title', u'Your surname'),
                        context=self.form.REQUEST))
            self.form._pfFixup(obj)

            # create a status field
            self.form.invokeFactory('FormSelectionField', 'status')
            obj = self.form['status']
            obj.fgField.__name__ = 'status'
            obj.setTitle(zope.i18n.translate(
                        _(u'signupsheet_statusfield_title', u'Status'),
                        context=self.form.REQUEST))
            obj.setFgVocabulary(('registered|%s' %
                                 zope.i18n.translate(
                                   _(u'signupsheet_statusfield_registered_opt',
                                     u'Registered'),
                                   context=self.form.REQUEST),
                                 'waitinglist|%s' %
                                 zope.i18n.translate(
                                  _(u'signupsheet_statusfield_waitinglist_opt',
                                    u'Waiting list'),
                                    context=self.form.REQUEST)
                                 )
                                )
            obj.setFgFormat('radio')
            self.form._pfFixup(obj)

            # create a mail field
            self.form.invokeFactory('FormStringField', 'email')
            obj = self.form['email']
            obj.fgField.__name__ = 'email'
            obj.setTitle(zope.i18n.translate(
                         _(u'signupsheet_emailfield_title',
                           u'E-Mail Address'),
                          context=self.form.REQUEST))
            obj.fgField.required = True
            obj.setFgStringValidator('isEmail')
            self.form._pfFixup(obj)

            #d2c adapter to save registrant under the form
            self.form.invokeFactory('FormSaveData2ContentAdapter',
                                    'registrants')
            obj = self.form['registrants']
            obj.setTitle(zope.i18n.translate(
                         _(u'pfg_registrants_title', u'Registrants'),
                         context=self.form.REQUEST))
            obj.setEntryType('registrant')
            obj.setTitleField('email')
            obj.setNiceIds(True)
            obj.setDynamicTitle("string:${here/surname} ${here/name}")
            self.form._pfFixup(obj)

            #Create first mailer; notification after registration
            self.form.invokeFactory('FormMailerAdapter', 'user_notification_mailer')
            mailer = self.form['user_notification_mailer']
            mailer.setIncludeEmpties(False)
            mailer.setTitle(zope.i18n.translate(
                _(u'pfg_user_notification_mailer', u'User notification mailer '),
                context=self.form.REQUEST))
            mailer.setDescription(
                zope.i18n.translate(
                  _(u'pfg_user_notification_mailer_description',
                    u'E-Mails Form Input for subscribers'),
                  context=self.form.REQUEST))
            mailer.setTo_field('email')
            mailer.setReplyto_field('email')
            mailer.setSubjectOverride('here/@@user_mailer_subject')
            mailer.setBody_pt(INITIAL_MAIL % zope.i18n.translate(
                               _(u'subscribtion_mail',
                                default=INITIAL_MAIL_MESSAGE,),
                                context=self.form.REQUEST),)
            self.form._pfFixup(mailer)

            #Create second mailer; subscription notification
            self.form.invokeFactory('FormMailerAdapter',
                                    'manager_notification_mailer')
            mailer = self.form['manager_notification_mailer']
            mailer.setIncludeEmpties(False)
            mailer.setTitle(zope.i18n.translate(
                _(u'pfg_manager_notification_mailer',
                  u'Manager notification mailer'),
                context=self.form.REQUEST))
            mailer.setDescription(
                zope.i18n.translate(
                  _(u'pfg_manager_notification_mailer_description',
                    u'E-Mails Form Input for signup sheet editors: this mailer send notifications to signupsheet managers'),
                  context=self.form.REQUEST))
            mailer.setTo_field('#NONE#')
            mailer.setReplyto_field('#NONE#')
            mailer.setExecCondition("python:context.restrictedTraverse('@@check_mailer')()")
            mailer.setSubjectOverride('here/@@manager_mailer_subject')
            mailer.setBody_pt(MANAGER_MAIL % zope.i18n.translate(
                               _(u'manager_subscribtion_mail',
                                default=MANAGER_MAIL_MESSAGE,),
                                context=self.form.REQUEST),)
            mailer.setExecCondition("python: here.restrictedTraverse('@@check_manager_mail_form')()")
            self.form._pfFixup(mailer)

            # create a thanks page
            self.form.invokeFactory('FormThanksPage', 'thank-you')
            obj = self.form['thank-you']
            obj.setIncludeEmpties(False)
            obj.setTitle(zope.i18n.translate(
                         _(u'pfg_thankyou_title', u'Thank You'),
                         context=self.form.REQUEST))
            obj.setDescription('')
            obj.setThanksPrologue(zope.i18n.translate(_(u"thanks_prologue",
                                                        default=u"Thank you for registering, we will contact you shortly. <br/>\nYou provided the following information:"),
                                                        context=self.form.REQUEST))
            self.form._pfFixup(obj)

            self.form.actionAdapter = ('registrants', 'mailer')
            self.form.thanksPage = 'thank-you'
