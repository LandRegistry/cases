import unittest
import responses
from application.server import app
from application.modify_titles import apply_change, get_title
from stub_json import response_json

TITLE_NUMBER = "TEST198"

class TestChangeTitleCase(unittest.TestCase):
    def setUp(self):
        self.search_url = 'http://nowhere/'
        self.client = app.test_client()

    def test_change_title(self):
        current_title = {"proprietors": [{"full_name": "Hank Schrader"}, {"full_name": ""}], "leases": [{"lease_term": 403, "lease_easements": "true", "lessor_name": "Sam Thompson", "lease_date": "2014-09-17", "lessee_name": "Bob Moore", "title_registered": "true", "lease_from": "2014-09-17", "alienation_clause": "true"}], "charges": [{"chargee_name": "Test Bank", "chargee_registration_number": "1234567", "chargee_address": "12 Test Street, London, SE1 33S", "charge_date": "2014-08-11", "charges-0-has_restriction": "true"}], "previous_sha256": "cafebabe", "easements": [{"easement_geometry": {"geometry": {"type": "Polygon", "properties": {"Description": "Polygon"}, "coordinates": [[[530667.0, 181425.0], [530687.0, 181434.0], [530752.0, 181282.0], [530732.0, 181273.0], [530667.0, 181425.0]]]}, "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG:27700"}}, "type": "Feature"}, "easement_description": "The land tinted blue on the title plan is subject to rights of way."}], "title_number": "TEST1411556289670", "extent": {"geometry": {"type": "Polygon", "properties": {"Description": "Polygon"}, "coordinates": [[[530647.0, 181419.0], [530855.0, 181500.0], [530917.0, 181351.0], [530713.0, 181266.0], [530647.0, 181419.0]]]}, "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG:27700"}}, "type": "Feature"}, "property": {"tenure": "Leasehold", "class_of_title": "absolute", "address": {"city": "London", "country": "GB", "postcode": "N1 4LT", "address_line_1": "10 High St"}}, "payment": {"titles": ["TEST275510140"], "price_paid": 7560115}}
        changed_title = {"proprietors": [{"full_name": "Hank Bond"}, {"full_name": ""}], "leases": [{"lease_term": 403, "lease_easements": "true", "lessor_name": "Sam Thompson", "lease_date": "2014-09-17", "lessee_name": "Bob Moore", "title_registered": "true", "lease_from": "2014-09-17", "alienation_clause": "true"}], "charges": [{"chargee_name": "Test Bank", "chargee_registration_number": "1234567", "chargee_address": "12 Test Street, London, SE1 33S", "charge_date": "2014-08-11", "charges-0-has_restriction": "true"}], "previous_sha256": "cafebabe", "easements": [{"easement_geometry": {"geometry": {"type": "Polygon", "properties": {"Description": "Polygon"}, "coordinates": [[[530667.0, 181425.0], [530687.0, 181434.0], [530752.0, 181282.0], [530732.0, 181273.0], [530667.0, 181425.0]]]}, "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG:27700"}}, "type": "Feature"}, "easement_description": "The land tinted blue on the title plan is subject to rights of way."}], "title_number": "TEST1411556289670", "extent": {"geometry": {"type": "Polygon", "properties": {"Description": "Polygon"}, "coordinates": [[[530647.0, 181419.0], [530855.0, 181500.0], [530917.0, 181351.0], [530713.0, 181266.0], [530647.0, 181419.0]]]}, "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG:27700"}}, "type": "Feature"}, "property": {"tenure": "Leasehold", "class_of_title": "absolute", "address": {"city": "London", "country": "GB", "postcode": "N1 4LT", "address_line_1": "10 High St"}}, "payment": {"titles": ["TEST275510140"], "price_paid": 7560115}}
        change_data = {"confirm": "true", "partner_name": "Jane", "application_type": "change-name-marriage", "marriage_country": "GB", "proprietor_new_full_name": "Hank Bond", "marriage_place": "London", "title_number": "TEST1411556289670", "proprietor_full_name": "Hank Schrader", "marriage_certificate_number": "NOWAY", "marriage_date": 1406847600}
        under_test = apply_change(current_title, change_data)
        self.assertEquals(under_test, changed_title)

    def test_change_title_when_name_not_in_proprietors(self):
        current_title = {"proprietors": [{"full_name": "Hank Schrader"}, {"full_name": ""}], "leases": [{"lease_term": 403, "lease_easements": "true", "lessor_name": "Sam Thompson", "lease_date": "2014-09-17", "lessee_name": "Bob Moore", "title_registered": "true", "lease_from": "2014-09-17", "alienation_clause": "true"}], "charges": [{"chargee_name": "Test Bank", "chargee_registration_number": "1234567", "chargee_address": "12 Test Street, London, SE1 33S", "charge_date": "2014-08-11", "charges-0-has_restriction": "true"}], "previous_sha256": "cafebabe", "easements": [{"easement_geometry": {"geometry": {"type": "Polygon", "properties": {"Description": "Polygon"}, "coordinates": [[[530667.0, 181425.0], [530687.0, 181434.0], [530752.0, 181282.0], [530732.0, 181273.0], [530667.0, 181425.0]]]}, "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG:27700"}}, "type": "Feature"}, "easement_description": "The land tinted blue on the title plan is subject to rights of way."}], "title_number": "TEST1411556289670", "extent": {"geometry": {"type": "Polygon", "properties": {"Description": "Polygon"}, "coordinates": [[[530647.0, 181419.0], [530855.0, 181500.0], [530917.0, 181351.0], [530713.0, 181266.0], [530647.0, 181419.0]]]}, "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG:27700"}}, "type": "Feature"}, "property": {"tenure": "Leasehold", "class_of_title": "absolute", "address": {"city": "London", "country": "GB", "postcode": "N1 4LT", "address_line_1": "10 High St"}}, "payment": {"titles": ["TEST275510140"], "price_paid": 7560115}}
        change_data = {"confirm": "true", "partner_name": "Jane", "application_type": "change-name-marriage", "marriage_country": "GB", "proprietor_new_full_name": "Hank Bond", "marriage_place": "London", "title_number": "TEST1411556289670", "proprietor_full_name": "Hank", "marriage_certificate_number": "NOWAY", "marriage_date": 1406847600}
        underTest = apply_change(current_title, change_data)
        print underTest
        self.assertEquals(underTest, None)

    @responses.activate
    def test_get_title(self):
        responses.add(responses.GET, '%s/auth/titles/%s' % (self.search_url, TITLE_NUMBER),
                      body=response_json, status=200, content_type='application/json')

        resp = get_title(self.search_url, TITLE_NUMBER)
        assert resp['title_number'] == TITLE_NUMBER

