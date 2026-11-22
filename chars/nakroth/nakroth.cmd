; ============================================================================
; NAKROTH - file lệnh (.cmd) - theo thiết kế v2
; Bảng phím chuẩn dự án (xem CLAUDE.md):
;   P1: W A S D + J K L U I O   |   P2: mũi tên + Numpad 1-6
;   J = a (đánh) | K = b (nhảy) | L = c (lướt) | U = x (chiêu) | I = y (tuyệt chiêu) | O = z (để dành)
; Nhảy bằng W đã bị tắt (AssertSpecial NoJump, nakroth.cns State -2), nhảy bằng lệnh "K".
; ============================================================================

[Defaults]
command.time = 15
command.buffer.time = 1

;-| Tuyệt chiêu |-------------------------------------------------------------
[Command]
name = "down_I"          ; S + I : Phán Quyết Cuối Cùng (3 thanh)
command = /$D, y
time = 1
buffer.time = 4

[Command]
name = "I"               ; I : Gươm Hành Quyết (1 thanh)
command = y
time = 1
buffer.time = 4

;-| Chiêu U |----------------------------------------------------------------
[Command]
name = "down_U"          ; S + U : Nguồn Cơn Rắc Rối
command = /$D, x
time = 1
buffer.time = 4

[Command]
name = "up_U"            ; W + U : Bồi Thẩm Đoàn lướt chéo lên
command = /$U, x
time = 1
buffer.time = 4

[Command]
name = "back_U"          ; A + U : Bồi Thẩm Đoàn lần 2 lướt lùi (chỉ dùng khi đang mở cửa sổ lần 2)
command = /$B, x
time = 1
buffer.time = 4

[Command]
name = "U"               ; U : Bồi Thẩm Đoàn (đất: lướt tới / trên không: lướt chéo xuống)
command = x
time = 1
buffer.time = 4

;-| Đánh thường |------------------------------------------------------------
[Command]
name = "down_J"          ; S + J : Quét đao thấp
command = /$D, a
time = 1
buffer.time = 5

[Command]
name = "up_J"            ; W + J : Vẩy đao
command = /$U, a
time = 1
buffer.time = 5

[Command]
name = "J"               ; J : chuỗi song đao / bổ đao trên không
command = a
time = 1
buffer.time = 5

;-| Di chuyển |--------------------------------------------------------------
[Command]
name = "back_L"          ; A + L : lướt lùi
command = /$B, c
time = 1
buffer.time = 3

[Command]
name = "L"               ; L : lướt tới
command = c
time = 1
buffer.time = 3

[Command]
name = "K"               ; K : nhảy
command = b
time = 1
buffer.time = 3

;-| Giữ hướng (bắt buộc, engine dùng) |---------------------------------------
[Command]
name = "holdfwd"
command = /$F
time = 1

[Command]
name = "holdback"
command = /$B
time = 1

[Command]
name = "holdup"
command = /$U
time = 1

[Command]
name = "holddown"
command = /$D
time = 1

; ============================================================================
; State -1: chuyển chiêu theo lệnh (chạy mỗi tick)
; Thứ tự quan trọng: lệnh có hướng (S+, W+, A+) đứng trước lệnh trơn.
; Biến dùng ở đây (xem bảng biến đầu nakroth.cns):
;   var(0) cửa sổ U lần 2 | var(1) cường hóa J | var(3) được hủy chiêu
;   var(4) số J trên không | var(5) hồi chiêu U | var(6) hồi chiêu S+U
; ============================================================================
[Statedef -1]

;---------------------------------------------------------------------------
; var(3) = 1 khi được phép hủy (cancel) sang chiêu U / tuyệt chiêu:
;   đứng/ngồi có ctrl | đòn J đất (200-499) đã chạm | đang lướt (700)
[State -1, Cancel reset]
type = VarSet
trigger1 = 1
var(3) = 0

[State -1, Cancel check]
type = VarSet
trigger1 = statetype != A && ctrl
trigger2 = (stateno = [200,499]) && movecontact
trigger3 = stateno = 700 && time >= 2
var(3) = 1

;===========================================================================
; TUYỆT CHIÊU
;---------------------------------------------------------------------------
; S + I : Phán Quyết Cuối Cùng (state 4000, 3000 power)
[State -1, S+I Phan Quyet Cuoi Cung]
type = ChangeState
value = 4000
triggerall = command = "down_I"
triggerall = power >= 3000
triggerall = statetype != A
trigger1 = var(3)
trigger2 = (stateno = [1000,1199]) && movecontact

;---------------------------------------------------------------------------
; I : Gươm Hành Quyết (state 3000, 1000 power)
[State -1, I Guom Hanh Quyet]
type = ChangeState
value = 3000
triggerall = command = "I"
triggerall = power >= 1000
triggerall = statetype != A
trigger1 = var(3)
trigger2 = (stateno = [1000,1199]) && movecontact

;===========================================================================
; CHIÊU 2 GỐC - S + U : Nguồn Cơn Rắc Rối (state 1100), hồi chiêu var(6)
[State -1, S+U Nguon Con Rac Roi]
type = ChangeState
value = 1100
triggerall = command = "down_U"
triggerall = statetype != A
triggerall = var(6) <= 0
trigger1 = var(3)
trigger2 = (stateno = [1000,1015]) && movecontact

;===========================================================================
; CHIÊU 1 GỐC - BỒI THẨM ĐOÀN
; Lần 1: U (đất 1000) | W+U (chéo lên 1200) | U trên không (chéo xuống 1300)
; Lần 2 (trong cửa sổ var(0) > 0): U/W+U = lướt tới chém, A+U = lướt lùi
;   đất: 1010 / 1015      trên không: 1020 / 1025
;---------------------------------------------------------------------------
; Lần 2 trên không, giữ A: lùi
[State -1, U lan 2 khong lui]
type = ChangeState
value = 1025
triggerall = command = "back_U"
triggerall = var(0) > 0
triggerall = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600 && movecontact
trigger3 = (stateno = 1200 || stateno = 1300) && animelemtime(4) >= 0

; Lần 2 trên không: lao ngang chém
[State -1, U lan 2 khong]
type = ChangeState
value = 1020
triggerall = command = "U" || command = "up_U"
triggerall = var(0) > 0
triggerall = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600 && movecontact
trigger3 = (stateno = 1200 || stateno = 1300) && animelemtime(4) >= 0

; Lần 2 dưới đất, giữ A: lướt lùi thoát thân
[State -1, U lan 2 lui]
type = ChangeState
value = 1015
triggerall = command = "back_U"
triggerall = var(0) > 0
triggerall = statetype != A
trigger1 = var(3)
trigger2 = stateno = 1000 && animelemtime(7) >= 0

; Lần 2 dưới đất: lướt tới chém (không hất)
[State -1, U lan 2]
type = ChangeState
value = 1010
triggerall = command = "U" || command = "up_U"
triggerall = var(0) > 0
triggerall = statetype != A
trigger1 = var(3)
trigger2 = stateno = 1000 && animelemtime(7) >= 0

;---------------------------------------------------------------------------
; Lần 1 trên không: lướt chéo xuống
[State -1, U tren khong]
type = ChangeState
value = 1300
triggerall = command = "U"
triggerall = statetype = A
triggerall = var(0) <= 0 && var(5) <= 0
triggerall = pos y < -15
trigger1 = ctrl
trigger2 = stateno = 600 && movecontact

; Lần 1 W + U: lướt chéo lên
[State -1, W+U]
type = ChangeState
value = 1200
triggerall = command = "up_U"
triggerall = statetype != A
triggerall = var(0) <= 0 && var(5) <= 0
trigger1 = var(3)

; Lần 1 U: lướt tới chém hất tung
[State -1, U Boi Tham Doan]
type = ChangeState
value = 1000
triggerall = command = "U"
triggerall = statetype != A
triggerall = var(0) <= 0 && var(5) <= 0
trigger1 = var(3)

;===========================================================================
; DI CHUYỂN
[State -1, Luot lui]
type = ChangeState
value = 705
triggerall = command = "back_L"
trigger1 = statetype = S && ctrl

[State -1, Luot toi]
type = ChangeState
value = 700
triggerall = command = "L"
trigger1 = statetype = S && ctrl

; K : nhảy (state 40 của engine). Nhảy được ngay khi đang lướt.
[State -1, Nhay]
type = ChangeState
value = 40
triggerall = command = "K"
trigger1 = statetype = S && ctrl
trigger2 = stateno = 700 && time >= 2

;===========================================================================
; ĐÁNH THƯỜNG
;---------------------------------------------------------------------------
; J trên không (600): nối tối đa 2 nhát khi trúng (var(4))
[State -1, J tren khong]
type = ChangeState
value = 600
triggerall = command = "J"
triggerall = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600 && movecontact && var(4) < 2
trigger3 = (stateno = 1200 || stateno = 1020) && movecontact

; W + J : Vẩy đao (240)
[State -1, W+J Vay dao]
type = ChangeState
value = 240
triggerall = command = "up_J"
triggerall = statetype = S
trigger1 = ctrl
trigger2 = (stateno = [200,230]) && movecontact
trigger3 = stateno = 700 && time >= 2

; S + J : Quét đao thấp (400)
[State -1, S+J Quet dao]
type = ChangeState
value = 400
triggerall = command = "down_J"
triggerall = statetype != A
trigger1 = ctrl
trigger2 = (stateno = [200,230]) && movecontact

; J cường hóa sau S+U (250): đòn J kế tiếp trong 3 giây
[State -1, J cuong hoa]
type = ChangeState
value = 250
triggerall = command = "J"
triggerall = statetype = S
triggerall = var(1) > 0
trigger1 = ctrl
trigger2 = stateno = 700 && time >= 2
trigger3 = (stateno = [200,240]) && movecontact

; Chuỗi J: nối nhát kế khi trúng, hoặc sau khung chém khi đánh hụt
[State -1, J4]
type = ChangeState
value = 230
triggerall = command = "J"
trigger1 = stateno = 220 && (movecontact || animelemtime(7) >= 0)

[State -1, J3]
type = ChangeState
value = 220
triggerall = command = "J"
trigger1 = stateno = 210 && (movecontact || animelemtime(6) >= 0)

[State -1, J2]
type = ChangeState
value = 210
triggerall = command = "J"
trigger1 = stateno = 200 && (movecontact || animelemtime(4) >= 0)

; J : nhát 1 (200)
[State -1, J1]
type = ChangeState
value = 200
triggerall = command = "J"
triggerall = statetype = S
trigger1 = ctrl
trigger2 = stateno = 700 && time >= 2
