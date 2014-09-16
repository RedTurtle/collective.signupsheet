# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from collective.signupsheet import signupsheetMessageFactory as _
from collective.signupsheet.config import INITIAL_MAIL
from collective.signupsheet.config import MANAGER_MAIL
from collective.signupsheet.interfaces import ISignupSheet
from collective.signupsheet.interfaces import ISignupSheetInitializer
from zope.component import adapts
from zope.interface import implements
from zope.i18n import translate


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
        self.form.setSubmitLabel(translate(
                                    _(u'signupsheet_formfolder_signup',
                                      u'Sign up'),
                                 context=self.form.REQUEST))
        self.form.setResetLabel(translate(
                                    _(u'signupsheet_formfolder_reset',
                                      u'Reset'),
                                 context=self.form.REQUEST))

        oids = self.form.objectIds()
        if not oids:
            form_name = self.form.REQUEST.form.get('title', '').decode('utf-8')
            # create a name field
            self.form.invokeFactory('FormStringField', 'name')

            obj = self.form['name']
            obj.fgField.__name__ = 'name'

            obj.setTitle(translate(
                         _(u'signupsheet_namefield_title', u'Your Name'),
                         context=self.form.REQUEST))
            obj.setFgTDefault('here/@@default_name_value')
            self.form._pfFixup(obj)

            # create a surname field
            self.form.invokeFactory('FormStringField', 'surname')
            obj = self.form['surname']
            obj.fgField.__name__ = 'surname'
            obj.setTitle(translate(
                        _(u'signupsheet_surnamefield_title', u'Your surname'),
                        context=self.form.REQUEST))
            obj.setFgTDefault('here/@@default_surname_value')
            self.form._pfFixup(obj)

            # create a mail field
            self.form.invokeFactory('FormStringField', 'email')
            obj = self.form['email']
            obj.fgField.__name__ = 'email'
            obj.setTitle(translate(
                         _(u'signupsheet_emailfield_title',
                           u'E-Mail Address'),
                          context=self.form.REQUEST))
            obj.fgField.required = True
            obj.setFgTDefault('here/@@default_email_value')
            obj.setFgStringValidator('isEmail')
            self.form._pfFixup(obj)

            #according to FormSaveData2ContentAdapter security seems that only
            #manager can create this kind of adapter
            pt = getToolByName(self.form, 'portal_types')
            type_info = pt.getTypeInfo('FormSaveData2ContentAdapter')
            obj = type_info._constructInstance(self.form, 'registrants')
            # CMFCore compatibility
            if hasattr(type_info, '_finishConstruction'):
                type_info._finishConstruction(obj)
            obj.setTitle(translate(
                         _(u'pfg_registrants_title', u'Registrants'),
                         context=self.form.REQUEST))
            obj.setEntryType('registrant')
            obj.setTitleField('email')
            obj.setNiceIds(True)
            obj.setDynamicTitle("here/@@get_registrant_title")
            self.form._pfFixup(obj)

            #Create first mailer; notification after registration
            self.form.invokeFactory('FormMailerAdapter',
                                    'user_notification_mailer')
            mailer = self.form['user_notification_mailer']
            mailer.setIncludeEmpties(False)
            mailer.setTitle(translate(
                _(u'pfg_user_notification_mailer', u'User notification mailer'),
                context=self.form.REQUEST))
            mailer.setDescription(
                translate(
                  _(u'pfg_user_notification_mailer_description',
                    u'E-Mails Form Input for subscribers'),
                  context=self.form.REQUEST))
            mailer.setTo_field('email')
            mailer.setReplyto_field('email')
            subject = translate(_(u"mailer_registration_subject_overrides",
                                  default=u"Your registration to \"${title}\" has been received",
                                  mapping={'title': form_name}),
                                context=self.form.REQUEST,)
            mailer.setMsg_subject(subject)
            mailer.setExecCondition("request/review_state|nothing")
            mailer.setBody_pt(INITIAL_MAIL % translate(
                               _(u'subscription_mail',
                                 default=u"""<p>
    Thank you for registering to <tal:title tal:replace="here/aq_inner/aq_parent/Title"/>
</p>

<p tal:condition="request/review_state|nothing">Your registration state is:
    <tal:review_state tal:replace="request/review_state" />
</p>

<p>You provided these informations:</p>"""),
                                context=self.form.REQUEST),)
            self.form._pfFixup(mailer)

            #Create second mailer; subscription notification
            self.form.invokeFactory('FormMailerAdapter',
                                    'manager_notification_mailer')
            mailer = self.form['manager_notification_mailer']
            mailer.setIncludeEmpties(False)
            mailer.setTitle(translate(
                _(u'pfg_manager_notification_mailer',
                  u'Manager notification mailer'),
                context=self.form.REQUEST))
            mailer.setDescription(
                translate(
                  _(u'pfg_manager_notification_mailer_description',
                    u'E-Mails Form Input for signup sheet editors: this mailer send notifications to signupsheet managers'),
                  context=self.form.REQUEST))
            mailer.setTo_field('#NONE#')
            mailer.setReplyto_field('#NONE#')
            mailer.setExecCondition("python:context.restrictedTraverse('@@check_mailer')()")
            subject = translate(_(u"mailer_registration_subject_overrides_manager",
                                  default=u"A new registration to \"${title}\" has been received",
                                  mapping={'title': form_name}),
                                context=self.form.REQUEST,)
            mailer.setMsg_subject(subject)
            mailer.setBody_pt(MANAGER_MAIL % translate(
                               _(u'manager_subscription_mail',
                                default=u"""<p>
    New registrant registered to <tal:s tal:content="here/aq_inner/aq_parent/Title" />
</p>

<p>
    Please check current registrants status at:
    <a href="" tal:attributes="href string:${here/aq_inner/aq_parent/absolute_url}/view_registrants"
       tal:content="string:${here/aq_inner/aq_parent/absolute_url}/view_registrants">
    </a>
</p>"""),
                                context=self.form.REQUEST),)
            mailer.setExecCondition("python: here.restrictedTraverse('@@check_manager_mail_form')()")
            self.form._pfFixup(mailer)

            # create a thanks page
            self.form.invokeFactory('FormThanksPage', 'thank-you')
            obj = self.form['thank-you']
            obj.setIncludeEmpties(False)
            obj.setTitle(translate(
                         _(u'pfg_thankyou_title', u'Thank You'),
                         context=self.form.REQUEST))
            obj.setDescription('')
            obj.setThanksPrologue(translate(_(u"thanks_prologue",
                                              default=u"Thank you for registering, we will contact you shortly. <br/>\nYou provided the following information:"),
                                              context=self.form.REQUEST))
            self.form._pfFixup(obj)
            self.form.addActionAdapter('registrants')
            self.form.addActionAdapter('manager_notification_mailer')
            self.form.thanksPage = 'thank-you'
