import json


def test_index(app, client):
    response = client.get("/")
    assert "Playlist" == response.data.decode(
        "utf-8"
    ), "Error: data mismatch for index route"
    assert response.status_code == 200, "Error: invalid response code for index route"


def test_get_songs(app, client):
    response1 = client.get("/songs")
    assert response1.status_code == 200, "Error: invalid response code for /songs route"

    response2 = client.get(
        "/songs", query_string={"page": 0, "column": "title", "direction": "asc"}
    )
    assert response2.status_code == 200, "Error: invalid response code for /songs route"
    data2 = json.loads(response2.data.decode())
    assert data2 is not None
    assert "songs" in data2
    assert "totalSongs" in data2


def test_update_song_rating(app, client):
    response1 = client.patch(
        "/songs/editRating", data=json.dumps({}), content_type="application/json"
    )
    data1 = response1.data.decode()
    assert json.loads(data1) == {"serverResponse": "Invalid song id"}
    assert response1.status_code == 400

    response2 = client.patch(
        "/songs/editRating",
        data=json.dumps({"id": ""}),
        content_type="application/json",
    )
    data2 = response2.data.decode()
    assert json.loads(data2) == {"serverResponse": "Song not found"}
    assert response2.status_code == 404

    response3 = client.patch(
        "/songs/editRating",
        data=json.dumps({"id": "wgewegwegwg", "newRating": 6}),
        content_type="application/json",
    )
    data3 = response3.data.decode()
    assert json.loads(data3) == {"serverResponse": "Rating must be from 0 to 5"}
    assert response3.status_code == 400


def test_get_all_songs(app, client):
    response1 = client.get("/songs/all")
    assert response1.status_code == 200
    data1 = json.loads(response1.data.decode())

    assert data1 is not None


def test_search_songs(app, client):
    response1 = client.get("/songs/search", query_string={"query": "a"})
    assert response1.status_code == 200
    data1 = json.loads(response1.data.decode())

    assert data1 is not None
    assert "songs" in data1
    assert "totalSongs" in data1
    assert len(data1["songs"]) > 0


def test_get_histogram(app, client):
    response1 = client.get("/songs/histogram")
    assert response1.status_code == 200
    data1 = json.loads(response1.data.decode())

    assert data1 is not None
    assert len(data1) > 0


def test_get_bar_chart(app, client):
    response1 = client.get("/songs/barChart")
    assert response1.status_code == 200
    data1 = json.loads(response1.data.decode())

    assert data1 is not None
    assert "acoustics" in data1
    assert "tempo" in data1


def test_get_scatter_chart(app, client):
    response1 = client.get("/songs/scatterChart")
    assert response1.status_code == 200
    data1 = json.loads(response1.data.decode())

    assert data1 is not None
    assert len(data1) > 0
