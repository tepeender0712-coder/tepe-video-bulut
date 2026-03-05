import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Tepe Video Turbo", page_icon="☁️")

st.title("☁️ Tepe Video Turbo")
st.write("Bulut Video İndirici")

url = st.text_input("YouTube video linki yapıştır:")

YDL_OPTS = {
    "quiet": True,
    "noplaylist": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
    "http_headers": {
        "User-Agent": "Mozilla/5.0"
    }
}

if url:

    try:

        with st.spinner("Video analiz ediliyor..."):

            opts = YDL_OPTS.copy()
            opts["skip_download"] = True

            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)

        title = info.get("title", "video")
        thumbnail = info.get("thumbnail")

        st.image(thumbnail)
        st.subheader(title)

        kalite = st.radio(
            "Kalite seç",
            ["HD (720p)", "Full HD (1080p)"]
        )

        if st.button("🚀 Videoyu Hazırla"):

            if "1080" in kalite:
                format_code = "bestvideo[height<=1080]+bestaudio/best"
            else:
                format_code = "bestvideo[height<=720]+bestaudio/best"

            output = "video.%(ext)s"

            opts = YDL_OPTS.copy()

            opts.update({
                "format": format_code,
                "merge_output_format": "mp4",
                "outtmpl": output
            })

            with st.spinner("Video indiriliyor..."):

                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url])

            file = os.listdir(".")[0]

            with open(file, "rb") as f:

                st.download_button(
                    "📥 Cihaza indir",
                    f,
                    file_name=file
                )

            os.remove(file)

    except Exception as e:

        st.error(f"Hata oluştu: {e}")

st.divider()
st.caption("Tepe Video Turbo | Cloud Edition")
