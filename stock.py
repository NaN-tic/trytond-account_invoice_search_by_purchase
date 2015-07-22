# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from sql import Cast, Literal
from sql.functions import Substring, Position

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.tools import grouped_slice, reduce_ids
from trytond.transaction import Transaction

__all__ = ['StockMove']
__metaclass__ = PoolMeta


class StockMove:
    __name__ = 'stock.move'
    purchase = fields.Function(fields.Many2One('purchase.purchase',
            'Purchase'),
        'get_purchase', searcher='search_purchase')
    purchase_date = fields.Function(fields.Date('Purchase Date'),
        'get_purchase_date', searcher='search_purchase_date')

    @classmethod
    def get_purchase(cls, lines, name):
        pool = Pool()
        PurchaseLine = pool.get('purchase.line')
        purchase_line = PurchaseLine.__table__()
        table = cls.__table__()
        cursor = Transaction().cursor

        line_ids = [l.id for l in lines]
        result = {}.fromkeys(line_ids, None)
        for sub_ids in grouped_slice(line_ids):
            cursor.execute(*table.join(purchase_line,
                    condition=((Cast(Substring(table.origin,
                                Position(',', table.origin) + Literal(1)),
                        cls.id.sql_type().base) == purchase_line.id)
                        & table.origin.ilike('purchase.line,%'))).select(
                    table.id, purchase_line.purchase,
                    where=reduce_ids(table.id, sub_ids)))
            result.update(dict(cursor.fetchall()))
        return result

    @classmethod
    def search_purchase(cls, name, clause):
        return [('origin.purchase', clause[1], clause[2], 'purchase.line')]

    @classmethod
    def get_purchase_date(cls, moves, name):
        pool = Pool()
        PurchaseLine = pool.get('purchase.line')
        Purchase = pool.get('purchase.purchase')
        table = cls.__table__()
        purchase_line = PurchaseLine.__table__()
        purchase = Purchase.__table__()
        cursor = Transaction().cursor

        move_ids = [m.id for m in moves]
        result = {}.fromkeys(move_ids, None)
        for sub_ids in grouped_slice(move_ids):
            cursor.execute(*table.join(purchase_line,
                    condition=((Cast(Substring(table.origin,
                                Position(',', table.origin) + Literal(1)),
                        cls.id.sql_type().base) == purchase_line.id)
                        & table.origin.ilike('purchase.line,%'))).join(
                    purchase, condition=(purchase.id == purchase_line.purchase)
                        ).select(table.id, purchase.purchase_date,
                    where=reduce_ids(table.id, sub_ids)))
            result.update(dict(cursor.fetchall()))
        return result

    @classmethod
    def search_purchase_date(cls, name, clause):
        return [('origin.purchase.purchase_date', clause[1], clause[2],
                'purchase.line')]
