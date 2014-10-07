import unittest
<<<<<<< HEAD
import responses
from application.server import app
from application.modify_titles import apply_change, get_title
from stub_json import response_json
=======
import datetime
from application.modify_titles import apply_change, apply_edition_date
>>>>>>> master

TITLE_NUMBER = "TEST198"

class TestChangeTitleCase(unittest.TestCase):
    def setUp(self):
        self.search_url = 'http://nowhere/'
        self.client = app.test_client()

    def test_change_title(self):
        name_to_change = "Hank Schrader"
        new_name = "Hank Bond"
        current_title = self._proprietor_model(name_to_change)
        changed_title = self._proprietor_model(new_name)
        change_data = {"confirm": "true", "partner_name": "Jane", "application_type": "change-name-marriage", "marriage_country": "GB", "proprietor_new_full_name": "Hank Bond", "marriage_place": "London", "title_number": "TEST1411556289670", "proprietor_full_name": "Hank Schrader", "marriage_certificate_number": "NOWAY", "marriage_date": 1406847600}
        under_test = apply_change(current_title, change_data)
        self.assertEquals(under_test, changed_title)

    def test_change_title_when_name_not_in_proprietors(self):
        name_to_change = "Hank Schrader"
        current_title = self._proprietor_model(name_to_change)
        change_data = {"confirm": "true", "partner_name": "Jane", "application_type": "change-name-marriage", "marriage_country": "GB", "proprietor_new_full_name": "Hank Bond", "marriage_place": "London", "title_number": "TEST1411556289670", "proprietor_full_name": "Hank", "marriage_certificate_number": "NOWAY", "marriage_date": 1406847600}
<<<<<<< HEAD
        underTest = apply_change(current_title, change_data)
        print underTest
        self.assertEquals(underTest, None)

    @responses.activate
    def test_get_title(self):
        responses.add(responses.GET, '%s/auth/titles/%s' % (self.search_url, TITLE_NUMBER),
                      body=response_json, status=200, content_type='application/json')

        resp = get_title(self.search_url, TITLE_NUMBER)
        assert resp['title_number'] == TITLE_NUMBER

=======
        under_test = apply_change(current_title, change_data)
        self.assertEquals(under_test, None)

    def _proprietor_model(self, full_name):
        return {"proprietorship" :
             {"template" : "PROPRIETOR(S):  *RP*",
              "full_text": "PROPRIETOR(S): Michael Jones of 8 Miller Way, Plymouth, Devon, PL6 8UQ",
              "fields" : {"proprietors":[{"name" : {"title" : "Mr", "full_name" : full_name, "decoration" : ""}, "address" : {"full_address": "8 Miller Way, Plymouth, Devon, PL6 8UQ", "house_no" : "8", "street_name" : "Miller Way", "town" : "Plymouth", "postal_county" : "Devon", "region_name" : "", "country" : "", "postcode":""}},
                                         {"name" : {"title" : "Mrs", "full_name" : "Betty Jones", "decoration" : ""}, "address" : {"full_address": "8 Miller Way, Plymouth, Devon, PL6 8UQ", "house_no" : "8", "street_name" : "Miller Way", "town" : "Plymouth", "postal_county" : "Devon", "region_name" : "", "country" : "", "postcode":""}}]},
              "deeds" : [],
              "notes" : []
             }
        }

    def test_apply_edition_date_when_the_key_exist(self):
        mod_date = '01-01-2014 10:09:30'
        current_title = {"created_ts": mod_date, "other": "values", "foo":"bar"}
        under_test = apply_edition_date(current_title)

        self.assertNotEquals(under_test['created_ts'], mod_date)
        self.assertLessEqual(datetime.datetime.strptime(under_test['created_ts'], '%d-%m-%Y %H:%M:%S'), datetime.datetime.utcnow(), '%d-%m-%Y %H:%M:%S')


    def test_apply_edition_date_when_the_key_does_not_exist(self):
        current_title = {"other": "values", "foo":"bar"}
        under_test = apply_edition_date(current_title)

        self.assertLessEqual(datetime.datetime.strptime(under_test['created_ts'], '%d-%m-%Y %H:%M:%S'), datetime.datetime.utcnow(), '%d-%m-%Y %H:%M:%S')
>>>>>>> master
