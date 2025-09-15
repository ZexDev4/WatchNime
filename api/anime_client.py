import requests
import random
import base64
from Crypto.Cipher import AES
from faker import Faker
import json

class AnimePlayClient:
    def __init__(self):
        self.faker = Faker()
        self.key_b64 = "YjRjODhlOTRiOTA5YTUzZjMyMmMxZGE4Njk5ZDMxMGU="
        self.iv_b64 = "aHhOZzRyUS14dlhQUWF0dA=="
        self.key = base64.b64decode(self.key_b64)
        self.iv = base64.b64decode(self.iv_b64)
        self.android_versions = ["28","29","30","31","32","33"]
        self.devices = ["ASUS_Z01QD/Asus","Samsung_G988B/Samsung","Xiaomi_Mi11/Xiaomi","Pixel_7/Google"]

    # -------------------------- 
    # AES Encrypt/Decrypt
    # -------------------------- 
    def pkcs7_pad(self, data):
        pad_len = 16 - (len(data) % 16)
        return data + bytes([pad_len] * pad_len)

    def aes_encrypt_email(self, email):
        email_bytes = email.encode()
        padded = self.pkcs7_pad(email_bytes)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(padded)
        return base64.b64encode(encrypted).decode()

    def aes_decrypt(self, cipher_text_b64):
        try:
            cipher_bytes = base64.b64decode(cipher_text_b64)
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            decrypted = cipher.decrypt(cipher_bytes)
            pad_len = decrypted[-1]
            decrypted = decrypted[:-pad_len]
            return decrypted.decode()
        except:
            return cipher_text_b64

    # -------------------------- 
    # Random User-Agent + IP
    # -------------------------- 
    def random_animeplay_ua(self):
        android = random.choice(self.android_versions)
        device = random.choice(self.devices)
        return f"AnimePlay/1.1.7 (Android {android}) {device}"

    def random_ip(self):
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

    def get_ip_info(self, ip):
        try:
            resp = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,org,timezone")
            data = resp.json()
            if data.get("status") == "success":
                org = data.get("org", "Unknown").encode('ascii', 'ignore').decode('ascii')
                country = data.get("country", "ID").encode('ascii', 'ignore').decode('ascii')
                region = data.get("regionName", "West Java").encode('ascii', 'ignore').decode('ascii')
                city = data.get("city", "Bandung").encode('ascii', 'ignore').decode('ascii')
                timezone = data.get("timezone", "Asia/Jakarta").encode('ascii', 'ignore').decode('ascii')
                return {
                    "Country": country,
                    "Region": region,
                    "City": city,
                    "Org": org,
                    "Timezone": timezone
                }
        except:
            pass
        return {"Country": "ID", "Region": "West Java", "City": "Bandung", "Org": "Unknown", "Timezone": "Asia/Jakarta"}

    # -------------------------- 
    # GET all anime episodes
    # -------------------------- 
    def get_all_anime(self):
        ip = self.random_ip()
        info = self.get_ip_info(ip)
        headers = {
            "Host": "cdn.anibox.id",
            "User-Agent": self.random_animeplay_ua(),
            "Client-Ip": ip,
            "Client-Country": info["Country"],
            "Client-City": info["City"],
            "Client-Loc": f"{round(random.uniform(-6.9,-6.1),4)},{round(random.uniform(107.5,107.7),4)}",
            "Client-Org": info["Org"],
            "Client-Postal": "40241",
            "Client-Timezone": info["Timezone"],
        }
        url = "https://cdn.anibox.id/catalog/episodes_anime.json"
        resp = requests.get(url, headers=headers, verify=True)
        decrypted = self.aes_decrypt(resp.text)
        try:
            return json.loads(decrypted)
        except:
            return []

    # -------------------------- 
    # Parse anime episodes
    # -------------------------- 
    def parse_anime(self, anime_all):
        parsed = []
        for ep in anime_all:
            series = ep.get("seri", {})
            parsed.append({
                "series_id": series.get("id"),
                "series_title": series.get("title"),
                "series_image": series.get("image_url"),
                "episode_id": ep.get("id"),
                "episode_number": ep.get("number"),
                "date_created": ep.get("date_created"),
                "total_views": ep.get("total_views"),
                "rating": series.get("rating")
            })
        return parsed

    # -------------------------- 
    # GET all donghua episodes
    # -------------------------- 
    def get_all_donghua(self):
        ip = self.random_ip()
        info = self.get_ip_info(ip)
        headers = {
            "Host": "cdn.anibox.id",
            "User-Agent": self.random_animeplay_ua(),
            "Client-Ip": ip,
            "Client-Country": info["Country"],
            "Client-City": info["City"],
            "Client-Loc": f"{round(random.uniform(-6.9,-6.1),4)},{round(random.uniform(107.5,107.7),4)}",
            "Client-Org": info["Org"],
            "Client-Postal": "40241",
            "Client-Timezone": info["Timezone"],
        }
        url = "https://cdn.anibox.id/catalog/episodes_donghua.json"
        resp = requests.get(url, headers=headers, verify=True)
        decrypted = self.aes_decrypt(resp.text)
        try:
            return json.loads(decrypted)
        except:
            return []

    # -------------------------- 
    # Parse donghua episodes
    # -------------------------- 
    def parse_donghua(self, donghua_all):
        parsed = []
        for ep in donghua_all:
            series = ep.get("seri", {})
            parsed.append({
                "series_id": series.get("id"),
                "series_title": series.get("title"),
                "series_image": series.get("image_url"),
                "episode_id": ep.get("id"),
                "episode_number": ep.get("number"),
                "date_created": ep.get("date_created"),
                "total_views": ep.get("total_views"),
                "rating": series.get("rating")
            })
        return parsed

    # -------------------------- 
    # GET series/video detail for donghua
    # -------------------------- 
    def get_series_detail_donghua(self, series_id):
        email_random = "zexdev4@gmail.com"
        devcode = self.aes_encrypt_email(email_random)

        ip = self.random_ip()
        info = self.get_ip_info(ip)
        headers = {
            "Host": "ap-1.dontol.net",
            "Authorization": f"Bearer {devcode}",
            "User-Agent": self.random_animeplay_ua(),
            "Client-Premium": "false",
            "Client-Subscription": "false",
            "Client-Expiry-Date": "null",
            "Advertising-Id": self.faker.uuid4(),
            "Package-Name": "dev.animeplay.app",
            "Ifps": "true",
            "Client-Ip": ip,
            "Client-City": info["City"],
            "Client-Region": info["Region"],
            "Client-Country": info["Country"],
            "Client-Loc": f"{round(random.uniform(-6.9,-6.1),4)},{round(random.uniform(107.5,107.7),4)}",
            "Client-Org": info["Org"],
            "Client-Postal": "40241",
            "Client-Timezone": info["Timezone"],
        }

        url = (f"https://ap-1.dontol.net/items/series/{series_id}?"
               "fields=*,episodes.id,episodes.number,episodes.total_views,episodes.title_indonesian,episodes.duration,"
               "episodes.thumbnail_url,episodes.date_created&deep[episodes][_limit]=-1")

        resp = requests.get(url, headers=headers, verify=True)
        decrypted = self.aes_decrypt(resp.text)
        try:
            data = json.loads(decrypted)
        except:
            return {}, []

        info_series = data.get('data', {})
        if not info_series:
            return {}, []

        series_info = {
            "id": info_series.get('id'),
            "title": info_series.get('title'),
            "title_english": info_series.get('title_english'),
            "title_japanese": info_series.get('title_japanese'),
            "original_title": info_series.get('title_synonyms'),
            "synopsis": info_series.get('synopsis'),
            "type": info_series.get('type'),
            "status": info_series.get('status'),
            "season": info_series.get('season_status'),
            "studio": info_series.get('studio'),
            "total_episode": info_series.get('total_episode'),
            "latest_episode": info_series.get('latest_episode'),
            "duration": info_series.get('duration'),
            "rating": info_series.get('rating'),
            "popularity": info_series.get('popularity'),
            "total_views": info_series.get('total_views'),
            "broadcast_days": info_series.get('broadcast_days'),
            "broadcast_time": info_series.get('broadcast_time'),
            "image_url": info_series.get('image_url') or info_series.get('original_image_url'),
            "genres": [],
            "recommendations": []
        }

        episodes_list = []
        for ep in info_series.get('episodes', []):
            episodes_list.append({
                "episode_id": ep.get('id'),
                "number": ep.get('number'),
                "views": ep.get('total_views'),
                "duration_min": round(ep['duration']/60, 2) if ep.get('duration') else None,
                "thumbnail": ep.get('thumbnail_url'),
                "date_created": ep.get('date_created')
            })

        return series_info, episodes_list

    # -------------------------- 
    # GET series/video detail for anime
    # -------------------------- 
    def get_series_detail_anime(self, series_id):
        email_random = "zexdev4@gmail.com"
        devcode = self.aes_encrypt_email(email_random)

        ip = self.random_ip()
        info = self.get_ip_info(ip)
        headers = {
            "Host": "ap-1.dontol.net",
            "Authorization": f"Bearer {devcode}",
            "User-Agent": self.random_animeplay_ua(),
            "Client-Premium": "false",
            "Client-Subscription": "false",
            "Client-Expiry-Date": "null",
            "Advertising-Id": self.faker.uuid4(),
            "Package-Name": "dev.animeplay.app",
            "Ifps": "true",
            "Client-Ip": ip,
            "Client-City": info["City"],
            "Client-Region": info["Region"],
            "Client-Country": info["Country"],
            "Client-Loc": f"{round(random.uniform(-6.9,-6.1),4)},{round(random.uniform(107.5,107.7),4)}",
            "Client-Org": info["Org"],
            "Client-Postal": "40241",
            "Client-Timezone": info["Timezone"],
        }

        url = (f"https://ap-1.dontol.net/items/series/{series_id}?"
               "fields=*,season.id,season.name,studio.id,studio.name,genres.genre.id,genres.genre.name,"
               "episodes.id,episodes.number,episodes.total_views,episodes.title_indonesian,episodes.duration,"
               "episodes.thumbnail_url,episodes.date_created&deep[episodes][_limit]=-1")

        resp = requests.get(url, headers=headers, verify=True)
        decrypted = self.aes_decrypt(resp.text)
        try:
            data = json.loads(decrypted)
        except:
            return {}, []

        info_series = data.get('data', {})
        if not info_series:
            return {}, []

        series_info = {
            "id": info_series.get('id'),
            "title": info_series.get('title'),
            "title_english": info_series.get('title_english'),
            "title_japanese": info_series.get('title_japanese'),
            "original_title": info_series.get('title_synonyms'),
            "synopsis": info_series.get('synopsis'),
            "type": info_series.get('type'),
            "status": info_series.get('status'),
            "season": info_series.get('season', {}).get('name'),
            "studio": info_series.get('studio', {}).get('name'),
            "total_episode": info_series.get('total_episode'),
            "latest_episode": info_series.get('latest_episode'),
            "duration": info_series.get('duration'),
            "rating": info_series.get('rating'),
            "popularity": info_series.get('popularity'),
            "total_views": info_series.get('total_views'),
            "broadcast_days": info_series.get('broadcast_days'),
            "broadcast_time": info_series.get('broadcast_time'),
            "image_url": info_series.get('image_url') or info_series.get('original_image_url'),
            "genres": [g['genre']['name'] for g in info_series.get('genres', []) if isinstance(g, dict) and 'genre' in g],
            "recommendations": [
                {"id": r['id'], "title": r['title'], "image_url": r['image_url']} 
                for r in info_series.get('recommendations', []) if isinstance(r, dict)
            ]
        }

        episodes_list = []
        for ep in info_series.get('episodes', []):
            episodes_list.append({
                "episode_id": ep.get('id'),
                "number": ep.get('number'),
                "views": ep.get('total_views'),
                "duration_min": round(ep['duration']/60, 2) if ep.get('duration') else None,
                "thumbnail": ep.get('thumbnail_url'),
                "date_created": ep.get('date_created')
            })

        return series_info, episodes_list

    # -------------------------- 
    # GET series/video detail for search
    # -------------------------- 
    def get_series_detail_search(self, series_id):
        email_random = "zexdev4@gmail.com"
        devcode = self.aes_encrypt_email(email_random)

        ip = self.random_ip()
        info = self.get_ip_info(ip)
        headers = {
            "Host": "ap-1.dontol.net",
            "Authorization": f"Bearer {devcode}",
            "User-Agent": self.random_animeplay_ua(),
            "Client-Premium": "false",
            "Client-Subscription": "false",
            "Client-Expiry-Date": "null",
            "Advertising-Id": self.faker.uuid4(),
            "Package-Name": "dev.animeplay.app",
            "Ifps": "true",
            "Client-Ip": ip,
            "Client-City": info["City"],
            "Client-Region": info["Region"],
            "Client-Country": info["Country"],
            "Client-Loc": f"{round(random.uniform(-6.9,-6.1),4)},{round(random.uniform(107.5,107.7),4)}",
            "Client-Org": info["Org"],
            "Client-Postal": "40241",
            "Client-Timezone": info["Timezone"],
        }

        url = (f"https://ap-1.dontol.net/items/series/{series_id}?"
               "fields=*,season.id,season.name,studio.id,studio.name,genres.genre.id,genres.genre.name,"
               "episodes.id,episodes.number,episodes.total_views,episodes.title_indonesian,episodes.duration,"
               "episodes.thumbnail_url,episodes.date_created,season_status&deep[episodes][_limit]=-1")

        try:
            resp = requests.get(url, headers=headers, verify=True)
            if resp.status_code != 200:
                return {}, []

            decrypted = self.aes_decrypt(resp.text)
            try:
                data = json.loads(decrypted)
            except json.JSONDecodeError:
                return {}, []

            info_series = data.get('data', {})
            if not info_series:
                return {}, []

            season_obj = info_series.get('season', {})
            season_name = season_obj.get('name') if isinstance(season_obj, dict) else None
            season = season_name or info_series.get('season_status')
            
            studio_obj = info_series.get('studio', {})
            studio_name = studio_obj.get('name') if isinstance(studio_obj, dict) else None
            studio = studio_name or info_series.get('studio')
            
            genres_list = info_series.get('genres', [])
            genres = []
            if isinstance(genres_list, list):
                for g in genres_list:
                    if isinstance(g, dict) and 'genre' in g:
                        genre_name = g.get('genre', {}).get('name')
                        if genre_name:
                            genres.append(genre_name)
            
            rec_list = info_series.get('recommendations', [])
            recommendations = []
            if isinstance(rec_list, list):
                for r in rec_list:
                    if isinstance(r, dict) and all(key in r for key in ['id', 'title', 'image_url']):
                        recommendations.append({
                            "id": r['id'],
                            "title": r['title'],
                            "image_url": r['image_url']
                        })

            series_info = {
                "id": info_series.get('id'),
                "title": info_series.get('title'),
                "title_english": info_series.get('title_english'),
                "title_japanese": info_series.get('title_japanese'),
                "original_title": info_series.get('title_synonyms'),
                "synopsis": info_series.get('synopsis'),
                "type": info_series.get('type'),
                "status": info_series.get('status'),
                "season": season,
                "studio": studio,
                "total_episode": info_series.get('total_episode'),
                "latest_episode": info_series.get('latest_episode'),
                "duration": info_series.get('duration'),
                "rating": info_series.get('rating'),
                "popularity": info_series.get('popularity'),
                "total_views": info_series.get('total_views'),
                "broadcast_days": info_series.get('broadcast_days'),
                "broadcast_time": info_series.get('broadcast_time'),
                "image_url": info_series.get('image_url') or info_series.get('original_image_url'),
                "genres": genres,
                "recommendations": recommendations
            }

            episodes_list = []
            episodes_data = info_series.get('episodes', [])
            if isinstance(episodes_data, list):
                for ep in episodes_data:
                    if isinstance(ep, dict):
                        episodes_list.append({
                            "episode_id": ep.get('id'),
                            "number": ep.get('number'),
                            "views": ep.get('total_views'),
                            "duration_min": round(ep.get('duration', 0)/60, 2) if ep.get('duration') else None,
                            "thumbnail": ep.get('thumbnail_url'),
                            "date_created": ep.get('date_created')
                        })

            return series_info, episodes_list

        except requests.RequestException:
            return {}, []

    # -------------------------- 
    # GET episode video
    # -------------------------- 
    def get_video(self, episode_id):
        email_random = "zexdev4@gmail.com"
        devcode = self.aes_encrypt_email(email_random)

        ip = self.random_ip()
        info = self.get_ip_info(ip)
        headers = {
            "Host": "ap-1.dontol.net",
            "Authorization": f"Bearer {devcode}",
            "User-Agent": self.random_animeplay_ua(),
            "Client-Premium": "false",
            "Client-Subscription": "false",
            "Client-Expiry-Date": "null",
            "Advertising-Id": self.faker.uuid4(),
            "Package-Name": "dev.animeplay.app",
            "Ifps": "true",
            "Client-Ip": ip,
            "Client-City": info["City"],
            "Client-Region": info["Region"],
            "Client-Country": info["Country"],
            "Client-Loc": f"{round(random.uniform(-6.9,-6.1),4)},{round(random.uniform(107.5,107.7),4)}",
            "Client-Org": info["Org"],
            "Client-Postal": "40241",
            "Client-Timezone": info["Timezone"],
        }

        url = f"https://ap-1.dontol.net/episodes/{episode_id}/videos"
        resp = requests.get(url, headers=headers, verify=True)
        decrypted = self.aes_decrypt(resp.text)
        try:
            return json.loads(decrypted)
        except:
            return {}

    # -------------------------- 
    # SEARCH series
    # -------------------------- 
    def search(self, keyword="naruto", page=1, limit=25, sort="title"):
        email_random = "zexdev4@gmail.com"
        devcode = self.aes_encrypt_email(email_random)

        ip = self.random_ip()
        info = self.get_ip_info(ip)

        headers = {
            "Host": "ap-1.dontol.net",
            "Authorization": f"Bearer {devcode}",
            "User-Agent": self.random_animeplay_ua(),
            "Client-Premium": "false",
            "Client-Subscription": "false",
            "Client-Expiry-Date": "null",
            "Advertising-Id": self.faker.uuid4(),
            "Package-Name": "dev.animeplay.app",
            "Ifps": "true",
            "Client-Ip": ip,
            "Client-City": info["City"],
            "Client-Region": info["Region"],
            "Client-Country": info["Country"],
            "Client-Loc": f"{round(random.uniform(-6.9,-6.1),4)},{round(random.uniform(107.5,107.7),4)}",
            "Client-Org": info["Org"],
            "Client-Postal": "40241",
            "Client-Timezone": info["Timezone"],
        }

        params = {
            'search': keyword,
            'page': str(page),
            'sort': sort,
            'fields': 'id,title,rating,latest_episode,image_url,broadcast,type,date_created',
            'limit': str(limit),
            'filter[status][_eq]': 'published'
        }

        try:
            resp = requests.get(
                'https://ap-1.dontol.net/items/series',
                params=params,
                headers=headers,
                verify=True
            )
            decrypted = self.aes_decrypt(resp.text)
            return json.loads(decrypted)
        except Exception as e:
            print(f"[!] Search failed: {e}")
            return {}
