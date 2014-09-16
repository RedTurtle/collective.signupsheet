A **signup sheet implementation** for Plone. New events-like content are added to your site, **users can subscribe** to
those events filling a **customizable form**.

.. contents:: **Table of contents**

How to use
==========

.. image:: http://blog.redturtle.it/pypi-images/collective.signupsheet/collective.signupsheet-0.1.0-01.png/image_preview
   :target: http://blog.redturtle.it/pypi-images/collective.signupsheet/collective.signupsheet-0.1.0-01.png
   :align: right
   :alt: Example form

After installation you can add a new content type to you site: the "*Signup Sheet*".

Starting configuration in the edit form is only about general information about the event, like:

* Max number of registrants (if any)
* Waiting list size (if any)
* Start/End date of the event
* Start/End date of early bird phase
* Registration deadline
* ...much more

After that your users can access a **subscription form**, but you can easily customize
*how* the form looks like.

Customizing the subscription form
---------------------------------

This product is based on `PloneFormGen`__ so you can use the same form construction features.
You have a great set of form fields available, but 3rd party products can enhance this list (for example:
a captcha protection field could help).

__ http://plone.org/products/ploneformgen

The form is automatically generated with three core fields:

* Name
* Surname
* Email

The *email* field is recommended but you can freely change/delete them all and add much more fields.

Whatever form you define, your users must fill the form to subscribe.

Handling subscriptions
----------------------

.. image:: http://blog.redturtle.it/pypi-images/collective.signupsheet/collective.signupsheet-0.1.0-02.png/image_mini
   :target: http://blog.redturtle.it/pypi-images/collective.signupsheet/collective.signupsheet-0.1.0-02.png
   :align: right
   :alt: Editing a subscriber

Every time a user fill the form, a "*registrant*" content is created inside the "*Registrants*" subsection of
the form.
The registrant is *real* working document that an administrator can edit later (we are using the poweful
`uwosh.pfg.d2c`__ here).

__ http://plone.org/products/uwosh.pfg.d2c

For users able to manage the signup sheet an administrative view "*View Registrant*" is given.

.. image:: http://blog.redturtle.it/pypi-images/collective.signupsheet/collective.signupsheet-0.1.0-03.png/image_preview
   :target: http://blog.redturtle.it/pypi-images/collective.signupsheet/collective.signupsheet-0.1.0-03.png
   :align: center
   :alt: View Registrants

From this view you can see the status of all subscriptions and confim them.
Right now confirming a user subscription has only internal meaning and confirmed or unconfirmed users are not
handled in different way.

Other features
--------------

Notification system
~~~~~~~~~~~~~~~~~~~

The Signup Sheet contains also two PloneFormGen mailer adapter, one for notification to the manager at every
new subscription, another for notify the user itself after the subscription (for receive a confirmation of filled
data).

You can customize tuose adapter for fit your needs (new mail messages, notify additional users, ...).

.. Note:: although both mailers are normal PloneFormGen items, the "*User notification mailer*" is
          **disabled** by default. It's used in a special way and must stay disabled for proper working.

Import/Export
~~~~~~~~~~~~~

Subscribers can be exported in a CSV format, or imported from a CSV with the proper format.

Calendar friendly
~~~~~~~~~~~~~~~~~

Signup sheet are shown in the Plone calendar portlet.

Credits
=======

Developed with the support of `S. Anna Hospital, Ferrara`__;
S. Anna Hospital supports the `PloneGov initiative`__.

__ http://www.ospfe.it/
__ http://www.plonegov.it/

Historical tribute to SignupSheet
---------------------------------

Altough this product is using more recent Plone technologies, it's miming all the features of another product:
`SignupSheet`__.

__ http://plone.org/products/signupsheet

The software stack used in the orginal product has become too old to be maintained anymore. We hope this new add-on
will give same features and best flexibility.


Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
