; ============================================================================
; NAKROTH - file lệnh (.cmd)
; Bảng phím chuẩn dự án (xem CLAUDE.md):
;   W A S D = hướng  |  J = a (đánh)  |  K = b (nhảy)  |  L = c (lướt)
;   U = x (chiêu)    |  I = y (tuyệt chiêu)  |  O = z (trợ thủ, để dành)
; Nhảy bằng W đã bị tắt (AssertSpecial NoJump trong nakroth.cns, State -2),
; nhảy do lệnh "K" bên dưới đảm nhiệm.
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
name = "up_U"            ; W + U : Phi Đao Thăng Thiên
command = /$U, x
time = 1
buffer.time = 4

[Command]
name = "U"               ; U : Bồi Thẩm Đoàn (đất) / Lướt chém không trung (trên không)
command = x
time = 1
buffer.time = 4

;-| Đánh thường |------------------------------------------------------------
[Command]
name = "down_J"          ; S + J : Quét chân
command = /$D, a
time = 1
buffer.time = 5

[Command]
name = "up_J"            ; W + J : Chém hất
command = /$U, a
time = 1
buffer.time = 5

[Command]
name = "J"               ; J : chuỗi song đao / chém trên không
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
; Thứ tự quan trọng: lệnh có hướng (S+, W+) phải đứng trước lệnh trơn.
; ============================================================================
[Statedef -1]

;---------------------------------------------------------------------------
; var(3) = 1 khi được phép hủy (cancel) sang chiêu U / tuyệt chiêu:
;   - đang đứng/ngồi và có ctrl
;   - đòn J đất (200-499) đã chạm đối thủ
;   - đang lướt (700)
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
trigger2 = (stateno = [1000,1299]) && movecontact

;---------------------------------------------------------------------------
; I : Gươm Hành Quyết (state 3000, 1000 power)
[State -1, I Guom Hanh Quyet]
type = ChangeState
value = 3000
triggerall = command = "I"
triggerall = power >= 1000
triggerall = statetype != A
trigger1 = var(3)
trigger2 = (stateno = [1000,1299]) && movecontact

;===========================================================================
; CHIÊU U
;---------------------------------------------------------------------------
; U trên không : Lướt chém không trung (state 1300)
[State -1, U tren khong]
type = ChangeState
value = 1300
triggerall = command = "U"
triggerall = statetype = A
triggerall = pos y < -15
trigger1 = ctrl
trigger2 = (stateno = 600 || stateno = 1200) && movecontact

;---------------------------------------------------------------------------
; S + U : Nguồn Cơn Rắc Rối (state 1100)
[State -1, S+U Nguon Con Rac Roi]
type = ChangeState
value = 1100
triggerall = command = "down_U"
triggerall = statetype != A
trigger1 = var(3)

;---------------------------------------------------------------------------
; W + U : Phi Đao Thăng Thiên (state 1200)
[State -1, W+U Phi Dao Thang Thien]
type = ChangeState
value = 1200
triggerall = command = "up_U"
triggerall = statetype != A
trigger1 = var(3)

;---------------------------------------------------------------------------
; U lần 2 : tái kích hoạt Bồi Thẩm Đoàn (state 1010)
; var(0) = số tick còn lại được bấm lần 2 (đặt trong state 1000)
[State -1, U lan 2]
type = ChangeState
value = 1010
triggerall = command = "U"
triggerall = statetype != A
triggerall = var(0) > 0
trigger1 = var(3)
trigger2 = stateno = 1000 && movecontact && animelemtime(7) >= 0

;---------------------------------------------------------------------------
; U : Bồi Thẩm Đoàn (state 1000)
[State -1, U Boi Tham Doan]
type = ChangeState
value = 1000
triggerall = command = "U"
triggerall = statetype != A
triggerall = var(0) <= 0
trigger1 = var(3)

;===========================================================================
; DI CHUYỂN
;---------------------------------------------------------------------------
; A + L : lướt lùi (state 705)
[State -1, Luot lui]
type = ChangeState
value = 705
triggerall = command = "back_L"
trigger1 = statetype = S && ctrl

;---------------------------------------------------------------------------
; L : lướt tới (state 700)
[State -1, Luot toi]
type = ChangeState
value = 700
triggerall = command = "L"
trigger1 = statetype = S && ctrl

;---------------------------------------------------------------------------
; K : nhảy (state 40 của engine). Có thể nhảy ngay khi đang lướt.
[State -1, Nhay]
type = ChangeState
value = 40
triggerall = command = "K"
trigger1 = statetype = S && ctrl
trigger2 = stateno = 700 && time >= 2

;===========================================================================
; ĐÁNH THƯỜNG
;---------------------------------------------------------------------------
; J trên không (state 600). Nối được 2 nhát liên tiếp khi trúng.
[State -1, J tren khong]
type = ChangeState
value = 600
triggerall = command = "J"
triggerall = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600 && movecontact && var(4) < 2
trigger3 = stateno = 1200 && movecontact

;---------------------------------------------------------------------------
; W + J : Chém hất (state 240)
[State -1, W+J Chem hat]
type = ChangeState
value = 240
triggerall = command = "up_J"
triggerall = statetype = S
trigger1 = ctrl
trigger2 = (stateno = [200,230]) && movecontact
trigger3 = stateno = 700 && time >= 2

;---------------------------------------------------------------------------
; S + J : Quét chân (state 400)
[State -1, S+J Quet chan]
type = ChangeState
value = 400
triggerall = command = "down_J"
triggerall = statetype != A
trigger1 = ctrl
trigger2 = (stateno = [200,230]) && movecontact

;---------------------------------------------------------------------------
; J cường hóa sau S+U (state 250) - var(1) > 0
[State -1, J cuong hoa]
type = ChangeState
value = 250
triggerall = command = "J"
triggerall = statetype = S
triggerall = var(1) > 0
trigger1 = ctrl
trigger2 = stateno = 700 && time >= 2

;---------------------------------------------------------------------------
; Chuỗi J: nhát 2, 3, 4 (nối khi trúng, hoặc sau khung chém khi đánh hụt)
[State -1, J4]
type = ChangeState
value = 230
triggerall = command = "J"
trigger1 = stateno = 220 && (movecontact || animelemtime(4) >= 0)

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

;---------------------------------------------------------------------------
; J : nhát 1 (state 200)
[State -1, J1]
type = ChangeState
value = 200
triggerall = command = "J"
triggerall = statetype = S
trigger1 = ctrl
trigger2 = stateno = 700 && time >= 2
