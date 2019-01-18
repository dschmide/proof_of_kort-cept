from django.test import TestCase, Client


class UserAttributes(TestCase):
    base_url = '/api/kort-cept'

    def test_attributes_get_no_user(self):
        # Create an instance of a GET request.
        c = Client()
        response = c.get(self.base_url + '/api/user_attributes/')
        self.assertEqual(response.status_code, 401)

    def test_attributes_wrongdata_notloggedin(self):
        # Create an instance of a POST request.
        c = Client()
        response = c.post(self.base_url + '/api/user_attributes/', {'koins': 'abc'})  # noqa
        print(response.content)
        self.assertEqual(response.status_code, 400)

    def test_attributes_deleteUser(self):
        # Create an instance of a POST request.
        c = Client()
        response = c.delete(
            self.base_url + '/api/user_attributes/1/'
        )
        print(response.content)
        self.assertEqual(response.status_code, 401)

    def test_attributes_updateUser(self):
        # Create an instance of a POST request.
        c = Client()
        response = c.put(
            self.base_url + '/api/user_attributes/1/',
            {
                'koins': 99,
                'towers': 99
            }
        )
        print(response.content)
        self.assertEqual(response.status_code, 401)


class LoginTests(TestCase):
    base_url = '/api/kort-cept'

    def test_auth_ok_nomail(self):
        # Create an instance of a POST request.
        c = Client()
        response = c.post(self.base_url + '/auth/users/create/', {'username': 'testuser', 'password': '1234ASDF'})  # noqa
        self.assertEqual(response.status_code, 201)

    def test_auth_badpw(self):
        # Create an instance of a POST request.
        c = Client()
        response = c.post(self.base_url + '/auth/users/create/', {'username': 'testuser2', 'password': 'asdf'})  # noqa
        self.assertEqual(response.status_code, 400)

    def test_auth_ok_withmail(self):
        # Create an instance of a POST request.
        c = Client()
        response = c.post(
            self.base_url + '/auth/users/create/',
            {'username': 'testuser3', 'password': '1234ASDF', 'email': 'asdfghj@gmail.com'}  # noqa
        )
        self.assertEqual(response.status_code, 201)

    def test_auth_ok_badmail(self):
        # Create an instance of a POST request.
        c = Client()
        response = c.post(
            self.base_url + '/auth/users/create/', {'username': 'testuser3', 'password': '1234ASDF', 'email': 'asdfgh'}  # noqa
        )
        self.assertEqual(response.status_code, 400)

    def test_login_correct(self):
        # Create an instance of a POST request.
        c = Client()
        # Create a User
        response = c.post(
            self.base_url + '/auth/users/create/',
            {'username': 'testuser3', 'password': '1234ASDF', 'email': 'asdfghj@gmail.com'}  # noqa
        )
        # Login with the same User, get a token
        response = c.post(
            self.base_url + '/auth/jwt/create/', {'username': 'testuser3', 'password': '1234ASDF'}  # noqa
        )
        print("token: ")
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_login_correct_post(self):
        # Create an instance of a POST request.
        c = Client()
        # Create a User
        response = c.post(
            self.base_url + '/auth/users/create/',
            {'username': 'testuser3', 'password': '1234ASDF', 'email': 'asdfghj@gmail.com'}  # noqa
        )
        # Login with the same User, get a token
        response = c.post(
            self.base_url + '/auth/jwt/create/', {'username': 'testuser3', 'password': '1234ASDF'}  # noqa
        )
        print("token: ")
        # print(response.context_data)
        # print(response.context['token'])
        self.assertEqual(response.status_code, 200)
