# KHUNG CHUẨN – luật chung cho mọi nhân vật (bản nháp, CHỜ DUYỆT)

> Mọi nhân vật dùng chung khung này. Bản thiết kế từng nhân vật chỉ ghi phần **riêng** (chiêu, nội tại, chiêu ẩn).
> Duyệt xong sẽ chép phần cốt lõi vào `CLAUDE.md` và làm `shared/char_template/` theo đúng khung.

---

## 1. Hình ảnh và tỉ lệ

| Mục | Chuẩn |
|---|---|
| Độ phân giải game | 1280×720 (16:9) |
| Hệ toạ độ (localcoord) | **640×360** cho cả nhân vật và map → đơn vị toạ độ trùng nhau |
| Chiều cao nhân vật | ~70 px (≈ 1/5 màn hình). Nhân vật to con tối đa ~90 px |
| Phong cách | Ít chi tiết, khối màu rõ, viền đậm. **Hiệu ứng chiêu là phần đẹp nhất** |
| Map | Rộng 2–3 màn hình, có bậc lơ lửng (nhảy lên, S+K xuống), nền nhiều lớp trôi chậm |
| Camera | Luôn ở giữa 2 nhân vật; đi xa nhau thì thu nhỏ (tối đa 0.8); nhảy lên cao thì camera theo |

*Đã làm thử (map `lab_bac`): bậc, S+K xuống bậc, camera giữa + thu nhỏ đều chạy được.*

---

## 2. Phím (giữ nguyên quy định 2 bộ phím)

| P1 | P2 | Bấm riêng | Ghi chú |
|---|---|---|---|
| W | ↑ | **Không làm gì** | Chỉ dùng trong tổ hợp (W+J, W+U…) |
| S | ↓ | **Giữ = đỡ đòn** | Đứng yên khi đỡ; A/D đổi hướng đỡ. Nhân vật đặc biệt: giữ S = tích nội tại thay đỡ |
| A / D | ← / → | Đi trái / phải | Khi đang đỡ: quay hướng đỡ |
| J | Num1 | Đánh thường | |
| K | Num2 | Nhảy (nhảy đôi khi đang bay) | S + K trên bậc = xuống bậc |
| L | Num3 | Lướt (đất và trên không) | Tốn thể lực |
| U | Num4 | Chiêu | |
| I | Num5 | Tuyệt chiêu | |
| O | Num6 | Trợ thủ (để dành) | |

Bỏ khỏi khung chuẩn: **cúi người**, **đỡ bằng cách giữ lùi** kiểu Mugen.

---

## 3. Cơ chế chung (mọi nhân vật đều có, nằm trong template)

### 3.1 Đỡ đòn
- Giữ S: nhân vật đứng yên, đỡ **mọi đòn từ phía trước mặt** (không phân đỡ cao/thấp).
- A / D khi đang giữ S: quay mặt đổi hướng đỡ.
- Bị đánh **từ sau lưng** khi đang đỡ → trúng đòn bình thường.
- Đỡ trên không: *chưa chốt* (đề xuất: không đỡ được trên không).

### 3.2 Thể lực (thanh chung cho đỡ và lướt)
| Việc | Thể lực |
|---|---|
| Tối đa | 100 |
| Lướt (đất / trên không) | −25 mỗi lần; không đủ thì không lướt được |
| Đỡ trúng 1 đòn | −(sát thương đòn đó ÷ 4), tối thiểu −5 |
| Hồi | +25 / giây khi **không đỡ và không lướt**; đang giữ S thì **không hồi** |
| Hết thể lực khi đang đỡ | **Vỡ thế**: choáng ~1 giây, đối thủ đánh tự do |

### 3.3 Thoát combo – S + L
- Đang bị đánh (trúng đòn), bấm S + L → thoát ra (biến mất / lộn / dịch chuyển…) – **hình thức tùy tướng**.
- Giá mặc định: **1 thanh năng lượng (1000)**. Tướng có thể đổi giá trong thiết kế riêng.
- Có vài tick bất tử sau khi thoát. Không dùng được khi đang nằm đất.

### 3.4 Di chuyển
- Nhảy đôi (K lần 2 khi đang bay), lướt trên không (L khi đang bay, 1 lần mỗi lần nhảy).
- Lên bậc: nhảy lên rồi rơi xuống mặt bậc. Xuống bậc: S + K. Đi ra mép bậc thì rơi.

### 3.5 Năng lượng
- Tối đa 3000 (3 thanh). Có từ đánh trúng, bị đánh, đỡ đòn.

---

## 4. Bộ chiêu bắt buộc (nhân vật nào cũng phải có)

| Nhóm | Lệnh | Yêu cầu |
|---|---|---|
| Đánh thường | `J` chuỗi 3–5 nhát | nhát cuối đẩy lùi hoặc hất |
| | `W + J` | đòn hất lên (mở combo trên không) |
| | `S + J` | đòn riêng (quét chân, đâm, phá đỡ… tùy tướng) |
| | `J` trên không | 1–2 nhát |
| Chiêu U (miễn phí, có thể hồi chiêu) | `U`, `W + U`, `S + U`, `U` trên không | 4 chiêu; có thể thêm `A/D + U` |
| Tuyệt chiêu | `I` (1 thanh), `S + I` (3 thanh) | `W + I` để dành cho tướng đặc biệt |
| Thoát combo | `S + L` | hình thức tùy tướng |
| Nội tại | không cần phím | mỗi tướng 1 nội tại |

### Chiêu ẩn / combo ẩn (khuyến khích, 1–3 cái mỗi tướng)
- Tổ hợp đặc biệt không ghi trong danh sách chiêu, ví dụ: `J J W+J U` đúng nhịp ra đòn khác,
  bấm U lần nữa sau chiêu U trúng, chiêu khi máu dưới 30%, biến hình…
- Ghi trong thiết kế ở mục riêng **"Chiêu ẩn"**.

---

## 5. Quy trình tạo một nhân vật

| Bước | Ai làm | Kết quả |
|---|---|---|
| 1. Lên ý tưởng | Người dùng | vài dòng mô tả |
| 2. Tra cứu | Claude | tư liệu nhân vật gốc (nếu có) |
| 3. Gợi ý bộ chiêu | Claude | bản thiết kế theo khung: chiêu bắt buộc + chiêu ẩn + nội tại |
| 4. **Duyệt thiết kế** | Người dùng | |
| 5. Dựng bằng **model test** + hiệu ứng tối giản | Claude | chơi được trong LAB. Nhân vật dị dạng (to, cầm vũ khí dài, bay…) thì làm thêm model test riêng |
| 6. **Duyệt lối chơi** (test trong LAB) | Người dùng | nhận xét → chỉnh |
| 7. Vẽ model chuẩn | Claude (thử, chấp nhận ~60% chất lượng mẫu) | sprite nhân vật |
| 8. **Duyệt hình** | Người dùng | |
| 9. Vẽ hiệu ứng chiêu thức | Claude | |
| 10. Âm thanh, AI máy đánh, cân bằng, ảnh đại diện, danh sách chiêu | Claude | |
| 11. **Duyệt cuối** → cập nhật Roster, commit | Người dùng / Claude | |

Model test: búp bê khớp nối ít chi tiết, cao ~70 px, đủ mọi động tác chuẩn, **đổi màu theo từng nhân vật**.
Số animation theo quy ước → khi thay model chuẩn không phải sửa logic.

---

## 6. Giữ nguyên từ trước
- Quy ước đánh số state/anim, quy ước biến (`var(0)–var(9)` hệ thống, `var(10)+` riêng), thang cân bằng.
- K = nhảy (tắt nhảy bằng W), LAB, Bù Nhìn (sẽ đổi sang model test).

## 7. Bỏ
- Nakroth (bỏ hẳn, vẫn còn trong lịch sử git nếu cần xem lại), hình KFM.

---

## Còn cần chốt
1. Đỡ được trên không không? (đề xuất: không)
2. Các con số thể lực ở mục 3.2 – để mặc định rồi chỉnh khi test?
3. Giá thoát combo mặc định 1 thanh năng lượng – được không?
