--;===========================================================
--; LAB - phòng luyện tập riêng của dự án MugenFake
--; Chỉ hoạt động khi chạy engine với cờ -lab (LAB.exe tự thêm cờ này).
--; Chạy Ikemen_GO.exe bình thường thì file này không làm gì.
--;
--; Tính năng:
--;  1. Mở thẳng màn chọn tướng của chế độ Training (bỏ qua màn hình tiêu đề).
--;     P2 luôn là Bù Nhìn (Config.TrainingChar = bunhin trong save/config.ini).
--;  2. Bảng thông tin trên màn hình khi đánh:
--;     tên tướng, state / anim / ctrl / năng lượng, sát thương đòn cuối,
--;     combo (số hit + tổng sát thương), combo lớn nhất, lợi thế khung hình,
--;     giá trị var(0)-var(11) của tướng (xem hồi chiêu, cửa sổ tái kích hoạt...).
--;  3. Hành vi bù nhìn: chỉnh trong menu tạm dừng (Enter) -> Training settings.
--;===========================================================

if getCommandLineValue('-lab') == nil then
	return
end

lab = {started = false}

-- Bỏ qua menu nên engine chưa ghi nhận lần bấm phím nào -> getLastInputController() = -1
-- và chế độ Training báo lỗi. Khi chưa có lần bấm, coi như người chơi 1.
local f_getLastInputController = getLastInputController
getLastInputController = function()
	local v = f_getLastInputController()
	if v == nil or v < 1 then
		return 1
	end
	return v
end

--;-----------------------------------------------------------
--; 1. Vào thẳng Training
--;-----------------------------------------------------------
hook.add('main.menu.loop', 'lab_start', function()
	if lab.started then return end
	lab.started = true
	main.f_default()
	local f = main.t_itemname.training({{itemname = 'training'}}, 1)
	textImgSetText(motif.select_info.title.TextSpriteData, 'LAB')
	-- Chỉ đánh đơn -> bỏ qua bước chọn Team Mode
	main.teamMenu[1].simul = false
	main.teamMenu[1].tag = false
	main.teamMenu[1].turns = false
	main.f_unlock(false)
	if f ~= nil then
		f() -- màn chọn tướng + các trận luyện tập; trả về khi bấm Esc ở màn chọn
	end
	os.exit()
end)

--;-----------------------------------------------------------
--; 2. Bảng thông tin
--;-----------------------------------------------------------
local LC_W, LC_H = 320, 240        -- hệ toạ độ vẽ (localcoord)
local X0, Y0, LINE = 6, 48, 8      -- góc trên trái bảng (dưới tên nhân vật), khoảng cách dòng
local NLINES = 6

local ui = nil
local function f_initUi()
	ui = {lines = {}}
	ui.font = fontNew('Open_Sans.def', 7)
	ui.bg = rectNew()
	rectSetLocalcoord(ui.bg, LC_W, LC_H)
	rectSetColor(ui.bg, 0, 0, 0)
	rectSetAlpha(ui.bg, 150, 106)
	rectSetWindow(ui.bg, X0 - 3, Y0 - LINE + 1, X0 + 172, Y0 + LINE * (NLINES - 1) + 3)
	for i = 1, NLINES do
		local ts = textImgNew()
		textImgSetFont(ts, ui.font)
		textImgSetLocalcoord(ts, LC_W, LC_H)
		textImgSetPos(ts, X0, Y0 + (i - 1) * LINE)
		textImgSetColor(ts, 255, 255, 255, 255)
		ui.lines[i] = ts
	end
	textImgSetColor(ui.lines[1], 255, 200, 90, 255)
end

-- trạng thái đo
local st = {
	frame = 0,
	p2Life = nil, p2WasHit = false,
	lastDmg = 0, comboDmg = 0, comboHits = 0, maxDmg = 0, maxHits = 0,
	advTracking = false, p1Rec = nil, p2Rec = nil, adv = nil,
}

local function f_resetStats()
	st.p2Life = nil
	st.lastDmg, st.comboDmg, st.comboHits, st.maxDmg, st.maxHits = 0, 0, 0, 0, 0
	st.advTracking, st.adv = false, nil
end

local function f_readPlayer(n)
	if not player(n) then return nil end
	local p = {
		name = name(), life = life(), lifeMax = lifeMax(), power = power(),
		state = stateNo(), anim = anim(), ctrl = ctrl(), moveType = moveType(),
		combo = comboCount(),
	}
	if n == 1 then
		p.vars = {}
		for i = 0, 11 do
			p.vars[#p.vars + 1] = tostring(var(i))
		end
	end
	return p
end

local function f_update(p1, p2)
	st.frame = st.frame + 1
	local p2Hit = p2.moveType == 'H'
	-- Combo kết thúc khi bù nhìn hết trạng thái bị đánh
	if not p2Hit then
		st.comboActive = false
	end
	-- Sát thương: theo dõi máu bù nhìn giảm (máu tăng lại do Training hồi máu thì bỏ qua)
	if st.p2Life ~= nil and p2.life < st.p2Life then
		local dmg = st.p2Life - p2.life
		st.lastDmg = dmg
		if not st.comboActive then
			st.comboActive = true
			st.comboDmg, st.comboHits = 0, 0
		end
		st.comboDmg = st.comboDmg + dmg
	end
	if st.comboActive then
		st.comboHits = math.max(st.comboHits, p1.combo, 1)
		if st.comboDmg > st.maxDmg or (st.comboDmg == st.maxDmg and st.comboHits > st.maxHits) then
			st.maxDmg, st.maxHits = st.comboDmg, st.comboHits
		end
	end
	st.p2Life = p2.life
	-- Lợi thế khung hình: ai lấy lại quyền điều khiển trước sau khi đòn chạm (trúng hoặc bị đỡ)
	if p2Hit and not st.p2WasHit then
		st.advTracking, st.p1Rec, st.p2Rec, st.p2Down = true, nil, nil, false
	end
	if st.advTracking then
		if p2.state >= 5100 and p2.state < 5200 then
			st.p2Down = true -- bù nhìn bị đánh ngã: số khung không còn ý nghĩa
		end
		if st.p1Rec == nil and p1.ctrl and p1.moveType ~= 'A' then
			st.p1Rec = st.frame
		end
		if st.p2Rec == nil and not p2Hit and p2.ctrl then
			st.p2Rec = st.frame
		end
		if st.p1Rec ~= nil and st.p2Rec ~= nil then
			st.adv = st.p2Down and 'ngã' or (st.p2Rec - st.p1Rec)
			st.advTracking = false
		end
	end
	st.p2WasHit = p2Hit
end

local function f_signed(n)
	if n == nil then return '--' end
	if type(n) == 'string' then return n end
	if n > 0 then return '+' .. n end
	return tostring(n)
end

local function f_draw(p1, p2)
	local L = ui.lines
	textImgSetText(L[1], 'LAB  |  ' .. p1.name .. '  vs  ' .. p2.name)
	textImgSetText(L[2], string.format('State %d   Anim %d   Ctrl %s   Năng lượng %d',
		p1.state, p1.anim, p1.ctrl and 'có' or 'không', p1.power))
	textImgSetText(L[3], string.format('Đòn cuối: %d    Combo: %d hit / %d sát thương',
		st.lastDmg, st.comboHits, st.comboDmg))
	textImgSetText(L[4], string.format('Combo lớn nhất: %d hit / %d    Lợi thế khung: %s',
		st.maxHits, st.maxDmg, f_signed(st.adv)))
	textImgSetText(L[5], 'var 0-5:   ' .. table.concat(p1.vars, '  ', 1, 6))
	textImgSetText(L[6], 'var 6-11:  ' .. table.concat(p1.vars, '  ', 7, 12))
	rectDraw(ui.bg)
	for _, ts in ipairs(L) do
		textImgDraw(ts)
	end
end

local lastRoundNo = -1
local function f_overlay()
	local okId, oldid = pcall(id)
	local ok, err = pcall(function()
		if ui == nil then f_initUi() end
		local okRn, rn = pcall(roundNo)
		if okRn and rn ~= lastRoundNo then
			lastRoundNo = rn
			f_resetStats()
		end
		local p1 = f_readPlayer(1)
		local p2 = f_readPlayer(2)
		if p1 == nil or p2 == nil then return end
		f_update(p1, p2)
		f_draw(p1, p2)
	end)
	if okId then pcall(playerId, oldid) end
	if not ok and not lab.errShown then
		lab.errShown = true
		print('LAB overlay error: ' .. tostring(err))
	end
end
hook.add('loop#training', 'lab_overlay', f_overlay)
-- đấu nhanh từ dòng lệnh (-lab -loadmotif -p1 .. -p2 ..): dùng để kiểm tra tự động
hook.add('loop#quickvs', 'lab_overlay', f_overlay)
