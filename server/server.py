from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from configs.config import Config

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

# Development mode: Enable CORS for frontend dev server
if app.debug:
    CORS(app)
# Production mode: Serve static files
else:
    app = Flask(__name__,
                static_folder='../frontend/build',
                static_url_path='')
    
    @app.route('/')
    def serve():
        return app.send_static_file('index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(app.static_folder, path)

config = Config()

@app.route('/api/teams', methods=['GET'])
def get_teams():
    """Get all teams"""
    try:
        teams = config.get_teams()
        return jsonify({'teams': teams}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/teams/<team_name>', methods=['GET'])
def get_team_info(team_name):
    """Get team configuration"""
    try:
        team_config = config.get_team_config(team_name)
        if team_config:
            return jsonify(team_config), 200
        return jsonify({'error': 'Team not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/teams/<team_id>/groups', methods=['GET'])
def get_team_groups(team_id):
    """Get groups for a team"""
    try:
        groups = config.get_groups(team_id)
        print(groups)
        if groups:
            return jsonify({'groups': groups}), 200
        return jsonify({'error': 'Team not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/teams/<team_name>/groups/<group_name>', methods=['GET'])
def get_group_info(team_name, group_name):
    """Get group configuration"""
    try:
        group_config = config.get_group_config(team_name, group_name)
        if group_config:
            return jsonify(group_config), 200
        return jsonify({'error': 'Group not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config', methods=['GET'])
def get_all_config():
    """Get entire configuration"""
    try:
        return jsonify(config.get_all_config()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
