# -*- coding: utf-8 -*-

from Products.Archetypes.atapi import (IntegerField, StringWidget,
                                       BooleanField, BooleanWidget,
                                       DateTimeField, CalendarWidget,
                                       TextField, RichWidget,
                                       Schema)
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.folder import ATFolder
from Products.PloneFormGen.content.form import (FormFolder,
                                                FormFolderSchema)

from zope.interface import implements

from collective.signupsheet import signupsheetMessageFactory as _
from collective.signupsheet.config import PROJECTNAME
from collective.signupsheet.interfaces import ISignupSheet

import zope.i18n


# BBB Permessi per la lettura dei dati??
SignupSheetSchema = FormFolderSchema.copy() + Schema((
    IntegerField('eventsize',
        required=1,
        default=0,
        #read_permission="SignupSheet: View Registration Info",
        validators=('isInt',),
        widget=StringWidget(
            visible={'edit': 'visible', 'view': 'invisible'},
            size=6,
            label=_('field_eventsize',
                    default=u'Number of registrants'),
            description=_('fieldhelp_eventsize',
                          default=u"Set to 0 for unlimited registration",)
             )
        ),
    IntegerField('waitlist_size',
        required=1,
        default=0,
        #read_permission="SignupSheet: View Registration Info",
        validators=('isInt',),
        widget=StringWidget(
            visible={'edit': 'visible', 'view': 'invisible'},
            size=6,
            label=_('field_waitlist_size',
                    default=u'Size of wait list',),
            description=_('fieldhelp_waitlist_size',
                          default=u""),
            )
        ),
    BooleanField('display_size_left',
        default=False,
        widget=BooleanWidget(
            visible={'edit': 'visible', 'view': 'invisible'},
            label=_('field_display_size_left', default=u'Display seats left'),
            description=_('fieldhelp_display_size_left',
                          default=u"Choose to show in the subscription page the number of seats left",)
            )
        ),
    DateTimeField('earlyBirdDate',
        required=0,
        default=None,
        #read_permission="SignupSheet: View Thank You",
        widget=CalendarWidget(
            label=_('field_early_bird_phase', default=u"Early bird phase until"),
            description=_("fieldhelp_early_bird_phase", default=u""),
            visible={'edit': 'visible', 'view': 'invisible'},
            size=6,
            )
        ),
    DateTimeField('registrationDeadline',
        required=0,
        default=None,
        #read_permission="SignupSheet: View Thank You",
        widget=CalendarWidget(
            label=_('field_registration_deadline',
                    default=u'Registration deadline'),
            description=_("fieldhelp_registration_deadline", default=u""),
            visible={'edit': 'visible', 'view': 'invisible'},
            size=6,
            )
        ),
    TextField('text',
        accessor='getBodyText',
        required=True,
        searchable=True,
        primary=True,
        validators=('isTidyHtmlWithCleanup',),
        default_content_type='text/html',
        default_output_type='text/x-html-safe',
        allowable_content_types=('text/html',
                                 'text/plain',),
        widget=RichWidget(
            label=_("label_body_text", default=u"Body Text"),
            description=_("help_body_text",
                          default=u"Text for front page of signup",),
            rows=25,
           ),
        ),
))

SignupSheetSchema.moveField('eventsize', after='description')
SignupSheetSchema.moveField('waitlist_size', after='eventsize')
SignupSheetSchema.moveField('display_size_left', after='waitlist_size')
SignupSheetSchema.moveField('earlyBirdDate', after='display_size_left')
SignupSheetSchema.moveField('registrationDeadline', after='earlyBirdDate')
SignupSheetSchema.moveField('text', after='registrationDeadline')


class SignupSheet(FormFolder):
    implements(ISignupSheet)

    schema = SignupSheetSchema

    def initializeArchetype(self, **kwargs):
        """ Create sample content that may help folks
            figure out how this gadget works.
            The same as PloneformGen do, but we overrides to create objects we
            are interest on: name, surname, status, email
        """
        ATFolder.initializeArchetype(self, **kwargs)
        self.setSubmitLabel(zope.i18n.translate(_(u'signupsheet_formfolder_signup',
                                                  u'Sign up'),
                                                context=self.REQUEST))
        self.setResetLabel(zope.i18n.translate(_(u'signupsheet_formfolder_reset',
                                                 u'Reset'),
                                              context=self.REQUEST))

        oids = self.objectIds()
        if not oids:
            # create a name field
            self.invokeFactory('FormStringField', 'name')
            obj = self['name']
            obj.fgField.__name__ = 'name'

            obj.setTitle(zope.i18n.translate(
                         _(u'signupsheet_namefield_title', u'Your Name'),
                         context=self.REQUEST))
            self._pfFixup(obj)

            # create a surname field
            self.invokeFactory('FormStringField', 'surname')
            obj = self['surname']
            obj.fgField.__name__ = 'surname'
            obj.setTitle(zope.i18n.translate(
                        _(u'signupsheet_surnamefield_title', u'Your surname'),
                        context=self.REQUEST))
            self._pfFixup(obj)

            # create a status field
            self.invokeFactory('FormSelectionField', 'status')
            obj = self['status']
            obj.fgField.__name__ = 'status'
            obj.setTitle(zope.i18n.translate(
                        _(u'signupsheet_statusfield_title', u'Status'),
                        context=self.REQUEST))
            obj.setFgVocabulary(('registered|%s' %
                                 zope.i18n.translate(
                                    _(u'signupsheet_statusfield_registered_opt',
                                      u'Registered'),
                                   context=self.REQUEST),
                                 'waitinglist|%s' %
                                 zope.i18n.translate(
                                    _(u'signupsheet_statusfield_waitinglist_opt',
                                      u'Waiting list'),
                                    context=self.REQUEST)
                                 )
                                )
            obj.setFgFormat('radio')
            self._pfFixup(obj)

            # create a mail field
            self.invokeFactory('FormStringField', 'email')
            obj = self['email']
            obj.fgField.__name__ = 'email'
            obj.setTitle(zope.i18n.translate(
                         _(u'signupsheet_emailfield_title',
                           u'Your E-Mail Address'),
                          context=self.REQUEST))
            obj.fgField.required = True
            obj.setFgStringValidator('isEmail')
            self._pfFixup(obj)

            # create a thanks page
            # BBB Decide what we want write here
            self.invokeFactory('FormThanksPage', 'thank-you')
            obj = self['thank-you']

            obj.setTitle(zope.i18n.translate(
                         _(u'pfg_thankyou_title', u'Thank You'),
                         context=self.REQUEST))
            obj.setDescription(zope.i18n.translate(
              _(u'pfg_thankyou_description', u'Thanks for your input.'),
              context=self.REQUEST))
            self._pfFixup(obj)
            self.thanksPage = 'thank-you'


registerATCT(SignupSheet, PROJECTNAME)
