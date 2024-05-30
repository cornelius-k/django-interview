from django.test import TestCase
from django.utils.http import urlencode
from interview.inventory.models import Inventory


class TestInventoryViews(TestCase):

    def test_inventory_list_view_with_invalid_after_date(self):
        '''
        Test that 400 status response is provided when an invalid date string format
        is used
        '''
        after_date_query = urlencode({'after-date': 'invalid-date'})
        path = f"/inventory/?{after_date_query}"
        response = self.client.get(path)
        self.assertEquals(response.status_code, 400)


    def test_inventory_list_view_with_valid_after_date(self):
        '''
        Test that Inventory list request with an after-date query string returns
        only inventory created after provided date
        '''
        after_date_query = urlencode({'after-date': '2020-10-03T19:00:00+0200'})
        path = f"/inventory/?{after_date_query}"
        response = self.client.get(path)
        '''
            Left off here, need to parse json response, check that response data matches expected size in inventory
        '''
        