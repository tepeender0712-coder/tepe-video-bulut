import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Tepe Video Turbo", page_icon="☁️")

st.title("☁️ Tepe Video Turbo v10")
st.caption("Bulut Video İndirme Merkezi")

url = st.text_input("YouTube linki yapıştır")

YDL_OPTS_BASE = {
    "quiet": True,
    "noplaylist": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
    "http_headers": {
        "User-Agent": "Mozilla/5.0"
    },
    "extractor_args": {
        "youtube": {
            "player_client": ["android","web"]
        }
    }
}

if url:

    try:

        with st.spinner("Video analiz ediliyor..."):

            ydl_opts = YDL_OPTS_BASE.copy()
            ydl_opts["skip_download"] = True

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

        title = info.get("title","video")
        thumb = info.get("thumbnail")

        st.image(thumb)
        st.subheader(title)

        format_sec = {
            "HD (720p)": "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "Full HD (1080p)": "bestvideo[height<=1080]+bestaudio/best"
        }

        kalite = st.radio("Kalite seç", list(format_sec.keys()))

        if st.button("🚀 Bulutta Hazırla"):

            out_file = "video.mp4"

            ydl_opts = YDL_OPTS_BASE.copy()
            ydl_opts.update({
                "format": format_sec[kalite],
                "merge_output_format": "mp4",
                "outtmpl": out_file
            })

            with st.spinner("Video indiriliyor..."):

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

            st.success("Video hazır!")

            with open(out_file,"rb") as f:

                st.download_button(
                    "📥 Cihaza indir",
                    f,
                    file_name=f"{title}.mp4",
                    mime="video/mp4"
                )

            os.remove(out_file)

    except Exception as e:
        st.error(f"Hata oluştu: {e}")

st.divider()
st.caption("Tepe Video Turbo v10 | Cloud Edition")

