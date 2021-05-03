# Analytics API Service

A service around the Google analytics API

Usage
-------

All responses will have the form

```json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

Subsequent response definitions will only detail the expected value of the `data field`

Realtime active users, city and page path
-------

**Definition**

`GET /realtime`

**Response**

- `200 OK` on success

```json
{
   "total_active": 11,
   "city":[
      [
         "Cape Town",
         "/",
         "5"
      ],
      ...
   ]
}
```


Total visits
-------

**Definition**

`GET /device-visits`
**Arguments**

- `"start-date":string` start date for fetching Analytics data.
- `"end-date":string` end date for fetching Analytics data.

Requests can specify a date formatted as YYYY-MM-DD, or as a relative date (e.g., today, yesterday or 30daysAgo)

**Response**

- `200 OK` on success

```json
{
   "headers":[
      "ga:deviceCategory",
      "ga:browser",
      "ga:pageviews"
   ],
   "rows":[
      [
         "desktop",
         "Chrome",
         "44336"
      ],
      ...
   ]
}
```

Home page analytics
-------

**Definition**

`GET /home`

**Arguments**

- `"start-date":string` start date for fetching Analytics data. (**required**)
- `"end-date":string` end date for fetching Analytics data. (**required**)

Requests can specify a date formatted as YYYY-MM-DD, or as a relative date (e.g., today, yesterday or 30daysAgo)

**Response**

- `200 OK` on success
```json
   "headers": [
         "ga:users",
         "ga:bounceRate",
         "ga:sessions",
         "ga:avgSessionDuration"
        ],
   "rows": [
      [
         "12345",
         "123.456...",
         "12345",
         "123.456..."
      ]
   ]
```

Daily analytics
-------

**Definition**

`GET /daily`

**Arguments**
- `"metrics":string` a comma-separated list of Analytics metrics. E.g., 'ga:1dayUsers'. At least one metric must be specified. (**required**)
- `"start-date":string` start date for fetching Analytics data. (**required**)
- `"end-date":string` end date for fetching Analytics data. (**required**)

Requests can specify a date formatted as YYYY-MM-DD, or as a relative date (e.g., today, yesterday or 30daysAgo)
**Sample query**
```
GET /daily?metrics=ga:1dayUsers&start-date=7daysAgo&end-date=yesterday
```
**Response**

- `200 OK` on success
```json
"headers": [
   "ga:date",
   "ga:1dayUsers"
],
"rows": [
   [
         "20200722",
         "6259"
   ],
   ...6 more...
]
```

Acquire analytics
-------

**Definition**

`GET /acquire`

Returns for top traffic source and the medium used for specified period together the with number of users.

**Arguments**

- `"start-date":string` start date for fetching Analytics data. (**required**)
- `"end-date":string` end date for fetching Analytics data. (**required**)

Requests can specify a date formatted as YYYY-MM-DD, or as a relative date (e.g., today, yesterday or 30daysAgo)

**Response**

- `200 OK` on success
```json
"headers": [
      "source/medium",
      "users"
],
"rows": [
   [
      "(direct) / (none)",
      "20126"
   ],
   [
      "google / organic",
      "8753"
   ],
   ...
]
```

Custom Usage
-------

See https://ga-dev-tools.appspot.com/dimensions-metrics-explorer/ for the possible dimensions and metrics

**Definition**

`GET /custom`

**Arguments**

- `"start-date":string` start date for fetching Analytics data. (**required**)
- `"end-date":string` end date for fetching Analytics data. (**required**)

- `"metrics":string` a comma-separated list of Analytics metrics. E.g., 'ga:sessions,ga:pageviews'. At least one metric must be specified. (**required**)
- `"dimensions":string` a comma-separated list of Analytics dimensions. E.g., 'ga:browser,ga:city'.

- `"filters":string` a comma-separated list of dimension or metric filters to be applied to Analytics data.

- `"sort":string` a comma-separated list of dimensions or metrics that determine the sort order for Analytics data.

Requests can specify a date formatted as YYYY-MM-DD, or as a relative date (e.g., today, yesterday or 30daysAgo)

**Example Query**
```
GET /custom?start-date=35daysAgo&end-date=today&metrics=ga:pageviews&dimensions=ga:deviceCategory,ga:browser
```

**Response**

- `200 OK` on success

```json
"headers": [
            "ga:deviceCategory",
            "ga:browser",
            "ga:pageviews"
        ],
        "rows": [
            [
                "desktop",
                "Chrome",
                "44336"
            ],
            ...
        ]
    }
```
