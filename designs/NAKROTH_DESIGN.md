# NAKROTH – Bản thiết kế nhân vật (v1, đã chốt)

> Nhân vật dựa trên tướng Nakroth (Liên Quân Mobile). Dự án cá nhân, phi lợi nhuận.
> Lối chơi: **sát thủ song đao, lướt liên tục, chém nhanh, máu mỏng.**

---

> Trạng thái: **Đã duyệt**. Thư mục nhân vật: `chars/nakroth/`

## 1. Phím điều khiển

Dùng bảng phím và khung lệnh chuẩn trong `CLAUDE.md`. Nakroth dùng đủ cả khung (kể cả `S + I` cấp 3), không thêm lệnh riêng.

---

## 2. Chỉ số (điểm khởi đầu, sẽ chỉnh khi test)

| Chỉ số | Giá trị | So với mặc định Mugen |
|---|---|---|
| Máu (life) | 850 | thấp hơn (mặc định 1000) |
| Tấn công (attack) | 110 | cao hơn |
| Phòng thủ (defence) | 90 | thấp hơn |
| Tốc độ đi | nhanh hơn KFM ~30% | |
| Lướt (L) | nhanh và xa nhất game | |
| Năng lượng tối đa | 3000 = 3 thanh | mặc định |

---

## 3. Đánh thường

| Lệnh | Tên | Mô tả | Sát thương gợi ý |
|---|---|---|---|
| `J` → `J` → `J` → `J` | Chuỗi song đao | 4 nhát liên hoàn. **Nhát 4 hất tung** đối thủ lên không | 25 / 25 / 30 / 45 |
| `W + J` | Chém hất | Chém từ dưới lên, hất đối thủ – mở combo trên không | 50 |
| `S + J` | Quét chân | Ngồi chém thấp, đánh ngã (phải đỡ thấp) | 40 |
| `J` (trên không) | Chém chéo không trung | Chém chéo xuống | 40 |

- Nhát 1 ra đòn rất nhanh (khoảng 4–5 tick), có thể hủy (cancel) các nhát J sang chiêu U.

---

## 4. Chiêu đặc biệt (không tốn năng lượng)

### `U` – Bồi Thẩm Đoàn
- Lướt nhanh tới trước một đoạn, chém **hất tung** đối thủ.
- **Tái kích hoạt:** bấm `U` lần nữa trong vòng **1 giây (60 tick)** → lướt thêm một đoạn, chém nhưng **không hất tung**.
- Không bấm lần 2 trong 1 giây thì mất lượt lướt thứ hai.
- Sát thương: 60 (lần 1) / 50 (lần 2).

### `S + U` – Nguồn Cơn Rắc Rối
- **Lộn ngược ra sau** (hướng xa đối thủ), có vài tick bất tử đầu để né đòn.
- Trong **3 giây (180 tick)** sau đó, nhát `J` kế tiếp biến thành **chém quét ngang tầm xa, sát thương lớn** (khoảng 90).
- Nên có hiệu ứng báo đang cường hóa (ví dụ nhân vật nháy đỏ).

### `W + U` – Phi Đao Thăng Thiên *(chiêu mới)*
- Lướt chéo lên trời chém, dùng để đuổi đối thủ đang bị hất tung.
- Sát thương: 55.

### `U` (trên không) – Lướt chém không trung *(chiêu mới)*
- Lướt chéo xuống đất, chém trúng thì đập đối thủ xuống.
- Sát thương: 55.

---

## 5. Tuyệt chiêu (tốn năng lượng)

### `I` – Gươm Hành Quyết (1 thanh = 1000 power)
- Chém liên tục phía trước (khoảng 6–8 nhát), nhát cuối **hất văng** đối thủ.
- **Siêu giáp:** trong lúc tung chiêu không bị đánh ngắt (vẫn nhận sát thương nhưng giảm ~50%).
  - Nếu siêu giáp khó làm ở bản đầu: tạm cho **bất tử** trong lúc tung chiêu, ghi chú lại để làm sau.
- Hiệu ứng: màn hình khựng nhẹ lúc kích hoạt (super pause).
- Tổng sát thương: ~200.

### `S + I` – Phán Quyết Cuối Cùng (3 thanh = 3000 power)
- Màn hình tối lại, Nakroth lướt xuyên qua đối thủ **qua lại nhiều lần** (5–6 lần), mỗi lần một vệt chém.
- Kết thúc bằng một nhát chém lớn, đối thủ ngã.
- Chỉ ra đòn khi nhát đầu trúng (nếu trượt thì chỉ chém 1 lần rồi hết chiêu).
- Tổng sát thương: ~380.

---

## 6. Nội tại – Thẩm Phán

1. **Nhát J thứ 4** trong chuỗi luôn hất tung (đã ghi ở mục 3).
2. **Mỗi khi một chiêu `U` (bất kỳ biến thể nào) trúng đối thủ** → trong **2,5 giây (150 tick)** Nakroth đánh nhanh hơn: các nhát J ra đòn và hồi đòn nhanh hơn rõ rệt.
   - Gợi ý cách làm: dùng biến (var) đếm thời gian; khi đang cường hóa thì dùng animation J phiên bản rút ngắn số tick mỗi khung.

---

## 7. Combo để kiểm tra

| # | Combo | Kiểm tra điều gì |
|---|---|---|
| 1 | `J J J` → `U` → `U` → `J J J J` | Cancel J sang U, tái kích hoạt U, nội tại tăng tốc |
| 2 | `W + J` → `W + U` → `J J` (trên không) → `U` (trên không) | Combo trên không |
| 3 | `S + U` → `J` (cường hóa) → `U` → `I` | Né + đòn cường hóa + nối tuyệt chiêu |
| 4 | `J J J J` (hất) → `I` | Tuyệt chiêu bắt đối thủ đang bay |

---

## 8. Hình ảnh

- **Giai đoạn 2:** dùng hình tạm. Gợi ý: tạm mượn sprite/animation của **Kung Fu Man** (có sẵn trong IKEMEN) để tập trung làm phần logic. Có thể thêm hiệu ứng vệt chém đơn giản.
- **Sau này:** người dùng sẽ tự lo sprite thật (tự vẽ, thuê vẽ, hoặc đổi sang nhân vật gốc cùng phong cách). Code phải tách bạch số animation để thay sprite không phải sửa logic.
- Màu chủ đạo cho hiệu ứng: **đỏ thẫm + bạc** (vệt chém đỏ).

---

## 9. Ghi chú triển khai v1 (hình tạm KFM)

Những điểm code bản đầu làm khác/thêm so với mục trên – cần người dùng xác nhận khi test:

- **Lướt lùi:** thêm `A + L` = lướt lùi ngắn (vài tick bất tử). `L` = lướt tới. Lướt tới hủy được sang J, `W+J`, U, tuyệt chiêu, nhảy.
- **J trên không:** nối được tối đa 2 nhát liên tiếp khi trúng (để chạy combo #2).
- **Chuỗi J:** nối nhát kế khi trúng, hoặc khi đánh hụt sau khung chém.
- **`I` siêu giáp:** tạm dùng **bất tử** toàn chiêu (phương án dự phòng). Siêu giáp thật để làm sau.
- **`S + I`:** lướt xuyên qua **5 lần** (40 + 5×48 + 100 = 380). Màn hình tối suốt chiêu.
- **Cường hóa `S+U`:** 180 tick tính **từ lúc tiếp đất**; nhân vật nháy đỏ khi đang cường hóa.
- **Nội tại tăng tốc:** anim J rút còn ~60% số tick; nhân vật có ánh bạc nhẹ khi đang tăng tốc.
- Sát thương ghi trong thiết kế là sát thương gốc; chỉ số attack 110 làm thực tế cao hơn ~10%.
