from flask import Flask, request
from flask_cors import CORS
from psycopg2.extras import RealDictCursor
from db import get_db_connection, close_db_connection
import simplejson as _json

app = Flask(__name__)
CORS(app)

ErrorCode = {
    "BAD_REQUEST": 400,
    "NOT_FOUND": 404,
    "INTERNAL_SERVER_ERROR": 500,
}

LIMIT = 10


@app.route("/")
def index():
    return "Playlist"


@app.route("/songs", methods=["GET"])
def get_songs():
    page_number = int(request.args.get("page", 0))
    column_to_sort = request.args.get("column", "").lower()
    direction_to_sort = request.args.get("direction", "").upper()

    return get_songs_by_filter(page_number, column_to_sort, direction_to_sort)


@app.route("/songs/editRating", methods=["PATCH"])
def update_song_rating():
    song_id = request.json.get("id", None)

    if song_id is None:
        return (
            _json.dumps({"serverResponse": "Invalid song id"}),
            ErrorCode["BAD_REQUEST"],
        )

    try:
        new_rating = int(request.json.get("newRating", None))
    except TypeError:
        new_rating = 0

    if not 0 <= new_rating <= 5:
        return (
            _json.dumps({"serverResponse": "Rating must be from 0 to 5"}),
            ErrorCode["BAD_REQUEST"],
        )

    song = get_song_by_id(song_id)

    if not song:
        return (
            _json.dumps({"serverResponse": "Song not found"}),
            ErrorCode["NOT_FOUND"],
        )

    update_query = f"""
    UPDATE SONGS
    SET RATING = %(rating)s
    WHERE ID = %(id)s
    """

    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute(update_query, {"rating": new_rating, "id": song_id})

    update_row_count = cursor.rowcount

    cursor.close()
    close_db_connection(connection)

    if update_row_count == 1:
        return _json.dumps({"message": "Rating updated"})

    return (
        _json.dumps({"serverResponse": "Could not update song rating"}),
        ErrorCode["INTERNAL_SERVER_ERROR"],
    )


@app.route("/songs/all", methods=["GET"])
def get_all_songs():
    select_query = f"""
    SELECT *
    FROM SONGS
    """

    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute(select_query)

    songs = cursor.fetchall()

    cursor.close()
    close_db_connection(connection)

    return _json.dumps(songs)


@app.route("/songs/search", methods=["GET"])
def search_songs():
    query = request.args.get("query", "").strip()

    print(query)

    if len(query) < 1:
        return get_songs_by_filter()

    select_query = f"""
    SELECT
        ID,
        TITLE,
        DANCEABILITY,
        ENERGY,
        MODE,
        ACOUSTICNESS,
        TEMPO,
        DURATION_MS,
        NUM_SECTIONS,
        NUM_SEGMENTS,
        RATING
    FROM SONGS
    WHERE TITLE ILIKE %s
    ORDER BY TITLE ASC
    LIMIT {LIMIT}
    """

    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    search_pattern = "%{}%".format(query)

    cursor.execute(select_query, (search_pattern,))

    songs = cursor.fetchall()
    result = {"songs": songs, "totalSongs": len(songs)}

    cursor.close()
    close_db_connection(connection)

    return _json.dumps(result)


@app.route("/songs/histogram", methods=["GET"])
def get_histogram():
    select_query = f"""
    SELECT TITLE, ROUND(DURATION_MS / 1000) AS DURATION_S
    FROM SONGS
    ORDER BY TITLE ASC
    """

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(select_query)

    songs = cursor.fetchall()

    return songs


@app.route("/songs/barChart", methods=["GET"])
def get_bar_chart():
    select_query = f"""
    SELECT TITLE,
        ACOUSTICNESS,
        TEMPO
    FROM SONGS
    ORDER BY TITLE ASC
    """

    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute(select_query)

    songs = cursor.fetchall()

    if len(songs) < 1:
        return []

    result = {"acoustics": [], "tempo": []}

    for song in songs:
        result["acoustics"].append([song["title"], song["acousticness"]])
        result["tempo"].append([song["title"], song["tempo"]])

    return _json.dumps(result)


@app.route("/songs/scatterChart", methods=["GET"])
def get_scatter_chart():
    select_query = f"""
    SELECT TITLE,
        DANCEABILITY
    FROM SONGS
    ORDER BY TITLE ASC
    """

    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute(select_query)

    songs = cursor.fetchall()

    if len(songs) < 1:
        return []

    result = []

    for song in songs:
        result.append([song["title"], song["danceability"]])

    return _json.dumps(result)


def get_songs_by_filter(page_number=0, column="", direction=""):
    select_query = f"""
    SELECT ID,
        TITLE,
        DANCEABILITY,
        ENERGY,
        MODE,
        ACOUSTICNESS,
        TEMPO,
        DURATION_MS,
        NUM_SECTIONS,
        NUM_SEGMENTS,
        RATING
    FROM SONGS
    {get_order_by_clause(column, direction)}
    OFFSET %(offset)s
    LIMIT {LIMIT}
    """

    OFFSET = page_number * LIMIT

    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        select_query,
        {"offset": OFFSET},
    )

    songs = cursor.fetchall()

    cursor.close()
    close_db_connection(connection)

    count = get_total_songs()

    result = {"songs": songs, "totalSongs": count["total_songs"]}

    return _json.dumps(result)


def get_song_by_id(id):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    select_query = f"""
    SELECT ID
    FROM SONGS
    WHERE ID = %(id)s
    LIMIT 1
    """

    cursor.execute(
        select_query,
        {"id": id},
    )

    song = cursor.fetchone()

    cursor.close()
    close_db_connection(connection)

    return song


def get_sorting_column(column_to_sort):
    column = column_to_sort.lower()

    sorting_columns = (
        "id",
        "title",
        "danceability",
        "energy",
        "mode",
        "acousticness",
        "tempo",
        "duration_ms",
        "num_sections",
        "num_segments",
        "rating",
    )

    return column if column in sorting_columns else ""


def get_sorting_direction(direction_to_sort):
    direction = direction_to_sort.upper()

    sorting_directions = ("ASC", "DESC")

    return direction if direction in sorting_directions else ""


def get_order_by_clause(column, direction):
    direction = get_sorting_direction(direction)
    column = get_sorting_column(column)

    return f"ORDER BY {column} {direction}" if len(column) > 0 else ""


def get_total_songs():
    select_query = f"""
    SELECT COUNT(ID) AS TOTAL_SONGS
    FROM SONGS
    """

    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute(select_query)

    count = cursor.fetchone()

    cursor.close()
    close_db_connection(connection)

    return count
