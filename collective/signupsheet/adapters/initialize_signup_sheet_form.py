# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements

from collective.signupsheet import signupsheetMessageFactory as _
from collective.signupsheet.interfaces import (ISignupSheet,
                                               ISignupSheetInitializer)

import zope.i18n


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
            # create a name field
            self.form.invokeFactory('FormStringField', 'name')
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
                           u'Your E-Mail Address'),
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
            obj.setDescription(zope.i18n.translate(
                _(u'pfg_registrant_description',
                  u'D2C adapter used to store registrants under the form'),
              context=self.form.REQUEST))
            obj.setEntryType('registrant')
            obj.setTitleField('email')
            obj.setNiceIds(True)
            self.form._pfFixup(obj)

            # create a thanks page
            # BBB Decide what we want write here
            self.form.invokeFactory('FormThanksPage', 'thank-you')
            obj = self.form['thank-you']

            obj.setTitle(zope.i18n.translate(
                         _(u'pfg_thankyou_title', u'Thank You'),
                         context=self.form.REQUEST))
            obj.setDescription(zope.i18n.translate(
              _(u'pfg_thankyou_description', u'Thanks for your input.'),
              context=self.form.REQUEST))
            self.form._pfFixup(obj)

            self.form.actionAdapter = ('registrants', )
            self.form.thanksPage = 'thank-you'
