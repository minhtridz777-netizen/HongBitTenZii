# Quy tắc làm việc với Git

## Các nhánh

| Nhánh | Vai trò | Ai được đẩy trực tiếp |
|---|---|---|
| `main` | **Bản ổn định**, chơi được. Chỉ nhận code từ `develop` khi đã test xong. Mỗi lần cập nhật gắn tag `v0.x` | Không ai (qua Pull Request) |
| `develop` | **Nhánh chính khi phát triển** (nhánh mặc định trên GitHub). Mọi nhánh việc đều tách ra từ đây và gộp về đây | Được, nhưng nên qua Pull Request |
| nhánh việc | Mỗi việc một nhánh, tách từ `develop`, xong thì gộp về `develop` rồi xoá | Người làm việc đó |

## Đặt tên nhánh việc

Chữ thường, không dấu, nối bằng gạch ngang `-`.

| Tiền tố | Dùng khi | Ví dụ |
|---|---|---|
| `tuong/<ten>` | Tạo / sửa một nhân vật (cả thiết kế lẫn code) | `tuong/ichigo`, `tuong/zoro-chieu-moi` |
| `map/<ten>` | Làm map (stage) | `map/lang-la`, `map/lab-bac-them-bac` |
| `khung/<mo-ta>` | Sửa cơ chế chung: `khung.cns`, `platforms.zss`, template | `khung/the-luc-hoi-nhanh` |
| `sua/<mo-ta>` | Sửa lỗi | `sua/nga-ket-tren-bac` |
| `cong-cu/<mo-ta>` | Công cụ trong `tools/`, LAB | `cong-cu/lab-hien-hitbox` |
| `giao-dien/<mo-ta>` | Menu, thanh máu, màn chọn | `giao-dien/thanh-the-luc` |
| `tai-lieu/<mo-ta>` | Chỉ sửa tài liệu | `tai-lieu/huong-dan-cai` |

Một nhánh = một việc. Không sửa nhân vật khác trong nhánh `tuong/<ten>`.

## Quy trình một việc

```powershell
git switch develop
git pull
git switch -c tuong/ichigo
# ... làm, commit nhiều lần ...
git push -u origin tuong/ichigo
```
Rồi mở **Pull Request vào `develop`** trên GitHub (điền mẫu có sẵn). Gộp xong thì xoá nhánh.

## Commit

- Message ngắn, tiếng Việt, mở đầu bằng **phạm vi**: `<phạm vi>: <làm gì>`.
  - `ichigo: thêm chiêu U tái kích hoạt` · `khung: lướt tốn 20% thể lực` · `map lang-la: thêm 2 bậc` · `sua: Bù Nhìn kẹt khi ngã trên bậc`
- Commit sau mỗi bước chạy được (nhân vật load không lỗi). Không commit code làm game crash.
- Không commit file của engine, `save/` (trừ `save/config.ini`), ảnh chụp test.

## Trước khi mở Pull Request
1. Nhân vật / map load được, không lỗi (xem "Ghi chú" trong `CLAUDE.md`).
2. Đã thử trong `LAB.exe`.
3. Thiết kế trong `designs/` đã cập nhật nếu đổi chiêu (thiết kế là nguồn chuẩn).
4. Sửa `khung.cns` / `platforms.zss` → ảnh hưởng **mọi** nhân vật: ghi rõ trong Pull Request và thử lại ít nhất nhân vật mẫu.

## Phát hành lên `main`
Khi `develop` ổn định: mở Pull Request `develop` → `main`, gộp, gắn tag:
```powershell
git switch main
git pull
git tag v0.1
git push origin v0.1
```

## Làm cùng Claude Code
Claude đọc `CLAUDE.md` và làm theo quy tắc này: mỗi việc tạo nhánh đúng tên từ `develop`, commit theo mẫu, đẩy nhánh lên
và mở Pull Request vào `develop` khi người dùng đồng ý.
