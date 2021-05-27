"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from levelupapi.models import Event
from levelupreports.views import Connection


def userevent_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    e.id as EventId,
                    e.datetime,
                    g.title as game_name,
                    gr.id as HOST,
                    u.first_name ||' '|| u.last_name as full_name
                FROM
                    levelupapi_event e
                JOIN
                    levelupapi_game g ON e.game_id = g.id
                JOIN
                    levelupapi_gamer gr ON e.host_id = gr.id
                JOIN
                    auth_user u ON gr.id = u.id
            """)

            dataset = db_cursor.fetchall()

            # Take the flat data from the database, and build the
            # following data structure for each event.

            events_by_user = {}

            for row in dataset:
                # Crete a Game instance and set its properties
                event = Event()
                event.name = row["name"]
                game.maker = row["maker"]
                game.difficulty = row["difficulty"]
                game.numberOfPlayers = row["numberOfPlayers"]
                game.game_type_id = row["game_type_id"]

                # Store the user's id
                uid = row["user_id"]

                # If the user's id is already a key in the dictionary...
                if uid in games_by_user:

                    # Add the current game to the `games` list for it
                    games_by_user[uid]['games'].append(game)

                else:
                    # Otherwise, create the key and dictionary value
                    games_by_user[uid] = {}
                    games_by_user[uid]["id"] = uid
                    games_by_user[uid]["full_name"] = row["full_name"]
                    games_by_user[uid]["games"] = [game]

        # Get only the values from the dictionary and create a list from them
        list_of_users_with_games = games_by_user.values()

        # Specify the Django template and provide data context
        template = 'users/list_with_games.html'
        context = {
            'usergame_list': list_of_users_with_games
        }

        return render(request, template, context)


# Note: You are strongly encouraged to take the time to understand the data structure above that is created from the results of the query.
# This is a common strategy for converting flat data from a SQL data set into a data structure to be used in your application.
