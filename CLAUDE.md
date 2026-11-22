# Dự án: Game đối kháng 2D trên IKEMEN GO

## Tổng quan
- Game đối kháng 2D kiểu Bleach vs Naruto / Mugen, chơi bằng bàn phím với tổ hợp phím combo, gồm **nhiều nhân vật**.
- **Người dùng**: lên ý tưởng nhân vật/chiêu thức, duyệt bản thiết kế, chơi thử và nhận xét.
- **Claude**: biến ý tưởng thành bản thiết kế, viết toàn bộ file nhân vật, sửa theo nhận xét.
- Engine: **IKEMEN GO bản Stable** (Windows 64-bit). Thư mục này là thư mục gốc của IKEMEN GO.
- Giao tiếp với người dùng bằng **tiếng Việt**, ngắn gọn, dễ hiểu.

---

## Cấu trúc thư mục

```
<gốc IKEMEN>/
├── CLAUDE.md                  ← file này (quy tắc chung toàn dự án)
├── designs/
│   ├── TEMPLATE_DESIGN.md     ← mẫu thiết kế nhân vật
│   └── <TÊN>_DESIGN.md        ← bản thiết kế từng nhân vật (nguồn chuẩn)
├── shared/
│   └── char_template/         ← bộ khung nhân vật dùng chung (tạo sau nhân vật đầu tiên)
├── chars/<tên>/               ← file nhân vật: .def .cns .cmd .air .sff .snd
├── tools/                     ← script Python sinh sprite/animation (xem tools/README.md)
└── data/select.def            ← danh sách nhân vật trong màn chọn (kiểm tra đúng vị trí)
```

- Tên thư mục nhân vật: chữ thường, không dấu, không khoảng trắng (vd `nakroth`, `kael`).
- **Bản thiết kế trong `designs/` là nguồn chuẩn.** Code làm đúng theo thiết kế; thay đổi gì thì cập nhật thiết kế trước.

---

## Chuẩn chung cho MỌI nhân vật

### Phím điều khiển

**Quy định chung:** người chơi chỉ dùng **một trong hai bộ phím** dưới đây, không thêm phím nào khác
(Enter / Numpad Enter chỉ để vào menu, tạm dừng). Nhân vật mới không được thiết kế chiêu cần phím ngoài bảng.

| Người chơi 1 | Người chơi 2 | Nút IKEMEN | Chức năng |
|---|---|---|---|
| W A S D | ↑ ← ↓ → | Up / Back / Down / Fwd | Di chuyển + hướng cho tổ hợp |
| J | Numpad 1 | `a` | Đánh thường |
| K | Numpad 2 | `b` | Nhảy |
| L | Numpad 3 | `c` | Lướt (dash) |
| U | Numpad 4 | `x` | Chiêu đặc biệt |
| I | Numpad 5 | `y` | Tuyệt chiêu |
| O | Numpad 6 | `z` | Trợ thủ (để dành) |

Nút phụ `d` / `w` của IKEMEN (đổi nhân vật chế độ Tag) để **Not used**. Cấu hình nằm ở `save/config.ini`.
Bảng ký hiệu trong file thiết kế dùng phím của người chơi 1.

- `S + J` = **giữ** S rồi bấm J. Ký hiệu `↓↘→ + U` = bấm lần lượt.
- **⚠ Vấn đề phím nhảy (giải quyết 1 lần cho cả dự án, ngay nhân vật đầu tiên):** IKEMEN mặc định nhảy bằng Up (W).
  - Phương án A (ưu tiên): K = nhảy, W chỉ là phím hướng. Tìm cách tắt nhảy bằng Up.
  - Phương án B (dự phòng): W = nhảy kiểu Mugen, K là nhảy phụ. Hỏi người dùng trước khi chọn B.
  - Ghi kết quả vào mục "Quyết định đã chốt" bên dưới.

### Bộ khung lệnh chuẩn
Mọi nhân vật dùng cùng khung để người chơi đổi nhân vật không phải học lại:

| Nhóm | Lệnh |
|---|---|
| Đánh thường | `J` (chuỗi), `W+J`, `S+J`, `J` trên không |
| Chiêu (miễn phí) | `U`, `S+U`, `W+U`, `U` trên không (có thể thêm `A/D+U`) |
| Tuyệt chiêu cấp 1 | `I` – tốn 1 thanh (1000 power) |
| Tuyệt chiêu cấp 3 | `S+I` – tốn 3 thanh (3000 power) |
| Nội tại | Tùy nhân vật, không cần phím |

Năng lượng tối đa: 3000 (3 thanh).

### Quy ước đánh số (để mọi nhân vật đọc giống nhau)

| Khoảng số (state & anim) | Dùng cho |
|---|---|
| 0–199 | State chung (đứng, đi, nhảy, bị đánh…) – theo chuẩn Mugen |
| 200–299 | Đánh thường đứng (chuỗi J, W+J) |
| 400–499 | Đánh thường ngồi (S+J) |
| 600–699 | Đánh thường trên không |
| 700–799 | Lướt (L) |
| 1000–1999 | Chiêu đặc biệt U |
| 3000–3999 | Tuyệt chiêu cấp 1 (I) |
| 4000–4999 | Tuyệt chiêu cấp 3 (S+I) |
| 8000–8999 | Helper, hiệu ứng, đạn |

- Biến: `var(0)–var(9)` để cho hệ thống chung (thời gian tái kích hoạt, cường hóa, nội tại…), `var(10)` trở lên tùy nhân vật. Ghi chú công dụng từng biến ở đầu file `.cns`.

### Thang cân bằng (điểm khởi đầu)

| Mục | Khoảng |
|---|---|
| Máu | 800–1200 (chuẩn 1000) |
| Đòn J lẻ | 20–50 |
| Chiêu U | 50–100 |
| Tuyệt chiêu cấp 1 | 180–250 |
| Tuyệt chiêu cấp 3 | 330–420 |

Nhân vật "đánh đau" thì phải có điểm yếu rõ (máu thấp, chậm, tầm ngắn…).

---

## Quy trình thêm một nhân vật mới

1. **Thiết kế:** người dùng đưa ý tưởng (có thể chỉ vài dòng). Claude tìm hiểu thêm nếu là nhân vật có sẵn, điền `TEMPLATE_DESIGN.md` thành `designs/<TÊN>_DESIGN.md`. **Người dùng duyệt** rồi mới làm.
2. **Dựng bằng hình tạm:** copy từ `shared/char_template/` (nếu đã có), không thì tham khảo KFM. Thứ tự: chỉ số + di chuyển + lướt → đánh thường → chiêu U → nội tại → tuyệt chiêu.
3. **Kiểm tra kỹ thuật:** nhân vật load được, không lỗi log, có trong màn chọn.
4. **Người dùng test** theo danh sách combo trong bản thiết kế → nhận xét → chỉnh.
5. **Hình ảnh thật + hiệu ứng + âm thanh** (khi người dùng có sprite).
6. **Cập nhật bảng Roster** bên dưới và commit.

### Làm nhiều nhân vật cùng lúc
- Mỗi nhân vật nằm gọn trong thư mục riêng, **không sửa nhân vật này khi đang làm nhân vật khác**.
- Có thể chia mỗi nhân vật cho một subagent chạy song song; mỗi nhân vật commit riêng.
- Thiết kế phải được duyệt hết trước khi dựng hàng loạt.

### Bộ khung dùng chung
- Sau khi nhân vật đầu tiên chạy ổn, tách các phần lặp lại (khung `.cmd` theo bảng phím, state lướt, cơ chế tái kích hoạt chiêu, cường hóa có thời hạn, super pause…) vào `shared/char_template/` kèm `README.md` hướng dẫn copy.
- Khi nhân vật mới cần cơ chế mà nhân vật cũ đã có → lấy từ template, không viết lại từ đầu. Cải tiến cơ chế chung thì cập nhật template.

---

## Quy tắc làm việc

1. **Không sửa file của engine** (exe, `external/script/`, dữ liệu mặc định) trừ khi thật sự cần và đã hỏi người dùng.
2. **Không cập nhật phiên bản engine** giữa chừng.
3. Không chắc cú pháp CNS/CMD/AIR hay tính năng IKEMEN: tra wiki chính thức `github.com/ikemen-engine/Ikemen-GO/wiki` và xem file của KFM (`chars/kfm/`), không đoán.
4. Dùng **Git**: commit sau mỗi bước chạy được, message ngắn tiếng Việt, ghi rõ tên nhân vật (vd `nakroth: thêm chiêu U tái kích hoạt`).
5. Sau mỗi lần sửa: kiểm tra nhân vật load được, sửa hết lỗi cú pháp rồi mới báo người dùng test.
6. **Claude không tự chơi được game.** Sau mỗi bước, đưa người dùng danh sách ngắn "cần test gì", chờ nhận xét rồi chỉnh.
7. Comment trong code bằng tiếng Việt, ghi rõ chiêu nào nằm ở đâu.
8. Hình tạm: được mượn sprite KFM. Số animation phải theo quy ước để sau thay sprite thật không phải sửa logic.

---

## Roster (cập nhật khi tiến độ thay đổi)

| Nhân vật | Thiết kế | Giai đoạn | Ghi chú |
|---|---|---|---|
| Nakroth | `designs/NAKROTH_DESIGN.md` (v2 đã duyệt) | Đã dựng v2 (hình tạm KFM + vệt chém tự vẽ) – chờ test | Load OK, trận AI-đấu-AI chạy không lỗi. Cần kiểm tra siêu giáp `I` |

## Lộ trình dự án
- [ ] Nhân vật đầu tiên (Nakroth) chơi được hoàn chỉnh với hình tạm
- [ ] Chốt phím nhảy + tạo `shared/char_template/`
- [ ] Thêm nhân vật 2–4 (dùng template)
- [ ] Sprite thật, hiệu ứng, âm thanh
- [ ] Màn chơi (stage), giao diện, chế độ chơi
- [ ] Đóng gói phát hành bản chơi riêng

## Quyết định đã chốt
- Engine: IKEMEN GO Stable (`v1.0.0`, build 2026.09.12).
- Phím nhảy: **Phương án A** – K = nhảy, W chỉ là hướng. Cách làm: mỗi nhân vật đặt
  `AssertSpecial flag = NoJump, flag2 = NoAirJump` trong `[Statedef -2]` của `.cns`, và trong `.cmd`
  lệnh `"K"` (`command = b`) → `ChangeState 40` khi `statetype = S && ctrl` (xem `chars/nakroth/`).
- Bàn phím: chỉ 2 bộ phím (xem "Phím điều khiển"). Bản gốc engine dùng mũi tên + Z/X/C, đã đổi trong `save/config.ini`.

## Ghi chú
- 60 tick = 1 giây.
- Kiểm tra load nhanh (không qua menu): `Ikemen_GO.exe -p1 <tên> -p2 kfm_zss -s stage0 -rounds 1 -windowed -nosound`.
  File nhân vật lỗi → engine thoát ngay với "panic"; chạy tiếp bình thường = load OK.
