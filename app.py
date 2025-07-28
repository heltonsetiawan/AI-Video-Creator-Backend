# AI-Video-Creator-Backend/app.py
import os
import base64 # Untuk encoding/decoding gambar jika Anda akan mengirim gambar
import requests # Jika Anda akan memanggil API secara langsung (bukan via SDK)

from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Impor untuk Google Generative AI ---
# Pastikan Anda sudah menginstal: pip install google-generativeai
import google.generativeai as genai

app = Flask(__name__)
CORS(app) # Mengizinkan panggilan dari frontend (domain berbeda)

# --- 1. Ambil API Key dari Environment Variable ---
# Nama 'GEMINI_API_KEY' harus persis sama dengan yang Anda set di Vercel.
GEMINI_API_KEY = os.environ.get("AIzaSyAyQwKSSz5-vpBu7OP68tNHNj4rcLqsXUo")

# --- 2. Konfigurasi Gemini API dengan API Key ---
# Ini harus dilakukan sebelum Anda mencoba menggunakan model Gemini.
# Pastikan GEMINI_API_KEY tidak None.
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY is not set. API calls will fail.")
    # Anda mungkin ingin menambahkan penanganan error yang lebih kuat di sini.

# Inisialisasi model Gemini.
# Untuk text-to-video, Anda akan memerlukan model yang mendukung video (seperti Veo 3)
# atau model multimodal yang bisa memahami prompt video.
# Jika Veo 3 belum tersedia secara umum via SDK, Anda mungkin perlu memanggilnya via REST API.
# Untuk tujuan percobaan, kita bisa gunakan model Gemini Pro untuk text-to-text dulu,
# atau placeholder jika Veo 3 tidak langsung tersedia.
# model = genai.GenerativeModel('gemini-1.5-flash') # Contoh untuk text-to-text atau multimodal
# model_for_video = None # Anda perlu inisialisasi model Veo 3 yang spesifik di sini

@app.route('/generate-video', methods=['POST'])
def generate_video():
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY not configured on server"}), 500

    data = request.json
    prompt_text = data.get('prompt_text')
    image_data_b64 = data.get('image_data') # Base64 encoded image string

    if not prompt_text and not image_data_b64:
        return jsonify({"error": "No prompt text or image data provided"}), 400

    video_url = None # Default
    try:
        # --- LOGIKA PANGGILAN API KE LAYANAN AI ---
        # BAGIAN PENTING: Implementasi nyata untuk memanggil Veo 3 atau API generatif video lainnya.

        if prompt_text:
            print(f"Generating video for text prompt: {prompt_text}")
            # --- CONTOH (PSEUDO-KODE/TEMPLATE) untuk panggil Gemini Veo 3 atau sejenisnya ---
            # Jika Veo 3 tersedia melalui google-generativeai SDK:
            # response = model_for_video.generate_content(prompt_text)
            # video_url = response.video.url # Asumsi SDK mengembalikan URL video

            # Jika Veo 3 belum tersedia via SDK dan harus pakai REST API (lebih kompleks):
            # headers = {"Authorization": f"Bearer YOUR_AUTH_TOKEN", "x-api-key": GEMINI_API_KEY}
            # api_payload = {"prompt": prompt_text, "output_format": "mp4"}
            # api_response = requests.post("https://api.google.com/ai/veo/generate", json=api_payload, headers=headers)
            # api_response.raise_for_status() # Akan memunculkan error untuk status kode 4xx/5xx
            # video_url = api_response.json().get("video_url")

            # --- Placeholder URL untuk Ujicoba Awal ---
            # Ganti ini dengan hasil URL video dari API AI yang sebenarnya.
            video_url = "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4" # Contoh video MP4 publik
            # Atau: video_url = "https://placeholder.com/video_generated_by_ai.mp4"

        if image_data_b64:
            print(f"Generating video for image data (plus prompt if any): {prompt_text}")
            # Jika Anda perlu mengirim gambar, Anda harus mendekode base64
            # image_bytes = base64.b64decode(image_data_b64)
            # Lalu kirim image_bytes ke API AI bersama dengan prompt_text jika ada.
            # Implementasi ini akan sangat bergantung pada API AI yang Anda gunakan.
            video_url = "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4" # Placeholder URL

        if video_url:
            return jsonify({"videoUrl": video_url}), 200
        else:
            return jsonify({"error": "Failed to generate video or video URL not found."}), 500

    except genai.APIError as e:
        # Penanganan error spesifik dari Gemini API
        print(f"Gemini API Error: {e}")
        return jsonify({"error": f"AI API Error: {e.args[0]}"}), 500
    except requests.exceptions.RequestException as e:
        # Penanganan error jika Anda memanggil API via requests
        print(f"HTTP Request Error: {e}")
        return jsonify({"error": f"Backend communication error: {str(e)}"}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": f"An unexpected server error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Pastikan debug=True hanya untuk pengembangan lokal.
    # Di Vercel, debug akan otomatis diatur oleh lingkungan Vercel.
    app.run(debug=True, port=5000)