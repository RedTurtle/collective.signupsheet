# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.Archetypes.atapi import (IntegerField, StringWidget,
                                       BooleanField, BooleanWidget,
                                       DateTimeField, CalendarWidget,
                                       TextField, RichWidget,
                                       Schema)
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.folder import ATFolder
from Products.CMFCore.permissions import ModifyPortalContent
from Products.PloneFormGen.content.form import (FormFolder,
                                                FormFolderSchema)
from Products.ATContentTypes import ATCTMessageFactory as _E

from zope.interface import implements

from collective.signupsheet import signupsheetMessageFactory as _
from collective.signupsheet.config import PROJECTNAME
from collective.signupsheet.interfaces import (ISignupSheet,
                                               ISignupSheetInitializer)


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
    DateTimeField('startDate',
        required=True,
        searchable=False,
        accessor='start',
        write_permission = ModifyPortalContent,
        default_method=DateTime,
        languageIndependent=True,
        widget = CalendarWidget(
            description= '',
            label=_E(u'label_event_start', default=u'Event Starts')
            )
        ),
    DateTimeField('endDate',
        required=True,
        searchable=False,
        accessor='end',
        write_permission = ModifyPortalContent,
        default_method=DateTime,
        languageIndependent=True,
        widget = CalendarWidget(
            description = '',
            label = _E(u'label_event_end', default=u'Event Ends')
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
SignupSheetSchema.moveField('startDate', after='waitlist_size')
SignupSheetSchema.moveField('endDate', after='startDate')
SignupSheetSchema.moveField('earlyBirdDate', after='endDate')
SignupSheetSchema.moveField('registrationDeadline', after='earlyBirdDate')
SignupSheetSchema.moveField('display_size_left', after='registrationDeadline')
SignupSheetSchema.moveField('text', after='display_size_left')


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
        ISignupSheetInitializer(self).form_initializer()

registerATCT(SignupSheet, PROJECTNAME)
