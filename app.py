from flask import Flask, jsonify, request
from api.anime_client import AnimePlayClient

app = Flask(__name__)
client = AnimePlayClient()

@app.route('/api/populer_episodes', methods=['GET'])
def get_populer_episodes():
    try:
        episodes = client.get_populer_episodes()
        parsed_episodes = client.parse_episodes(episodes)
        return jsonify({"status": "success", "data": parsed_episodes}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/series/<series_id>', methods=['GET'])
def get_series_detail(series_id):
    try:
        series_info, episodes = client.get_series_detail(series_id)
        if not series_info:
            return jsonify({"status": "error", "message": "Series not found"}), 404
        return jsonify({"status": "success", "series": series_info, "episodes": episodes}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/episode/<episode_id>/video', methods=['GET'])
def get_video(episode_id):
    try:
        videos = client.get_video(episode_id)
        if not videos:
            return jsonify({"status": "error", "message": "No videos found"}), 404
        return jsonify({"status": "success", "data": videos}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search():
    try:
        keyword = request.args.get('keyword', 'naruto')
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 25, type=int)
        sort = request.args.get('sort', 'title')
        search_results = client.search(keyword, page, limit, sort)
        parsed_results = client.parse_search_results(search_results)
        return jsonify({"status": "success", "data": parsed_results}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
