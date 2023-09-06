# Playlist

## Setup
```
mkdir myfolder
cd myfolder
git clone https://github.com/AnkitKachhadiya/playlist.git
```

### Client
```
cd client
```
- For installing dependencies
```
npm i 
#or 
npm i --force 
```

- For formatting files
```
npm run format
```

- For linting
```
npm run lint
```

- For running tests (make sure that backend is running else tests will fail)
```
npm test
```

- Set the `apiURL` in `.src/config/settings.json` according to which your backend is running at (default `url` is already provided).

- For running client
```
npm run dev
```
- Your terminal should display the `url` on which client is running or try [http://localhost:5173/](http://localhost:5173/) 

### Server

```
cd server
```
- Create and activate a virtual environment for your Python backend. Visit [here](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) to learn how to do one.
- Install `pip`. Visit [here](https://pip.pypa.io/en/stable/installation/) to learn how to install.


- For installing dependencies
```
pip install -r requirements.txt
```

- Create `.env` file using `.env.sample` and provide valid values for the `DB` configuration.

- Run below command to create database table and for normalizing `playlist.json` data (make sure your database is running and `.env` file has all the connection details).
```
python setup.py
```

- Run server
```
flask --app app run
```

- For running tests
- Note: After running tests your database will get reset.
```
python -m pytest
```

## Project

- Used `React` for the frontend and various libraries
- Used `Flask` for backend
- Data normalization: `PostgreSQL` for database