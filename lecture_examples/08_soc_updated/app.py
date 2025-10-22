from flask import Flask
from app.api.players.routes import register_player_routes
from app.api.teams.routes import register_team_routes
from app.api.colleges.routes import register_college_routes


def create_app():
    app = Flask(__name__)
    register_player_routes(app)
    register_team_routes(app)
    register_college_routes(app)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
