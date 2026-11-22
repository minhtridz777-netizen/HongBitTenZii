# NAKROTH – Bản thiết kế nhân vật (v2, đã duyệt)

> Nhân vật dựa trên tướng Nakroth (Liên Quân Mobile). Dự án cá nhân, phi lợi nhuận.
> Lối chơi: **sát thủ song đao, lướt liên tục, chém nhanh, máu mỏng.**
> Trạng thái: **v2 đã duyệt và đã dựng code** (`chars/nakroth/`), chờ người dùng test.

---

## 0. Nakroth gốc trong Liên Quân (đã tra cứu)

| Kỹ năng gốc | Cơ chế trong Liên Quân |
|---|---|
| **Nội tại – Thẩm Phán Oai Nghiêm** | Cứ **đòn đánh thường thứ 4** thì hất tung mục tiêu. Mỗi khi kỹ năng trúng địch (trang chính thức: hoặc khi dùng Nguồn Cơn Rắc Rối) → **+50% tốc đánh ~2,5 giây**. |
| **Chiêu 1 – Bồi Thẩm Đoàn** | **Lướt tới** chém, **hất tung** mục tiêu. Được tung **lần 2 miễn phí trong 5 giây**: lướt thêm một đoạn, cùng sát thương nhưng **không hất tung**. Chỉ sau lần 2 mới bắt đầu hồi chiêu. Xuyên tường. |
| **Chiêu 2 – Nguồn Cơn Rắc Rối** | **Lộn ngược ra sau** (ngược hướng ngắm). **Đòn đánh thường kế tiếp trong 3 giây** thành **chém quét ngang**, tầm xa hơn, sát thương rất lớn (hệ số cao nhất bộ chiêu). Bản thân cú lộn không gây sát thương. Là chiêu thoát thân chính. |
| **Chiêu cuối – Gươm Hành Quyết** | Đứng tại chỗ **chém liên tục** vào kẻ địch trong tầm (tầm ngắn). **Miễn khống chế** suốt chiêu (vẫn mất máu, không phải bất tử). Không hủy được. **Nhát cuối hất tung** kẻ địch. |
| **Combo kinh điển** | Chiêu 2 lao vào → Chiêu 1 hất tung → Chiêu cuối → đánh thường (chém quét) → Chiêu 1 lần 2 để rút lui. |

Nguồn: [trang chính thức Liên Quân](https://lienquan.garena.vn/hoc-vien/tuong-skin/d/nakroth/), [Samurai Gamers](https://samurai-gamers.com/arena-of-valor/aov-nakroth/), [Finhay](https://www.finhay.com.vn/cach-len-do-nakroth-di-rung), [FPT Shop](https://fptshop.com.vn/tin-tuc/giai-tri/cach-choi-nakroth-lien-quan-166805).
Các nguồn không ghi số nhát chém của chiêu cuối → tự chọn 8 nhát.

**Chuyển sang game đối kháng:** Nakroth gốc chỉ có 3 chiêu + nội tại, trong khi khung chuẩn của dự án cần nhiều lệnh hơn.
Nguyên tắc v2: **mọi chiêu đều là biến thể của 3 chiêu gốc**, không bịa chiêu mới; **mọi đòn đều là chém bằng song đao** (bỏ hết đấm, đá).

---

## 1. Phím điều khiển

Dùng bảng phím chuẩn trong `CLAUDE.md` (P1: WASD + JKLUIO, P2: mũi tên + Numpad 1–6). Không thêm phím riêng.

---

## 2. Chỉ số

| Chỉ số | Giá trị | Ghi chú |
|---|---|---|
| Máu | 850 | máu mỏng (chuẩn 1000) |
| Tấn công / Phòng thủ | 110 / 90 | |
| Tốc độ đi | nhanh hơn KFM ~30% | |
| Lướt `L` / `A + L` | lướt tới nhanh và xa nhất game / lướt lùi ngắn, vài tick bất tử | |
| Năng lượng | 3000 = 3 thanh | |

**Điểm yếu:** máu mỏng, chiêu U có hồi chiêu, chiêu cuối đứng yên (bị né là hụt).

---

## 3. Đánh thường – toàn bộ là chém song đao

| Lệnh | Tên | Mô tả | Sát thương |
|---|---|---|---|
| `J` → `J` → `J` → `J` | Chuỗi song đao | Nhát 1 chém ngang đao phải, nhát 2 chém ngang đao trái, nhát 3 chém chéo hai đao, nhát 4 hai đao vẩy lên | 25 / 25 / 30 / 40 |
| `W + J` | Vẩy đao | Hai đao vẩy từ dưới lên, hất đối thủ – mở combo trên không | 45 |
| `S + J` | Quét đao thấp | Ngồi quét đao sát đất, đánh ngã (phải đỡ thấp) | 40 |
| `J` (trên không) | Bổ đao | Hai đao bổ chéo xuống | 40 |

- Nhát 1 ra đòn nhanh (3–4 tick). Đòn J trúng thì hủy được sang chiêu U và tuyệt chiêu.

---

## 4. Nội tại – Thẩm Phán Oai Nghiêm

1. **Đòn J thứ 4 hất tung** (đúng bản gốc): có bộ đếm số đòn J **trúng** (đứng, ngồi, trên không đều tính). Cứ đến đòn thứ 4 thì đòn đó hất tung, rồi đếm lại.
   - Khi đòn kế tiếp là đòn thứ 4 → hai đao lóe đỏ để người chơi biết.
   - Bộ đếm về 0 nếu **2 giây** không đánh trúng đòn J nào → đánh đủ chuỗi `J J J J` từ đầu thì nhát 4 hất tung.
   - `W + J` luôn hất tung (không cần là đòn thứ 4). Đòn chém quét cường hóa được đếm nhưng không đổi thành hất tung.
2. **Tăng tốc đánh:** khi chiêu U bất kỳ trúng đối thủ, **hoặc khi dùng `S + U`** → 150 tick (2,5 giây) các đòn J nhanh hơn ~50%. Có ánh bạc trên người khi đang tăng tốc.

---

## 5. Chiêu U (không tốn năng lượng)

### `U` – Bồi Thẩm Đoàn (chiêu 1 gốc)
- **Lần 1:** lướt tới xa (~1/3 màn hình), chém **hất tung**. Sát thương 60.
- **Lần 2:** bấm `U` trong vòng **5 giây (300 tick)** → lướt thêm một đoạn, chém **không hất tung**, sát thương 60 (bằng lần 1, như bản gốc).
  - Giữ `A` khi bấm lần 2 → **lướt lùi** để rút lui (như combo gốc dùng lần 2 để thoát).
- **Hồi chiêu:** chỉ bắt đầu sau lần 2 (hoặc khi hết 5 giây mà không dùng): **2 giây** mới dùng lại được. Đây là giới hạn để không spam lướt.
- `W + U` và `U` trên không là **lần 1 theo hướng khác** của cùng chiêu này (cùng cửa sổ lần 2, cùng hồi chiêu):
  - **`W + U` – Bồi Thẩm Đoàn (lướt chéo lên):** lướt chéo lên trời chém, đuổi đối thủ bị hất. Sát thương 55.
  - **`U` trên không – Bồi Thẩm Đoàn (lướt chéo xuống):** lướt chéo xuống đất, trúng thì đập đối thủ xuống. Sát thương 55.

### `S + U` – Nguồn Cơn Rắc Rối (chiêu 2 gốc)
- **Lộn ngược ra sau** (xa đối thủ), vài tick bất tử đầu. Bản thân cú lộn không gây sát thương.
- Kích hoạt nội tại tăng tốc đánh ngay khi dùng.
- **Đòn J kế tiếp trong 3 giây (180 tick)** thành **chém quét ngang tầm xa**, sát thương 90 – đòn thường mạnh nhất. Nhân vật nháy đỏ khi đang cường hóa.
- **Hồi chiêu 3 giây.**

---

## 6. Tuyệt chiêu (tốn năng lượng)

### `I` – Gươm Hành Quyết (chiêu cuối gốc, 1 thanh = 1000 power)
- Màn hình khựng nhẹ (super pause). Nakroth **đứng tại chỗ** chém liên tục **8 nhát** vào vùng phía trước (tầm ngắn).
- **Siêu giáp thật:** không bị đánh ngắt hay bị ném, **vẫn mất máu** (giảm ~30% sát thương nhận vào). Không còn dùng bất tử như v1.
- Không hủy được giữa chừng. **Nhát cuối hất tung thẳng lên** (để nối tiếp combo, không đánh văng ra xa).
- Sát thương: 7 nhát × 20 + nhát cuối 60 = **200**.

### `S + I` – Phán Quyết Cuối Cùng (3 thanh = 3000 power)
Tái hiện đúng **combo kinh điển** của Nakroth trong một chiêu, màn hình tối lại suốt chiêu:
1. **Bồi Thẩm Đoàn:** lướt tới chém hất tung (50). **Trượt thì hết chiêu.**
2. **Gươm Hành Quyết trên không:** bay lên chém liên tục quanh đối thủ đang lơ lửng, vệt chém đỏ từ nhiều hướng (6 nhát × 30).
3. **Nguồn Cơn Rắc Rối:** lộn ngược ra sau, đáp đất.
4. **Chém quét ngang** kết thúc thật lớn, đối thủ ngã (150).
- Tổng sát thương: 50 + 180 + 150 = **380**. Bất tử suốt chiêu (chiêu 3 thanh).

---

## 7. Combo để kiểm tra

| # | Combo | Kiểm tra điều gì |
|---|---|---|
| 1 | `J J J J` (hất) → `U` → `U` (lần 2) | Nội tại đòn 4, tái kích hoạt U |
| 2 | `S + U` → `J` (chém quét) → `U` → `I` | Combo kinh điển của bản gốc |
| 3 | `W + J` → `W + U` → `J J` (trên không) → `U` (lần 2) | Combo trên không |
| 4 | `U` → `I` → `A + U` (lần 2, lướt lùi) | Hất tung → chiêu cuối → rút lui |
| 5 | Bị đánh trong lúc `I` | Siêu giáp: không bị ngắt, vẫn mất máu |

---

## 8. Hình ảnh

- **Hiện tại (hình tạm):** sprite Kung Fu Man – chỉ có đấm, đá. Để trông giống chém hơn:
  - Chọn động tác KFM gần dáng chém nhất (đấm, chưởng), bỏ các động tác đá.
  - **Claude tự vẽ vệt chém đỏ thẫm + bạc đơn giản** gắn lên mọi đòn chém, chờ sprite thật.
- **Sau này:** người dùng lo sprite thật Nakroth cầm song đao. Số animation đã tách sẵn theo quy ước, thay sprite không phải sửa logic.

---

## 9. Ghi chú kỹ thuật (bản dựng v2)

- **Siêu giáp `I`:** `HitOverride` với `keepstate = 1` (bị trúng không đổi state) + `DefenceMulSet 0.7`.
  Wiki IKEMEN không ghi rõ `keepstate` của HitOverride có trừ máu hay không → **cần test #5**.
  Nếu bị trúng mà không mất máu, hoặc bị đánh văng khỏi chiêu, báo lại để đổi cách làm.
- **Vệt chém:** Claude tự vẽ (sprite 8000–8099, bảng màu riêng) và đóng vào `nakroth.sff`.
  Công cụ sinh lại nằm ở `tools/` (xem `tools/README.md`).
- Hồi chiêu U / S+U chưa có biểu tượng trên màn hình. Cần thì làm sau.

---

## 10. Thay đổi so với v1

| Mục | v1 | v2 (đúng bản gốc hơn) |
|---|---|---|
| Đánh thường | đấm/đá của KFM, nhát 4 hất tung | tất cả là chém song đao; **đòn J thứ 4 bất kỳ** hất tung (bộ đếm) |
| U lần 2 | trong 1 giây, 50 sát thương | trong **5 giây**, 60 (bằng lần 1), giữ A để lướt lùi; có hồi chiêu 2 giây |
| `W + U`, `U` trên không | chiêu mới tự nghĩ | biến thể hướng của Bồi Thẩm Đoàn |
| `S + U` | chỉ cường hóa J | thêm tăng tốc đánh ngay khi dùng; hồi chiêu 3 giây |
| `I` | bất tử, chém tiến tới, nhát cuối đánh văng | **siêu giáp thật**, đứng yên, 8 nhát, nhát cuối **hất tung lên** |
| `S + I` | lướt xuyên qua lại 5 lần | tái hiện combo kinh điển: Chiêu 1 → Chiêu cuối trên không → Chiêu 2 → chém quét |
| Hình | chỉ sprite KFM | thêm vệt chém đỏ/bạc tự vẽ |
