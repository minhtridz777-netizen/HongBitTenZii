# MugenFake – game đối kháng 2D trên IKEMEN GO

Game đối kháng 2D kiểu Bleach vs Naruto: nhân vật nhỏ, map rộng có bậc nhảy, chơi bằng bàn phím.
Nhân vật được thiết kế và viết code cùng Claude (Claude Code) – xem `CLAUDE.md`.

> Dự án cá nhân, phi lợi nhuận. Engine IKEMEN GO không nằm trong repo này.

## Cài đặt (Windows 64-bit)

1. Tải **IKEMEN GO v1.0.0** (Windows 64-bit) tại
   https://github.com/ikemen-engine/Ikemen-GO/releases/tag/v1.0.0 và giải nén vào một thư mục, vd `D:\MugenFake`.
2. Đưa repo này vào **chính thư mục đó** (repo ghi đè vài file cấu hình của engine):

   ```powershell
   cd D:\MugenFake
   git init
   git remote add origin <link repo này>
   git fetch origin
   git checkout -f -b develop --track origin/develop
   ```
3. Chạy:
   - `LAB.exe` – phòng test tướng: chọn tướng, đánh Bù Nhìn, có bảng sát thương/combo.
   - `Ikemen_GO.exe` – game bình thường.

Công cụ sinh hình/map (tuỳ chọn): Python 3 + `pip install pillow` – xem `tools/README.md`.

## Phím
| Người chơi 1 | Người chơi 2 | Chức năng |
|---|---|---|
| W A S D | ↑ ← ↓ → | W: chỉ dùng trong tổ hợp · S: giữ để đỡ · A/D: đi |
| J | Numpad 1 | Đánh thường |
| K | Numpad 2 | Nhảy (nhảy đôi) · S+K trên bậc: xuống |
| L | Numpad 3 | Lướt (xuyên người) · W+L: Bước Ma · S+L: thoát combo |
| U | Numpad 4 | Chiêu |
| I | Numpad 5 | Tuyệt chiêu (I, W+I: 1 thanh · S+I: 3 thanh) |

## Tài liệu
| File | Nội dung |
|---|---|
| `CLAUDE.md` | Quy tắc dự án (Claude đọc file này đầu tiên) |
| `.github/CONTRIBUTING.md` | **Quy tắc nhánh, commit, Pull Request** – đọc trước khi đóng góp |
| `designs/KHUNG_CHUAN.md` | Luật chung mọi nhân vật |
| `designs/QUY_TRINH_TAO_TUONG.md` | Quy trình tạo tướng – nói với Claude "tạo tướng <tên>" hoặc gõ `/tao-tuong <tên>` |
| `.claude/` | Lệnh tắt `/tao-tuong` và agent `nghien-cuu-tuong` cho Claude Code |
| `shared/char_template/README.md` | Template nhân vật + cơ chế chung |
| `tools/README.md` | Công cụ sinh model test, map, chụp màn hình test |

## Ghi chú bản quyền
- Engine IKEMEN GO: MIT (tải riêng, không kèm repo).
- Âm thanh tạm (`*.snd`) copy từ nhân vật mẫu Kung Fu Man đi kèm IKEMEN – sẽ thay bằng âm thanh riêng.
- Model test, hiệu ứng, map thử: tự sinh bằng code trong `tools/`.
