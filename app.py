import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Tepe Video Turbo | Bulut", page_icon="☁️")
st.title("☁️ Tepe Video Turbo (Bulut Sürümü)")
st.markdown("*(Herhangi bir cihazdan, kurulumsuz indirme merkezi)*")

link = st.text_input("YouTube Video Linkini Yapıştırın:")

if link:
    try:
        @st.cache_data(ttl=600)
        def analiz_et(url):
            with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'noplaylist': True}) as ydl:
                return ydl.extract_info(url, download=False)

        with st.spinner("Bulut sunucusu videoyu analiz ediyor..."):
            bilgi = analiz_et(link)
            
            # --- YENİ: MB HESAPLAMA EKRANI ---
            boyut_bayt = bilgi.get('filesize') or bilgi.get('filesize_approx')
            if boyut_bayt:
                boyut_mb = boyut_bayt / (1024 * 1024)
                st.info(f"📦 **Tahmini Dosya Boyutu:** {boyut_mb:.2f} MB")
            else:
                st.info("📦 **Tahmini Dosya Boyutu:** YouTube bu veriyi gizlemiş.")
            
        secim = st.radio("Gerçek Kalite Seçenekleri:", ["HD (720p)", "Full HD (1080p)"])
    
        # AŞAMA 1: SUNUCUYA İNDİRME BUTONU
        if st.button("🚀 BULUTTA HAZIRLA"):
            
            if "1080p" in secim:
                f_id = "bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best"
            else:
                f_id = "bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4]/best"

            dosya_adi = f"{bilgi.get('title', 'Video')}.mp4"
            gecici_yol = "gecici_video.mp4"

            ayarlar = {
                'format': f_id,
                'outtmpl': gecici_yol, # Video, Amerika'daki sunucunun geçici hafızasına iniyor
                'merge_output_format': 'mp4',
                'noplaylist': True 
            }
            
            with st.status("Bulut motorları işliyor (Sunucuya Çekiliyor)...", expanded=True) as s:
                with yt_dlp.YoutubeDL(ayarlar) as ydl:
                    ydl.download([link])
                s.update(label="Bulutta Hazır! ✅", state="complete")
            
            # AŞAMA 2: CİHAZA İNDİRME BUTONU (Sihirli Dönüşüm)
            with open(gecici_yol, "rb") as file:
                st.success("Tebrikler! Video sunucuda hazırlandı. Cihazınıza kaydetmek için tıklayın:")
                st.download_button(
                    label="📥 CİHAZIMA İNDİR",
                    data=file,
                    file_name=dosya_adi,
                    mime="video/mp4"
                )
                
            # --- YENİ: SUNUCU HAFIZASINI TEMİZLEME ---
            try:
                os.remove(gecici_yol)
            except:
                pass

    except Exception as e:
        st.error(f"Sistemde bir aksama oldu: {e}")

st.divider()
st.caption("Tepe Video Turbo v9.0 | Cloud & SaaS Architecture")
