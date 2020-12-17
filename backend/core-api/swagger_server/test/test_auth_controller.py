# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.token_data import TokenData  # noqa: E501
from swagger_server.models.user_data import UserData  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAuthController(BaseTestCase):
    """AuthController integration test stubs"""

    def test_change_password(self):
        """Test case for change_password

        User change password
        """
        query_string = [('email', 'email_example'),
                        ('newPassword', 'newPassword_example'),
                        ('recoveryCode', 'recoveryCode_example')]
        response = self.client.open(
            '/api/auth/password/change',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_check_recovery_password(self):
        """Test case for check_recovery_password

        Recovery password check
        """
        query_string = [('email', 'email_example'),
                        ('recoveryCode', 'recoveryCode_example')]
        response = self.client.open(
            '/api/auth/password/recovery/check',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login(self):
        """Test case for login

        User login
        """
        body = UserData()
        response = self.client.open(
            '/api/auth/login/email',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_logout(self):
        """Test case for logout

        User logout
        """
        response = self.client.open(
            '/api/auth/logout',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_recovery_password(self):
        """Test case for recovery_password

        Recovery password
        """
        query_string = [('email', 'email_example')]
        response = self.client.open(
            '/api/auth/password/recovery',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
