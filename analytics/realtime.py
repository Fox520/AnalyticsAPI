import time
from flask import session
from flask_restful import Resource

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
KEY_FILE_LOCATION = "keys/client-secrets.json"
VIEW_ID = ""


def initialize_service():
    """
    Returns:
        https://googleapis.github.io/google-api-python-client/docs/dyn/analytics_v3.data.html
        An authorized data resource service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES
    )

    # Build the service object.
    return build("analytics", "v3", credentials=credentials).data()


def get_realtime_report():
    result = (
        service.realtime()
        .get(ids=VIEW_ID, metrics="rt:activeUsers", dimensions="ga:city,ga:pagePath")
        .execute()
    )
    return [result.get("totalsForAllResults").get("rt:activeUsers"), result.get("rows")]


service = initialize_service()


class RealTime(Resource):
    def get(self):
        if session.get("last_time_fetch") == None:
            r = get_realtime_report()
            recent_data = {
                "data": {"total_active": r[0], "city": r[1]},
                "message": "success",
            }
            session["recent_data"] = recent_data
            session["last_time_fetch"] = time.time()
            return recent_data, 200
        elif time.time() - session.get("last_time_fetch") < 60:
            return session.get("recent_data"), 200
        else:
            r = get_realtime_report()
            recent_data = {
                "data": {"total_active": r[0], "city": r[1]},
                "message": "success",
            }
            session["recent_data"] = recent_data
            session["last_time_fetch"] = time.time()
            return recent_data, 200
