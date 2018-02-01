# This file is part product_attachments module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.product_attachments.tests.test_product_attachments import suite
except ImportError:
    from .test_product_attachments import suite

__all__ = ['suite']
