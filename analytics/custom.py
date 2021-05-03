import time
from flask_restful import Resource, reqparse

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
KEY_FILE_LOCATION = "keys/client-secrets.json"
VIEW_ID = ""

custom_get_args = reqparse.RequestParser()
custom_get_args.add_argument(
    "start-date",
    type=str,
    help="Start date for fetching analytics data.",
    required=True,
)
custom_get_args.add_argument(
    "end-date", type=str, help="End date for fetching analytics data.", required=True
)

custom_get_args.add_argument(
    "metrics",
    type=str,
    help="A comma-separated list of Analytics metrics. E.g., 'ga:sessions,ga:pageviews'. At least one metric must be specified.",
    required=True,
)

custom_get_args.add_argument(
    "dimensions",
    type=str,
    help="A comma-separated list of Analytics dimensions. E.g., 'ga:browser,ga:city'.",
    required=False,
)

custom_get_args.add_argument(
    "filters",
    type=str,
    help="A comma-separated list of dimension or metric filters to be applied to Analytics data.",
    required=False,
)

custom_get_args.add_argument(
    "sort",
    type=str,
    help="A comma-separated list of dimensions or metrics that determine the sort order for Analytics data.",
    required=False,
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


def get_custom_report(
    _start, _end, _metrics, _dimensions=None, _filters=None, _sort=None
):
    result = (
        service.ga()
        .get(
            ids=VIEW_ID,
            metrics=_metrics,
            dimensions=_dimensions,
            start_date=_start,
            end_date=_end,
            sort=_sort,
            filters=_filters,
        )
        .execute()
    )
    output = {"headers": [d["name"] for d in result.get("columnHeaders")]}
    output["rows"] = result.get("rows")

    return output


service = initialize_service()


class Custom(Resource):
    def get(self):
        args = custom_get_args.parse_args()
        try:
            result = get_custom_report(
                args.get("start-date"),
                args.get("end-date"),
                args.get("metrics"),
                args.get("dimensions"),
                args.get("filters"),
                args.get("sort"),
            )
            return {"data": result, "message": "success"}, 200
        except Exception as e:
            return {"data": None, "message": str(e)}, 400
