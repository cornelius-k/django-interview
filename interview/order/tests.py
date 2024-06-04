from django.test import TestCase
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

    def test_get_order_tags(self) -> None:
        '''
        Test getting all tags for an order id returns
        the correct number of tags
        '''
        order = self.order_objs.first()
        response = self.client.get(f'/orders/{order.id}/tags/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), len(order.tags.all()))
