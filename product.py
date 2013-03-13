#This file is part product_attachments module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Product']
__metaclass__ = PoolMeta


class Product:
    'Product'
    __name__ = 'product.product'
    attachments = fields.One2Many('ir.attachment', 'resource', 'Attachments')
