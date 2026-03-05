import streamlit as st
import yt_dlp
import os
import glob

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
            
            # --- YENİ: ZEKİ FORMAT SEÇİCİ (Uzantı Dayatması Yok) ---
            if "1080p" in secim:
                f_id = "bestvideo[height<=1080]+bestaudio/best"
            else:
                f_id = "bestvideo[height<=720]+bestaudio/best"

            # %(ext)s komutu ile orijinal uzantıyı koruyoruz
            ayarlar = {
                'format': f_id, 
                'outtmpl': 'gecici_video.%(ext)s', 
                'noplaylist': True 
            }
            ayarlar.update(ortak_ayarlar) 
            
            with st.status("Bulut motorları işliyor (Sunucuya Çekiliyor)...", expanded=True) as s:
                with yt_dlp.YoutubeDL(ayarlar) as ydl:
                    ydl.download([link])
                s.update(label="Bulutta Hazır! ✅", state="complete")
            
            # --- YENİ: İNEN DOSYAYI DİNAMİK OLARAK BULMA ---
            # Sunucuya inen dosya .mp4 mü .webm mi onu tespit ediyoruz
            inen_dosyalar = glob.glob("gecici_video.*")
            
            if inen_dosyalar:
                gercek_yol = inen_dosyalar[0]
                uzanti = gercek_yol.split('.')[-1] # Uzantıyı kelime olarak alıyoruz (mp4, webm vb.)
                
                dosya_adi = f"{bilgi.get('title', 'Video')}.{uzanti}"
                mime_turu = f"video/{uzanti}"

                with open(gercek_yol, "rb") as file:
                    st.success(f"Tebrikler! Video ({uzanti.upper()} formatında) sunucuda hazırlandı:")
                    st.download_button(
                        label="📥 CİHAZIMA İNDİR",
                        data=file,
                        file_name=dosya_adi,
                        mime=mime_turu
                    )
                
                try:
                    os.remove(gercek_yol)
                except:
                    pass
            else:
                st.error("Dosya sunucuda bulunamadı.")

    except Exception as e:
        st.error(f"Sistemde bir aksama oldu: {e}")

st.divider()
st.caption("Tepe Video Turbo v9.5 | Dynamic Format Resolution")
