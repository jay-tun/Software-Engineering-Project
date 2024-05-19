import unittest
from unittest.mock import patch, Mock
from requests.exceptions import HTTPError
import sys
sys.path.append('../src/wdc')
from wdc import DatabaseConnection  # Ensure you import your class correctly

class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        """Setup for all tests; create a DatabaseConnection instance."""
        self.endpoint_url = "https://ows.rasdaman.org/rasdaman/ows"
        self.db_connection = DatabaseConnection(self.endpoint_url)

    @patch('requests.post')  # Make sure to patch 'requests.post' in the correct location
    def test_send_request_success(self, mock_post):
        """Test send_request successfully gets data from the server using a WCPS query."""
        # Create a mock response object with necessary attributes
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b'Successful response'
        mock_post.return_value = mock_response
        
        # Execute the function under test using a WCPS query example
        wcps_query = "for $c in (AvgLandTemp) return encode($c, 'csv')"
        response = self.db_connection.send_request(wcps_query)
        
        # Assertions to verify the expected outcomes
        self.assertEqual(response.content, b'Successful response')
        mock_post.assert_called_once_with(self.endpoint_url, data={'query': wcps_query}, verify=False)

    @patch('requests.post')
    def test_send_request_http_error(self, mock_post):
        """Test send_request handling HTTPError correctly using a WCPS query."""
        # Setup the mock to raise an HTTPError
        wcps_query = "for $c in (AvgLandTemp) return encode($c, 'csv')"
        mock_post.side_effect = HTTPError("HTTP Error occurred")
        
        # Execute the function under test
        response = self.db_connection.send_request(wcps_query)
        
        # Assertions to verify the expected outcomes
        self.assertIsNone(response)
        mock_post.assert_called_once_with(self.endpoint_url, data={'query': wcps_query}, verify=False)

    @patch('requests.post')
    def test_send_request_general_exception(self, mock_post):
        """Test send_request handling general exceptions with a WCPS query."""
        # Setup the mock to raise a general exception
        wcps_query = "for $c in (AvgLandTemp) return encode($c, 'csv')"
        mock_post.side_effect = Exception("General Error occurred")
        
        # Execute the function under test
        response = self.db_connection.send_request(wcps_query)
        
        # Assertions to verify the expected outcomes
        self.assertIsNone(response)
        mock_post.assert_called_once_with(self.endpoint_url, data={'query': wcps_query}, verify=False)

if __name__ == '__main__':
    unittest.main()
