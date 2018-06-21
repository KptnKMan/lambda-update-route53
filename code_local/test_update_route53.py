import unittest

# import module/script for test
# import update_route53
# alternatively and better for readability use only sub-function:
from update_route53 import check_ip

import mock

test_table = [
    (("https://someurl.com", "1.2.3.4"), "1.2.3.4"),
    (("https://someurl.com", None), "1.2.3.4"),
    (("someurl.com", "1.2.3.4"), "1.2.3.4"),
    (("someurl", "1.2.3.4"), "1.2.3.4"),
    (("1.1.1.1", "1.2.3.4"), "1.2.3.4"),
    (("!#$^(&%#@!", "1.2.3.4"), "1.2.3.4"),
    (("https://someurl.com", "1.2.3.4"), "")
]


# define a function that can do anything
def mocked_urllib_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, response_string):
            self.response_string = response_string

        def read(self):
            return self.response_string

    test_urls = {test[0][0]: test[1] for test in test_table}
    if args[0] in test_urls:
        return MockResponse(test_urls[args[0]])

    return MockResponse('')


# create TestCase class
class CheckIpTestCase(unittest.TestCase):

    @mock.patch("urllib.urlopen", side_effect=mocked_urllib_get)
    def test_check_ip_manual(self, mock_urlopen):
        """
        testing manually supplying an IP to function
        """

        for test in test_table:

            # set variable to be tested
            # ip = test[0][1]

            # setup running of function
            result = check_ip(test[0][0], test[0][1])

            # setup assert of expected response
            self.assertEqual(result, test[1])


# declare entry point
if __name__ == '__main__':
    unittest.main()
