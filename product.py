# This file is part product_attachments module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, Bool

__all__ = ['Template', 'Product']
__metaclass__ = PoolMeta

STATES = {
    'readonly': ~Eval('active', True),
    }
DEPENDS = ['active']


class Template:
    __name__ = 'product.template'
    attachments = fields.One2Many('ir.attachment', 'resource',
        'Attachments', states=STATES, depends=DEPENDS)

    @classmethod
    def delete(cls, templates):
        pool = Pool()
        Attachment = pool.get('ir.attachment')

        attachments = [a for t in templates for a in t.attachments]
        Attachment.delete(attachments)
        super(Template, cls).delete(templates)


class Product:
    __name__ = 'product.product'
    attachments = fields.One2Many('ir.attachment', 'resource',
        'Attachments', states=STATES, depends=DEPENDS)

    @classmethod
    def delete(cls, products):
        pool = Pool()
        Attachment = pool.get('ir.attachment')

        attachments = [a for p in products for a in p.attachments]
        Attachment.delete(attachments)
        super(Product, cls).delete(products)
