# This file is part product_attachments module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from mimetypes import guess_type

import slug
from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = ['Attachment']


def slugify(value):
    """Convert attachment name to slug: az09 and replace spaces by -"""
    fname = value.lower().split('.')
    fn = fname[0]
    try:
        name = slug.slug(fn)
        if len(fname) > 1:
            return '%s.%s' % (name, fname[1])
        else:
            return name
    except:
        return value


class Attachment(metaclass=PoolMeta):
    __name__ = 'ir.attachment'
    active = fields.Boolean('Active', select=True)

    @staticmethod
    def default_active():
        return True

    @classmethod
    def _get_models_check_mime_type(cls):
        '''Return list of Model names to check the mime type and slugify the
         names of their attachments'''
        return ['product.template']

    @classmethod
    def create(cls, vlist):
        for vals in vlist:
            if vals['type'] == 'link':
                continue
            model_name, record_id = vals['resource'].split(',', 1)
            if model_name not in cls._get_models_check_mime_type():
                continue
            filename = slugify(vals['name'])
            if not guess_type(filename)[0]:
                raise UserError(gettext('product_attachments.not_known_mimetype',
                    filename=filename))
            vals['name'] = filename

            if 'resource' in vals and 'data' in vals:
                resource = vals['resource']
                data = vals['data']

                model_name, id = resource.split(',')
                Model = Pool().get(model_name)
                if hasattr(Model, 'thumb'):
                    record = Model(int(id))
                    if not record.thumb:
                        # save each record because you could create multiple
                        # attachments related with differents models
                        record.thumb = data
                        record.thumb_filename = filename
                        record.save()

        return super(Attachment, cls).create(vlist)

    @classmethod
    def write(cls, *args):
        actions = iter(args)
        args = []
        to_slugify = True
        for attachments, values in zip(actions, actions):
            for attachment in attachments:
                if (attachment.resource.__name__ not in
                        cls._get_models_check_mime_type()
                        or attachment.type == 'link'):
                    to_slugify = False
            if to_slugify and values.get('name'):
                filename = slugify(values['name'])
                if not guess_type(filename)[0]:
                    raise UserError(gettext(
                    'product_attachments.not_known_mimetype',
                        filename=filename))
                values['name'] = filename
            args.extend((attachments, values))
        return super(Attachment, cls).write(*args)
