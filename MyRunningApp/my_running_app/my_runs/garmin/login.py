from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

from datetime import date
from MyRunningApp.MyRunningApp.my_running_app.config.credentials import user_name, pw


"""
Enable debug logging
"""
import logging
logging.basicConfig(level=logging.DEBUG)

today = date.today()


"""
Initialize Garmin client with credentials
Only needed when your program is initialized
"""
print("Garmin(email, password)")
print("----------------------------------------------------------------------------------------")
try:
    client = Garmin(user_name, pw)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client init: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client init")
    quit()

"""
Login to Garmin Connect portal
Only needed at start of your program
The library will try to relogin when session expires
"""
print("client.login()")
print("----------------------------------------------------------------------------------------")
try:
    client.login()
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client login: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client login")
    quit()

"""
Get full name from profile
"""
print("client.get_full_name()")
print("----------------------------------------------------------------------------------------")
try:
    print(client.get_full_name())
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get full name: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get full name")
    quit()

print("client.get_activities(0,1)")
print("----------------------------------------------------------------------------------------")
try:
    activities = client.get_activities(0,1) # 0=start, 1=limit
    print(activities)
    import csv
    keys = activities[0].keys()
    output_file = f"./activity.csv"
    with open(output_file, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(activities)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get activities: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get activities")
    quit()
try:
    for activity in activities:
        activity_id = activity["activityId"]
        print("client.download_activities(%s)", activity_id)
        print("----------------------------------------------------------------------------------------")

        csv_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.CSV)
        output_file = f"./{str(activity_id)}.csv"
        with open(output_file, "wb") as fb:
          fb.write(csv_data)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occurred during Garmin Connect Client get activity data: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occurred during Garmin Connect Client get activity data")
    quit()