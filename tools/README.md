# tools/ – công cụ Python sinh file nhân vật (hình tạm)

Cần Python 3 + Pillow (`pip install pillow`). Chạy từ thư mục gốc dự án.

| File | Công dụng |
|---|---|
| `sff2.py` | Đọc/ghi file sprite SFF v2 (thư viện). |
| `airlib.py` | Đọc/ghi file animation .air (thư viện). |
| `gen_slash_sff.py` | Vẽ vệt chém đỏ/bạc (nhóm sprite 8000–8099, bảng màu riêng 8000,1) và ghép vào SFF nguồn. |
| `gen_nakroth_air.py` | Sinh `chars/nakroth/nakroth.air` từ `kfm.air` (anim chung + anim chiêu + anim vệt chém). |

Sinh lại sprite và animation của Nakroth:

```powershell
python tools/gen_slash_sff.py chars/kfm/kfm.sff chars/nakroth/nakroth.sff tools/preview
```

```powershell
python tools/gen_nakroth_air.py chars/kfm/kfm.air chars/nakroth/nakroth.air
```

Lưu ý: `gen_nakroth_air.py` **ghi đè** `nakroth.air`. Khi đã có sprite thật và sửa `.air` bằng tay thì không chạy lại script này nữa.
Số thứ tự elem có Clsn1 in ra khi chạy được dùng trong `AnimElem = ...` của `nakroth.cns` – đổi nguồn anim thì phải kiểm tra lại.
