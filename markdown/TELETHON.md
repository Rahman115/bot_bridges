# Menjalankan di Laptop Sebelum Deployment ke Raspberry Pi/VPS

## 🖥️ Menjalankan di Laptop (Development Environment)

Tidak ada perubahan signifikan dalam kode untuk menjalankan di laptop vs Raspberry Pi/VPS. Yang membedakan hanyalah **environment** dan **cara menjalankannya**.

### 1️⃣ Persiapan di Laptop

```bash
# Buat folder proyek di laptop
cd Documents
mkdir telegram-discord-bridge
cd telegram-discord-bridge

# Buat virtual environment
python -m venv venv

# Aktivasi (Windows)
venv\Scripts\activate

# Aktivasi (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install telethon python-telegram-bot discord.py python-dotenv
```

### 2️⃣ Testing dengan Telethon

Kode yang Anda tanyakan (`from telethon import TelegramClient, events`) sudah benar dan digunakan dalam implementasi di atas. Tidak ada perubahan signifikan antara menjalankan di laptop vs Raspberry Pi.

**Perbedaan utama yang perlu diperhatikan:**

| Aspek | Laptop | Raspberry Pi/VPS |
|-------|--------|------------------|
| **Session file** | Tersimpan di folder proyek | Sama, tapi backup penting |
| **Uptime** | Saat laptop menyala | 24/7 |
| **Network** | Bisa berubah (WiFi pindah) | Stabil (server) |
| **Power** | Harus selalu menyala | Hemat daya (Pi) |

### 3️⃣ Versi Sederhana untuk Testing Cepat

Buat file `test_telegram_reader.py` untuk testing koneksi Telethon:

```python
#!/usr/bin/env python3
"""
Simple test script untuk Telethon reader
Menampilkan pesan dari Telegram group ke console
"""

import asyncio
import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Konfigurasi
API_ID = int(os.getenv('TELEGRAM_API_ID', 0))
API_HASH = os.getenv('TELEGRAM_API_HASH', '')
PHONE = os.getenv('TELEGRAM_PHONE', '')
CHAT_ID = int(os.getenv('TELEGRAM_READ_CHAT_ID', 0))

# Buat client
client = TelegramClient('test_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=[CHAT_ID]))
async def handler(event):
    """Handler untuk pesan baru"""
    message = event.message
    sender = await event.get_sender()
    sender_name = sender.first_name if sender else "Unknown"
    
    print(f"\n📨 Pesan dari {sender_name}:")
    print(f"   {message.message}")
    print(f"   Waktu: {message.date}")
    print("-" * 50)

async def main():
    """Main function"""
    print("Memulai Telegram Reader Test...")
    print(f"Monitoring chat ID: {CHAT_ID}")
    print("Tekan Ctrl+C untuk berhenti\n")
    
    # Start client
    await client.start(phone=PHONE)
    print("✓ Client started successfully!")
    
    # Dapatkan info chat
    try:
        entity = await client.get_entity(CHAT_ID)
        if hasattr(entity, 'title'):
            print(f"✓ Monitoring group: {entity.title}")
        else:
            print(f"✓ Monitoring chat: {entity.id}")
    except Exception as e:
        print(f"⚠️ Warning: Tidak bisa dapat info chat: {e}")
    
    # Jalankan sampai dihentikan
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTest dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
```

### 4️⃣ Testing Discord Reader

Buat file `test_discord_reader.py`:

```python
#!/usr/bin/env python3
"""
Simple test script untuk Discord reader
"""

import asyncio
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN', '')
CHANNEL_ID = int(os.getenv('DISCORD_READ_CHANNEL_ID', 0))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✓ Bot Discord siap: {bot.user}')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        print(f'✓ Monitoring channel: #{channel.name} di {channel.guild.name}')
    else:
        print(f'❌ Channel ID {CHANNEL_ID} tidak ditemukan!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.channel.id == CHANNEL_ID:
        print(f"\n📨 [Discord] {message.author}:")
        print(f"   {message.content}")
        print(f"   Channel: #{message.channel.name}")
        print("-" * 50)
    
    await bot.process_commands(message)

# Jalankan bot
bot.run(TOKEN)
```

### 5️⃣ Testing Telegram Sender

Buat file `test_telegram_sender.py`:

```python
#!/usr/bin/env python3
"""
Test Telegram Bot sender
"""

import asyncio
from telegram import Bot
from telegram.error import TelegramError
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
CHAT_ID = int(os.getenv('TELEGRAM_SEND_CHAT_ID', 0))

async def send_test_message():
    """Kirim pesan test"""
    bot = Bot(token=TOKEN)
    
    try:
        # Test 1: Dapatkan info bot
        me = await bot.get_me()
        print(f"✓ Bot Telegram: @{me.username}")
        
        # Test 2: Kirim pesan sederhana
        await bot.send_message(
            chat_id=CHAT_ID,
            text="🔄 Test pesan dari bridge bot!",
            disable_web_page_preview=True
        )
        print(f"✓ Pesan terkirim ke chat ID: {CHAT_ID}")
        
        # Test 3: Kirim pesan dengan prefix
        await bot.send_message(
            chat_id=CHAT_ID,
            text="📱 [Test] Ini adalah pesan test dengan prefix",
            disable_web_page_preview=True
        )
        print("✓ Pesan kedua terkirim")
        
    except TelegramError as e:
        print(f"❌ Error Telegram: {e}")
    except Exception as e:
        print(f"❌ Error umum: {e}")

if __name__ == "__main__":
    asyncio.run(send_test_message())
```

### 6️⃣ Script Testing Lengkap

Buat file `run_tests.py` untuk menjalankan semua test:

```python
#!/usr/bin/env python3
"""
Script untuk menjalankan semua test secara berurutan
"""

import subprocess
import sys
import os
from dotenv import load_dotenv

def print_header(text):
    """Print header dengan format"""
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60)

def run_test(script_name, description):
    """Jalankan test script"""
    print_header(description)
    
    try:
        # Jalankan script dengan python yang sama
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("⚠️ Test timeout (30 detik)")
        return False
    except Exception as e:
        print(f"❌ Error menjalankan test: {e}")
        return False

def main():
    """Main function"""
    print_header("TELEGRAM-DISCORD BRIDGE TEST SUITE")
    
    # Load environment
    load_dotenv()
    
    # Cek environment variables
    required_vars = [
        'TELEGRAM_API_ID', 'TELEGRAM_API_HASH', 'TELEGRAM_PHONE',
        'TELEGRAM_READ_CHAT_ID', 'TELEGRAM_BOT_TOKEN', 
        'TELEGRAM_SEND_CHAT_ID', 'DISCORD_BOT_TOKEN', 'DISCORD_READ_CHANNEL_ID'
    ]
    
    print("\n📋 Checking environment variables:")
    all_good = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
            print(f"  ✓ {var}: {masked}")
        else:
            print(f"  ❌ {var}: NOT SET")
            all_good = False
    
    if not all_good:
        print("\n❌ Environment variables tidak lengkap. Periksa file .env")
        return
    
    print("\n✅ Environment OK, memulai tests...")
    
    # Run tests
    tests = [
        ("test_telegram_sender.py", "Test 1: Telegram Bot Sender"),
        ("test_telegram_reader.py", "Test 2: Telegram Reader (akan berjalan 10 detik)"),
        ("test_discord_reader.py", "Test 3: Discord Reader (akan berjalan 10 detik)")
    ]
    
    for script, desc in tests:
        if not os.path.exists(script):
            print(f"\n⚠️ File {script} tidak ditemukan, skip...")
            continue
            
        success = run_test(script, desc)
        if success:
            print(f"\n✅ {desc} selesai")
        else:
            print(f"\n❌ {desc} gagal")
        
        input("\nTekan Enter untuk lanjut ke test berikutnya...")
    
    print_header("TEST SELESAI")

if __name__ == "__main__":
    main()
```

### 7️⃣ Tips untuk Development di Laptop

1. **Gunakan Python virtual environment** (sudah)
2. **Testing dengan sesi pendek**: Jangan jalankan 24/7 di laptop
3. **Monitoring log**: Perhatikan `bridge.log`
4. **Simulasi putus koneksi**: Matikan WiFi sebentar untuk test reconnect
5. **Test semua fitur**: Filter, delay, error handling

### 8️⃣ Perbedaan Kode untuk Telethon

Tidak ada perbedaan signifikan dalam penggunaan `from telethon import TelegramClient, events`. Yang perlu diperhatikan:

```python
# Cara 1: Decorator (yang kita gunakan)
@client.on(events.NewMessage(chats=[CHAT_ID]))
async def handler(event):
    pass

# Cara 2: add_event_handler (alternatif)
async def handler(event):
    pass
client.add_event_handler(handler, events.NewMessage(chats=[CHAT_ID]))
```

Keduanya valid dan tidak ada perubahan performa signifikan antara laptop dan Pi/VPS.

### 9️⃣ Checklist Sebelum Pindah ke Raspberry Pi

- [x] Semua test berjalan di laptop
- [x] File `.env` sudah lengkap
- [x] Session file Telethon tersimpan
- [x] Discord bot sudah diinvite ke server
- [x] Log menunjukkan tidak ada error
- [x] Delay sudah diatur (2-3 detik)
- [x] Filter berfungsi sesuai keinginan

### 🔟 Migration ke Raspberry Pi

```bash
# Di Raspberry Pi
# 1. Clone repo dari laptop (atau copy via SCP)
git clone https://github.com/username/telegram-discord-bridge.git
# atau
scp -r telegram-discord-bridge pi@raspberrypi.local:~

# 2. Setup environment
cd telegram-discord-bridge
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Copy file .env dari laptop
scp .env pi@raspberrypi.local:~/telegram-discord-bridge/

# 4. Copy session file (penting!)
scp reader_session.session pi@raspberrypi.local:~/telegram-discord-bridge/

# 5. Test di Pi
python main.py
```

## 📊 Kesimpulan

1. **Tidak ada perubahan kode** yang diperlukan untuk pindah dari laptop ke Raspberry Pi/VPS
2. **Session file** bisa dicopy langsung, tidak perlu login ulang
3. **Testing di laptop** sangat disarankan sebelum deployment
4. **Perbedaan utama** hanya di environment (OS, network, uptime)

Dengan testing di laptop terlebih dahulu, Anda bisa memastikan semua fitur berfungsi sebelum menjalankan 24/7 di Raspberry Pi atau VPS.