from django.test import TestCase
from datetime import timedelta
from django.utils.dateparse import parse_date
from interview.order.models import Order

class TestOrderViews(TestCase):
    fixtures = ['order_views_fixtures.json']
    order_objs = Order.objects.all()
    
    @classmethod
    def setUpClass(cls):
        '''
        Clear all Order objects before running tests
        so that only those provided in fixtures are present in database
        '''
        all_orders = Order.objects.all()
        all_orders.delete()
        super(TestOrderViews, cls).setUpClass()
        
    def test_order_within_embargo_dates(self) -> None:
        '''
        Test that providing a valid date range returns all orders within that start and
        embargo date range
        '''
        start_date = self.order_objs.first().start_date
        embargo_date = self.order_objs.first().embargo_date
        response = self.client.get(f'/orders/?start_date={start_date}&embargo_date={embargo_date}')
        self.assertEquals(response.status_code, 200)
        self.assertGreater(len(response.data), 0)
        for order in response.data:
            self.assertGreaterEqual(parse_date(order['start_date']), start_date)
            self.assertLessEqual(parse_date(order['embargo_date']), embargo_date)

    def test_order_within_embargo_dates_no_results(self) -> None:
        '''
        Test that when providing a valid date range that no records fall within,
        an empty result set is provided
        '''
        start_date = self.order_objs.first().start_date + timedelta(1)
        embargo_date = self.order_objs.first().embargo_date - timedelta(1)
        response = self.client.get(f'/orders/?start_date={start_date}&embargo_date={embargo_date}')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 0)
