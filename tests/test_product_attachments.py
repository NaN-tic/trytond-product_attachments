# This file is part of the product_attachments module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class ProductAttachmentsTestCase(ModuleTestCase):
    'Test Product Attachments module'
    module = 'product_attachments'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductAttachmentsTestCase))
    return suite
