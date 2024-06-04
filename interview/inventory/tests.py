from django.test import TestCase
from django.utils.http import urlencode
from rest_framework.response import Response
from interview.inventory.views import INVENTORY_LIST_DEFAULT_PAGE_SIZE, INVENTORY_LIST_MAX_PAGE_SIZE


class TestInventoryViews(TestCase):
    fixtures = ['inventory_views_fixtures.json']    

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

