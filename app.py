# AI-Video-Creator-Backend/app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS # Untuk mengatasi CORS saat frontend memanggil backend
# from google.generativeai import GenerativeModel # Contoh jika pakai Google Generative AI Python SDK
# import google.generativeai as genai

app = Flask(__name__)
CORS(app) # Mengizinkan frontend (berjalan di domain berbeda) untuk memanggil API ini

# Ambil API Key dari environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Jika menggunakan Google Generative AI SDK:
# genai.configure(api_key=GEMINI_API_KEY)
# model = genai.GenerativeModel('gemini-1.5-flash') # Ganti dengan model Veo yang sesuai

@app.route('/generate-video', methods=['POST'])
def generate_video():
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY not configured"}), 500

    data = request.json
    prompt_text = data.get('prompt_text')
    image_data = data.get('image_data') # Jika ada, untuk image-to-video

    if not prompt_text and not image_data:
        return jsonify({"error": "No prompt text or image data provided"}), 400

    # --- Di sini Anda akan menambahkan logika untuk memanggil API AI ---
    # Contoh (pseudo-code untuk Gemini Veo 3 - implementasi sebenarnya akan lebih kompleks):
    try:
        # Ini adalah bagian di mana Anda akan menggunakan library Python Google/RunwayML
        # untuk mengirim prompt dan menerima video.
        # Contoh:
        # if prompt_text:
        #     response = model.generate_content(prompt_text)
        #     video_url = response.video.url # Asumsi ada atribut video.url
        # elif image_data:
        #     # Logika untuk mengirim gambar ke API AI
        #     response = model.generate_content([prompt_text, {"mime_type": "image/jpeg", "data": base64.b64decode(image_data)}])
        #     video_url = response.video.url
        video_url = "https://example.com/your-generated-video.mp4" # Placeholder URL

        return jsonify({"videoUrl": video_url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) # debug=True hanya untuk pengembangan lokal