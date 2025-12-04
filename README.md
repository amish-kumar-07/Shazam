# Voice-Based Song Recognition and Playback (Shazam Clone)

## Overview
This project records the user's voice or humming, identifies the song using ACRCloud’s Music Recognition API, and automatically plays the top-matched song through Spotify’s web player. It demonstrates a complete pipeline from audio capture to cloud recognition and playback.

---

## Features
- Record audio directly through the microphone.
- Send recorded WAV audio to ACRCloud for recognition.
- Extract song title, artist, album, Spotify track ID.
- Automatically open and play the top song in Spotify.
- JSON parsing of metadata for customized output and UI integration.

---

## System Architecture

### 1. Audio Capture
- Uses `sounddevice` and `soundfile` to record 8 seconds of mono audio at 44.1 kHz.
- Saves audio as `sample.wav`.

### 2. Cloud-Based Song Recognition
- ACRCloud API receives and processes the audio.
- Generates a signature using HMAC-SHA1 and your secret key.
- ACRCloud identifies the song using its global fingerprint database.
- Returns metadata: song title, artists, album, Spotify IDs, scores.

### 3. Playback Module
- Extracts Spotify track ID from `external_metadata`.
- Opens the Spotify track URL in the browser for direct playback.
- Fallback option: open YouTube search if Spotify data isn’t available.

---

## Data Flow Diagram

```

[Microphone]
↓
[Audio Recorder → sample.wav]
↓
[ACRCloud Signature + API Request]
↓
[Song Metadata Response (JSON)]
↓
[Track ID Extraction]
↓
[Spotify Web Playback]

```

---

## Recognition Flow

1. User hums/sings into the mic.
2. Program records and saves the audio.
3. Audio is uploaded to ACRCloud for recognition.
4. ACRCloud compares audio fingerprint with its database.
5. Top match is returned with confidence scores.
6. Spotify track ID extracted.
7. Browser opens Spotify link and plays the song.

---

## Technologies Used
- **Python**
- **sounddevice** for audio capture  
- **soundfile** for WAV writing  
- **requests** for API calls  
- **HMAC-SHA1** for ACRCloud signing  
- **Spotify Web Player** for playback  

---

## How to Run

1. Install dependencies:
```

pip install sounddevice soundfile requests

```

2. Add your ACRCloud credentials:
- host  
- access key  
- access secret  

3. Run the script:
```

python recognize.py

```

4. Hum/sing into your mic.
5. Spotify automatically opens your recognized song.

---

## Limitations / Known Issues

### 1. Humming Accuracy
- Humming detection is less reliable than full audio.
- Indian and non-Western melodies sometimes mismatch.

### 2. Requires Internet
- Recognition works only with ACRCloud’s cloud services.

### 3. No Local Playback
- Full track cannot be played inside Python due to Spotify restrictions.
- Only browser playback is supported.

### 4. Microphone Sensitivity
- Background noise reduces accuracy.
- Poor audio input may lead to incorrect song detection.

### 5. API Limitations
- ACRCloud free tier has request limits.
- Lyrics may not be available unless subscribing to higher plans.

---

## Future Improvements

- Embed a local audio player for preview clips.
- Add lyrics fetching from Audd.io or Genius.
- Implement GUI for cleaner user interaction.
- Real-time recognition using streaming audio.
- Build custom humming recognition for Indian songs.

---

## Conclusion
This project is a functional and educational Shazam-style system using Python. It demonstrates real-time audio capture, secure API communication, cloud-based fingerprinting, and Spotify playback, offering a complete end-to-end solution.
```
