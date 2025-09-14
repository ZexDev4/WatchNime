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
                return {
                    "Country": data.get("country","ID"),
                    "Region": data.get("regionName","West Java"),
                    "City": data.get("city","Bandung"),
                    "Org": data.get("org","Unknown"),
                    "Timezone": data.get("timezone","Asia/Jakarta")
                }
        except:
            pass
        return {"Country":"ID","Region":"West Java","City":"Bandung","Org":"Unknown","Timezone":"Asia/Jakarta"}

    def get_populer_episodes(self):
        ip = self.random_ip()
        info = self.get_ip_info(ip)
        headers = {
            "Host": "cdn.anibox.id",
            "User-Agent": self.random_animeplay_ua(),
            "Client-Ip": ip,
            "Client-Country": info["Country"],
            "Client-City": info["City"],
            "Client-Org": info["Org"],
            "Client-Postal": "40241",
            "Client-Timezone": info["Timezone"],
            "Accept-Encoding": "gzip, deflate, br"
        }
        url = "https://cdn.anibox.id/catalog/episodes_all.json"
        resp = requests.get(url, headers=headers, verify=True)
        decrypted = self.aes_decrypt(resp.text)
        try:
            return json.loads(decrypted)
        except:
            return []

    def parse_episodes(self, episodes_all):
        parsed = []
        for ep in episodes_all:
            series = ep["seri"]
            parsed.append({
                "series_id": series["id"],
                "series_title": series["title"],
                "series_image": series["image_url"],
                "episode_id": ep["id"],
                "episode_number": ep["number"],
                "date_created": ep["date_created"],
                "total_views": ep["total_views"],
                "rating": series.get("rating")
            })
        return parsed

    def get_series_detail(self, series_id):
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
            "Accept-Encoding": "gzip, deflate, br"
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

        series_info = {
            "id": info_series.get('id'),
            "title": info_series.get('title'),
            "title_english": info_series.get('title_english'),
            "title_japanese": info_series.get('title_japanese'),
            "original_title": info_series.get('original_title'),
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
            "genres": [g['genre']['name'] for g in info_series.get('genres', [])],
            "recommendations": [
                {"id": r['id'], "title": r['title'], "image_url": r['image_url']} 
                for r in info_series.get('recommendations', [])
            ]
        }

        episodes_list = []
        for ep in info_series.get('episodes', []):
            episodes_list.append({
                "episode_id": ep['id'],
                "number": ep['number'],
                "views": ep['total_views'],
                "duration_min": round(ep['duration']/60, 2),
                "thumbnail": ep['thumbnail_url'],
                "date_created": ep['date_created']
            })

        return series_info, episodes_list

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
            data = json.loads(decrypted)
            videos = []
            for video in data.get("data", []):
                videos.append({
                    "id": video.get("id"),
                    "status": video.get("status"),
                    "backup_status": video.get("backup_status"),
                    "quality": video.get("quality"),
                    "file_size": video.get("file_size"),
                    "download_url": video.get("download_url"),
                    "streaming_url": video.get("streaming_url")
                })
            return videos
        except:
            return []

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
            'filter[status][_eq]': 'published',
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
            return []

    def parse_search_results(self, search_json):
        parsed = []
        for item in search_json.get("data", []):
            parsed.append({
                "id": item.get("id"),
                "title": item.get("title"),
                "type": item.get("type"),
                "latest_episode": item.get("latest_episode"),
                "rating": item.get("rating"),
                "broadcast": item.get("broadcast"),
                "date_created": item.get("date_created"),
                "image_url": item.get("image_url")
            })
        return parsed
