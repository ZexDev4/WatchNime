from flask import Flask, jsonify, request
from api.anime_client import AnimePlayClient

app = Flask(__name__)
client = AnimePlayClient()

@app.route('/api/anime', methods=['GET'])
def get_all_anime():
    anime_all = client.get_all_anime()
    parsed_anime = client.parse_anime(anime_all)
    return jsonify({"data": parsed_anime})

@app.route('/api/donghua', methods=['GET'])
def get_all_donghua():
    donghua_all = client.get_all_donghua()
    parsed_donghua = client.parse_donghua(donghua_all)
    return jsonify({"data": parsed_donghua})

@app.route('/api/anime/<series_id>', methods=['GET'])
def get_anime_series(series_id):
    series_info, episodes = client.get_series_detail_anime(series_id)
    return jsonify({"series_info": series_info, "episodes": episodes})

@app.route('/api/donghua/<series_id>', methods=['GET'])
def get_donghua_series(series_id):
    series_info, episodes = client.get_series_detail_donghua(series_id)
    return jsonify({"series_info": series_info, "episodes": episodes})

@app.route('/api/search', methods=['GET'])
def search_series():
    keyword = request.args.get('keyword', 'naruto')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 25, type=int)
    sort = request.args.get('sort', 'title')
    results = client.search(keyword, page, limit, sort)
    return jsonify(results)

@app.route('/api/series/<series_id>', methods=['GET'])
def get_series_detail(series_id):
    series_info, episodes = client.get_series_detail_search(series_id)
    return jsonify({"series_info": series_info, "episodes": episodes})

@app.route('/api/episode/<episode_id>/video', methods=['GET'])
def get_episode_video(episode_id):
    video_data = client.get_video(episode_id)
    return jsonify(video_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
