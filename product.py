# This file is part product_attachments module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import os
import hashlib
import magic
from PIL import Image
from mimetypes import guess_type
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction
from trytond.config import config

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
    thumb = fields.Function(fields.Binary('Thumb', filename='thumb_filename',
        help='Thumbnail Product Image'), 'get_thumb', setter='set_thumb')
    thumb_filename = fields.Char('File Name',
        help='Thumbnail Product File Name')
    thumb_path = fields.Function(fields.Char('Thumb Path'), 'get_thumbpath')

    @classmethod
    def __setup__(cls):
        super(Template, cls).__setup__()
        cls._error_messages.update({
            'not_file_mime': ('Not know file mime "%(file_name)s"'),
            'not_file_mime_image': ('"%(file_name)s" file mime is not an image ' \
                '(jpg, png or gif)'),
            'image_size': ('Thumb "%(file_name)s" size is larger than "%(size)s"Kb'),
        })

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
            if not digest:
                continue
            image = '%s/%s/%s/%s/%s' % (
                path,
                db_name,
                digest[:2],
                digest[2:4:],
                digest,
                )
            if not os.path.isfile(image):
                return
            mimetype = magic.from_file(image, mime=True)
            if mimetype in _IMAGE_TYPES:
                return digest
        return


    def get_thumb(self, name):
        db_name = Transaction().cursor.dbname
        filename = self.thumb_filename
        if not filename:
            return None
        filename = os.path.join(config.get('database', 'path'), db_name,
            'esale', 'thumb', filename[0:2], filename[2:4], filename)

        value = None
        try:
            with open(filename, 'rb') as file_p:
                value = fields.Binary.cast(file_p.read())
        except IOError:
            pass
        return value

    def get_thumbpath(self, name):
        filename = self.thumb_filename
        if not filename:
            return None
        return '%s/%s/%s' % (filename[:2], filename[2:4], filename)

    @classmethod
    def set_thumb(cls, templates, name, value):
        if value is None:
            return
        if not value:
            cls.write(templates, {
                'thumb_filename': None,
                })
            return

        Config = Pool().get('product.configuration')
        product_config = Config(1)
        size = product_config.thumb_size or 150

        db_name = Transaction().cursor.dbname
        esaledir = os.path.join(
            config.get('database', 'path'), db_name, 'esale', 'thumb')

        for template in templates:
            file_name = template.thumb_filename or 'unknown'

            file_mime, _ = guess_type(file_name)
            if not file_mime:
                cls.raise_user_error('not_file_mime', {
                        'file_name': file_name,
                        })
            if file_mime not in _IMAGE_TYPES:
                # is not image, not create a thumb
                continue

            _, ext = file_mime.split('/')
            digest = '%s.%s' % (hashlib.md5(value).hexdigest(), ext)
            subdir1 = digest[0:2]
            subdir2 = digest[2:4]
            directory = os.path.join(esaledir, subdir1, subdir2)
            filename = os.path.join(directory, digest)

            if not os.path.isdir(directory):
                os.makedirs(directory, 0775)
            os.umask(0022)
            with open(filename, 'wb') as file_p:
                file_p.write(value)

            # square and thumbnail thumb image
            thumb_size = size, size
            try:
                im = Image.open(filename)
            except:
                if os.path.exists(filename):
                    os.remove(filename)
                cls.raise_user_error('not_file_mime_image', {
                        'file_name': file_name,
                        })

            width, height = im.size
            if width > height:
               delta = width - height
               left = int(delta/2)
               upper = 0
               right = height + left
               lower = height
            else:
               delta = height - width
               left = 0
               upper = int(delta/2)
               right = width
               lower = width + upper

            im = im.crop((left, upper, right, lower))
            im.thumbnail(thumb_size, Image.ANTIALIAS)
            im.save(filename)

            cls.write([template], {
                'thumb_filename': digest,
                })


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
