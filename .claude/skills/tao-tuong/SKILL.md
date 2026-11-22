---
name: tao-tuong
description: Tạo một nhân vật (tướng) mới cho game đối kháng MugenFake theo đúng quy trình dự án - tra cứu, viết bản thiết kế, chờ duyệt, dựng bằng model test, tự kiểm tra. Dùng khi người dùng gõ /tao-tuong <tên> hoặc nói "tạo tướng <tên>".
argument-hint: <tên nhân vật> [ý tưởng thêm]
---

# Tạo tướng: $ARGUMENTS

Làm đúng theo **`designs/QUY_TRINH_TAO_TUONG.md`** (đọc file đó trước, nó là nguồn chuẩn; file này chỉ là lối tắt).
Luật chung: `designs/KHUNG_CHUAN.md`. Quy tắc Git: `.github/CONTRIBUTING.md`. Giao tiếp tiếng Việt, ngắn gọn.

## Các bước

1. **A1 – Nhận yêu cầu**
   - Tên tướng là phần đầu của tham số; phần sau (nếu có) là ý tưởng của người dùng.
   - Kiểm tra Roster trong `CLAUDE.md`. Đặt tên thư mục `<ten>`: chữ thường, không dấu, không khoảng trắng.
   - Tạo nhánh `tuong/<ten>` từ `develop` (`git switch develop`, `git pull`, `git switch -c tuong/<ten>`).
   - Tạo `designs/<TEN>_DESIGN.md` từ `designs/TEMPLATE_DESIGN.md`, trạng thái "Nháp".

2. **A2 + A4 – Tra cứu và gợi ý bộ chiêu: giao cho agent `nghien-cuu-tuong`**
   - Gọi agent với: tên tướng, ý tưởng của người dùng, đường dẫn file thiết kế.
   - Agent điền mục 0 (Hồ sơ tra cứu) và bản nháp các mục 1–9 vào file thiết kế, trả về tóm tắt.
   - Đọc lại file thiết kế, kiểm tra: đủ bộ chiêu bắt buộc, đúng thang cân bằng, không dùng phím ngoài bảng phím chuẩn,
     có điểm yếu rõ. Sửa nếu thiếu.

3. **A3 – Nhờ người dùng tìm ảnh**: 1–3 ảnh (toàn thân, chiêu đặc trưng) bỏ vào `designs/ref/<ten>/`.
   Không gấp, chỉ cần trước bước vẽ model chuẩn. Không tự tải ảnh.

4. **A5 – ✅ DỪNG, chờ người dùng duyệt thiết kế.**
   Gửi bảng tóm tắt bộ chiêu + nội tại + chiêu ẩn + điểm yếu. Sửa theo nhận xét đến khi người dùng chốt
   → trạng thái "Đã duyệt", commit `<ten>: thiết kế`.

5. **Giai đoạn B** (chỉ làm sau khi thiết kế đã duyệt): làm theo B1–B3 trong quy trình
   (copy template, sinh model test, viết chiêu, tự kiểm tra trong LAB bằng `tools/shot.py` + `LAB_LOG=1`, commit).

6. **B4 – ✅ DỪNG, gửi danh sách "cần test gì"**, chờ người dùng chơi thử trong `LAB.exe`.
   Khi người dùng đồng ý: đẩy nhánh `tuong/<ten>` lên và mở Pull Request vào `develop`.

Các giai đoạn C (vẽ model chuẩn, hiệu ứng) và D (âm thanh, AI, cân bằng) làm khi người dùng yêu cầu,
vẫn theo `designs/QUY_TRINH_TAO_TUONG.md`.
