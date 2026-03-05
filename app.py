import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Tepe Video Turbo | Bulut", page_icon="☁️")
st.title("☁️ Tepe Video Turbo (Bulut Sürümü)")
st.markdown("*(Herhangi bir cihazdan, kurulumsuz indirme merkezi)*")

link = st.text_input("YouTube Video Linkini Yapıştırın:")

ortak_ayarlar = {
    'cookiefile': 'cookies.txt',  
    'extractor_args': {'youtube': ['player_client=default,-android_sdkless']},
    'http_headers': {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'}
}

if link:
    try:
        @st.cache_data(ttl=600)
        def analiz_et(url):
            analiz_ayarlari = {'quiet': True, 'no_warnings': True, 'noplaylist': True}
            analiz_ayarlari.update(ortak_ayarlar) 
            with yt_dlp.YoutubeDL(analiz_ayarlari) as ydl:
                return ydl.extract_info(url, download=False)

        with st.spinner("Bulut sunucusu videoyu analiz ediyor..."):
            bilgi = analiz_et(link)
            
            boyut_bayt = bilgi.get('filesize') or bilgi.get('filesize_approx')
            if boyut_bayt:
                boyut_mb = boyut_bayt / (1024 * 1024)
                st.info(f"📦 **Tahmini Dosya Boyutu:** {boyut_mb:.2f} MB")
            else:
                st.info("📦 **Tahmini Dosya Boyutu:** YouTube bu veriyi gizlemiş.")
            
        secim = st.radio("Gerçek Kalite Seçenekleri:", ["HD (720p)", "Full HD (1080p)"])
    
        if st.button("🚀 BULUTTA HAZIRLA"):
            
            # --- YENİ: ESNEK FORMAT SEÇİMİ (ÇÖKMEYİ ÖNLER) ---
            if "1080p" in secim:
                f_id = "bestvideo[height<=1080]+bestaudio/best"
            else:
                f_id = "bestvideo[height<=720]+bestaudio/best"

            dosya_adi = f"{bilgi.get('title', 'Video')}.mp4"
            gecici_yol = "gecici_video.mp4"

            ayarlar = {
                'format': f_id, # Esnek formatı kullanıyoruz
                'outtmpl': gecici_yol, 
                'merge_output_format': 'mp4', # Ne bulursan bul, bize MP4 olarak birleştir diyoruz!
                'noplaylist': True 
            }
            ayarlar.update(ortak_ayarlar) 
            
            with st.status("Bulut motorları işliyor (Sunucuya Çekiliyor)...", expanded=True) as s:
                with yt_dlp.YoutubeDL(ayarlar) as ydl:
                    ydl.download([link])
                s.update(label="Bulutta Hazır! ✅", state="complete")
            
            with open(gecici_yol, "rb") as file:
                st.success("Tebrikler! Video sunucuda hazırlandı. Cihazınıza kaydetmek için tıklayın:")
                st.download_button(
                    label="📥 CİHAZIMA İNDİR",
                    data=file,
                    file_name=dosya_adi,
                    mime="video/mp4"
                )
                
            try:
                os.remove(gecici_yol)
            except:
                pass

    except Exception as e:
        st.error(f"Sistemde bir aksama oldu: {e}")

st.divider()
st.caption("Tepe Video Turbo v9.3 | Ultimate Format Fallback")
