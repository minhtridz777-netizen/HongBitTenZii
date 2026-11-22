# Template nhân vật (khung chuẩn)

Nhân vật mẫu **"Mau"** chạy được trong LAB, có đủ khung chuẩn (`designs/KHUNG_CHUAN.md`), dùng **model test**.

| File | Vai trò | Nhân vật mới |
|---|---|---|
| `khung.cns` | Cơ chế chung: đi, nhảy, nhảy đôi, lướt xuyên người (đất/trên không), giữ S đỡ, thể lực, thoát combo S+L | **Không copy** – trỏ tới bằng `st2` |
| `mau.def` | Khai báo file | copy, đổi tên |
| `mau.cmd` | Lệnh (giữ nguyên) + bảng chuyển chiêu State -1 (sửa) | copy, sửa phần CHUYỂN CHIÊU |
| `mau.cns` | Chỉ số + bộ chiêu mẫu | copy, viết lại chiêu theo thiết kế |
| `mau.sff`, `mau.air` | Model test + hiệu ứng tối giản (sinh bằng `tools/gen_model.py`) | sinh lại với màu riêng |
| `mau.snd` | Âm thanh tạm (KFM) | copy |

## Tạo nhân vật mới `<ten>`

```powershell
mkdir chars/<ten>
```

```powershell
copy shared/char_template/mau.cmd chars/<ten>/<ten>.cmd; copy shared/char_template/mau.cns chars/<ten>/<ten>.cns; copy shared/char_template/mau.def chars/<ten>/<ten>.def; copy shared/char_template/mau.snd chars/<ten>/<ten>.snd
```

```powershell
python tools/gen_model.py chars/<ten> <ten> <mau chinh R,G,B> <mau phu R,G,B>
```

Rồi sửa `chars/<ten>/<ten>.def`:
- đổi `name`, `displayname`, tên các file `mau.*` → `<ten>.*`
- **`st2 = ../../shared/char_template/khung.cns`** (đường dẫn tới cơ chế chung)

Thêm vào `data/select.def`: `<ten>, stages/lab_bac.def` → mở `LAB.exe` là test được.

## Quy tắc khi viết chiêu
- Số state/anim theo `KHUNG_CHUAN.md` mục 6. Biến `var(0)–var(9)` là của hệ thống (khung dùng var 0, 1; cmd dùng var 2), chiêu riêng dùng `var(10)` trở lên.
- **HitDef luôn `guardflag = MA`** (game không phân đỡ cao/thấp) và dùng tia nhỏ `sparkno = S8010`, `guard.sparkno = S8010`.
- Thể lực khi đỡ: engine tự trừ = sát thương × 2.5 (hằng số trong `[Constants]` của `mau.cns`).
- Nội tại / cơ chế riêng: viết trong `[Statedef -2]` của file `.cns` nhân vật (khung.cns dùng `-3`).
- Thoát combo mẫu là "biến mất ra sau lưng" (state 860/865 trong khung.cns). Tướng muốn kiểu khác:
  viết state riêng 870–899 và thêm vào `.cmd` một `ChangeState` sang đó **trước** khi khung xử lý (cùng điều kiện: `down_L`, `movetype = H`, `power >= 1000`).

## Lưu ý về hình (khi vẽ model chuẩn)
- **Animation bị đánh / ngã (5000–5300) phải có thời lượng giống KFM**: engine chờ `AnimTime = 0` ở nhiều state
  (vd 5100 chờ hết anim rồi mới nảy, 5101). Để khung `-1` (vô hạn) sai chỗ là nhân vật đứng hình, không ngã, không bị đánh được.
- Số khung không bị giới hạn. Model test được chèn khung trung gian tự động; sprite thật vẽ bao nhiêu khung cũng được,
  chỉ cần giữ đúng **số thứ tự elem** của khung có vùng đánh mà file `.cns` dùng (`AnimElem = ...`).
- Vùng đánh của đòn hất lên phải phủ cả cánh tay vung (không chỉ nắm tay), nếu không sẽ hụt đối thủ đang đứng.

## Cơ chế chung hoạt động thế nào (để sửa khi cần)
- **Đỡ bằng S:** engine chỉ đỡ khi "giữ lùi", nên khung bật cờ `AutoGuard` khi đang giữ S (state 800 / 120–155) và đối thủ ở phía trước.
  Engine hay tự chuyển sang tư thế ngồi sau khi đỡ; khung đưa về lại thế đỡ (hoặc đứng nếu đã thả S).
- **Thể lực = guard points của engine** (thanh dọc cạnh ảnh đại diện). Lướt trừ 250/1000. Đang đỡ thì khung chặn bộ đếm hồi của engine.
  Hết thể lực khi đỡ → engine cho vỡ thế.
- **Bậc:** `shared/system/platforms.zss` (chung cho mọi nhân vật, không cần code trong nhân vật). Nhân vật đang ngã được bậc "giữ" thêm 30 đơn vị để kịp chạm bậc; vì vậy bậc phải cao ít nhất 40.
- **Lướt (kiểu Bleach vs Naruto):** `PlayerPush = 0` để vụt xuyên qua người đối thủ, bất tử 4 tick đầu, vệt mờ (AfterImage).
  Tốn 20% thể lực dưới đất, 30% trên không. Đòn J đất 200–239 / J trên không 600–699 trúng thì hủy sang lướt.
- **Bộ đệm phím J = 1 tick** (trong `.cmd`): để 5 tick thì 1 lần bấm ra 2 đòn, vì engine giữ lần bấm trong lúc khựng hình.
