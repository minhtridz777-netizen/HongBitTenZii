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
│   ├── char_template/         ← template: khung.cns (cơ chế chung, mọi tướng trỏ tới) + nhân vật mẫu "Mau" (xem README.md)
│   └── system/platforms.zss   ← code bậc dùng chung (nạp qua save/config.ini)
├── chars/<tên>/               ← file nhân vật: .def .cns .cmd .air .sff .snd
├── chars/bunhin/              ← Bù Nhìn: bao cát cho LAB / chế độ Training (model test màu rơm, không có đòn)
├── stages/lab_bac.def         ← map thử 640×360, rộng 3 màn hình, 6 bậc (map của LAB)
├── LAB.exe                    ← phòng luyện tập: mở thẳng màn chọn tướng, đánh Bù Nhìn
├── external/mods/lab.lua      ← logic LAB (mod của dự án, chỉ chạy khi có cờ -lab)
├── tools/                     ← script Python sinh sprite/animation, chụp màn hình test (xem tools/README.md)
└── data/select.def            ← danh sách nhân vật trong màn chọn (kiểm tra đúng vị trí)
```

### LAB – phòng test tướng
- Mở `LAB.exe` → chọn tướng (J) → vào trận với Bù Nhìn: không giới hạn thời gian, tự hồi máu và năng lượng.
- Bảng thông tin góc trên trái: state/anim/ctrl, sát thương đòn cuối, combo, combo lớn nhất, lợi thế khung hình, var(0)–var(11).
- Enter (người chơi 1) mở menu tạm dừng → chỉnh Bù Nhìn (đứng/ngồi/nhảy, đỡ đòn, thoát ngã, AI...), về màn chọn tướng.
- `external/mods/lab.lua` là file của dự án (không phải file engine). `Ikemen_GO.exe` chạy bình thường thì mod không làm gì.
- Tướng mới chỉ cần có trong `data/select.def` là hiện trong LAB.

- Tên thư mục nhân vật: chữ thường, không dấu, không khoảng trắng (vd `nakroth`, `kael`).
- **Bản thiết kế trong `designs/` là nguồn chuẩn.** Code làm đúng theo thiết kế; thay đổi gì thì cập nhật thiết kế trước.

---

## Chuẩn chung cho MỌI nhân vật

> **Nguồn chuẩn đầy đủ: `designs/KHUNG_CHUAN.md`** (đã duyệt): tỉ lệ hình, phím, cơ chế chung, bộ chiêu bắt buộc, quy trình.
> Phần dưới đây là tóm tắt; mâu thuẫn thì theo KHUNG_CHUAN.md.

### Hình ảnh
- Game 1280×720, hệ toạ độ **640×360** cho cả nhân vật và map. Nhân vật cao ~56 px (≈1/6 màn hình), ít chi tiết, hiệu ứng đẹp.
- Map rộng 2–3 màn hình, có bậc lơ lửng (code chung `shared/system/platforms.zss`, map khai báo bậc ở `[Constants]`).
- Camera giữa 2 nhân vật, xa nhau thì thu nhỏ.

### Phím điều khiển

**Quy định chung:** người chơi chỉ dùng **một trong hai bộ phím** dưới đây, không thêm phím nào khác
(Enter / Numpad Enter chỉ để vào menu, tạm dừng). Nhân vật mới không được thiết kế chiêu cần phím ngoài bảng.

| Người chơi 1 | Người chơi 2 | Nút IKEMEN | Chức năng |
|---|---|---|---|
| W | ↑ | Up | Bấm riêng **không làm gì**, chỉ dùng trong tổ hợp |
| S | ↓ | Down | **Giữ = đỡ** (đứng yên, A/D đổi hướng đỡ). S + K trên bậc = xuống bậc |
| A D | ← → | Back / Fwd | Đi trái / phải |
| J | Numpad 1 | `a` | Đánh thường |
| K | Numpad 2 | `b` | Nhảy (nhảy đôi khi đang bay) |
| L | Numpad 3 | `c` | Lướt đất / trên không (tốn thể lực) |
| U | Numpad 4 | `x` | Chiêu đặc biệt |
| I | Numpad 5 | `y` | Tuyệt chiêu |
| O | Numpad 6 | `z` | Trợ thủ (để dành) |

Nút phụ `d` / `w` của IKEMEN (đổi nhân vật chế độ Tag) để **Not used**. Cấu hình nằm ở `save/config.ini`.
Bảng ký hiệu trong file thiết kế dùng phím của người chơi 1.

- `S + J` = **giữ** S rồi bấm J. Ký hiệu `↓↘→ + U` = bấm lần lượt.
- Không có cúi người, không đỡ bằng cách giữ lùi kiểu Mugen. Không đỡ được trên không.
- Nhảy bằng K, đã tắt nhảy bằng W (xem "Quyết định đã chốt").

### Cơ chế chung (mọi nhân vật, nằm trong template)
- **Đỡ (giữ S):** chặn mọi đòn từ phía trước mặt; bị đánh sau lưng thì trúng đòn.
- **Thể lực** (thanh chung cho đỡ và lướt, tối đa 100): lướt đất −20, trên không −30; đỡ trúng đòn −(sát thương ÷ 4); hồi khi không đỡ không lướt;
  đang giữ S thì không hồi; hết thể lực khi đang đỡ → vỡ thế (choáng ~1 giây). Số liệu mặc định, chỉnh khi test.
- **Thoát combo (S + L)** khi đang trúng đòn: tốn 1 thanh năng lượng, hình thức thoát tùy tướng.
- **Lướt kiểu Bleach vs Naruto:** xuyên qua người đối thủ, bất tử đầu cú lướt, hủy được từ đòn J trúng.
- **Nhảy đôi, lướt trên không**, lên/xuống bậc.

### Bộ khung lệnh chuẩn
Mọi nhân vật dùng cùng khung để người chơi đổi nhân vật không phải học lại:

| Nhóm | Lệnh |
|---|---|
| Đánh thường | `J` (chuỗi 3–5 nhát), `W+J` (hất), `S+J` (tùy tướng), `J` trên không |
| Chiêu (miễn phí, có thể hồi chiêu) | `U`, `W+U`, `S+U`, `U` trên không (có thể thêm `A/D+U`) |
| Tuyệt chiêu | `I` – 1 thanh, `W+I` – 1 thanh, `S+I` – 3 thanh |
| Thoát combo | `S+L` – 1 thanh |
| Nội tại | Tùy nhân vật, không cần phím |
| Chiêu ẩn | 1–3 tổ hợp đặc biệt mỗi tướng (khuyến khích) |

Năng lượng tối đa: 3000 (3 thanh).

### Quy ước đánh số (để mọi nhân vật đọc giống nhau)

| Khoảng số (state & anim) | Dùng cho |
|---|---|
| 0–199 | State chung (đứng, đi, nhảy, bị đánh…) – theo chuẩn Mugen |
| 200–299 | Đánh thường đứng (chuỗi J, W+J) |
| 400–499 | S + J |
| 600–699 | Đánh thường trên không |
| 700–799 | Lướt đất / trên không, nhảy đôi |
| 800–899 | Cơ chế chung: đỡ, vỡ thế, thoát combo |
| 1000–1999 | Chiêu đặc biệt U |
| 3000–3499 | Tuyệt chiêu `I` |
| 3500–3999 | Tuyệt chiêu `W + I` |
| 4000–4999 | Tuyệt chiêu `S + I` |
| 8000–8999 | Helper, hiệu ứng, đạn |

- Biến: `var(0)–var(9)` để cho hệ thống chung (thời gian tái kích hoạt, cường hóa, nội tại…), `var(10)` trở lên tùy nhân vật. Ghi chú công dụng từng biến ở đầu file `.cns`.

### Thang cân bằng (điểm khởi đầu)

| Mục | Khoảng |
|---|---|
| Máu | 800–1200 (chuẩn 1000) |
| Đòn J lẻ | 20–50 |
| Chiêu U | 50–100 |
| Tuyệt chiêu `I`, `W+I` (1 thanh) | 180–250 |
| Tuyệt chiêu `S+I` (3 thanh) | 330–420 |

Nhân vật "đánh đau" thì phải có điểm yếu rõ (máu thấp, chậm, tầm ngắn…).

---

## Quy trình thêm một nhân vật mới

Chi tiết ở `designs/KHUNG_CHUAN.md` mục 5. Các bước **in đậm** là chỗ người dùng duyệt:

1. Người dùng lên ý tưởng → 2. Claude tra cứu → 3. Claude gợi ý bộ chiêu theo khung (chiêu bắt buộc + chiêu ẩn + nội tại),
   điền `TEMPLATE_DESIGN.md` thành `designs/<TÊN>_DESIGN.md` → **4. Duyệt thiết kế**
5. Dựng bằng **model test** + hiệu ứng tối giản (copy `shared/char_template/`), chạy được trong LAB, không lỗi →
   **6. Duyệt lối chơi** (người dùng test trong LAB, nhận xét, chỉnh)
7. Claude vẽ model chuẩn (chấp nhận ~60% chất lượng mẫu) → **8. Duyệt hình**
9. Vẽ hiệu ứng chiêu thức → 10. Âm thanh, AI máy đánh, cân bằng, ảnh đại diện, danh sách chiêu →
   **11. Duyệt cuối** → cập nhật Roster, commit

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
| Mau (mẫu) | `designs/KHUNG_CHUAN.md` | Template chạy trong LAB | Không phải nhân vật chơi – dùng để copy |

## Lộ trình dự án
- [x] Chốt phím nhảy (K), LAB, thử bậc + camera (map `lab_bac`)
- [x] Khung chuẩn (`designs/KHUNG_CHUAN.md`)
- [x] Model test (búp bê khớp nối ~56 px) + `shared/char_template/` có đủ cơ chế chung, chạy trong LAB
- [ ] Map đầu tiên theo tỉ lệ mới (640×360, có bậc)
- [ ] Nhân vật đầu tiên theo quy trình mới
- [ ] Thêm nhân vật 2–4 (dùng template)
- [ ] Sprite thật, hiệu ứng, âm thanh
- [ ] Màn chơi (stage), giao diện, chế độ chơi
- [ ] Đóng gói phát hành bản chơi riêng

## Quyết định đã chốt
- Engine: IKEMEN GO Stable (`v1.0.0`, build 2026.09.12).
- Phím nhảy: **Phương án A** – K = nhảy, W chỉ là hướng. Cách làm: mỗi nhân vật đặt
  `AssertSpecial flag = NoJump, flag2 = NoAirJump` trong `[Statedef -2]` của `.cns`, và trong `.cmd`
  lệnh `"K"` (`command = b`) → `ChangeState 40` (nằm sẵn trong `shared/char_template/khung.cns`).
- Bàn phím: chỉ 2 bộ phím (xem "Phím điều khiển"). Bản gốc engine dùng mũi tên + Z/X/C, đã đổi trong `save/config.ini`.

## Ghi chú
- 60 tick = 1 giây.
- Nakroth (thiết kế/code cũ) đã xoá theo khung mới; xem lại bằng git nếu cần.
- Kiểm tra load nhanh (không qua menu): `Ikemen_GO.exe -p1 <tên> -p2 kfm_zss -s stage0 -rounds 1 -windowed -nosound`.
  File nhân vật lỗi → engine thoát ngay với "panic"; chạy tiếp bình thường = load OK.
- Claude tự xem hình trong game: `python tools/shot.py <tiền tố ảnh> <giây1,giây2,...> -- -lab -loadmotif -p1 <tên> -p2 bunhin -p1.ai 8 -s stage0 -rounds 1 -windowed -nosound`
  (máy tự đánh Bù Nhìn, có bảng LAB, chụp cửa sổ game vào các giây chỉ định). Lưu ảnh vào thư mục tạm, không vào dự án.
  Thêm `SHOT_KEYS="6:S:2,8:S+I"` để bấm phím cho P1, `LAB_LOG=1` để in log mỗi lần state P1/P2 đổi (kiểm chiêu tự động).
  Đường dẫn tướng mẫu: `-p1 ../shared/char_template/mau.def`; năng lượng ban đầu: `-p1.power 3000`.
