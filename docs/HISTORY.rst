Changelog
=========

0.2.0 (2014-10-27)
------------------

- Removed some bad tab condition expressions [keul]
- Fixed security issues: some views were not protected
  with right permissions [keul]
- Merged features from `Products.SignupSheetNotification`__
  (an unreleased add-on for original SignupSheet package) [keul]

__ https://svn.plone.org/svn/collective/Products.SignupSheetNotification/trunk/


0.1.2 (2014-09-19)
------------------

- Email's subject is now taken from the "Subject" field
  but dynamically created
  [fdelia]
- Fixed action adapter "Registrants" not deselectable
  (although deselecting it has no meaning)
  [fdelia]
- Fixed encodings errors on sending mail and exporting
  [keul]
- Added german translation
  [staeff]
- Some sanity to i18n structure: defaults better created by
  i18ndude call
  [keul]
- Added *delete* action to registrant view
  [staeff] 

0.1.1 (2014-07-29)
------------------

- Fixing packaging error that prevent this
  to be released on the Python Package Index.
  [keul]

0.1.0 (2014-07-25)
------------------

- Initial release
