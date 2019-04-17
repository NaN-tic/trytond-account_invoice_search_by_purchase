# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from sql import Cast, Literal
from sql.aggregate import Max
from sql.functions import Substring, Position

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.tools import grouped_slice, reduce_ids
from trytond.transaction import Transaction

__all__ = ['InvoiceLine']

_STATES = {
    'invisible': ~Eval('context', {}).get('type', '').in_(['in']),
    }


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'
    purchase = fields.Function(fields.Many2One('purchase.purchase',
            'Purchase', states=_STATES),
        'get_purchase', searcher='search_purchase')
    purchase_shipment_date = fields.Function(fields.Date('Shipment Date',
            states=_STATES),
        'get_purchase_shipment_date', searcher='search_purchase_shipment_date')

    def get_purchase(self, name):
        pool = Pool()
        PurchaseLine = pool.get('purchase.line')

        if isinstance(self.origin, PurchaseLine):
            return self.origin.purchase.id

    @classmethod
    def search_purchase(cls, name, clause):    
        return [('origin.' + clause[0],) + tuple(clause[1:3])
            + ('purchase.line',) + tuple(clause[3:])]

    @classmethod
    def get_purchase_shipment_date(cls, lines, name):
        pool = Pool()
        PurchaseLine = pool.get('purchase.line')
        Move = pool.get('stock.move')
        table = cls.__table__()
        purchase_line = PurchaseLine.__table__()
        move = Move.__table__()
        cursor = Transaction().connection.cursor()

        line_ids = [l.id for l in lines]
        result = {}.fromkeys(line_ids, None)
        for sub_ids in grouped_slice(line_ids):
            cursor.execute(*table.join(purchase_line,
                    condition=((Cast(Substring(table.origin,
                                Position(',', table.origin) + Literal(1)),
                        cls.id.sql_type().base) == purchase_line.id)
                        & table.origin.ilike('purchase.line,%'))).join(
                    move, condition=((Cast(Substring(move.origin,
                                Position(',', move.origin) + Literal(1)),
                        cls.id.sql_type().base) == purchase_line.id)
                        & move.origin.ilike('purchase.line,%'))).select(
                    table.id, Max(move.effective_date),
                    where=reduce_ids(table.id, sub_ids), group_by=(table.id,)))
            result.update(dict(cursor.fetchall()))
        return result

    @classmethod
    def search_purchase_shipment_date(cls, name, clause):
        return [('origin.moves.effective_date', clause[1], clause[2],
                'purchase.line')]
