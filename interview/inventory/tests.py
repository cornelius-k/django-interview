from django.test import TestCase
from django.utils.http import urlencode
from interview.inventory.models import Inventory
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
from interview.inventory import views
from rest_framework.response import Response
from urllib.parse import urlencode
from interview.inventory.views import INVENTORY_LIST_DEFAULT_PAGE_SIZE, INVENTORY_LIST_MAX_PAGE_SIZE


class TestInventoryViews(TestCase):
    fixtures = ['inventory_views_fixtures.json']
    inventory_objs = Inventory.objects.all().order_by('created_at')
    
    # @classmethod
    # def setUpClass(cls):
    #     '''
    #     Clear all Inventory objects before running tests
    #     so that only those provided in fixtures are present in database
    #     '''
    #     all_inventory = Inventory.objects.all()
    #     all_inventory.delete()
    #     super(TestInventoryViews, cls).setUpClass()

    def request_with_querystring(self, path, **kwargs) -> Response:
        '''
        form a querystring from the kwargs and make a request to path
        '''
        qs = urlencode(kwargs)
        path = f"{path}?{qs}"
        return self.client.get(path)
    
    def test_inventory_pagination_exists(self) -> None:
        '''
        Test that response has paginated results set with the correct
        number of items
        '''
        res = self.client.get('/inventory/')
        self.assertEquals(len(res.data['results']), INVENTORY_LIST_DEFAULT_PAGE_SIZE)       
        [self.assertIn(key, res.data) for key in ['count', 'next', 'previous', 'results']]

    def test_inventory_pagination_limit(self) -> None:
        '''
        Test that providing a limit querystring parameter changes the
        results set size up to the limit maximum
        '''
        res = self.request_with_querystring('/inventory/', limit=2)
        self.assertEquals(len(res.data['results']), 2)
        res = self.request_with_querystring('/inventory/', limit=INVENTORY_LIST_MAX_PAGE_SIZE + 1)
        self.assertEquals(len(res.data['results']), INVENTORY_LIST_MAX_PAGE_SIZE)

