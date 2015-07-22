# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .stock import *
from .invoice import *


def register():
    Pool.register(
        StockMove,
        InvoiceLine,
        module='account_invoice_search_by_purchase', type_='model')
