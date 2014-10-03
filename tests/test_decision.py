import unittest
import json
import responses
from application.server import app
from application.decision import Decision

class TestDecisionCase(unittest.TestCase):
    CASE = {"data": "{\"action\":\"change of name\"}"}

    def test_post(self):
        #decision = Decision(self)
        #decision.post(self.CASE)

        pass