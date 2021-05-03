import time
from flask_restful import Resource, reqparse

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
KEY_FILE_LOCATION = "keys/client-secrets.json"
VIEW_ID = ""

visits_get_args = reqparse.RequestParser()
visits_get_args.add_argument(
    "start-date",
    type=str,
    help="Start date for fetching analytics data.",
    required=True,
)
visits_get_args.add_argument(
    "end-date", type=str, help="End date for fetching analytics data.", required=True
)


home_get_args = reqparse.RequestParser()
home_get_args.add_argument(
    "start-date",
    type=str,
    help="Start date for fetching analytics data.",
    required=True,
)
home_get_args.add_argument(
    "end-date", type=str, help="End date for fetching analytics data.", required=True
)

daily_get_args = reqparse.RequestParser()
daily_get_args.add_argument(
    "metrics",
    type=str,
    help="A comma-separated list of Analytics metrics. E.g., 'ga:1dayUsers'. At least one metric must be specified.",
    required=True,
)
daily_get_args.add_argument(
    "start-date",
    type=str,
    help="Start date for fetching analytics data.",
    required=True,
)
daily_get_args.add_argument(
    "end-date", type=str, help="End date for fetching analytics data.", required=True
)


acquire_get_args = reqparse.RequestParser()
acquire_get_args.add_argument(
    "start-date",
    type=str,
    help="Start date for fetching analytics data.",
    required=True,
)
acquire_get_args.add_argument(
    "end-date", type=str, help="End date for fetching analytics data.", required=True
)


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


def get_devices_report(_start, _end):
    result = (
        service.ga()
        .get(
            ids=VIEW_ID,
            metrics="ga:users,ga:newUsers",
            dimensions="ga:deviceCategory",
            start_date=_start,
            end_date=_end,
        )
        .execute()
    )
    output = {"headers": [d["name"] for d in result.get("columnHeaders")]}
    output["rows"] = result.get("rows")

    return output


def get_home_report(_start, _end):
    result = (
        service.ga()
        .get(
            ids=VIEW_ID,
            metrics="ga:users,ga:bounceRate,ga:sessions,ga:avgSessionDuration",
            start_date=_start,
            end_date=_end,
        )
        .execute()
    )
    output = {"headers": [d["name"] for d in result.get("columnHeaders")]}
    output["rows"] = result.get("rows")

    return output


def get_daily_report(_metrics, _start, _end):
    result = (
        service.ga()
        .get(
            ids=VIEW_ID,
            metrics=_metrics,  # ga:1dayUsers
            dimensions="ga:date",
            start_date=_start,
            end_date=_end,
        )
        .execute()
    )
    output = {"headers": [d["name"] for d in result.get("columnHeaders")]}
    output["rows"] = result.get("rows")

    return output


def get_lowest(high):
    low = 9999999999999
    index = -1
    i = 0
    for e in high:
        if int(e[1]) < low:
            low = int(e[1])
            index = i
        i += 1
    return low, index


def acquire_report(_start, _end):
    result = (
        service.ga()
        .get(
            ids=VIEW_ID,
            metrics="ga:users",
            dimensions="ga:sourceMedium",
            start_date=_start,
            end_date=_end,
        )
        .execute()
    )
    output = {"headers": ["source/medium", "users"]}
    # Sort by number of users
    high = []
    for entry in result.get("rows"):
        ll = get_lowest(high)
        if len(high) < 4:
            high.append(entry)
        elif int(entry[1]) > ll[0]:
            high.pop(ll[1])
            high.append(entry)
    # count others
    others = 0
    for entry in result.get("rows"):
        if entry not in high:
            others += int(entry[1])
    high.append(["others", others])
    output["rows"] = str(high)

    return output


service = initialize_service()


class Visits(Resource):
    def get(self):
        args = visits_get_args.parse_args()
        try:
            result = get_devices_report(args.get("start-date"), args.get("end-date"))
            return {"data": result, "message": "success"}, 200
        except Exception as e:
            return {"data": None, "message": str(e)}, 400


class Home(Resource):
    def get(self):
        args = home_get_args.parse_args()
        try:
            result = get_home_report(args.get("start-date"), args.get("end-date"))
            return {"data": result, "message": "success"}, 200
        except Exception as e:
            return {"data": None, "message": str(e)}, 400


class Daily(Resource):
    def get(self):
        args = daily_get_args.parse_args()
        try:
            result = get_daily_report(
                args.get("metrics"), args.get("start-date"), args.get("end-date")
            )
            return {"data": result, "message": "success"}, 200
        except Exception as e:
            return {"data": None, "message": str(e)}, 400


class Acquire(Resource):
    def get(self):
        args = acquire_get_args.parse_args()
        try:
            result = acquire_report(args.get("start-date"), args.get("end-date"))
            return {"data": result, "message": "success"}, 200
        except Exception as e:
            return {"data": None, "message": str(e)}, 400

