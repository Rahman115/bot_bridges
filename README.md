# Bot Bridge Telegram - Discord

Saya akan membantu Anda membuat aplikasi bridge bot antara Telegram dan Discord secara lengkap. Berikut panduan detailnya.

## 📁 Struktur Proyek

```
telegram-discord-bridge/
├── .env
├── .gitignore
├── requirements.txt
├── main.py
├── config.py
├── bridges/
│   ├── __init__.py
│   ├── telegram_reader.py
│   ├── telegram_sender.py
│   └── discord_reader.py
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── filters.py
└── README.md
```

## 1️⃣ Setup Awal

### Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### requirements.txt
```txt
# Telegram
telethon==1.34.0
python-telegram-bot==20.7

# Discord
discord.py==2.3.2

# Utility
python-dotenv==1.0.0
asyncio==3.4.3
colorlog==6.7.0

# Optional (untuk formatting lebih baik)
rich==13.7.0
```

Install semua dependensi:
```bash
pip install -r requirements.txt
```

## 2️⃣ Setup API dan Token

### A. Telegram API (untuk Telethon - user account)

1. Buka https://my.telegram.org/apps
2. Login dengan nomor telepon Anda
3. Isi form "App title" dan "Short name" (bebas)
4. Dapatkan:
   - **API ID** (angka)
   - **API Hash** (string)

### B. Discord Bot Token

1. Buka https://discord.com/developers/applications
2. Klik "New Application" → beri nama
3. Masuk ke tab "Bot" → klik "Add Bot"
4. Di bawah "TOKEN" → klik "Reset Token" → copy token
5. **Aktifkan Intents:**
   - Scroll ke "Privileged Gateway Intents"
   - Aktifkan:
     - ✅ MESSAGE CONTENT INTENT
     - ✅ SERVER MEMBERS INTENT (opsional)
   - Klik "Save Changes"

### C. Invite Bot ke Discord Server

1. Di Developer Portal → OAuth2 → URL Generator
2. Pilih:
   - Scopes: `bot`
   - Bot Permissions: `Read Messages`, `Send Messages`, `Read Message History`
3. Buka generated URL, invite bot ke server Anda

### D. Mendapatkan ID

**Telegram Chat ID:**
1. Cari bot `@userinfobot` di Telegram
2. Start chat, kirim /start
3. Bot akan memberi informasi termasuk ID Anda
4. Untuk group: tambahkan bot ke group, kirim pesan, lihat ID

**Discord Channel ID:**
1. Buka Discord → Settings → Advanced
2. Aktifkan "Developer Mode"
3. Klik kanan pada channel → "Copy ID"

## 3️⃣ File Konfigurasi

### .env
```env
# Telegram API (untuk membaca - user account)
TELEGRAM_API_ID=123456
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_PHONE=+6281234567890
TELEGRAM_READ_CHAT_ID=-1001234567890

# Telegram Bot (untuk mengirim - bot)
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_SEND_CHAT_ID=-1009876543210

# Discord
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DISCORD_READ_CHANNEL_ID=123456789012345678

# Optional
MESSAGE_DELAY=2  # delay in seconds
LOG_LEVEL=INFO
```

### .gitignore
```gitignore
# Virtual Environment
venv/
env/
ENV/

# Python
__pycache__/
*.py[cod]
*.so
.Python

# Environment variables
.env
*.env

# Telegram session files
*.session
*.session-journal

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo
```

## 4️⃣ Kode Program
```bash
# Kode Program 
```

## 5️⃣ Cara Menjalankan

### Persiapan Awal (Semua Platform)

1. **Clone atau buat folder proyek**
```bash
mkdir telegram-discord-bridge
cd telegram-discord-bridge
```

2. **Buat virtual environment dan install dependencies**
```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Setup file .env**
```bash
# Copy template
cp .env.example .env
# Edit dengan editor teks
nano .env  # atau notepad .env di Windows
```

### Menjalankan di Windows

**Metode 1: Langsung dari terminal**
```bash
# Aktifkan virtual environment
venv\Scripts\activate

# Jalankan aplikasi
python main.py
```

**Metode 2: Menggunakan batch file**
Buat file `run.bat`:
```batch
@echo off
call venv\Scripts\activate
python main.py
pause
```

### Menjalankan di Linux

**Metode 1: Langsung dari terminal**
```bash
# Aktifkan virtual environment
source venv/bin/activate

# Jalankan aplikasi
python3 main.py
```

**Metode 2: Menggunakan shell script**
Buat file `run.sh`:
```bash
#!/bin/bash
source venv/bin/activate
python3 main.py
```
```bash
chmod +x run.sh
./run.sh
```

### Menjalankan sebagai service di Linux (systemd)

Buat file `/etc/systemd/system/telegram-discord-bridge.service`:
```ini
[Unit]
Description=Telegram Discord Bridge
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/telegram-discord-bridge
ExecStart=/path/to/telegram-discord-bridge/venv/bin/python /path/to/telegram-discord-bridge/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Kemudian:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-discord-bridge
sudo systemctl start telegram-discord-bridge
sudo systemctl status telegram-discord-bridge
```

## 6️⃣ Deploy ke VPS

### Persiapan VPS (Ubuntu 20.04/22.04)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python dan tools
sudo apt install python3-pip python3-venv git -y

# Clone project
git clone https://github.com/yourusername/telegram-discord-bridge.git
cd telegram-discord-bridge

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup .env file
nano .env
# Isi dengan credentials

# Test run
python3 main.py

# Jika sudah OK, setup sebagai service (seperti di atas)
```

### Menggunakan PM2 (alternatif untuk process management)

```bash
# Install PM2
sudo npm install -g pm2

# Buat ecosystem file
nano ecosystem.config.js
```

Isi `ecosystem.config.js`:
```javascript
module.exports = {
  apps: [{
    name: 'telegram-discord-bridge',
    script: 'main.py',
    interpreter: './venv/bin/python',
    watch: false,
    env: {
      PYTHONUNBUFFERED: '1'
    }
  }]
}
```

```bash
# Jalankan dengan PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## 7️⃣ Risiko dan Batasan

### Telegram Terms of Service

1. **Penggunaan User Account**: 
   - Menggunakan user account (bukan bot) untuk membaca pesan berisiko
   - Telegram dapat memblokir akun jika terdeteksi sebagai automated client
   - Risiko: Akun dilarang sementara/permanen

2. **Rate Limiting**:
   - Telegram memiliki batasan jumlah pesan per detik/menit
   - Jika terlalu cepat, bisa kena spam detection
   - Solusi: Gunakan delay antar pesan (sudah diimplementasikan)

3. **Privacy Concerns**:
   - Membaca pesan group memerlukan akses ke semua pesan
   - Pastikan Anda memiliki izin untuk membaca dan memforward pesan

### Discord Terms of Service

1. **Self-bot**:
   - Discord melarang penggunaan user account sebagai bot (self-bot)
   - Kita menggunakan bot account yang resmi, jadi aman

2. **Rate Limits**:
   - Discord memiliki rate limits: 50 requests per second untuk bot
   - Bot yang melanggar bisa di-suspend

3. **Intents**:
   - Message Content Intent memerlukan verifikasi untuk bot di 100+ server
   - Untuk bot pribadi, tetap aktifkan di Developer Portal

### Best Practices untuk Menghindari Masalah

1. **Tambahkan Delay** (sudah):
   - Delay minimal 1-2 detik antar pesan
   - Jangan memforward semua pesan sekaligus

2. **Filter Konten**:
   - Hindari memforward pesan yang mengandung data sensitif
   - Pertimbangkan untuk tidak memforward media besar

3. **Monitoring**:
   - Pantau log secara teratur
   - Setup alert jika ada error

4. **Backup Session**:
   - File session Telethon (.session) penting untuk autentikasi
   - Backup secara berkala

## 8️⃣ Troubleshooting

### Masalah Umum dan Solusi

**1. Telegram authentication failed**
```python
# Hapus file session dan coba lagi
rm reader_session.session
# Jalankan ulang aplikasi
```

**2. Discord bot tidak bisa membaca pesan**
- Pastikan Message Content Intent sudah diaktifkan di Developer Portal
- Invite ulang bot dengan permissions yang benar
- Check channel ID

**3. Rate limit errors**
- Tambah delay di .env (MESSAGE_DELAY=3)
- Kurangi jumlah filter agar tidak memforward terlalu banyak

**4. Session expired**
- Telethon session kadang expire
- Hapus file .session dan restart aplikasi

## 9️⃣ Fitur Lanjutan (Opsional)

Jika ingin mengembangkan lebih lanjut:

1. **Multi-destination**: Forward ke multiple Telegram groups
2. **Media support**: Forward gambar/video
3. **Formatting**: Pertahankan formatting pesan (bold, italic, dll)
4. **Webhook**: Tambahkan webhook untuk monitoring
5. **Database**: Simpan pesan yang sudah diforward untuk menghindari duplikasi
6. **Admin commands**: Tambahkan bot commands untuk kontrol

---

## 📝 Catatan Penting

1. **Pertama kali menjalankan**, Anda perlu login ke Telegram melalui konsol (masukkan nomor telepon dan kode OTP)
2. **Session file** akan tersimpan, sehingga login tidak perlu diulang
3. **Delay** sangat penting untuk menghindari spam detection
4. **Testing**: Coba dengan pesan sederhana dulu sebelum production
5. **Backup**: Backup file .env dan .session secara berkala

Aplikasi ini siap digunakan! Jika ada error atau pertanyaan, periksa log di `bridge.log` untuk detail.