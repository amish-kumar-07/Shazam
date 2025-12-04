import sounddevice as sd
import soundfile as sf
import time
import hashlib
import base64
import requests
import json
import os
import hmac
import webbrowser

# ================== RECORD AUDIO ==================

samplerate = 44100  # Hz
channels = 1        # mono
duration = 8        # seconds
filename = "sample.wav"

print("Recording...")
audio = sd.rec(
    int(duration * samplerate),
    samplerate=samplerate,
    channels=channels,
    dtype='int16'
)
sd.wait()
sf.write(filename, audio, samplerate)
print(f"Saved: {filename}")
print("Audio size:", os.path.getsize(filename), "bytes")


# ================== ACRCloud Credentials ==================
host = "identify-ap-southeast-1.acrcloud.com"       # your host
access_key = "79d940327bc4592e7163ef043b31ae1a"     # your key
access_secret = "1xn6A1ZTmbnnVJnv8zHx0RnVFnzgWy2YKCV0tDrY"  # your secret
# ===========================================================


def recognize_song(audio_file_path):
    http_method = "POST"
    http_uri = "/v1/identify"
    data_type = "audio"
    signature_version = "1"
    timestamp = str(int(time.time()))

    # ---- Build string to sign EXACT order ----
    string_to_sign = "\n".join([
        http_method,
        http_uri,
        access_key,
        data_type,
        signature_version,
        timestamp
    ])

    # ---- Correct HMAC-SHA1 signature ----
    sign = base64.b64encode(
        hmac.new(
            access_secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha1
        ).digest()
    ).decode('utf-8')

    files = {
        'sample': ('sample.wav', open(audio_file_path, 'rb'), 'audio/wav')
    }

    data = {
        'access_key': access_key,
        'data_type': data_type,
        'signature_version': signature_version,
        'signature': sign,
        'timestamp': timestamp,
        'sample_bytes': str(os.path.getsize(audio_file_path))
    }

    print("Sending request to:", f"https://{host}{http_uri}")

    response = requests.post(
        f"https://{host}{http_uri}",
        files=files,
        data=data
    )

    return response.json()


# ================== RUN RECOGNIZER ==================

result = recognize_song("sample.wav")
print(json.dumps(result, indent=4))

top = result["metadata"]["music"][0]  # Top match

# Check if Spotify metadata exists
spotify_data = top.get("external_metadata", {}).get("spotify", {})

if "track" in spotify_data:
    track_id = spotify_data["track"]["id"]
    print("Playing Top Song:", top["title"])
    print("Spotify Track ID:", track_id)

    url = f"https://open.spotify.com/track/{track_id}"
    webbrowser.open(url)
else:
    print("Spotify ID not found. Opening YouTube instead...")

    # Fallback to YouTube search
    import urllib.parse
    query = urllib.parse.quote(f"{top['title']} {top['artists'][0]['name']}")
    youtube_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(youtube_url)


