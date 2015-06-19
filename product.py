# This file is part product_attachments module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction
from trytond.config import config
import magic

__all__ = ['Template', 'Product']
__metaclass__ = PoolMeta
_IMAGE_TYPES = ['image/jpeg', 'image/png',  'image/gif']
STATES = {
    'readonly': ~Eval('active', True),
    }
DEPENDS = ['active']


class Template:
    __name__ = 'product.template'
    attachments = fields.One2Many('ir.attachment', 'resource',
        'Attachments', states=STATES, depends=DEPENDS)
    image = fields.Function(fields.Char('Image'),
        'get_image')

    @classmethod
    def delete(cls, templates):
        pool = Pool()
        Attachment = pool.get('ir.attachment')

        attachments = [a for t in templates for a in t.attachments]
        Attachment.delete(attachments)
        super(Template, cls).delete(templates)

    def get_image(self, name):
        '''Return a digest product image'''
        if not self.attachments:
            return

        path = config.get('database', 'path')
        db_name = Transaction().cursor.dbname

        for attach in self.attachments:
            digest = attach.digest
            image = '%s/%s/%s/%s/%s' % (
                path,
                db_name,
                digest[:2],
                digest[2:4:],
                digest,
                )

            mimetype = magic.from_file(image, mime=True)
            if mimetype in _IMAGE_TYPES:
                return digest
        return


class Product:
    __name__ = 'product.product'
    attachments = fields.One2Many('ir.attachment', 'resource',
        'Attachments', states=STATES, depends=DEPENDS)
    image = fields.Function(fields.Char('Image'),
        'get_image')

    @classmethod
    def delete(cls, products):
        pool = Pool()
        Attachment = pool.get('ir.attachment')

        attachments = [a for p in products for a in p.attachments]
        Attachment.delete(attachments)
        super(Product, cls).delete(products)

    def get_image(self, name):
        '''Return a digest product image'''
        if not self.attachments:
            return self.template.get_image(name)

        path = config.get('database', 'path')
        db_name = Transaction().cursor.dbname

        for attach in self.attachments:
            digest = attach.digest
            image = '%s/%s/%s/%s/%s' % (
                path,
                db_name,
                digest[:2],
                digest[2:4:],
                digest,
                )

            mimetype = magic.from_file(image, mime=True)
            if mimetype in _IMAGE_TYPES:
                return digest
        return
