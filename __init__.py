# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import stock
from . import invoice


def register():
    Pool.register(
        stock.StockMove,
        invoice.InvoiceLine,
        module='account_invoice_search_by_purchase', type_='model')
