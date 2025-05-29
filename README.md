Kappa Railway PingBot

Kurulum (Railway için):
1. Railway.app'e giriş yap
2. Yeni proje oluştur → "Deploy from GitHub"
3. Bu dosyaları bir GitHub reposuna yükle
4. Railway'de Environment Variables ayarla:
   - BOT_TOKEN: Telegram bot tokenin
   - CHAT_ID: Telegram chat ID (örnek: 7883022926)
   - TARGET_URL: (isteğe bağlı) Gönderilecek hedef URL
   - REQUESTS_PER_SECOND: (varsayılan 50)

5. Deploy edildiğinde Railway sunucusu istek göndermeye başlar.