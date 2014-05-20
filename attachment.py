#This file is part product_attachments module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import PoolMeta

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
    def create(cls, vlist):
        for vals in vlist:
            vals['name'] = slugify(vals['name'])
        return super(Attachment, cls).create(vlist)

    @classmethod
    def write(cls, *args):
        actions = iter(args)
        args = []
        for attachments, values in zip(actions, actions):
            if values.get('name'):
                values['name'] = slugify(values['name'])
            args.extend((attachments, values))
        return super(Attachment, cls).write(*args)
