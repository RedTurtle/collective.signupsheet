# -*- coding: utf-8 -*-

from Products.PloneFormGen.interfaces import IPloneFormGenForm
from zope.interface import Interface


class ISignupSheet(IPloneFormGenForm):
    """
    Marker interface for signup sheet form
    """


class ISignupSheetInitializer(Interface):
    """
    We use this interface for adapters that provides form initialization
    actions.
    Maybe in a future we'll create some user interface in control panel or in
    the form itself that will allow to select which configuration use to init
    the form
    """

    def form_initializer(self):
        """
        This method is called over the adapted form and initialize it
        """


class IGetRegistrants(Interface):
    """
    This interface is used to create an utility to retrieve registrant from a
    form
    """

    def get_registrant(self):
        """
        Use this method to get registrants for a given form
        """

    def get_registrants_brains(self, form):
        """
        Use this method to get registrant brains for a given form
        """

    def get_registrants_folder(self, form):
        """
        Use this method to get registrants folder for a given form
        """


class ISignupSheetMailer(Interface):
    """
    This interface is used to create and send mail from the signup sheet module
    """

    def send_mail(self):
        """
        Use this method to send mail
        """
