# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import unittest
import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import doctest_teardown, doctest_checker


class AccountInvoiceSearchByPurchaseTestCase(ModuleTestCase):
    'Test Purchase module'
    module = 'account_invoice_search_by_purchase'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountInvoiceSearchByPurchaseTestCase))
    suite.addTests(doctest.DocFileSuite(
            'scenario_account_invoice_search_by_purchase.rst',
            tearDown=doctest_teardown, encoding='UTF-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE,
            checker=doctest_checker))
    return suite
