# Template nhân vật (khung chuẩn)

Nhân vật mẫu **"Mau"** chạy được trong LAB, có đủ khung chuẩn (`designs/KHUNG_CHUAN.md`), dùng **model test**.

| File | Vai trò | Nhân vật mới |
|---|---|---|
| `khung.cns` | Cơ chế chung: đi, nhảy, nhảy đôi, lướt (đất/trên không), giữ S đỡ, thể lực, thoát combo S+L | **Không copy** – trỏ tới bằng `st2` |
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

## Cơ chế chung hoạt động thế nào (để sửa khi cần)
- **Đỡ bằng S:** engine chỉ đỡ khi "giữ lùi", nên khung bật cờ `AutoGuard` khi đang giữ S (state 800 / 120–155) và đối thủ ở phía trước.
  Engine hay tự chuyển sang tư thế ngồi sau khi đỡ; khung đưa về lại thế đỡ (hoặc đứng nếu đã thả S).
- **Thể lực = guard points của engine** (thanh dọc cạnh ảnh đại diện). Lướt trừ 250/1000. Đang đỡ thì khung chặn bộ đếm hồi của engine.
  Hết thể lực khi đỡ → engine cho vỡ thế.
- **Bậc:** `shared/system/platforms.zss` (chung cho mọi nhân vật, không cần code trong nhân vật).
