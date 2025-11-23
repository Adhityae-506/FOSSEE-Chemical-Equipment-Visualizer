import io
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from .utils import parse_and_summarize_csv
from rest_framework.authtoken.models import Token

User = get_user_model()

class UtilsTests(APITestCase):
    def test_parse_valid_csv(self):
        csv = "equipment_name,type,flowrate,pressure,temperature\nPump1,Centrifugal,120.5,1.2,85.0\nValve2,Ball,80.0,1.0,25.5\n"
        f = io.StringIO(csv)
        summary, df = parse_and_summarize_csv(f)
        self.assertEqual(summary['total_equipment'], 2)
        self.assertAlmostEqual(summary['average_flowrate'], round((120.5+80.0)/2, 2))

    def test_missing_column(self):
        csv = "equipment_name,type,pressure,temperature\nPump1,C,1.2,85.0"
        f = io.StringIO(csv)
        with self.assertRaises(ValueError) as cm:
            parse_and_summarize_csv(f)
        self.assertIn("missing required column", str(cm.exception))

class APITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user).key

    def test_upload_requires_auth(self):
        url = '/api/datasets/upload/'
        with open('tests_sample.csv', 'w') as fh:
            fh.write("equipment_name,type,flowrate,pressure,temperature\nPump1,C,10,1,20\n")
        # no auth
        with open('tests_sample.csv', 'rb') as f:
            res = self.client.post(url, {'file': f})
        self.assertEqual(res.status_code, 401)

    def test_upload_valid(self):
        url = '/api/auth/login/'
        # login
        r = self.client.post('/api/auth/login/', {'username':'testuser','password':'testpass'}, format='json')
        self.assertEqual(r.status_code, 200)
        token = r.data['token']
        url = '/api/datasets/upload/'
        csv = "equipment_name,type,flowrate,pressure,temperature\nPump1,Centrifugal,120.5,1.2,85.0\n"
        with io.BytesIO(csv.encode('utf-8')) as f:
            f.name = 'sample.csv'
            res = self.client.post(url, {'file': f}, HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(res.status_code, 201)
        self.assertIn('summary', res.data)
