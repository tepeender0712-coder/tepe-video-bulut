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
body{
background:#0f172a;
color:white;
font-family:Arial;
text-align:center;
padding:40px;
}
input{
padding:10px;
width:60%;
margin:10px;
}
button{
padding:10px 20px;
margin:10px;
cursor:pointer;
}
.card{
background:#1e293b;
padding:30px;
border-radius:10px;
display:inline-block;
}
</style>
</head>
<body>

<div class="card">
<h2>Tepe Video Bulut</h2>

<form method="post">
<input name="url" placeholder="Video URL"><br>

<button name="type" value="video">MP4 indir</button>
<button name="type" value="mp3">MP3 indir</button>

</form>

{% if title %}
<h3>{{title}}</h3>
<p>Boyut: {{size}} MB</p>
<a href="/download">İndir</a>
{% endif %}

</div>

</body>
</html>
"""

video_file = None

@app.route("/", methods=["GET","POST"])
def index():
    global video_file

    if request.method == "POST":

        url = request.form["url"]
        type = request.form["type"]

        ydl_opts = {
            "outtmpl": "video.%(ext)s",
            "cookiefile": "cookie.txt",
        }

        if type == "mp3":
            ydl_opts["format"] = "bestaudio"
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }]
        else:
            ydl_opts["format"] = "best"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            if type == "mp3":
                filename = filename.rsplit(".",1)[0] + ".mp3"

        video_file = filename

        size = round(os.path.getsize(filename) / (1024*1024),2)

        return render_template_string(
            HTML,
            title=info["title"],
            size=size
        )

    return render_template_string(HTML)

@app.route("/download")
def download():
    global video_file
    return send_file(video_file, as_attachment=True)

app.run(host="0.0.0.0", port=10000)
