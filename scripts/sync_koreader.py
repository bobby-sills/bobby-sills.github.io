import os
import json
import sqlite3
from datetime import datetime, timedelta
import requests
from requests.auth import HTTPBasicAuth

# Get WebDAV credentials from environment
webdav_url = os.environ['WEBDAV_URL']
webdav_username = os.environ['WEBDAV_USERNAME']
webdav_password = os.environ['WEBDAV_PASSWORD']

# Download the file from WebDAV
response = requests.get(
    webdav_url,
    auth=HTTPBasicAuth(webdav_username, webdav_password),
    timeout=30
)
response.raise_for_status()

# Save to temporary file
with open('koreader.db', 'wb') as f:
    f.write(response.content)

# Connect to SQLite database
conn = sqlite3.connect('koreader.db')
cursor = conn.cursor()

# Query reading progress for each book (latest reading session)
cursor.execute("""
    SELECT
        b.title,
        b.authors,
        ROUND((CAST(d.page AS FLOAT) / d.total_pages) * 100, 2) AS percentage_completed,
        d.start_time
    FROM page_stat_data d
    JOIN book b ON b.id = d.id_book
    WHERE d.start_time = (
        SELECT MAX(d1.start_time)
        FROM page_stat_data d1
        WHERE d1.id_book = d.id_book
    )
    ORDER BY percentage_completed ASC
""")

books = cursor.fetchall()

# Query reading statistics for the past year
def get_yearly_reading_stats(tracked_books):
    """Get daily reading statistics for the past year, split by book for tracked books only."""
    # Calculate timestamp for 1 year ago
    one_year_ago = datetime.now() - timedelta(days=365)
    start_timestamp = int(one_year_ago.timestamp())

    # First, get per-book daily stats for tracked books
    book_stats_query = """
    SELECT dates,
           b.title,
           count(*) AS pages,
           sum(sum_duration) AS durations
    FROM   (
        SELECT id_book,
               strftime('%Y-%m-%d', start_time, 'unixepoch', 'localtime') AS dates,
               sum(duration) AS sum_duration
        FROM   page_stat
        WHERE  start_time >= ?
        GROUP  BY id_book, page, dates
    ) ps
    JOIN book b ON b.id = ps.id_book
    WHERE b.title IN ({})
    GROUP  BY dates, b.title
    ORDER  BY dates DESC, b.title;
    """.format(','.join('?' * len(tracked_books)))

    cursor.execute(book_stats_query, (start_timestamp, *tracked_books))
    book_results = cursor.fetchall()

    # Organize by date
    daily_stats_map = {}
    for date, title, pages, duration_seconds in book_results:
        if date not in daily_stats_map:
            daily_stats_map[date] = {
                "date": date,
                "total_pages": 0,
                "total_duration_seconds": 0,
                "books": []
            }

        daily_stats_map[date]["total_pages"] += pages
        daily_stats_map[date]["total_duration_seconds"] += duration_seconds
        daily_stats_map[date]["books"].append({
            "title": title,
            "pages": pages,
            "duration_seconds": duration_seconds,
            "duration_hours": round(duration_seconds / 3600, 2)
        })

    # Convert to list and add total_duration_hours
    daily_stats = []
    for date in sorted(daily_stats_map.keys(), reverse=True):
        day_data = daily_stats_map[date]
        day_data["total_duration_hours"] = round(day_data["total_duration_seconds"] / 3600, 2)
        # Keep legacy fields for backward compatibility
        day_data["pages"] = day_data["total_pages"]
        day_data["duration_seconds"] = day_data["total_duration_seconds"]
        day_data["duration_hours"] = day_data["total_duration_hours"]
        daily_stats.append(day_data)

    return daily_stats

# List of books to track
books_to_track = ["Middlemarch", "Project Hail Mary"]

yearly_stats = get_yearly_reading_stats(books_to_track)

# Filter for specific books
filtered_books = []
for row in books:
    if row[0] in books_to_track:
        book_data = {
            "title": row[0],
            "authors": row[1],
            "percentage_completed": row[2]
        }
        # Add date_completed if book is at 100%
        if row[2] >= 100.0:
            # Format timestamp to match manual-data.json format (e.g., "11 Oct 2025")
            date_obj = datetime.fromtimestamp(row[3])
            book_data["date_completed"] = date_obj.strftime("%d %b %Y")
        filtered_books.append(book_data)

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Split into two separate files
# 1. Book information
book_data = {
    "updated_at": datetime.now().isoformat(),
    "books": filtered_books
}

# 2. Reading statistics (time read per day)
stats_data = {
    "updated_at": datetime.now().isoformat(),
    "yearly_stats": yearly_stats
}

# Write book data file
with open('data/koreader-books.json', 'w') as f:
    json.dump(book_data, f, indent=2)

# Write reading stats file
with open('data/koreader-stats.json', 'w') as f:
    json.dump(stats_data, f, indent=2)

conn.close()
