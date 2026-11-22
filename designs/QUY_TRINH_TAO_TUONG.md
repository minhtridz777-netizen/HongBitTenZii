# QUY TRÌNH TẠO TƯỚNG (đã chốt)

> **Kích hoạt:** người dùng nói "tạo tướng <tên>" (có thể kèm vài dòng ý tưởng).
> Claude làm liền một mạch theo các bước dưới đây, **chỉ dừng ở các bước ✅** để chờ người dùng,
> ngoài ra chỉ hỏi khi thiếu thông tin thật sự. Luật chung: `designs/KHUNG_CHUAN.md`.

---

## Giai đoạn A – Thiết kế (chỉ tài liệu, chưa đụng code)

### A1. Nhận yêu cầu
- Kiểm tra bảng Roster trong `CLAUDE.md`: tướng đã có chưa.
- Đặt tên thư mục: chữ thường, không dấu, không khoảng trắng (vd `ichigo`, `zoro`).
- Tạo `designs/<TEN>_DESIGN.md` từ `designs/TEMPLATE_DESIGN.md` (trạng thái "Nháp").

### A2. Tra cứu (Claude tự làm, bằng tìm kiếm web)
Tìm và ghi vào mục **0. Hồ sơ tra cứu** của bản thiết kế, kèm link nguồn:
- Tác phẩm gốc, vai trò, tính cách, phong cách chiến đấu.
- Vũ khí, năng lực, dáng người (nhỏ / to con / vũ khí dài / biết bay…), màu chủ đạo.
- **Kỹ năng nổi tiếng**, chiêu cuối, biến hình (đây là nguồn để đặt chiêu).
- Nếu nhân vật đã có trong game đối kháng khác (Bleach vs Naruto, Jump Force, Mugen…): bộ chiêu ở đó để tham khảo.
- Tướng **tự nghĩ** (không có bản gốc): bỏ bước này, gợi ý từ ý tưởng của người dùng.
- Nguồn mâu thuẫn thì ghi rõ nguồn nào nói gì, không tự đoán.

### A3. Nhờ người dùng tìm ảnh
- Nhắn người dùng: tìm **1–3 ảnh** (toàn thân, chiêu đặc trưng, ảnh bìa) bỏ vào `designs/ref/<ten>/`.
- Claude **không tự tải ảnh**. Không có ảnh vẫn làm tiếp giai đoạn A và B; bắt buộc có trước bước C1.

### A4. Viết bản thiết kế
Điền đủ `designs/<TEN>_DESIGN.md`:
- Lối chơi 1 câu, chỉ số, **điểm yếu rõ** (theo thang cân bằng trong `CLAUDE.md`).
- **Bộ chiêu bắt buộc**, lấy từ kỹ năng gốc (ghi rõ chiêu nào lấy từ kỹ năng nào):
  chuỗi `J`, `W+J` (hất), `S+J`, `J` trên không, `U`, `W+U`, `S+U`, `U` trên không, `I`, `W+I`, `S+I`.
- Kiểu thoát combo `S+L` riêng (hoặc dùng mặc định), nội tại, **1–3 chiêu ẩn**.
- 4–5 combo để kiểm tra.
- Màu model test (R,G,B chính + phụ), có cần biến thể model test không.
- Không thiết kế chiêu cần phím ngoài bảng phím chuẩn.

### A5. ✅ Người dùng duyệt thiết kế
- Gửi tóm tắt ngắn (bảng chiêu + điểm đặc biệt), chờ duyệt. Sửa đến khi chốt → trạng thái "Đã duyệt".

---

## Giai đoạn B – Dựng bằng model test

### B1. Tạo thư mục từ template
Làm theo `shared/char_template/README.md`:
- Copy `mau.cmd`, `mau.cns`, `mau.def`, `mau.snd` sang `chars/<ten>/<ten>.*`.
- `.def`: đổi tên, tên file, **`st2 = ../../shared/char_template/khung.cns`**.
- Sinh model test: `python tools/gen_model.py chars/<ten> <ten> R,G,B R,G,B`.
- Tướng có vũ khí / to con / bay: thêm tư thế, biến thể trong `tools/gen_model.py` (giữ đúng số anim chuẩn).

### B2. Viết chiêu theo thứ tự
Chỉ số → đánh thường → chiêu U → nội tại → tuyệt chiêu → chiêu ẩn → thoát combo riêng.
- Mỗi chiêu có **hiệu ứng tối giản** theo màu của tướng (vệt chém, cầu, tia… – nhóm 8000+).
- Theo "Quy tắc khi viết chiêu" trong `shared/char_template/README.md` (guardflag MA, tia nhỏ S8010, biến var(10)+…).
- Comment tiếng Việt, ghi rõ chiêu nào ở đâu; bảng biến ở đầu file `.cns`.

### B3. Tự kiểm tra (bắt buộc trước khi báo người dùng)
- Nhân vật load được (engine không "panic").
- Thêm vào `data/select.def`: `<ten>, stages/lab_bac.def`.
- Dùng `tools/shot.py` + `LAB_LOG=1` + `SHOT_KEYS` (xem Ghi chú trong `CLAUDE.md`) **thử từng chiêu**:
  có ra đòn, có trúng Bù Nhìn, sát thương khớp thiết kế (bảng LAB), đối thủ ngã/đứng dậy bình thường, không kẹt.
- Chụp vài ảnh xem hình, hiệu ứng có hiện đúng.
- Commit: `<ten>: dựng bằng model test`.

### B4. ✅ Người dùng chơi thử trong LAB
- Gửi danh sách ngắn "cần test gì" (theo mục Combo để kiểm tra + chiêu ẩn).
- Nhận xét → chỉnh → kiểm tra lại (B3) → commit. Lặp đến khi người dùng hài lòng.

---

## Giai đoạn C – Hình thật

### C1. Vẽ model chuẩn
- Dựa trên ảnh trong `designs/ref/<ten>/`. Chấp nhận ~60% chất lượng mẫu, phong cách ít chi tiết.
- **Giữ nguyên số animation và số thứ tự elem có vùng đánh** (code chiêu không phải sửa).
- Animation bị đánh/ngã giữ thời lượng như model test (không dùng khung vô hạn sai chỗ).

### C2. ✅ Người dùng duyệt hình

### C3. Vẽ hiệu ứng chiêu thức đẹp (thay hiệu ứng tối giản)

### C4. ✅ Người dùng duyệt hiệu ứng

---

## Giai đoạn D – Hoàn thiện

### D1. Âm thanh, AI, cân bằng
- Âm thanh chiêu (thay âm thanh tạm), AI cho máy đánh, cân bằng với các tướng đã có.
- Ảnh đại diện từ model chuẩn: 9000,0 = 50×50 (khung thanh máu), 9000,1 = 240×280 (màn chọn).

### D2. ✅ Người dùng duyệt lần cuối
- Cập nhật bảng **Roster** trong `CLAUDE.md`, trạng thái thiết kế "Xong", commit.

---

## Mẫu tin nhắn cho người dùng
- Sau A3: "Bạn tìm giúp 1–3 ảnh <tên> (toàn thân, chiêu đặc trưng) bỏ vào `designs/ref/<ten>/` nhé – không gấp, cần trước bước vẽ model chuẩn."
- Ở mỗi bước ✅: tóm tắt ngắn đã làm gì, cần người dùng làm/duyệt gì.
