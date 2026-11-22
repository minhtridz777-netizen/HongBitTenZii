; ============================================================================
; MẪU - file lệnh. Phần "LỆNH" giữ nguyên cho mọi nhân vật (khung.cns cần các tên này).
; Phần "CHUYỂN CHIÊU" (State -1) là bộ chiêu riêng - sửa theo thiết kế từng tướng.
; Phím P1: W A S D + J(a) K(b) L(c) U(x) I(y) O(z) | P2: mũi tên + Numpad 1-6
; ============================================================================

[Defaults]
command.time = 15
command.buffer.time = 1

;-| Tuyệt chiêu |-------------------------------------------------------------
[Command]
name = "down_I"
command = /$D, y
time = 1
buffer.time = 4

[Command]
name = "up_I"
command = /$U, y
time = 1
buffer.time = 4

[Command]
name = "I"
command = y
time = 1
buffer.time = 4

;-| Chiêu U |----------------------------------------------------------------
[Command]
name = "down_U"
command = /$D, x
time = 1
buffer.time = 4

[Command]
name = "up_U"
command = /$U, x
time = 1
buffer.time = 4

[Command]
name = "U"
command = x
time = 1
buffer.time = 4

;-| Đánh thường |------------------------------------------------------------
[Command]
name = "down_J"
command = /$D, a
time = 1
buffer.time = 5

[Command]
name = "up_J"
command = /$U, a
time = 1
buffer.time = 5

[Command]
name = "J"
command = a
time = 1
buffer.time = 5

;-| Di chuyển (khung.cns dùng) |----------------------------------------------
[Command]
name = "down_L"          ; S + L : thoát combo
command = /$D, c
time = 1
buffer.time = 4

[Command]
name = "back_L"          ; A + L : lướt lùi
command = /$B, c
time = 1
buffer.time = 3

[Command]
name = "L"
command = c
time = 1
buffer.time = 3

[Command]
name = "K"
command = b
time = 1
buffer.time = 3

[Command]
name = "press_back"      ; bấm hướng sau lưng (quay hướng đỡ)
command = B
time = 1

[Command]
name = "walkfwd"
command = /$F
time = 1

[Command]
name = "walkback"
command = /$B
time = 1

;-| Giữ hướng (engine dùng) |--------------------------------------------------
[Command]
name = "holdfwd"
command = /$F
time = 1

; QUAN TRỌNG: engine đỡ đòn khi "holdback" -> gán = giữ S để đỡ bằng S
[Command]
name = "holdback"
command = /$D
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
; CHUYỂN CHIÊU (State -1) - BỘ CHIÊU MẪU, sửa theo thiết kế từng tướng
; var(2) = được hủy sang chiêu U / tuyệt chiêu (tính mỗi tick)
; ============================================================================
[Statedef -1]

[State -1, Cancel reset]
type = VarSet
trigger1 = 1
var(2) = 0

[State -1, Cancel check]
type = VarSet
trigger1 = statetype != A && ctrl
trigger2 = (stateno = [200,499]) && movecontact
trigger3 = stateno = 700 && time >= 2
var(2) = 1

;--- Tuyệt chiêu ---
[State -1, S+I]
type = ChangeState
value = 4000
triggerall = command = "down_I" && power >= 3000 && statetype != A
trigger1 = var(2)
trigger2 = (stateno = [1000,1299]) && movecontact

[State -1, W+I]
type = ChangeState
value = 3500
triggerall = command = "up_I" && power >= 1000 && statetype != A
trigger1 = var(2)
trigger2 = (stateno = [1000,1299]) && movecontact

[State -1, I]
type = ChangeState
value = 3000
triggerall = command = "I" && power >= 1000 && statetype != A
trigger1 = var(2)
trigger2 = (stateno = [1000,1299]) && movecontact

;--- Chiêu U ---
[State -1, U tren khong]
type = ChangeState
value = 1300
triggerall = command = "U" && statetype = A && pos y < -15
trigger1 = ctrl
trigger2 = (stateno = [600,699]) && movecontact

[State -1, S+U]
type = ChangeState
value = 1100
triggerall = command = "down_U" && statetype != A
trigger1 = var(2)

[State -1, W+U]
type = ChangeState
value = 1200
triggerall = command = "up_U" && statetype != A
trigger1 = var(2)

[State -1, U]
type = ChangeState
value = 1000
triggerall = command = "U" && statetype != A
trigger1 = var(2)

;--- Đánh thường ---
[State -1, J tren khong 2]
type = ChangeState
value = 610
triggerall = command = "J" && statetype = A
trigger1 = stateno = 600 && movecontact

[State -1, J tren khong]
type = ChangeState
value = 600
triggerall = command = "J" && statetype = A
trigger1 = ctrl
trigger2 = stateno = 1200 && movecontact

[State -1, W+J]
type = ChangeState
value = 240
triggerall = command = "up_J" && statetype = S
trigger1 = ctrl
trigger2 = (stateno = [200,220]) && movecontact

[State -1, S+J]
type = ChangeState
value = 400
triggerall = command = "down_J" && statetype = S
trigger1 = ctrl
trigger2 = (stateno = [200,220]) && movecontact

[State -1, J3]
type = ChangeState
value = 220
triggerall = command = "J"
trigger1 = stateno = 210 && (movecontact || animelemtime(3) >= 0)

[State -1, J2]
type = ChangeState
value = 210
triggerall = command = "J"
trigger1 = stateno = 200 && (movecontact || animelemtime(3) >= 0)

[State -1, J1]
type = ChangeState
value = 200
triggerall = command = "J" && statetype = S
trigger1 = ctrl
trigger2 = stateno = 700 && time >= 2
