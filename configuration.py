# This file is part product_attachments module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


__all__ = ['Configuration']


class Configuration(metaclass=PoolMeta):
    __name__ = 'product.configuration'
    thumb_size = fields.Integer('Thumb Size',
        help='Thumbnail Product Image Size (width and height)')

    @staticmethod
    def default_thumb_size():
        return 150
