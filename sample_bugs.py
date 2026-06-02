# sample_bugs.py — Example bug reports to test your system

SAMPLE_BUGS = [
    {
        "id": "BUG-001",
        "title": "Login page crashes on submit with empty password",
        "description": """
            When a user clicks the Login button without entering a password,
            the entire page crashes with a JavaScript TypeError: Cannot read
            properties of null (reading 'length'). This happens on Chrome 124,
            Firefox 120, and Safari 17. Affects 100% of users who make this mistake.
            No error message is shown, just a white screen.
        """,
        "reporter": "QA Team",
        "environment": "Production v2.3.1",
    },
    {
        "id": "BUG-002",
        "title": "API returns 500 when date parameter is in DD/MM/YYYY format",
        "description": """
            The /api/reports endpoint returns HTTP 500 Internal Server Error
            when the date query parameter uses DD/MM/YYYY format (e.g. 25/12/2024).
            Works fine with YYYY-MM-DD format. Backend Python code likely uses
            datetime.strptime without handling multiple formats.
        """,
        "reporter": "API Team",
        "environment": "Staging",
    }
]