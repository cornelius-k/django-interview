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
        
    def test_update_order_active_status_true(self) -> None:
        '''
        Test setting active status of an order to True
        '''
        order = self.order_objs.first()
        self.assertFalse(order.is_active)
        response = self.client.patch(f'/orders/{order.id}/active', {"is_active": True}, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        order.refresh_from_db()
        self.assertTrue(order.is_active)

    def test_update_order_active_status_false(self) -> None:
        '''
        Test setting active status of an order to False
        '''
        order = self.order_objs.first()
        order.is_active = True
        order.save()
        self.assertTrue(order.is_active)
        response = self.client.patch(f'/orders/{order.id}/active', {"is_active": False}, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        order.refresh_from_db()
        self.assertFalse(order.is_active)
