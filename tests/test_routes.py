import unittest
from modelo import app

class TestFlaskRoutes(unittest.TestCase):

    def test_classify_route(self):
        with app.test_client() as client:
            response = client.post('/classify', json={"headline": "test headline"})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertIn("result", data)
            self.assertIn("certainty", data)

    def test_get_all_entries_route(self):
        with app.test_client() as client:
            response = client.get('/all_entries')
            self.assertEqual(response.status_code, 200)

    def test_fact_check_route(self):
        with app.test_client() as client:
            response = client.get('/fact_check', query_string={"query": "test"})
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
