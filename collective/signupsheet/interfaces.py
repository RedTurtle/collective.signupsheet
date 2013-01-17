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
