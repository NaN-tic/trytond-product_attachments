# This file is part product_attachments module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from .attachment import *
from .product import *

def register():
    Pool.register(
        Attachment,
        Template,
        Product,
        module='product_attachments', type_='model')
