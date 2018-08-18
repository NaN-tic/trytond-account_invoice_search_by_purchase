# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['StockMove']


class StockMove(metaclass=PoolMeta):
    __name__ = 'stock.move'
    purchase_date = fields.Function(fields.Date('Purchase Date'),
        'get_purchase_date', searcher='search_purchase_date')

    def get_purchase_date(self, name):
        return self.purchase.purchase_date if self.purchase else None

    @classmethod
    def search_purchase_date(cls, name, clause):
        return [('origin.purchase.' + clause[0],) + tuple(clause[1:3])
            + ('purchase.line',) + tuple(clause[3:])]
