from datetime import date
import os
import logging
from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)  # #https://pypi.org/project/garminconnect/

from my_runs.utils import read_text_file
from manage import ROOT_DIR


class GarminPortal:
    _client = None

    def __init__(self):
        self.activity_summary_output_path = os.path.join(ROOT_DIR, 'my_runs', 'garmin', str(date.today()))
        self._create_output_directory()
        self._user_name, self._pw = read_text_file(os.path.join(ROOT_DIR, 'config/credentials.txt')) #more secure
        self._initialize_garmin_client()
        self._login_to_garmin_portal()

    def _create_output_directory(self):
        os.makedirs(self.activity_summary_output_path, exist_ok=True)

    def _initialize_garmin_client(self):
        try:
            self._client = Garmin(self._user_name, self._pw)
        except (
                GarminConnectConnectionError,
                GarminConnectAuthenticationError,
                GarminConnectTooManyRequestsError,
        ) as err:
            print("Error occurred during Garmin Connect Client init: %s" % err)
            raise err
        except Exception:  # pylint: disable=broad-except
            print("Unknown error occurred during Garmin Connect Client init")
            raise Exception

    def _login_to_garmin_portal(self):
        """
        Login to Garmin Connect portal
        Only needed at start of your program
        The library will try to relogin when session expires
        """
        try:
            self._client.login()
        except (
                GarminConnectConnectionError,
                GarminConnectAuthenticationError,
                GarminConnectTooManyRequestsError,
        ) as err:
            print("Error occurred during Garmin Connect Client login: %s" % err)
            raise err
        except Exception:  # pylint: disable=broad-except
            print("Unknown error occurred during Garmin Connect Client login")
            raise Exception

    def get_summary_activities(self, activity_range: tuple):
        return self._client.get_activities(*activity_range)

    def get_splits_of_activity(self, activity_id: int):
        split_data = self._client.get_activity_splits(activity_id)
        splits = {}
        for split_number, split in enumerate(split_data['lapDTOs']):
            if split['distance'] == 1000.0: #sometimes I press wrong button on watch and split != 1 km
                splits[split_number + 1] = {
                    'elapsed_time': split['elapsedDuration'],
                    'moving_time': split['movingDuration']
                }
        return splits




