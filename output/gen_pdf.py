# -*- coding: utf-8 -*-
from fpdf import FPDF

FONT = "C:/Windows/Fonts/simhei.ttf"

BLUE = (27, 111, 208)
DARK = (45, 45, 48)
GRAY = (120, 120, 125)
GREEN = (43, 182, 115)
RED = (192, 57, 43)
LGRAY = (235, 236, 240)

pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.add_font("hei", "", FONT)
pdf.add_font("hei", "B", FONT)
pdf.set_auto_page_break(True, margin=20)
pdf.set_margins(15, 15, 15)


def title_section(txt):
    pdf.set_font("hei", "B", 15)
    pdf.set_text_color(*BLUE)
    pdf.ln(3)
    y = pdf.get_y()
    pdf.set_xy(15, y)
    pdf.cell(180, 9, txt)
    py = y + 9
    pdf.set_draw_color(*BLUE)
    pdf.set_line_width(0.9)
    pdf.line(15, py - 1, 195, py - 1)
    pdf.set_xy(15, py + 3)


def body(txt, size=11, color=DARK):
    pdf.set_font("hei", "", size)
    pdf.set_text_color(*color)
    pdf.set_x(15)
    pdf.multi_cell(180, 6.3, txt)


def bullet(txt):
    pdf.set_font("hei", "", 11)
    pdf.set_text_color(*DARK)
    pdf.set_x(18)
    pdf.multi_cell(177, 6.3, "·  " + txt)


def need_space(h):
    if pdf.get_y() + h > 276:
        pdf.add_page()


def spacer(h=3):
    pdf.ln(h)


# ---------- 封面 ----------
pdf.add_page()
pdf.ln(30)
pdf.set_text_color(*BLUE)
pdf.set_font("hei", "B", 30)
pdf.cell(0, 16, "正压防爆控制系统", ln=1, align="C")
pdf.cell(0, 16, "用 户 使 用 说 明 书", ln=1, align="C")
pdf.ln(10)
pdf.set_draw_color(*BLUE)
pdf.set_line_width(1.2)
pdf.line(55, pdf.get_y(), 155, pdf.get_y())
pdf.ln(10)
pdf.set_text_color(*DARK)
pdf.set_font("hei", "", 15)
pdf.cell(0, 10, "谷子防爆电气有限公司", ln=1, align="C")
pdf.set_font("hei", "", 12)
pdf.set_text_color(*GRAY)
pdf.cell(0, 8, "版本：V1.0.1", ln=1, align="C")
pdf.cell(0, 8, "服务电话：13023456789", ln=1, align="C")

# ---------- 一、产品概述 ----------
pdf.add_page()
title_section("一、产品概述")
body("本系统是一套正压防爆电气控制装置，用于对防爆柜体进行正压维持、换气吹扫、欠压断电保护，并对柜内压力、温度以及柜体流失流量进行实时监测与显示。采用 3.5 寸彩色显示屏，通过 3 个实体按键完成全部操作。")
spacer()
body("主要功能：", 11)
for t in [
    "柜内压力、温度实时监测与显示；",
    "进气 / 排气继电器自动稳压控制（维持柜内正压）；",
    "换气吹扫倒计时；",
    "欠压延时自动切断送电（防爆安全保护）；",
    "超压、欠压、超温、传感器故障声光报警；",
    "压力衰减法测量柜体流失流量（每 30s 自动滚动测量）；",
    "参数、密码、校准数据掉电保存。",
]:
    bullet(t)

# ---------- 二、技术参数 ----------
title_section("二、主要技术参数")
pdf.ln(1)
rows = [
    ("主控芯片", "GD32F103RCT6（ARM Cortex-M3）"),
    ("显示屏", "3.5 寸 TFT 彩色屏，480×320 横屏"),
    ("压力传感器", "压力变送器（柜内正压）"),
    ("温度传感器", "PT100 铂电阻"),
    ("继电器输出", "进气、排气、警报、送电 共 4 路"),
    ("按键", "3 个（短按 / 长按 3 秒）"),
    ("报警方式", "蜂鸣器 + 屏幕声光提示"),
]
col_w = [45, 135]
pdf.set_draw_color(180, 182, 186)
pdf.set_line_width(0.3)
for k, v in rows:
    pdf.set_font("hei", "B", 11)
    pdf.set_fill_color(*LGRAY)
    pdf.cell(col_w[0], 9, k, border=1, fill=True)
    pdf.set_font("hei", "", 11)
    pdf.cell(col_w[1], 9, v, border=1, ln=1)
spacer(3)
body("出厂默认参数：")
pdf.ln(1)
params = [
    ("压力下限", "150 Pa"),
    ("压力下下限", "80 Pa"),
    ("压力上限", "300 Pa"),
    ("压力上上限", "400 Pa"),
    ("温度上限", "80 ℃"),
    ("换气时间", "900 s"),
    ("流量满量程", "3200 m³/h"),
    ("系统密码", "555（万能密码 995）"),
]
for k, v in params:
    pdf.set_font("hei", "B", 11)
    pdf.set_fill_color(*LGRAY)
    pdf.cell(55, 8.5, k, border=1, fill=True)
    pdf.set_font("hei", "", 11)
    pdf.cell(55, 8.5, v, border=1, ln=1)


# ---------- 三、接线 ----------
pdf.add_page()
title_section("三、系统组成与接线")
body("系统由主控单元、传感器、继电器输出和显示按键四部分组成。传感器信号接入主控 ADC，主控根据压力、温度控制各继电器动作。")

# 接线框图
def draw_wiring():
    x0, y0 = 15, pdf.get_y() + 3
    pdf.set_line_width(0.4)
    # 左：传感器
    pdf.set_draw_color(*BLUE)
    pdf.set_fill_color(240, 244, 252)
    pdf.rect(x0, y0, 52, 62, "DF")
    pdf.set_font("hei", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.set_xy(x0 + 4, y0 + 4)
    pdf.cell(44, 6, "输入 · 传感器")
    pdf.set_font("hei", "", 9)
    pdf.set_text_color(*DARK)
    items = [("温度传感器 PT100", "PC5 / ADC15"), ("压力变送器（柜压）", "PC4 / ADC14"), ("风压变送器（备）", "PC2 / ADC12")]
    yy = y0 + 14
    for a, b in items:
        pdf.set_fill_color(255, 255, 255)
        pdf.rect(x0 + 4, yy, 44, 13, "DF")
        pdf.set_xy(x0 + 6, yy + 2)
        pdf.set_font("hei", "", 9)
        pdf.cell(0, 4.5, a)
        pdf.set_xy(x0 + 6, yy + 7)
        pdf.set_text_color(*GRAY)
        pdf.cell(0, 4.5, b)
        pdf.set_text_color(*DARK)
        yy += 16
    # 中：主控
    mx0 = x0 + 66
    pdf.set_draw_color(*GREEN)
    pdf.set_fill_color(238, 250, 243)
    pdf.rect(mx0, y0, 48, 62, "DF")
    pdf.set_fill_color(*GREEN)
    pdf.rect(mx0 + 6, y0 + 6, 36, 12, "F")
    pdf.set_font("hei", "B", 11)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(mx0 + 6, y0 + 8)
    pdf.cell(36, 8, "GD32F103", align="C")
    pdf.set_font("hei", "", 9)
    pdf.set_text_color(*DARK)
    pdf.set_xy(mx0 + 4, y0 + 24)
    pdf.cell(0, 5, "显示屏/按键/蜂鸣器")
    pdf.set_xy(mx0 + 4, y0 + 33)
    pdf.cell(0, 5, "正压稳压 / 欠压断电")
    pdf.set_xy(mx0 + 4, y0 + 42)
    pdf.cell(0, 5, "流失流量监测")
    # 右：继电器
    rx0 = mx0 + 62
    pdf.set_draw_color(*RED)
    pdf.set_fill_color(253, 242, 242)
    pdf.rect(rx0, y0, 52, 62, "DF")
    pdf.set_font("hei", "B", 10)
    pdf.set_text_color(*RED)
    pdf.set_xy(rx0 + 4, y0 + 4)
    pdf.cell(44, 6, "输出 · 继电器")
    pdf.set_font("hei", "", 9)
    pdf.set_text_color(*DARK)
    rel = [("排气", "PD2"), ("进气", "PC0"), ("警报", "PC12"), ("送电", "PC1")]
    yy = y0 + 14
    for a, b in rel:
        pdf.set_fill_color(255, 255, 255)
        pdf.rect(rx0 + 4, yy, 44, 11, "DF")
        pdf.set_xy(rx0 + 6, yy + 3)
        pdf.cell(30, 5, a)
        pdf.cell(14, 5, b)
        yy += 13
    # 箭头
    pdf.set_draw_color(90, 90, 95)
    pdf.set_line_width(0.7)
    pdf.line(x0 + 52, y0 + 31, mx0, y0 + 31)
    pdf.line(mx0 + 48, y0 + 31, rx0, y0 + 31)
    # 小箭头
    pdf.line(mx0 - 3, y0 + 31, mx0, y0 + 28)
    pdf.line(mx0 - 3, y0 + 31, mx0, y0 + 34)
    pdf.line(rx0 - 3, y0 + 28, rx0, y0 + 31)
    pdf.line(rx0 - 3, y0 + 34, rx0, y0 + 31)
    pdf.set_y(y0 + 66)

draw_wiring()
spacer(4)
body("注意：接线前请确认断电，传感器与继电器接线应遵循柜体电气图纸与防爆规范。")


# ---------- 四、界面说明 ----------
pdf.add_page()
title_section("四、界面与按键说明")

# 屏幕绘制辅助
def screen(x, y, w, h):
    pdf.set_draw_color(150, 150, 155)
    pdf.set_fill_color(255, 255, 255)
    pdf.set_line_width(0.5)
    pdf.rect(x, y, w, h, "DF")

def btn(x, y, w, h, label, fill=DARK):
    pdf.set_fill_color(*fill)
    pdf.rect(x, y, w, h, "F")
    pdf.set_font("hei", "", 10)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(x, y + h / 2 - 3)
    pdf.cell(w, 6, label, align="C")
    pdf.set_text_color(*DARK)

body("4.1 主页面——上电自检后进入", 11, BLUE)
spacer(1)
sx, sy = 30, pdf.get_y()
screen(sx, sy, 120, 80)
# 界面内容
pdf.set_font("hei", "B", 13)
pdf.set_text_color(*BLUE)
pdf.set_xy(sx, sy + 18)
pdf.cell(120, 8, "欢迎使用正压防爆系统", align="C")
pdf.set_font("hei", "", 10)
pdf.set_text_color(*DARK)
pdf.set_xy(sx, sy + 32)
pdf.cell(120, 6, "服务电话 : 13023456789", align="C")
pdf.set_font("hei", "B", 12)
pdf.set_text_color(*BLUE)
pdf.set_xy(sx, sy + 44)
pdf.cell(120, 7, "谷子防爆电气有限公司", align="C")
btn(sx + 4, sy + 62, 36, 12, "正压启动")
btn(sx + 42, sy + 62, 36, 12, "系统设置")
btn(sx + 80, sy + 62, 36, 12, "系统调试")
pdf.set_y(sy + 82)

pdf.ln(2)
need_space(110)
body("4.2 正压运行界面", 11, BLUE)
spacer(1)
sy = pdf.get_y()
screen(sx, sy, 120, 80)
# 顶栏
for i, t in enumerate(["进气", "排气", "送电", "警报"]):
    pdf.set_fill_color(235, 236, 240)
    pdf.rect(sx + i * 16, sy, 14, 7, "F")
    pdf.set_font("hei", "", 7.5)
    pdf.set_text_color(*DARK)
    pdf.set_xy(sx + i * 16, sy + 1.5)
    pdf.cell(14, 5, t, align="C")
pdf.set_font("hei", "", 9.5)
pdf.set_text_color(*DARK)
pdf.set_xy(sx + 4, sy + 13)
pdf.cell(0, 5, "柜内温度 :  26℃")
pdf.set_xy(sx + 4, sy + 22)
pdf.cell(0, 5, "柜内压力 :  0250Pa")
pdf.set_fill_color(*GREEN)
pdf.rect(sx, sy + 29, 120, 9, "F")
pdf.set_text_color(255, 255, 255)
pdf.set_font("hei", "B", 10)
pdf.set_xy(sx, sy + 31)
pdf.cell(120, 6, "系统运行中", align="C")
pdf.set_font("hei", "", 9.5)
pdf.set_text_color(*DARK)
pdf.set_xy(sx + 4, sy + 44)
pdf.cell(0, 5, "压力正常值 : 0150 ~ 0300Pa")
pdf.set_xy(sx + 4, sy + 53)
pdf.cell(0, 5, "流失流量 : 0027 L/h")
btn(sx + 4, sy + 62, 36, 12, "取消警报")
btn(sx + 80, sy + 62, 36, 12, "返回主页")
pdf.set_y(sy + 82)

pdf.ln(2)
need_space(110)
body("4.3 系统设置菜单", 11, BLUE)
spacer(1)
sy = pdf.get_y()
screen(sx, sy, 120, 80)
pdf.set_font("hei", "B", 10)
pdf.set_text_color(*DARK)
pdf.set_xy(sx + 4, sy + 4)
pdf.cell(0, 5, "系统设置")
menu = ["修改密码", "校准传感器", "设置参数", "恢复出厂"]
yy = sy + 13
for i, m in enumerate(menu):
    if i == 0:
        pdf.set_fill_color(*DARK)
        pdf.rect(sx + 4, yy, 40, 9, "F")
        pdf.set_text_color(255, 255, 255)
    else:
        pdf.set_text_color(*DARK)
    pdf.set_font("hei", "", 9)
    pdf.set_xy(sx + 8, yy + 2)
    pdf.cell(40, 5, m)
    yy += 11.5
pdf.set_text_color(*DARK)
btn(sx + 4, sy + 62, 36, 12, "返回主页")
btn(sx + 42, sy + 62, 36, 12, "下一选项")
btn(sx + 80, sy + 62, 36, 12, "确认")
pdf.set_y(sy + 82)

pdf.ln(2)
need_space(55)
body("4.4 按键通用规则", 11, BLUE)
spacer(1)
key_rows = [
    ("KEY1", "确认 / 值加 1 / 消音", "返回主页"),
    ("KEY2", "下一选项 / 下一位", "放弃修改"),
    ("KEY3", "进入 / 确认 / 下一项", "保存 / 恢复出厂"),
]
pdf.set_font("hei", "B", 10)
pdf.set_fill_color(*LGRAY)
pdf.cell(22, 8, "按键", border=1, fill=True, align="C")
pdf.cell(90, 8, "短按", border=1, fill=True, align="C")
pdf.cell(68, 8, "长按（3 秒）", border=1, fill=True, align="C", ln=1)
pdf.set_font("hei", "", 10)
for a, b, c in key_rows:
    pdf.cell(22, 8, a, border=1, align="C")
    pdf.cell(90, 8, b, border=1)
    pdf.cell(68, 8, c, border=1, ln=1)


# ---------- 五、操作指南 ----------
pdf.add_page()
title_section("五、操作指南")

body("5.1 开机", 11, BLUE)
body("接通电源，系统上电自检并显示开机动画（约 3 秒），随后进入主页面。屏幕长时间无操作会息屏，按任意键唤醒。")
spacer()

body("5.2 正压启动", 11, BLUE)
spacer(1)
# 流程图
def draw_flow():
    cx = 105
    fy = pdf.get_y()
    steps = [
        ("上电开机（自检）", BLUE),
        ("主页按「正压启动」", BLUE),
        ("换气倒计时（默认 900s）", (232, 179, 57)),
        ("压力达到正常范围？", (232, 179, 57)),
        ("自动送电（接通负载）", GREEN),
        ("系统运行中（稳压+流失流量监测）", GREEN),
    ]
    yy = fy
    for i, (txt, col) in enumerate(steps):
        if i == 3:
            w = 70
            pdf.set_fill_color(*col)
            # 菱形近似
            pdf.polygon([(cx - w / 2, yy), (cx, yy - 12), (cx + w / 2, yy), (cx, yy + 12)], style="F")
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("hei", "", 9.5)
            pdf.set_xy(cx - w + 20, yy - 3)
            pdf.cell(w * 1.4 - 40, 6, txt, align="C")
            yy += 16
        else:
            w = 90 if i == 5 else 72
            pdf.set_fill_color(*col)
            pdf.rect(cx - w / 2, yy, w, 12, "F")
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("hei", "", 9.5)
            pdf.set_xy(cx - w / 2, yy + 3)
            pdf.cell(w, 6, txt, align="C")
            yy += 12
        if i != 5:
            pdf.set_draw_color(90, 90, 95)
            pdf.set_line_width(0.8)
            pdf.line(cx, yy, cx, yy + 7)
            yy += 7
    pdf.set_y(yy + 2)

need_space(125)
draw_flow()
pdf.ln(3)
body("操作步骤：")
for t in [
    "1. 在主页面按 KEY1（正压启动）；",
    "2. 系统进入换气倒计时（默认 900 秒），期间自动控制进 / 排气阀吹扫换气；",
    "3. 倒计时结束且柜压达到正常范围后，自动送电接通负载；",
    "4. 进入「系统运行中」，持续稳压、报警监测，并每 30 秒自动测算流失流量；",
    "5. 运行中按 KEY3 返回主页，按 KEY1 对报警消音。",
]:
    body(t)
spacer()

body("5.3 系统设置 / 修改密码 / 校准 / 参数设置", 11, BLUE)
for t in [
    "· 系统设置：主页按 KEY2，输入密码（默认 555）进入；KEY2 移动选项、KEY3 确认。",
    "· 修改密码：KEY1 加值、KEY2 移动位；长按 KEY3 保存、长按 KEY1 返回。",
    "· 校准传感器：可校准温度、压力显示值；长按 KEY3 保存、长按 KEY2 放弃。",
    "· 设置参数：依次设置压力下限/下下限/上限/上上限、温度上限、换气时间、流量量程。",
]:
    body(t)
spacer()

body("5.4 系统调试", 11, BLUE)
body("危险！调试模式会在现场直接送电，务必确认危险区域无人、环境安全后方可操作。")
body("主页按 KEY3，输入密码进入调试页 → 按 KEY3（确认调试）送电 → 调试结束按 KEY3（调试结束）退出。")


# ---------- 六、参数说明 ----------
pdf.add_page()
title_section("六、参数说明")
pdf.ln(1)
p = [
    ("压力下限", "柜压低于此值开始补气", "Pa"),
    ("压力下下限", "柜压低于此值触发报警/欠压保护", "Pa"),
    ("压力上限", "柜压高于此值开始排气泄压", "Pa"),
    ("压力上上限", "柜压高于此值触发报警", "Pa"),
    ("温度上限", "柜温超过此值触发报警", "℃"),
    ("换气时间", "正压启动吹扫倒计时时长", "s"),
    ("流量量程", "进气流量计满量程（备用）", "m³/h"),
]
pdf.set_font("hei", "B", 10)
pdf.set_fill_color(*LGRAY)
pdf.cell(30, 8.5, "参数", border=1, fill=True, align="C")
pdf.cell(110, 8.5, "含义", border=1, fill=True, align="C")
pdf.cell(30, 8.5, "单位", border=1, fill=True, align="C", ln=1)
pdf.set_font("hei", "", 10)
for a, b, c in p:
    pdf.cell(30, 8.5, a, border=1, align="C")
    pdf.cell(110, 8.5, b, border=1)
    pdf.cell(30, 8.5, c, border=1, align="C", ln=1)

spacer(4)
title_section("七、流失流量监测说明")
body("流失流量用于量化柜体的密封性 / 泄漏程度，采用压力衰减法测量：")
for t in [
    "测量时机：仅在柜体稳定（进、排气阀都关闭）时自动进行，不影响正常稳压；",
    "测量周期：每 30 秒自动结算并刷新一次；",
    "计算方式：流失流量(L/h) = 8.275 × 压降(Pa)/时间(s) × 293.15/(273.15+柜温℃)；",
    "温度修正：使用 PT100 实测柜温自动修正（工作温度 -50~120℃）；",
    "前提：结果依赖柜体密闭容积（出厂按 0.25 m³ 计），容积不符或测量期间开柜门会导致偏差。",
]:
    bullet(t)


# ---------- 八、报警与保护 ----------
title_section("八、报警与保护")
pdf.ln(1)
al = [
    ("柜压低于下下限或高于上上限", "声光报警"),
    ("柜压低于下下限持续 10 秒", "自动切断送电（欠压断电保护）"),
    ("柜温超过上限", "声光报警"),
    ("温度 / 压力传感器断线或超程", "声光报警"),
    ("换气时间内压力不能恢复", "压力恢复超时报警"),
]
pdf.set_font("hei", "B", 10)
pdf.set_fill_color(*LGRAY)
pdf.cell(90, 8.5, "情况", border=1, fill=True, align="C")
pdf.cell(90, 8.5, "动作", border=1, fill=True, align="C", ln=1)
pdf.set_font("hei", "", 10)
for a, b in al:
    pdf.cell(90, 8.5, a, border=1)
    pdf.cell(90, 8.5, b, border=1, ln=1)
spacer(2)
body("报警解除后蜂鸣器可按 KEY1 消音；故障排除且参数恢复正常后报警自动复位。")


# ---------- 九、安全须知 ----------
title_section("九、安全须知")
for t in [
    "本设备属防爆场合用电气装置，安装、接线、调试须由具备资质的专业人员进行；",
    "通电运行前确认柜门关闭、防爆面完好、紧固件齐全；",
    "系统处于报警或欠压断电状态时，先排查故障，严禁屏蔽报警继续使用；",
    "压力、温度传感器量程应与柜体实际工况匹配；",
    "更改参数、密码后请核对无误再投入运行。",
]:
    bullet(t)


# ---------- 十、常见问题 ----------
title_section("十、常见问题")
pdf.ln(1)
faq = [
    ("无法进入设置/调试", "密码错误", "用默认密码 555 或万能密码 995"),
    ("柜压始终偏低", "柜体泄漏 / 进气管堵塞", "检查密封性与气源"),
    ("流失流量偏大", "柜门未关严或含其他开口", "检查柜体密闭性"),
    ("报警不响", "处于消音状态 / 蜂鸣器故障", "检查消音状态或硬件"),
    ("屏幕息屏无显示", "进入省电息屏", "按任意键唤醒"),
]
pdf.set_font("hei", "B", 10)
pdf.set_fill_color(*LGRAY)
pdf.cell(45, 8.5, "现象", border=1, fill=True, align="C")
pdf.cell(60, 8.5, "可能原因", border=1, fill=True, align="C")
pdf.cell(75, 8.5, "处理", border=1, fill=True, align="C", ln=1)
pdf.set_font("hei", "", 9.5)
for a, b, c in faq:
    pdf.cell(45, 8.5, a, border=1)
    pdf.cell(60, 8.5, b, border=1)
    pdf.cell(75, 8.5, c, border=1, ln=1)

spacer(6)
pdf.set_font("hei", "", 9)
pdf.set_text_color(*GRAY)
pdf.cell(0, 5, "本说明书最终解释权归谷子防爆电气有限公司所有。", align="C")

out = "E:/gd32f103rct6-618-3.5/output/正压防爆控制系统使用说明书.pdf"
pdf.output(out)
print("OK:", out)