import urllib.request
import os
import ssl
import time

# 1. Tạo thư mục sounds
if not os.path.exists('sounds'):
    os.makedirs('sounds')
    print("📂 Đã tạo thư mục 'sounds'")

# 2. Danh sách link file - Sử dụng link đúng từ lichess lila repo
# Link mới từ branch chính của lichess
urls = {
    "move.mp3": "https://github.com/lichess-org/lila/raw/master/public/sound/standard/Move.mp3",
    "capture.mp3": "https://github.com/lichess-org/lila/raw/master/public/sound/standard/Capture.mp3",
    "check.mp3": "https://github.com/lichess-org/lila/raw/master/public/sound/standard/GenericNotify.mp3",  # Check sound
    "checkmate.mp3": "https://github.com/lichess-org/lila/raw/master/public/sound/standard/Confirmation.mp3",
}

# 3. Bỏ qua lỗi SSL (để tránh lỗi chứng chỉ trên một số máy Windows/Mac cũ)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print("--- 🚀 BẮT ĐẦU TẢI TỪ LICHESS GITHUB ---")

# Giả làm trình duyệt Chrome để không bị GitHub chặn
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for filename, url in urls.items():
    save_path = os.path.join('sounds', filename)
    print(f"⬇️  Đang tải: {filename}...", end=" ")
    
    try:
        # Tạo request với headers giả lập trình duyệt
        req = urllib.request.Request(url, headers=headers)
        
        # Mở kết nối và tải dữ liệu
        with urllib.request.urlopen(req, context=ctx) as response:
            data = response.read()
            
            # Ghi dữ liệu vào file
            with open(save_path, 'wb') as f:
                f.write(data)
                
        print(f"✅ OK! ({len(data)} bytes)")
        
    except Exception as e:
        print(f"\n❌ LỖI: {e}")

print("\n🎉 Hoàn tất! Hãy mở folder 'sounds' để kiểm tra.")