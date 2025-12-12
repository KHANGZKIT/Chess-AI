import urllib.request
import os
import ssl

# 1. Tạo thư mục sounds nếu chưa có
if not os.path.exists('sounds'):
    os.makedirs('sounds')
    print("Đã tạo thư mục 'sounds'")

# 2. Danh sách link file âm thanh gốc từ Lichess (Nguồn: Github lila)
# Lưu ý: File gốc là .mp3 (chất lượng cao hơn .wav tự tạo)
urls = {
    "move.mp3": "https://raw.githubusercontent.com/ornicar/lila/master/public/sound/standard/Move.mp3",
    "capture.mp3": "https://raw.githubusercontent.com/ornicar/lila/master/public/sound/standard/Capture.mp3",
    "check.mp3": "https://raw.githubusercontent.com/ornicar/lila/master/public/sound/standard/Check.mp3", 
    "checkmate.mp3": "https://raw.githubusercontent.com/ornicar/lila/master/public/sound/standard/Victory.mp3", # Dùng tiếng chiến thắng cho checkmate
}

# Bỏ qua lỗi chứng chỉ SSL (nếu có)
ssl._create_default_https_context = ssl._create_unverified_context

print("--- ĐANG TẢI ÂM THANH TỪ LICHESS ---")

for filename, url in urls.items():
    save_path = os.path.join('sounds', filename)
    try:
        print(f"Đang tải: {filename}...")
        urllib.request.urlretrieve(url, save_path)
        print(f"✅ Thành công: {save_path}")
    except Exception as e:
        print(f"❌ Lỗi khi tải {filename}: {e}")

print("\nHoàn tất! Kiểm tra thư mục 'sounds'.")