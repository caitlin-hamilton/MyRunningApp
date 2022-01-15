from my_runs.garmin import GarminPortal,GarminConnectConnectionError
from unittest import TestCase
from datetime import datetime
import os
import django
import mock

from my_runs.activity_handler import create_split_entry, create_run_entry

class TestActivityHandler(TestCase):

    @mock.patch('my_runs.activity_handler.convert_epoch_to_str')
    @mock.patch('my_runs.activity_handler.Run')
    def test_create_run_entry(self, mock_run, mock_convert_epoch_to_str):
        test_run = {
            'startTimeLocal': 'test 20/12/2020',
            'duration': 12303,
            'activityId': 123,
            'activityName': 'Test',
            'distance': 1000
        }
        mock_convert_epoch_to_str.return_value = datetime.now()
        create_run_entry(test_run)
        self.assertTrue(mock_run().save.assert_called)

    @mock.patch('my_runs.activity_handler.Run')
    def test_create_split_entry(self, mock_run, mock_split):
        test_splits = {1: {'elapsed_time': 120.08565565, 'moving_time': 180.89}}
        create_split_entry(test_splits, mock_run())
        self.assertTrue(mock_split().save.assert_called)