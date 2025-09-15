from flask import Flask, jsonify, request
from api.anime_client import AnimePlayClient

app = Flask(__name__)
client = AnimePlayClient()

@app.route('/api/anime', methods=['GET'])
def get_all_anime():
    try:
        anime_all = client.get_all_anime()
        parsed_anime = client.parse_anime(anime_all)
        return jsonify({"data": parsed_anime})
    except Exception as e:
        return jsonify({"error": f"Failed to fetch anime: {str(e)}"}), 500

@app.route('/api/donghua', methods=['GET'])
def get_all_donghua():
    try:
        donghua_all = client.get_all_donghua()
        parsed_donghua = client.parse_donghua(donghua_all)
        return jsonify({"data": parsed_donghua})
    except Exception as e:
        return jsonify({"error": f"Failed to fetch donghua: {str(e)}"}), 500

@app.route('/api/anime/<series_id>', methods=['GET'])
def get_anime_series(series_id):
    try:
        series_info, episodes = client.get_series_detail_anime(series_id)
        if not series_info and not episodes:
            return jsonify({"error": f"Anime series with ID {series_id} not found"}), 404
        return jsonify({"series_info": series_info, "episodes": episodes})
    except Exception as e:
        return jsonify({"error": f"Failed to fetch anime series: {str(e)}"}), 500

@app.route('/api/donghua/<series_id>', methods=['GET'])
def get_donghua_series(series_id):
    try:
        series_info, episodes = client.get_series_detail_donghua(series_id)
        if not series_info and not episodes:
            return jsonify({"error": f"Donghua series with ID {series_id} not found"}), 404
        return jsonify({"series_info": series_info, "episodes": episodes})
    except Exception as e:
        return jsonify({"error": f"Failed to fetch donghua series: {str(e)}"}), 500

@app.route('/api/series/<series_id>', methods=['GET'])
def get_series_detail(series_id):
    """
    Get details of a series (anime or donghua) by series ID.
    Returns series information and episode list.
    Example: GET /api/series/123
    """
    try:
        series_info, episodes = client.get_series_detail_search(series_id)
        if not series_info and not episodes:
            return jsonify({"error": f"Series with ID {series_id} not found"}), 404
        return jsonify({
            "series_info": series_info,
            "episodes": episodes,
            "type": series_info.get("type", "unknown").lower()  # Indicate if anime or donghua
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch series details: {str(e)}"}), 500

@app.route('/api/search', methods=['GET'])
def search_series():
    """
    Search for series by keyword.
    Query params: keyword (default: 'naruto'), page (default: 1), limit (default: 25), sort (default: 'title')
    Example: GET /api/search?keyword=naruto&page=1&limit=10&sort=title
    """
    try:
        keyword = request.args.get('keyword', 'naruto')
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 25, type=int)
        sort = request.args.get('sort', 'title')
        results = client.search(keyword, page, limit, sort)
        if not results.get("data"):
            return jsonify({"error": f"No series found for keyword '{keyword}'"}), 404
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

@app.route('/api/episode/<episode_id>/video', methods=['GET'])
def get_episode_video(episode_id):
    try:
        video_data = client.get_video(episode_id)
        if not video_data:
            return jsonify({"error": f"Video for episode ID {episode_id} not found"}), 404
        return jsonify(video_data), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch video: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
