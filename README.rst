Introduction
============

This package has beed created thinking to switch the old `Products.SignupSheet`__ with a new product more in the Plone 4.x way.

__ http://plone.org/products/signupsheet

Products.SignupSheet looks like a form with a bunch of fields that an admin can change dinamically. From here to `Products.PloneFormGen`__ it's just a short step.

__ http://plone.org/products/ploneformgen


PloneFormGen allow us to create form dinamically and this is the first important brick. The old Products.SignupSheet was able to create objects (Registrant archetypes) and add/remove/modify it's fields dinamically. In this case we decide to use `uwosh.pfg.d2c`__. This is a PloneFormGen adapter that allow to add a new action; at form submission this action saves form data into an archetype. This archetype is completely based on schema extender, so every time someone change fields in the form, also fields on this archetypes changes.

__ http://plone.org/products/uwosh.pfg.d2c


Usage
=====

Install collective.signupsheet from portal_quickinstaller, and the install profile will install also uwosh.pfg.d2c. After product installation you'll have in the content menu a new entry called Signup Sheet.

When someone create a new form, you have all the FormFolder functionality plus the field from Products.SignupSheet. You will see two more fields: start and end date. In this way you will be able to treat the Signup Sheet as an event and it will be put in plone calendar portlet.

Adding a new signup sheet will give you also a set of objects within the form:

 * a *name* FormStringField;
 * a *surname* FormStringField;
 * an *email* FormStringField;
 * a *registrants* FormSaveData2ContentAdapter;
 * a couple of mailer FormMailerAdapter;
 * a *thank-you* page FormThanksPage;ter;
 * a thank-you page FormThanksPage;

Those object are configured with default values and text (depending on site language) more or less in the way the old Products.SignupSheet was configured.


Sub object configuration
------------------------
Here all the settings made on sub objects during signupsheet creation:
 * *name* field: the default value is setted to 'here/@@default_name_value'. In this way when user try to sign up, if it's a registered user, his name is calculated;
 * *surname* field: the same as name, calling 'here/@@default_surname_value';
 * *email* field: same as name and surname; default value is computed by 'here/@@default_email_value'; there is also *isEmail* validator setted;
 * *registrants* adapter: is configured to calculate dynamically created object's title, basing on name and surname fields;
 * *subscriber mail* and *manager mail* adapter: creation configure dynamically mail subject and mail body;
 * *thank you* page: there is a default message;

If you want, on user subscription, you can send a mail also to a signup sheet
'manger', manually setting the second mailer in the form (the "Manager notification
mailer"): need to add a mail addres.


Main difference from Products.Signupsheet
-----------------------------------------
 * gestione dello stato tramite workflow (and so slitghlty different wf)

Authors
-------
The product was developed by

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/
