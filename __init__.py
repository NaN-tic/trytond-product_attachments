# This file is part product_attachments module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import attachment
from . import configuration
from . import product


def register():
    Pool.register(
        configuration.Configuration,
        attachment.Attachment,
        product.Template,
        product.Product,
        module='product_attachments', type_='model')
