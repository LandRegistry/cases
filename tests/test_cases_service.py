import json
import unittest
from application.server import app
from application import db, service

class CasesServiceTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        db.create_all()
        self.app = app
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_save_cases_and_get_cases_returns_the_cases(self):
        with self.app.test_request_context():
            empty_response = self.client.get('/cases')
            self.assertEquals(empty_response.status_code, 200)
            self.assertEquals(empty_response.data, '[]')

            post_response = self.client.post('/cases',
                                             data=json.dumps({"title_number":"test_title", "application_type":"change_name",
                                                              "request_details":{"data": "{\"some\":\"detail\"}"}, "work_queue":"casework", "submitted_by":"jo_user"}),
                                             headers={'content-type': 'application/json'})
            self.assertEquals(post_response.status_code, 200)

            self.assertEquals(json.loads(post_response.data)['status'], 'successful')

            response_after_post = self.client.get('/cases')
            self.assertEquals(response_after_post.status_code, 200)

            case = json.loads(response_after_post.data)[0]

            self.assertEquals(case['title_number'], 'test_title')
            self.assertEquals(case['application_type'], 'change_name')
            self.assertEquals(case['request_details'], '{"data": "{\\"some\\":\\"detail\\"}"}')
            self.assertEquals(case['work_queue'], 'casework')
            self.assertEquals(case['submitted_by'], 'jo_user')


    def test_save_invalid_input_data(self):
      with self.app.test_request_context():
          empty_response = self.client.get('/cases')
          self.assertEquals(empty_response.status_code, 200)
          self.assertEquals(empty_response.data, '[]')

          post_response = self.client.post('/cases',
                                           data=json.dumps({ "work_queue":"casework", "submitted_by":"jo_user"}),
                                           headers={'content-type': 'application/json'})
          self.assertEquals(post_response.status_code, 400)

          self.assertEquals(json.loads(post_response.data)['status'], 'failed to save casework item')


    def save_case_without_work_queue(self, title_number):
        post_response = self.client.post('/cases',
                                         data=json.dumps({"title_number":title_number, "application_type":"change_name",
                                                          "request_details":{"data": "{\"some\":\"detail\"}"}, "submitted_by":"jo_user"}),
                                         headers= {'content-type': 'application/json'})
        self.assertEquals(post_response.status_code, 200)
        self.assertEquals(json.loads(post_response.data)['status'], 'successful')
        response_after_post = self.client.get('/cases')
        self.assertEquals(response_after_post.status_code, 200)
        case = json.loads(response_after_post.data)[0]
        self.assertEquals(case['title_number'], title_number)
        self.assertEquals(case['status'], 'pending')
        self.assertEquals(case['work_queue'], None)
        return response_after_post

    def test_update_case_with_work_queue_is_successful(self):
        with self.app.test_request_context():
            response = self.save_case_without_work_queue('test_title1')
            self.client.put('/cases/%s' % json.loads(response.data)[0]['id'],
                            data=json.dumps({"work_queue": "casework"}),
                            headers={'content-type': 'application/json'})
            response_after_put = self.client.get('/cases')

            self.assertEquals(response_after_put.status_code, 200)

            case_after_save = json.loads(response_after_put.data)[0]

            self.assertEquals(case_after_save['title_number'], 'test_title1')
            self.assertEquals(case_after_save['work_queue'], 'casework')

    def test_update_case_without_work_queue_fails(self):
        with self.app.test_request_context():
            self.save_case_without_work_queue('test_title2')
            response = self.client.put('/cases/test_title2',
                            data=json.dumps({"wrong": "data"}),
                            headers={'content-type': 'application/json'})

            self.assertEquals(response.status_code, 400)
            self.assertEquals(response.data, 'Invalid data when updating the id for case: %s' % 'test_title2')

    def test_approve_case_is_successful(self):
        with self.app.test_request_context():
            self.save_case_without_work_queue('test_title3')
            case = self.client.get("/cases")

            case_id = json.loads(case.data)[0]['id']

            self.client.put('/cases/complete/%s'% case_id,
                            headers={'content-type': 'application/json'})
            response_after_put = self.client.get('/cases')
            self.assertEquals(response_after_put.status_code, 200)

            case_after_save = json.loads(response_after_put.data)[0]

            self.assertEquals(case_after_save['title_number'], 'test_title3')
            self.assertEquals(case_after_save['status'], 'approved')

    def post_case(self, title, queue):
        post_response = self.client.post('/cases',
                                         data=json.dumps({"title_number": title, "application_type": "change_name",
                                                          "request_details":{"data": "{\"some\":\"detail\"}"}, "work_queue": queue, "submitted_by": "jo_user"}),
                                         headers={'content-type': 'application/json'})
        self.assertEquals(post_response.status_code, 200)

    def test_get_cases_by_work_queue_returns_only_cases_with_the_right_queue(self):
        with self.app.test_request_context():
            self.post_case('title5', 'casework')
            self.post_case('title6', 'check')

            response = self.client.get('/cases')
            self.assertEquals(response.status_code, 200)
            cases = json.loads(response.data)
            self.assertEquals(len(cases), 2)

            response = self.client.get('/cases/pending/casework')
            self.assertEquals(response.status_code, 200)
            cases = json.loads(response.data)
            self.assertEquals(cases[0]['title_number'], 'title5')
            self.assertEquals(cases[0]['work_queue'], 'casework')
            self.assertEquals(len(cases), 1)

            check_response = self.client.get('/cases/pending/check')
            self.assertEquals(check_response.status_code, 200)
            checks = json.loads(check_response.data)
            self.assertEquals(checks[0]['title_number'], 'title6')
            self.assertEquals(checks[0]['work_queue'], 'check')
            self.assertEquals(len(checks), 1)


    def test_get_cases_by_title_returns_only_cases_with_that_title(self):
        with self.app.test_request_context():
            self.post_case('title5', 'casework')
            self.post_case('title5', 'check')
            self.post_case('title6', 'check')

            response = self.client.get('/cases')
            self.assertEquals(response.status_code, 200)
            cases = json.loads(response.data)
            self.assertEquals(len(cases), 3)

            response = self.client.get('/cases/property/title5')
            self.assertEquals(response.status_code, 200)
            cases = json.loads(response.data)
            self.assertEquals(len(cases), 2)
            self.assertEquals(cases[0]['title_number'], 'title5')
            self.assertEquals(cases[0]['work_queue'], 'casework')
            self.assertEquals(cases[1]['title_number'], 'title5')
            self.assertEquals(cases[1]['work_queue'], 'check')

    def test_complete_case_returns_error_if_already_been_approved(self):
        with self.app.test_request_context():
            self.post_case('title7', 'casework')
            response = self.client.get('/cases/property/title7')
            self.assertEquals(response.status_code, 200)
            case_id = json.loads(response.data)[0]['id']

            first_response = self.client.put('/cases/complete/%s' % case_id)
            self.assertEquals(first_response.status_code, 200)

            second_response = self.client.put('/cases/complete/%s' % case_id)
            self.assertEquals(second_response.status_code, 400)
            self.assertEquals(second_response.data, 'Case: %s has already been approved' % case_id)

    def test_get_cases_by_work_queue_returns_cases_for_status_plus_error(self):
        with self.app.test_request_context():
            self.post_case('title8', 'casework')
            self.post_case('title9', 'casework')

            response = self.client.get('/cases')
            self.assertEquals(response.status_code, 200)
            cases = json.loads(response.data)
            self.assertEquals(len(cases), 2)

            self.assertTrue(service.update_case_with_status(cases[1]['id'], 'error'))

            response = self.client.get('/cases/pending/casework')
            self.assertEquals(response.status_code, 200)
            cases = json.loads(response.data)
            self.assertEquals(len(cases), 2)
            self.assertEquals(cases[0]['title_number'], 'title8')
            self.assertEquals(cases[0]['work_queue'], 'casework')
            self.assertEquals(cases[0]['status'], 'pending')
            self.assertEquals(cases[1]['title_number'], 'title9')
            self.assertEquals(cases[1]['work_queue'], 'casework')
            self.assertEquals(cases[1]['status'], 'error')
