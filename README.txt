Introduction
============
This package has beed created thinking to switch the old `Products.SignupSheet`
package to a new one more in the Plone 4.x way.

Regarding Products.SignupSheet it's look like a form with a bunch of fields that
an admin can change dinamically.
From here to `Products.PloneFormGen` it's just a short step.

PloneFormGen Allow us to create form dinamically and this is the first important
brick. The old SignupSheet was able to create objects (Registrant archetypes)
and change (add/remove/modify) it's field dinamically. 
In this case we decide to use `uwosh.pfg.d2c`. This is a great adapter created to
works with PloneFormGen that allow to add an action at the form submission and
during this action save the form data into an archetype. This archetype completely
based on schema extender, so every time someone change fields in the form, also fields
on those archetypes changes.
