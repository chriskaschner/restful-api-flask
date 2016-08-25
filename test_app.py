import pytest
import os
import tempfile
###todo fix this to import from different folder location
import original_app
import unittest
import json
import requests
from base64 import b64encode
username = 'ReturnPath'
password = 'python'

headers = {
    'Authorization': 'Basic ' + b64encode("{0}:{1}".format(username, password))
}

class AppTestCase(unittest.TestCase):
    def setUp(self):
        # self.db_fd, zoriginal_app.app.config['DATABASE'] = tempfile.mkstemp()
        original_app.app.config['TESTING'] = True
        self.app = original_app.app.test_client()

    def tearDown(self):
        # os.close(self.db_fd)
        # os.unlink(zoriginal_app.app.config['DATABASE'])
        pass

    def test_correct_response_code(self):
        """Check that root exists"""
        rv = self.app.get('/img/api/v1.0/images')
        self.assertEquals(rv.status_code, 200)
        assert 'images' in rv.data

    def test_non_existing_url(self):
        """Check that 404 gets thrown for a root address that doesn't exist"""
        rv = self.app.get('/a-bad-address')
        self.assertEquals(rv.status_code, 404)

    def test_individual_image_that_exists(self):
        """Check that an image exists"""
        rv = self.app.get('/img/api/v1.0/images/2',
        headers=headers)
        self.assertEquals(rv.status_code, 200)

    def test_individual_image_that_doesnt_exist(self):
        """Check that 404 gets thrown for an image address that doesn't exist"""
        rv = self.app.get('/img/api/v1.0/images/crazy-non-existing')
        self.assertEquals(rv.status_code, 404)

    def test_create_new_image(self):
        """create a new image file using JSON and POST"""
        rv=self.app.post('/img/api/v1.0/images',
           data=json.dumps(dict(url='http://imgdirect.s3-website-us-west-2.amazonaws.com/neither.jpg')),
           content_type = 'application/json',
           headers=headers)
        self.assertEquals(rv.status_code, 201)
        self.assertIn('neither.jpg',rv.data)

    def test_create_not_json_new_image(self):
        """attempt to create an image without JSON"""
        rv=self.app.post('/img/api/v1.0/images',
           data='http://imgdirect.s3-website-us-west-2.amazonaws.com/neither.jpg',
           content_type = 'application/json',
           headers=headers)
        self.assertEquals(rv.status_code, 400)

    def test_created_image_now_exists(self):
        """Check that previosuly created image exists"""
        rv = self.app.get('/img/api/v1.0/images/3',
        headers=headers)
        self.assertEquals(rv.status_code, 200)
        self.assertIn('neither.jpg',rv.data)

    def test_update_existing_image(self):
        """Update existing image title"""
        rv=self.app.put('/img/api/v1.0/images/3',
           data=json.dumps(dict(title='C-ron-ron')),
           content_type = 'application/json',
           headers=headers)
        self.assertEquals(rv.status_code, 200)
        self.assertIn('C-ron-ron',rv.data)

    def test_put_inference_on_image(self):
        """Use PUT to run inference on an image"""
        rv=self.app.put('/img/api/v1.0/inference/3',
           data=json.dumps(dict(id=3)),
           content_type = 'application/json',
           headers=headers)
        self.assertEquals(rv.status_code, 200)
        self.assertIn('0.8584',rv.data)
        self.assertIn('\"uri\": \"http:',rv.data)

    def test_get_inference_on_image(self):
        """Try to use GET to run inference on an image"""
        rv=self.app.get('/img/api/v1.0/inference/3',
           data=json.dumps(dict(id=3)),
           content_type = 'application/json',
           headers=headers)
        self.assertEquals(rv.status_code, 405)

    def test_put_image_size(self):
        """Use PUT to determine image size"""
        rv=self.app.put('/img/api/v1.0/resize/3',
           data=json.dumps(dict(id=3)),
           content_type = 'application/json',
           headers=headers)
        self.assertEquals(rv.status_code, 200)
        self.assertIn('\"uri\": \"http:',rv.data)

    def test_get_image_size(self):
        """Attempt to use GET for image size"""
        rv=self.app.get('/img/api/v1.0/resize/3',
           data=json.dumps(dict(id=3)),
           content_type = 'application/json',
           headers=headers)
        self.assertEquals(rv.status_code, 405)

    def test_z_delete_existing_image(self):
        """Does a record get deleted correctly"""
        rv=self.app.delete('/img/api/v1.0/images/3',
           content_type = 'application/json',
           headers=headers)
        self.assertEquals(rv.status_code, 200)
        self.assertIn('true',rv.data)

if __name__ == '__main__':
        unittest.main()
# @pytest.fixture
# def client(request):
#     db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
#     flaskr.app.config['TESTING'] = True
#     client = flaskr.app.test_client()
#     with flaskr.app.app_context():
#         flaskr.init_db()
#
#     def teardown():
#         os.close(db_fd)
#         os.unlink(flaskr.app.config['DATABASE'])
#     request.addfinalizer(teardown)
#
#     return client
#
#
# def login(client, username, password):
#     return client.post('/login', data=dict(
#         username=username,
#         password=password
#     ), follow_redirects=True)
#
#
# def logout(client):
#     return client.get('/logout', follow_redirects=True)
