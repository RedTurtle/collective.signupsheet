Introduction
============
This package has beed created thinking to switch the old `Products.SignupSheet`__
package to a new one more in the Plone 4.x way.

__ http://plone.org/products/signupsheet

Regarding Products.SignupSheet it's look like a form with a bunch of fields that
an admin can change dinamically.
From here to `Products.PloneFormGen`__ it's just a short step.

__ http://plone.org/products/ploneformgen

PloneFormGen Allow us to create form dinamically and this is the first important
brick. The old SignupSheet was able to create objects (Registrant archetypes)
and change (add/remove/modify) it's field dinamically.
In this case we decide to use `uwosh.pfg.d2c`__. This is a great adapter created to
works with PloneFormGen that allow to add an action at the form submission and
during this action save the form data into an archetype. This archetype completely
based on schema extender, so every time someone change fields in the form, also fields
on those archetypes changes.

__ http://plone.org/products/uwosh.pfg.d2c

Usage
-----

Install from portal_quickinstaller collective.signupsheeet and you'll install
also uwosh.pfg.d2c. After production installation you'll have in the content menu
a new entry called Signup Sheet.

Adding a new signup sheet will give you a new object, based on FormFolder
with a set of objects within:

 * a *name*  (FormStringField);
 * a *surname* (FormStringField);
 * a *state* (FormStringField);
 * an *email* (FormStringField);
 * a *registrants* (FormSaveData2ContentAdapter);
 * a couple of mailer (FormMailerAdapter);
 * a *thank-you* page (FormThanksPage);

Those object are preconfigured with default values more or less in the way the
old Products.SignupSheet was preconfigured.

Authors
-------
The product was developed by

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/