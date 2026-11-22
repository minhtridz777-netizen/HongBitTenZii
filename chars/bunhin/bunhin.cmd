; Bù Nhìn - chỉ có các lệnh giữ hướng bắt buộc (để chế độ Training điều khiển ngồi/nhảy/đỡ).

[Defaults]
command.time = 15
command.buffer.time = 1

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

[Statedef -1]

[State -1, Khong co chieu]
type = Null
trigger1 = 0
