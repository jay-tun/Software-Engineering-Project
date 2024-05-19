import unittest
from unittest.mock import MagicMock, patch
from query_datacube import dbc, dco

class TestDBC(unittest.TestCase):
    def setUp(self):
        self.server_url = "https://ows.rasdaman.org/rasdaman/ows"
        self.dbc = dbc(self.server_url)

    @patch('requests.post')
    def test_send_query_success(self, mock_post):
        # Test sending a query successfully
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Query result"
        mock_post.return_value = mock_response

        wcps_query = "SELECT * FROM data"
        response = self.dbc.send_query(wcps_query)

        # Assert that the correct HTTP POST request was made
        mock_post.assert_called_once_with(
            self.server_url,
            data={'query': wcps_query},
            verify=False
        )
        self.assertEqual(response.content, b"Query result")

    @patch('requests.post')
    def test_send_query_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500  # Internal Server Error
        mock_post.return_value = mock_response

        wcps_query = "INVALID QUERY"
        response = self.dbc.send_query(wcps_query)

        mock_post.assert_called_once_with(
            self.server_url,
            data={'query': wcps_query},
            verify=False
        )
        self.assertEqual(response.status_code, 500)
        self.assertIsNone(response.content)

class TestDCO(unittest.TestCase):
     # Set up a dco instance with a mock dbc instance
    def setUp(self):
        self.server_url = "https://ows.rasdaman.org/rasdaman/ows"
        self.dbc = dbc(self.server_url)
        self.dco = dco(self.dbc)

    def test_w_for(self):
        text = '$c in (AvgTemperatureColorScaled)'
        self.dco.w_for(text)
        self.assertIn(f'for {text}\n', self.dco.query)

    def test_where(self):
        text = '$c in (AvgTemperatureColorScaled)'
        self.dco.where(text)
        self.assertIn(f'where {text}\n', self.dco.query)

    def test_encode(self):
        text = '$c[ansi("2003-03")], "image/png"'
        self.dco.encode(text)
        self.assertIn(f'return \n encode({text})\n', self.dco.query)

    def test_average(self):
        text = '$c[ansi("2015-01")]'
        self.dco.average(text)
        self.assertIn(f'return \n encode(average({text}))\n', self.dco.query)

    def test_minimum(self):
        text = '$c[ansi("2015-01")]'
        self.dco.minimum(text)
        self.assertIn(f'return \n encode(minimum({text}))\n', self.dco.query)

    def test_maximum(self):
        text = '$c[ansi("2015-01")]'
        self.dco.maximum(text)
        self.assertIn(f'return \n encode(maximum({text}))\n', self.dco.query)

    @patch.object(dbc, 'send_query')
    def test_execute(self, mock_send_query):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Query result"
        mock_send_query.return_value = mock_response

        response = self.dco.execute()

        mock_send_query.assert_called_once_with(self.dco.query)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Query result")

if __name__ == '__main__':
    unittest.main()
