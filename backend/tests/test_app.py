import unittest
from app import app, db
from models import User, File

class FileSharingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        db.connection.drop_database('file_sharing_test')
        self.db = db.get_db()

    def tearDown(self):
      
        self.db.connection.drop_database('file_sharing_test')

    def test_signup(self):
        response = self.app.post('/auth/signup', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'role': 'ClientUser'
        })
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        
        self.app.post('/auth/signup', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'role': 'ClientUser'
        })
        
        response = self.app.post('/auth/login', json={
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_upload_file(self):
       
        self.app.post('/auth/signup', json={
            'username': 'opsuser',
            'email': 'opsuser@example.com',
            'password': 'testpassword',
            'role': 'OpsUser'
        })
        login_response = self.app.post('/auth/login', json={
            'email': 'opsuser@example.com',
            'password': 'testpassword'
        })
        token = login_response.get_json()['token']

        
        response = self.app.post('/file/upload', data={
            'file': (io.BytesIO(b"this is a test file"), 'test.pptx')
        }, headers={'x-access-tokens': token})
        self.assertEqual(response.status_code, 201)

    def test_list_files(self):
        
        self.app.post('/auth/signup', json={
            'username': 'clientuser',
            'email': 'clientuser@example.com',
            'password': 'testpassword',
            'role': 'ClientUser'
        })
        login_response = self.app.post('/auth/login', json={
            'email': 'clientuser@example.com',
            'password': 'testpassword'
        })
        token = login_response.get_json()['token']

      
        response = self.app.get('/file/files', headers={'x-access-tokens': token})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
