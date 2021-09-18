import os
from config import environ
from sys import platform
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db_drop_and_create_all

database_path = environ['PROD_DATABASE_URL']

class TestPricelee(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # db_drop_and_create_all(self.db)

        # Test data
        self.user_id = '112442572274179169362'
        self.manager_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJpclpNMkJSN1o5Z19PcFI1OVlrUSJ9.eyJpc3MiOiJodHRwczovL2ZzLXdlYmRldi5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTI0NDI1NzIyNzQxNzkxNjkzNjIiLCJhdWQiOlsiY29mZmVlc2hvcCIsImh0dHBzOi8vZnMtd2ViZGV2LmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MzE5MDU0NDgsImV4cCI6MTYzMTk5MTg0OCwiYXpwIjoiZ1dXOEVqb2VON21QZzUyUzV5R1BxdGF3QmJ5M0xoRDEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkZWFscyIsInBvc3Q6ZHJpbmtzIiwicG9zdDpmaWx0ZXJzIl19.ba-GOvUx3IG3qDMBvE1gGMMVb6ViNeFwtWbpjf480Vx5LGRDGOEd_zvQ-3eWdOTC1yBUlpGvia1131EVqy4y_9yhAXJI8K6NmZCAVuTIgfociStl0POUjtArpUjKsc_xlqxJj1jKzSNrYiUSSZa7YVmj-yuOAXNvqQrr11PJ6iJSHYAHLBuReTG7wCS1lWhrw76U2dPHiBRAdBL5NNhgWrzAsIYvpDBV6LHGso039LMHX6Uhre-lQkA_AHUnb5w5IRDIAq0uQDMCS9_FX_sZKA2hgRMQcdNiekmdv7dbcyVCcJFVvTULRrG5luFMXH0NmnutSUlDFyeYRaRZoeQXjA'
        self.admin_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJpclpNMkJSN1o5Z19PcFI1OVlrUSJ9.eyJpc3MiOiJodHRwczovL2ZzLXdlYmRldi5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTI0NDI1NzIyNzQxNzkxNjkzNjIiLCJhdWQiOlsiY29mZmVlc2hvcCIsImh0dHBzOi8vZnMtd2ViZGV2LmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MzE5MDU0NDgsImV4cCI6MTYzMTk5MTg0OCwiYXpwIjoiZ1dXOEVqb2VON21QZzUyUzV5R1BxdGF3QmJ5M0xoRDEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkZWFscyIsInBvc3Q6ZHJpbmtzIiwicG9zdDpmaWx0ZXJzIl19.ba-GOvUx3IG3qDMBvE1gGMMVb6ViNeFwtWbpjf480Vx5LGRDGOEd_zvQ-3eWdOTC1yBUlpGvia1131EVqy4y_9yhAXJI8K6NmZCAVuTIgfociStl0POUjtArpUjKsc_xlqxJj1jKzSNrYiUSSZa7YVmj-yuOAXNvqQrr11PJ6iJSHYAHLBuReTG7wCS1lWhrw76U2dPHiBRAdBL5NNhgWrzAsIYvpDBV6LHGso039LMHX6Uhre-lQkA_AHUnb5w5IRDIAq0uQDMCS9_FX_sZKA2hgRMQcdNiekmdv7dbcyVCcJFVvTULRrG5luFMXH0NmnutSUlDFyeYRaRZoeQXjA'
        self.new_user = {
            'user_id': '105407191042025854556',
            'email': 'bzinouba1347@gmail.com',
            'user_name': 'bzinouba1347'
        }
        self.new_deal = {
            'deal_name': 'Dell 27 Curved Gaming Monitor - S2722DGM Featuring FreesSync Premium',
            'deal_link': 'https://deals.dell.com/en-us/productdetail/ag5n',
            'deal_image': 'https://snpi.dell.com/snp/images/products/large/en-us~210-AZZP/210-AZZP.jpg',
            'deal_price': 299.99,
            'deal_currency': 'USD',
            'deal_store': 'Dell'
        }
        self.get_auth_alerts = {
            'user_id': self.user_id,
            'page_number': 1
        }
        self.get_unauth_alerts = {
            'user_id': '1',
            'page_number': 1
        }
        self.new_auth_alert = {
            'user_id': self.user_id,
            'desired_price': 25.0,
            'product_id': '110538092605',
            # 'product_name': 'Laptop battery for DELL Latitude 6MT4T E5470 E5570 7.6V 62Wh',
            # 'product_link': 'https://cgi.sandbox.ebay.com/Laptop-battery-DELL-Latitude-6MT4T-E5470-E5570-7-6V-62Wh-/110538092605',
            # 'product_image': 'https://thumbs2.sandbox.ebaystatic.com/m/m24uZs-gnzxrtT1_19PUQxw/140.jpg',
            # 'product_price': 'USD 28.5',
            # 'product_store': 'ebay'
        }
        self.new_unauth_alert = {
            'user_id': '1',
            'desired_price': 25.0,
            'product_id': '110538092605',
            'product_name': 'Laptop battery for DELL Latitude 6MT4T E5470 E5570 7.6V 62Wh',
            'product_link': 'https://cgi.sandbox.ebay.com/Laptop-battery-DELL-Latitude-6MT4T-E5470-E5570-7-6V-62Wh-/110538092605',
            'product_image': 'https://thumbs2.sandbox.ebaystatic.com/m/m24uZs-gnzxrtT1_19PUQxw/140.jpg',
            'product_price': 'USD 28.5',
            'product_store': 'ebay'
        }
        self.edit_auth_alert = {
            'user_id': self.user_id,
            'alert_id': 1,
            'new_desired_price': 23
        }
        self.edit_unauth_alert = {
            'user_id': '1',
            'alert_id': 1,
            'new_desired_price': 25
        }
        self.del_auth_alert = {
            'user_id': self.user_id,
            'alert_id': 2
        }
        self.del_unauth_alert = {
            'user_id': '1',
            'alert_id': 2
        }
        self.new_filter = {
            'filter': 'price'
        }
        self.new_search = {
            'keywords': 'laptop',
            'filters': {
                'location': '',
                'min_price': '',
                'max_price': '',
                'store': 'ebay',
                'categoryId': ''
            },
            'page_number': 1
        }
        
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_add_user_200(self):
        """ Response must return 200 - new user successfully added"""
        response = self.client().post('/user', json=self.new_user)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    def test_add_user_400(self):
        """ Response must return a Bad Request"""
        response = self.client().post('/user')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Bad Request')

    def test_get_search_filters_200(self):
        """ Response must return 200 - a list of available filters"""
        response = self.client().get('/filters')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data['success'])
        # self.assertTrue(response_data['filters'])

    def test_add_search_filter_200(self):
        """ Response must return 200 - new filter successfully added"""
        headers = {
            'Authorization': 'Bearer ' + self.manager_token
        }
        response = self.client().post('/filters', 
                                    json=self.new_filter,
                                    headers=headers )
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    def test_add_search_filter_401(self):
        """ Response must return 401 - an Auth error"""
        response = self.client().post('/filters', json=self.new_filter)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data['success'], False)

    def test_add_deal_200(self):
        """ Response must return 200 - new deal successfully added"""
        headers = {
            'Authorization': 'Bearer ' + self.admin_token
        }
        response = self.client().post('/deals', 
                                    json=self.new_deal,
                                    headers=headers)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    def test_add_deal_401(self):
        """ Response must return 401 - an Auth error"""
        response = self.client().post('/deals', json=self.new_deal)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data['success'], False)

    def test_search_stores_200(self):
        """ Response must return 200 - a products list"""
        response = self.client().post('/search', json=self.new_search)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['total_items'])

    def test_search_stores_400(self):
        """ Response must return a Bad Request"""
        response = self.client().post('/search')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Bad Request')

    def test_get_recent_alerts_200(self):
        """ Response must return 200 - user's recent alerts list"""
        response = self.client().post('/recent_alerts', json=self.get_auth_alerts)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['total_items'])

    def test_get_recent_alerts_404(self):
        """ Response must return 404 - Not Found"""
        response = self.client().post('/recent_alerts', json=self.get_unauth_alerts)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)

    def test_get_alerts_200(self):
        """ Response must return 200 - user's alerts list"""
        response = self.client().post('/alerts', json=self.get_auth_alerts)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['total_items'])

    def test_get_alerts_404(self):
        """ Response must return 404 - Not Found"""
        response = self.client().post('/alerts', json=self.get_unauth_alerts)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)

    def test_add_alert_200(self):
        """ Response must return 200 - new alert successfully added"""
        response = self.client().post('/alerts/add', json=self.new_auth_alert)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    def test_add_alert_404(self):
        """ Response must return 404 - Not Found error"""
        response = self.client().post('/alerts/add', json=self.new_unauth_alert)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)

    def test_edit_alert_200(self):
        """ Response must return 200 - alert successfully edited"""
        response = self.client().patch('/alerts', json=self.edit_auth_alert)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    def test_edit_alert_404(self):
        """ Response must return 404 - Not Found error"""
        response = self.client().patch('/alerts', json=self.edit_unauth_alert)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)

    def test_delete_alert_200(self):
        """ Response must return 200 - alert successfully deleted"""
        response = self.client().delete('/alerts', json=self.del_auth_alert)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    def test_delete_alert_404(self):
        """ Response must return 404 - Not Found error"""
        response = self.client().delete('/alerts', json=self.del_unauth_alert)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['success'], False)

if __name__ == "__main__":
    unittest.main()