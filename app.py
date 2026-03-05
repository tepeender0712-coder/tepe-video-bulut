from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Tepe Video Bulut</title>
<style>
body{ background:#0f172a; color:white; font-family:Arial; text-align:center; padding:40px; }
input{ padding:10px; width:60%; margin:10px; border-radius: 5px; border: none; }
button{ padding:10px 20px; margin:10px; cursor:pointer; background:#3b82f6; color:white; border:none; border-radius:5px; font-weight:bold;}
button:hover{ background:#2563eb; }
.card{ background:#1e293b; padding:30px; border-radius:10px; display:inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.3);}
</style>
</head>
<body>
<div class="card">
<h2>🚀 Tepe Video Bulut</h2>
<p>YouTube linkini yapıştırın ve formatı seçin</p>
<form method="post">
<input name="url" placeholder="https://youtube.com/watch?v=..."><br>
<button name="type" value="video">MP4 Olarak İndir</button>
<button name="type" value="mp3">MP3 (Ses) Olarak İndir</button>
</form>

{% if title %}
<hr style="border-color: #334155; margin-top:20px;">
<h3 style="color:#10b981;">✅ {{title}}</h3>
<p>📦 Boyut: {{size}} MB</p>
<a href="/download" style="display:inline-block; padding:10px 20px; background:#10b981; color:white; text-decoration:none; border-radius:5px; margin-top:10px;">Cihazına Kaydet</a>
{% endif %}
</div>
</body>
</html>
"""

video_file = None

@app.route("/", methods=["GET", "POST"])
def index():
    global video_file
    if request.method == "POST":
        url = request.form["url"]
        islem_tipi = request.form["type"]

        ydl_opts = {
            "outtmpl": "gecici_video.%(ext)s",
            "cookiefile": "cookies.txt",  # EHLYET DOSYAMIZIN DOĞRU ADI BURADA
        }

        if islem_tipi == "mp3":
            ydl_opts["format"] = "bestaudio"
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }]
        else:
            ydl_opts["format"] = "best"

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

                if islem_tipi == "mp3":
                    filename = filename.rsplit(".", 1)[0] + ".mp3"

            video_file = filename
            size = round(os.path.getsize(filename) / (1024 * 1024), 2)

            return render_template_string(HTML, title=info["title"], size=size)
            
        except Exception as e:
            return f"<h3 style='color:red;'>Bir Hata Oluştu: {str(e)}</h3><br><a href='/'>Geri Dön</a>"

    return render_template_string(HTML)

@app.route("/download")
def download():
    global video_file
    if video_file and os.path.exists(video_file):
        return send_file(video_file, as_attachment=True)
    return "Dosya bulunamadı, lütfen tekrar deneyin."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

