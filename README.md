# ♟️ Chess AI - Trí Tuệ Nhân Tạo Chơi Cờ Vua

> Dự án môn học **Trí Tuệ Nhân Tạo (TTNT)** - Đại học Công nghiệp Hà Nội (HAUI)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📖 Giới Thiệu

Đây là game cờ vua được xây dựng bằng **Python** và **Pygame**, tích hợp AI sử dụng thuật toán **Negamax với cắt tỉa Alpha-Beta** để tìm nước đi tối ưu.

### ✨ Tính Năng

- 🎮 Giao diện đồ họa trực quan với Pygame
- 🤖 AI thông minh sử dụng thuật toán Negamax + Alpha-Beta Pruning
- ♟️ Hỗ trợ đầy đủ luật cờ vua:
  - Nhập thành (Castling)
  - Bắt tốt qua đường (En Passant)
  - Phong cấp tốt (Pawn Promotion)
  - Phát hiện Chiếu/Chiếu hết/Hòa
- 🔄 Undo nước đi (phím Z)
- 🔁 Reset game (phím R)
- 📝 Hiển thị lịch sử nước đi
- ✨ Animation di chuyển quân mượt mà
- 💡 Highlight gợi ý nước đi hợp lệ

---

## 🛠️ Cài Đặt

### Yêu Cầu Hệ Thống

- Python 3.8 trở lên
- Pygame 2.0 trở lên

### Hướng Dẫn Cài Đặt

1. **Clone hoặc tải project về máy:**
   ```bash
   git clone <repository-url>
   cd chess
   ```

2. **Tạo môi trường ảo (khuyến nghị):**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Cài đặt thư viện cần thiết:**
   ```bash
   pip install pygame
   ```

---

## 🎮 Cách Chơi

### Khởi động game:
```bash
python ChessMain.py
```

### Điều Khiển

| Thao tác | Mô tả |
|----------|-------|
| **Chuột trái** | Chọn quân cờ và di chuyển |
| **Phím Z** | Undo - Hoàn tác nước đi |
| **Phím R** | Reset - Chơi lại từ đầu |

### Chế Độ Chơi

Mặc định: **Người (Trắng)** vs **Máy (Đen)**

Để thay đổi chế độ, chỉnh sửa trong file `ChessMain.py`:
```python
player_one = True   # True = Người chơi, False = AI
player_two = False  # True = Người chơi, False = AI
```

| player_one | player_two | Chế độ |
|------------|------------|--------|
| True | False | Người vs Máy |
| True | True | Người vs Người |
| False | False | Máy vs Máy |

---

## 📁 Cấu Trúc Dự Án

```
chess/
├── ChessMain.py      # Giao diện đồ họa & vòng lặp game chính
├── ChessEngine.py    # Logic cờ vua & quản lý trạng thái
├── ChessAI.py        # Thuật toán AI (Negamax + Alpha-Beta)
├── images/           # Hình ảnh quân cờ
│   ├── wK.png, wQ.png, wR.png, wB.png, wN.png, wp.png
│   └── bK.png, bQ.png, bR.png, bB.png, bN.png, bp.png
└── README.md         # Hướng dẫn sử dụng
```

---

## 🧠 Thuật Toán AI

### Negamax với Alpha-Beta Pruning

AI sử dụng thuật toán **Negamax** (biến thể của Minimax) kết hợp **cắt tỉa Alpha-Beta** để tối ưu hóa việc tìm kiếm.

**Độ sâu tìm kiếm:** 3 nước (có thể điều chỉnh trong `ChessAI.py`)

### Hàm Đánh Giá (Evaluation Function)

1. **Giá trị quân cờ:**
   | Quân | Điểm |
   |------|------|
   | Vua (King) | ∞ |
   | Hậu (Queen) | 9 |
   | Xe (Rook) | 5 |
   | Tượng (Bishop) | 3 |
   | Mã (Knight) | 3 |
   | Tốt (Pawn) | 1 |

2. **Piece-Square Tables:** Điểm thưởng/phạt dựa trên vị trí quân cờ trên bàn

---

## 👥 Thành Viên Nhóm

| STT | Họ và Tên | Vai trò |
|-----|-----------|---------|
| 1 | Vũ Tiến Khang | Team Lead, Core Logic, AI |
| 2 | Lại Hải Nam | GUI, Integration |
| 3 | Mai Văn Hưng | Game Engine, Testing |
| 4 | Nguyễn Huy Hoàng | AI Evaluation, Documentation |

---

## 📸 Screenshots

```
┌─────────────────────────────────────────┐
│  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜  │  Move Log Panel  │
│  ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟  │                  │
│  ·  ·  ·  ·  ·  ·  ·  ·  │  1. e4 e5      │
│  ·  ·  ·  ·  ·  ·  ·  ·  │  2. Nf3 Nc6    │
│  ·  ·  ·  ·  ·  ·  ·  ·  │  ...           │
│  ·  ·  ·  ·  ·  ·  ·  ·  │                │
│  ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙  │                  │
│  ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖  │                  │
└─────────────────────────────────────────┘
         512 x 512 px      250 px
```

---

## 📄 License

Dự án được phát triển cho mục đích học tập tại **Đại học Công nghiệp Hà Nội (HAUI)**.

---

## 🔗 Tham Khảo

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Chess Programming Wiki](https://www.chessprogramming.org/)
- [Negamax Algorithm](https://en.wikipedia.org/wiki/Negamax)
- [Alpha-Beta Pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)

---

<p align="center">
  Made with ❤️ by HAUI Students | Kỳ 5 - Môn TTNT
</p>
