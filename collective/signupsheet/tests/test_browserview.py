# -*- coding: utf-8 -*-
from Testing import ZopeTestCase as ztc

import unittest
import doctest

from collective.signupsheet.tests.base import FunctionalDocTestCase


def test_suite():
    return unittest.TestSuite([
        ztc.ZopeDocFileSuite(
            'registrants_view.txt',
            package='collective.signupsheet.tests',
            test_class=FunctionalDocTestCase,
            globs={},
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE |
                        doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
