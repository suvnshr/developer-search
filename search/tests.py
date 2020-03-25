from django.test import TestCase
from django.conf import settings

# Create your tests here.


class ProductionTestCase(TestCase):

    def test_is_debug_off(self):
        """ ensures that the project has DEBUG set to False """

        self.assertFalse(settings.DEBUG, "DEBUG is ON, not ready for production !")


    def test_is_https_forced(self):
        """ 
            ensures that the settings which ensure that https is enforced on site, 
            are enabled and correct. 
        """

        self.assertTrue(hasattr(settings, 'SECURE_PROXY_SSL_HEADER'),
                        "SSL header setting not present")
        self.assertTrue(hasattr(settings, 'SECURE_SSL_REDIRECT'),
                        "SSL redirect setting not present")

        self.assertEqual(
            settings.SECURE_PROXY_SSL_HEADER,
            ('HTTP_X_FORWARDED_PROTO', 'https'), "SSL Header setting wrong"
        )

        self.assertTrue(settings.SECURE_SSL_REDIRECT,
                        "SSL redirect setting wrong")
