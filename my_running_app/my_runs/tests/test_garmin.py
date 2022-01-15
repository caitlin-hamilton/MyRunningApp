from my_runs.garmin import GarminPortal,GarminConnectConnectionError
from unittest import TestCase
import mock


class TestGarmin(TestCase):

    @mock.patch('my_runs.garmin.read_text_file')
    @mock.patch('my_runs.garmin.ROOT_DIR', '/root')
    @mock.patch('my_runs.garmin.os.makedirs')
    @mock.patch('my_runs.garmin.Garmin')
    def test_garmin_portal_init_success(self, mock_garmin, mock_os_makedirs, mock_read_text_file):
        mock_read_text_file.return_value = ('user', 'pw')
        test_garmin = GarminPortal()
        self.assertEqual(mock_garmin(), test_garmin._client)

    @mock.patch('my_runs.garmin.read_text_file')
    @mock.patch('my_runs.garmin.ROOT_DIR', '/root')
    @mock.patch('my_runs.garmin.os.makedirs')
    @mock.patch('my_runs.garmin.Garmin')
    def test_garmin_portal_init_fail(self, mock_garmin, mock_os_makedirs, mock_read_text_file):
        mock_read_text_file.return_value = ('user', 'pw')
        mock_garmin().login.side_effect = GarminConnectConnectionError
        with self.assertRaises(GarminConnectConnectionError):
            GarminPortal()

    @mock.patch('my_runs.garmin.read_text_file')
    @mock.patch('my_runs.garmin.ROOT_DIR', '/root')
    @mock.patch('my_runs.garmin.os.makedirs')
    @mock.patch('my_runs.garmin.Garmin')
    def test_garmin_portal_get_splits(self, mock_garmin, mock_os_makedirs, mock_read_text_file):
        mock_read_text_file.return_value = ('user', 'pw')
        mock_garmin().get_activity_splits.return_value = {'lapDTOs': [
            {'distance': 1000.0, 'elapsedDuration': 100, 'movingDuration': 200},
            {'distance': 89.0, 'elapsedDuration': 100, 'movingDuration': 200},
        ]}
        test_gp = GarminPortal()
        actual_result = test_gp.get_splits_of_activity(100)
        self.assertDictEqual(actual_result, {1: {'elapsed_time': 100, 'moving_time': 200}})

