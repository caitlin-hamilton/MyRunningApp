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
import csv

logging.basicConfig(level=logging.DEBUG)
URL = 'https://connect.garmin.com/modern/proxy/activity-service/activity/4347437241'


class GarminPortal:
    _client = None

    def __init__(self):
        self.activity_summary_output_path = os.path.join(ROOT_DIR, 'my_runs', 'garmin', str(date.today()))
        self._create_output_directory()
        self._user_name, self._pw = read_text_file(os.path.join(ROOT_DIR, 'config/credentials.txt'))
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

    def get_activity(self):
        activity = self._client.fetch_data(URL)
        return [activity]

    def get_summary_activities(self, activity_range: tuple):
        return self._client.get_activities(*activity_range)

    def get_splits_of_activity(self, activity_id):
        logging.info('Hello')
        splits = self._client.get_activity_splits(activity_id)
        for split in splits:
            if split['distance'] == 1000.0: #sometimes I press wrong button on watch and split != 1 km
                return {
                    'elapsed_time': split['elapsedDuration'],
                    'moving_time': split['movingDuration'],
                    'avg_pace': split["averageSpeed"]
                }

    # def get_splits_of_activity(self, activity_id):
    #     #turn this into a generator
    #     splits = {}
    #     csv_data = self._client.download_activity(activity_id, dl_fmt=self._client.ActivityDownloadFormat.CSV)
    #     split_activity_data = csv_data.split(b"\n")
    #     for row_number, split in enumerate(split_activity_data):
    #         if row_number == 0:
    #             row_headings = split.decode("utf-8").split(",")
    #             for index, heading in enumerate(row_headings):
    #                 if heading == 'Time':
    #                     elapsed_time_index = index
    #                 elif heading == 'Moving Time':
    #                     moving_time_index = index
    #                 elif heading == 'Avg Pace':
    #                     avg_pace = index
    #         elif row_number in [len(split_activity_data) - 1, len(split_activity_data) - 2]:
    #             # -1, -2 are summary rows not data rows
    #             continue
    #         else:
    #             split = split.decode("utf-8").split(",")
    #             data = {'elapsed_time': split[elapsed_time_index], 'moving_time': split[moving_time_index],
    #                     'avg_pace': split[avg_pace]}
    #             splits[split[0]] = data
    #     return splits

    def download_splits_of_activities(self, activities):
        try:
            for activity in activities:
                activity_id = activity["activityId"]
                csv_data = self._client.download_activity(activity_id, dl_fmt=self._client.ActivityDownloadFormat.CSV)
                output_file = os.path.join(self.activity_summary_output_path, '{}.csv'.format(str(activity_id)))
                with open(output_file, "wb") as output_file:
                    output_file.write(csv_data)

        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as err:
            print("Error occurred during Garmin Connect Client get activity data: %s" % err)
            raise err
        except Exception:  # pylint: disable=broad-except
            print("Unknown error occurred during Garmin Connect Client get activity data")
            raise Exception


if __name__ == '__main__':
    gp = GarminPortal()
    activities = gp.get_new_summary_activities((0, 3))



