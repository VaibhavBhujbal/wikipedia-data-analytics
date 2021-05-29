from app import app
import unittest
app.testing = True


class FlaskTest(unittest.TestCase):

    def test_query_mysql(self):
        with app.test_client() as client:
            expected_data = """b'[{"cat_files":0,"cat_id":1,"cat_pages":51,"cat_subcats":1,
            "cat_title":"Category_needed"}]\\n' """
            sent = {'query': 'select * from category limit 1;'}
            result = client.post('/', json=sent)
            self.assertEqual(result.status_code, 200)
            self.assertEqual(str(result.data), str(expected_data))

    def test_get_outdated_page(self):
        with app.test_client() as client:
            expected_data = """b'[{"page_id":321249}]\\n'"""
            result = client.get('/?category=Living people')
            self.assertEqual(result.status_code, 200)
            self.assertEqual(str(result.data), str(expected_data))



