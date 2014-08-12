#This file is part product_attachments module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import PoolMeta
from mimetypes import guess_type

import logging

try:
    import slug
except ImportError:
    logging.getLogger('product attachments').error(
            'Unable to import slug. Install slug package.')

__all__ = ['Attachment']
__metaclass__ = PoolMeta

def slugify(value):
    """Convert attachment name to slug: az09 and replace spaces by -"""
    fname = value.lower().split('.')
    fn = fname[0]
    try:
        if isinstance(fn, unicode):
            name = slug.slug(fn)
        else:
            name = slug.slug(unicode(fn, 'UTF-8'))

        if len(fname) > 1:
            return '%s.%s' % (name, fname[1])
        else:
            return name
    except:
        return value


class Attachment:
    __name__ = 'ir.attachment'

    @classmethod
    def __setup__(cls):
        super(Attachment, cls).__setup__()
        cls._error_messages.update({
                'not_known_mimetype': ('Filename "%s" not known mime type '
                    '(add extension filename).'),
                })

    @classmethod
    def _get_models_check_mime_type(cls):
        '''Return list of Model names to check the mime type and slugify the
         names of their attachments'''
        return ['product.template']

    @classmethod
    def create(cls, vlist):
        for vals in vlist:
            model_name, record_id = vals['resource'].split(',', 1)
            if model_name not in cls._get_models_check_mime_type():
                continue
            filename = slugify(vals['name'])
            if not guess_type(filename)[0]:
                cls.raise_user_error('not_known_mimetype',
                    (filename,))
            vals['name'] = filename
        return super(Attachment, cls).create(vlist)

    @classmethod
    def write(cls, *args):
        actions = iter(args)
        args = []
        to_slugify = True
        for attachments, values in zip(actions, actions):
            for attachment in attachments:
                if (attachment.resource.__name__ not in
                        cls._get_models_check_mime_type()):
                    to_slugify = False
            if to_slugify and values.get('name'):
                filename = slugify(values['name'])
                if not guess_type(filename)[0]:
                    cls.raise_user_error('not_known_mimetype',
                        (filename,))
                values['name'] = filename
            args.extend((attachments, values))
        return super(Attachment, cls).write(*args)
