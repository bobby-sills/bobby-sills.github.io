import os
import json
import sqlite3
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# Get credentials from environment
credentials_json = os.environ['GOOGLE_CREDENTIALS']
file_id = os.environ['FILE_ID']

# Parse credentials
credentials_info = json.loads(credentials_json)
credentials = service_account.Credentials.from_service_account_info(
    credentials_info,
    scopes=['https://www.googleapis.com/auth/drive.readonly']
)

# Build Drive API client
service = build('drive', 'v3', credentials=credentials)

# Download the file
request = service.files().get_media(fileId=file_id)
file_handle = io.BytesIO()
downloader = MediaIoBaseDownload(file_handle, request)

done = False
while not done:
    status, done = downloader.next_chunk()

# Save to temporary file
with open('koreader.db', 'wb') as f:
    f.write(file_handle.getvalue())

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
def get_yearly_reading_stats():
    """Get daily reading statistics for the past year."""
    # Calculate timestamp for 1 year ago
    one_year_ago = datetime.now() - timedelta(days=365)
    start_timestamp = int(one_year_ago.timestamp())

    sql_query = """
    SELECT dates,
           count(*) AS pages,
           sum(sum_duration) AS durations
    FROM   (
        SELECT strftime('%Y-%m-%d', start_time, 'unixepoch', 'localtime') AS dates,
               sum(duration) AS sum_duration
        FROM   page_stat
        WHERE  start_time >= ?
        GROUP  BY id_book, page, dates
    )
    GROUP  BY dates
    ORDER  BY dates DESC;
    """

    cursor.execute(sql_query, (start_timestamp,))
    results = cursor.fetchall()

    # Convert to list of dictionaries
    daily_stats = []
    for date, pages, duration_seconds in results:
        daily_stats.append({
            "date": date,
            "pages": pages,
            "duration_seconds": duration_seconds,
            "duration_hours": round(duration_seconds / 3600, 2)
        })

    return daily_stats

yearly_stats = get_yearly_reading_stats()

# List of books to track
books_to_track = ["Middlemarch"]

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
