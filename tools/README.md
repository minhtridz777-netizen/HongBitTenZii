# tools/ – công cụ Python sinh file nhân vật (hình tạm)

Cần Python 3 + Pillow (`pip install pillow`). Chạy từ thư mục gốc dự án.

| File | Công dụng |
|---|---|
| `sff2.py` | Đọc/ghi file sprite SFF v2 (thư viện). |
| `airlib.py` | Đọc/ghi file animation .air (thư viện). |
| `puppet.py` | Model test: búp bê khớp nối vẽ bằng code (thư viện tư thế, IK chân, hộp va chạm tự động). |
| `gen_model.py` | Sinh sprite + animation model test cho 1 nhân vật (đủ anim chuẩn, bộ chiêu mẫu, hiệu ứng, ảnh đại diện). |
| `gen_stage_lab.py` | Sinh map thử `stages/lab_bac` (640×360, 6 bậc). |
| `gen_slash_sff.py` | (cũ) Vẽ vệt chém đỏ/bạc và ghép vào một SFF có sẵn. |
| `shot.py` | Chạy engine với tham số, chụp cửa sổ game ở các giây chỉ định (kể cả khi bị che). Biến môi trường `SHOT_KEYS="7:J,9:J"` gửi phím vào cửa sổ game. |
| `lab/LAB.cs`, `lab/build.ps1` | Mã nguồn + script biên dịch `LAB.exe` (dùng trình biên dịch C# có sẵn trong Windows). |

Biên dịch lại LAB.exe:

```powershell
powershell -ExecutionPolicy Bypass -File tools/lab/build.ps1
```

Sinh lại model test:

```powershell
python tools/gen_model.py shared/char_template mau 150,155,170 220,70,60
```

```powershell
python tools/gen_model.py chars/bunhin bunhin 205,165,80 120,78,30 --no-moves
```

Lưu ý: `gen_model.py` **ghi đè** `.sff` và `.air`. Số elem có Clsn1 in ra khi chạy được dùng trong `AnimElem = ...` của file `.cns` – đổi tư thế/số khung thì kiểm tra lại.
