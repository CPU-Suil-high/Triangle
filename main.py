import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import colorchooser
import tkinter.messagebox

from sympy import *

import ctypes

from PIL import ImageGrab, Image, ImageTk
import matplotlib.mathtext as mathtext

parser = mathtext.MathTextParser("Bitmap")

ctypes.windll.shcore.SetProcessDpiAwareness(1)

def main():
    global angleStrings, sideStrings
    createMainWindow()
    init()
    placeMainWidget()
    run()
    mainWindow.mainloop()

# 필요한 변수 정의
def init():
    global angleStrings, sideStrings, resultDegStrings, resultRadStrings, resultRadFloatStrings, resultSideStrings, resultSideFloatStrings, angleDisplayTypeStrings, sideDisplayTypeStrings, angleEnterTypeString, triangleColor
    angleStrings = [tk.StringVar(value="60") for _ in range(3)]
    sideStrings = [tk.StringVar(value="1") for _ in range(3)]

    resultDegStrings = [tk.StringVar() for _ in range(3)]
    resultRadStrings = [tk.StringVar() for _ in range(3)]
    resultRadFloatStrings = [tk.StringVar() for _ in range(3)]
    resultSideStrings = [tk.StringVar() for _ in range(3)]
    resultSideFloatStrings = [tk.StringVar() for _ in range(3)]

    angleDisplayTypeStrings = [tk.StringVar(value="Deg") for _ in range(3)]
    sideDisplayTypeStrings = [tk.StringVar(value="Char") for _ in range(3)]

    angleEnterTypeString = tk.StringVar(value="deg")

    triangleColor = "#ffffff"

def runHelp():
    createHelpWindow()
    placeHelpWidget()

# 도움말 창 생성
def createHelpWindow():
    global helpWindow
    helpWindow = tk.Toplevel()
    helpWindow.title("도움말")
    helpWindow.geometry("650x540")
    helpWindow.resizable(False, False)

# 도움말 위젯 배치
def placeHelpWidget():
    global helpWindow
    # 설명 내용
    contant = \
"""* 알고 있는 각과 변의 길이를 입력하고 실행하면 나머지 각과 길이를 구합니다

* 모르는 각과 길이는 비워두거나 0을 넣습니다

* 입력한 정보가 부족하거나 삼각형이 될 수 없는 값을 입력하면 실행되지 않습니다

<입력 방법>
분수 -> ((분자) / (분모)) or Rational((분자), (분모))

루트 a -> sqrt(a)

sinA       -> sin(A)
cosA      -> cos(A)
arcsinA   -> asin(A)
arccosA  -> acos(A)
(A의 단위는 rad)

원주율 -> pi

더하기 -> +
빼기    -> -
곱하기 -> *
나누기 -> /

x의 n제곱 -> x**n

x를 육십분법으로 변환 -> deg(x)
(x의 단위는 rad)
"""
    # 설명 라벨
    label = tk.Label(helpWindow, text=contant, font=("", 10), justify="left")
    label.pack(side="top", anchor="w", padx=10, pady=10)

# 메인 화면 생성
def createMainWindow():
    global mainWindow
    mainWindow = tk.Tk()
    mainWindow.title("삼각형")
    mainWindow.geometry("710x560")
    mainWindow.resizable(True, True)

# 메인 위젯 배치
def placeMainWidget():
    global mainWindow, canvas, angleStrings, sideStrings, resultDegStrings, resultRadStrings, resultRadFloatStrings, resultSideStrings, resultSideFloatStrings, angleButton, angleDisplayTypeStrings, sideDisplayTypeStrings
    # canvas grid 배치용 frame
    frame = tk.Frame(mainWindow)
    frame.grid(column=0, row=0, columnspan=10, rowspan=30)

    # 삼각형이 그려질 canvas
    canvas = tk.Canvas(frame, width=500, height=500, background="white")
    canvas.images = []
    canvas.pack(fill="both")

    # 삼각형 각도 입력 위젯
    for i in range(3):
        # 설명 label
        label = tk.Label(mainWindow, text="[각도 "+("A", "B", "C")[i]+"]", font=("", 10, "bold"))
        label.grid(column=11+i, row=26)
        # 각도 입력 entry
        entry = tk.Entry(mainWindow, textvariable=angleStrings[i], width=10)
        entry.grid(column=11+i, row=27, padx=5, pady=0)
    
    # 입력 단위 표시 및 변경 버튼
    angleButton = tk.Button(mainWindow, textvariable=angleEnterTypeString, command=clickEnterTypeButton) # degree
    angleButton.grid(column=14, row=27, padx=5, sticky="w")
    # 삼각형 변의 길이 입력 위젯
    for i in range(3):
        # 설명 label
        label = tk.Label(mainWindow, text="[변 "+("a", "b", "c")[i]+"]", font=("", 10, "bold"))
        label.grid(column=11+i, row=28)
        # 변의길이 입력 entry
        entry = tk.Entry(mainWindow, textvariable=sideStrings[i], width=10)
        entry.grid(column=11+i, row=29, padx=5, pady=0)

    # 각도 결과 위젯 배치
    for i in range(3):
        # 설명 label
        label1 = tk.Label(mainWindow, text="[각도 "+("A", "B", "C")[i]+"]", font=("", 10, "bold"))
        label1.grid(column=11+i, row=1, padx=5)
        # deg결과
        label2 = tk.Label(mainWindow, textvariable=resultDegStrings[i])
        label2.grid(column=11+i, row=2, padx=5)
        # rad결과
        label3 = tk.Label(mainWindow, textvariable=resultRadStrings[i])
        label3.grid(column=11+i, row=3, padx=5)
        # rad float 결과
        label4 = tk.Label(mainWindow, textvariable=resultRadFloatStrings[i])
        label4.grid(column=11+i, row=4, padx=5)

    # 단위 표시
    label1 = tk.Label(mainWindow, text="deg") # degree
    label1.grid(column=14, row=2, padx=5, sticky="w")

    label2 = tk.Label(mainWindow, text="rad") # radian
    label2.grid(column=14, row=3, padx=5, sticky="w")

    label3 = tk.Label(mainWindow, text="rad") # radian
    label3.grid(column=14, row=4, padx=5, sticky="w")
    
    # 길이 결과 위젯 배치
    for i in range(3):
        # 설명 label
        label1 = tk.Label(mainWindow, text="[변 "+("a", "b", "c")[i]+"]", font=("", 10, "bold"))
        label1.grid(column=11+i, row=6, padx=5)
        # side 결과
        label2 = tk.Label(mainWindow, textvariable=resultSideStrings[i])
        label2.grid(column=11+i, row=7, padx=5)
        # side float 결과
        label2 = tk.Label(mainWindow, textvariable=resultSideFloatStrings[i])
        label2.grid(column=11+i, row=8, padx=5)
    
    # 삼각형 그리기 옵션 위젯
    # 각도 표시 설정 위젯
    for i in range(3):
        # A B C 표시 label
        label1 = tk.Label(mainWindow, text="[각도 "+("A", "B", "C")[i]+"]", font=("", 10, "bold"))
        label1.grid(column=0+i*4, row=31, padx=5, pady=5)

        # 각도 표시 설정 combobox
        comboBox = ttk.Combobox(mainWindow, textvariable=angleDisplayTypeStrings[i], values=("Deg", "Expr", "Float", "None"), exportselection=False, width=10, state="readonly")
        comboBox.grid(column=0+i*4, row=32, padx=5, pady=5)

    # 변의 길이 표시 설정 위젯
    for i in range(3):
        # a b c 표시 label
        label = tk.Label(mainWindow, text="[변 "+("a", "b", "c")[i]+"]", font=("", 10, "bold"))
        label.grid(column=0+i*4, row=33, padx=5, pady=5)

        # 길이 표시 설정 combobox
        comboBox = ttk.Combobox(mainWindow, textvariable=sideDisplayTypeStrings[i], values=("Char", "Expr", "Float", "None"), exportselection=False, width=10, state="readonly")
        comboBox.grid(column=0+i*4, row=34, padx=5, pady=5)

    # 색변경 button
    colorButton = tk.Button(mainWindow, text="색변경", command=changeColor)
    colorButton.grid(column=11, row=32)
    
    # 실행 button
    runButton = tk.Button(mainWindow, text="실행", command=run)
    runButton.grid(column=11, row=34)

    # 이미지 저장 button
    saveButton = tk.Button(mainWindow, text="저장", command=saveImage)
    saveButton.grid(column=12, row=34)

    # 도움말 buttom
    helpButton = tk.Button(mainWindow, text="도움말", command=runHelp)
    helpButton.grid(column=13, row=34)

# 삼각형 계산 후 그리기 실행
def run():
    global angles, sides, resultDegStrings, resultRadStrings, resultSideStrings, angleButton, mainWindow, angleEnterTypeString
    # 공백 0으로 채우기
    for i in range(3):
        if (angleStrings[i].get() == ""):
            angleStrings[i].set("0")
        if (sideStrings[i].get() == ""):
            sideStrings[i].set("0")

    
    # 문자열로 된 각도와 변의 길이 실수로 변환
    try:
        if (angleEnterTypeString.get() == "rad"):
            angles = [sympify(angle.get()) for angle in angleStrings]
        elif (angleEnterTypeString.get() == "deg"):
            angles = [rad(sympify(angle.get())) for angle in angleStrings]
        else:
            raise "angleEnterType is rad or deg"
        sides = [sympify(side.get()) for side in sideStrings]
    except:
        tkinter.messagebox.showerror("error", "잘못된 값이 입력되었습니다.")
        return

    try:
        getTriangle()
        if (not checkTriangle()):
            tkinter.messagebox.showerror("error", "잘못된 값이 입력되었습니다.")
            return
    except:
        tkinter.messagebox.showerror("error", "잘못된 값이 입력되었습니다.")
        return
    
    # 결과 반영
    for i in range(3):
        # deg
        resultDegStrings[i].set(str(float(deg(angles[i]))))
        # rad
        resultRadStrings[i].set(str(angles[i]))
        resultRadFloatStrings[i].set(str(float(angles[i])))
        # side
        resultSideStrings[i].set(str(sides[i]))
        resultSideFloatStrings[i].set(str(float(sides[i])))

    # 위젯 배치에 따라 윈도우 창 크기 조절
    mainWindow.update()
    mainWindow.geometry(f"{angleButton.winfo_x() + angleButton.winfo_width() + 10}x660")

    drawTriangle()

def checkTriangle():
    global angles, sides
    # 3개의 각의 합이 180이 아닐때
    if (round((float(sum(angles)) - pi), 10) != 0):
        return False
    # 마이너스인 각이 존재할때
    elif (min(angles) < 0):
        return False
    # 가장 큰 변의 길이가 나머지 길이의 합과 같거나 클때
    elif (max(sides) >= sum(sides) + max(sides)):
        return False
    # 각이나 변의 길이에 0인 값이 있을 때
    elif (angles.count(0) != 0 or sides.count(0) != 0):
        return False
    # x / sinX 값이 모두 같지 않을 때
    elif (float(sides[0] / sin(angles[0])) != float(sides[1] / sin(angles[1])) or float(sides[0] / sin(angles[0])) != float(sides[2] / sin(angles[2]))):
        return False
    else:
        return True

# 삼각형 그리기
def drawTriangle():
    global canvas, angles, sides, resultSideFloatStrings, resultSideStrings, resultRadStrings, resultRadFloatStrings, resultDegStrings
    # canvs 초기화
    canvas.delete("all")
    canvas.images.clear()
    # canvas 크기
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    a, b, c = sides
    A, B, C = angles

    # 변의 길이 canvas 크기에 맞게 조절
    sumSide = sum(sides)

    a = a / sumSide * 600
    b = b / sumSide * 600
    c = c / sumSide * 600

    # 삼각형 꼭짓점 위치
    BPos = Vecotr(float(width/2-a/2), height/3*2)
    CPos = Vecotr(float(width/2+a/2), height/3*2)
    APos = Vecotr(float(BPos[0] + cos(B) * c), float(BPos[1] - sin(B) * c))

    # 삼각형 그리기
    canvas.create_polygon(*APos, *BPos, *CPos, fill=triangleColor)
    canvas.create_line(*APos, *BPos, *CPos, *APos, fill="black", capstyle="round", joinstyle="round", width=2)
    
    # A B C 그리기
    canvas.create_text(APos.x, APos.y - 20, text="A", font=("", 20)) # A
    canvas.create_text(BPos.x - 20, BPos.y + 20, text="B", font=("", 20)) # B
    canvas.create_text(CPos.x + 20, CPos.y + 20, text="C", font=("", 20)) # C

    # 벡터
    vecAB = BPos - APos
    vecAC = CPos - APos
    vecBC = CPos - BPos

    # 삼각형의 내심 좌표
    IPos = (vecAB.distance()*CPos + vecBC.distance()*APos + vecAC.distance()*BPos)/(vecAB.distance() + vecAC.distance() + vecBC.distance())

    vecAI = IPos - APos
    vecBI = IPos - BPos
    vecCI = IPos - CPos

    # A B C 각도 위치
    angleSize = 40
    angleAPos = APos + vecAI.normalize()*angleSize
    angleBPos = BPos + vecBI.normalize()*angleSize
    angleCPos = CPos + vecCI.normalize()*angleSize

    # a b c 위치
    aPos = (BPos + CPos)/2
    aPos.y += 40

    vec = Vecotr(vecAC.normalize().y*40, -vecAC.normalize().x*40) # 벡터AC에 수직방향인 벡터
    bPos = (APos + CPos)/2 + vec

    vec = Vecotr(-vecAB.normalize().y*40, vecAB.normalize().x*40) # 벡터AB에 수직방향인 벡터
    cPos = (APos + BPos)/2 + vec

    # A B C 각도 그리기
    # A
    ALine = True
    AType = angleDisplayTypeStrings[0].get()
    if (AType == "Deg"):
        result = float(resultDegStrings[0].get())
        if (result - int(result) == 0):
            text = str(int(result))
        else:
            text = resultDegStrings[0].get()
        id = canvas.create_text(*angleAPos, text=text, font=("", 10), anchor="n")
        _, y, x, _ = canvas.bbox(id)
        canvas.create_oval(x, y, x+3, y+3)
    elif (AType == "Expr"):
        drawMathExpr(canvas, sympify(resultRadStrings[0].get()), "n", angleAPos, 12)
    elif (AType == "Float"):
        canvas.create_text(*angleAPos, text=resultRadFloatStrings[0].get(), font=("", 10), anchor="n")
    elif (AType == "None"):
        ALine = False
    
    # B
    BLine = True
    BType = angleDisplayTypeStrings[1].get()
    if (BType == "Deg"):
        result = float(resultDegStrings[1].get())
        if (result - int(result) == 0):
            text = str(int(result))
        else:
            text = resultDegStrings[1].get()
        id = canvas.create_text(*angleBPos, text=text, font=("", 10), anchor="w")
        _, y, x, _ = canvas.bbox(id)
        canvas.create_oval(x, y, x+3, y+3)
    elif (BType == "Expr"):
        drawMathExpr(canvas, sympify(resultRadStrings[1].get()), "w", angleBPos, 12)
    elif (BType == "Float"):
        canvas.create_text(*angleBPos, text=resultRadFloatStrings[1].get(), font=("", 10), anchor="w")
    elif (BType == "None"):
        BLine = False
    
    # C
    CLine = True
    CType = angleDisplayTypeStrings[2].get()
    if (CType == "Deg"):
        result = float(resultDegStrings[2].get())
        if (result - int(result) == 0):
            text = str(int(result))
        else:
            text = resultDegStrings[2].get()
        id = canvas.create_text(*angleCPos, text=text, font=("", 10), anchor="e")
        _, y, x, _ = canvas.bbox(id)
        canvas.create_oval(x, y, x+3, y+3)
    elif (CType == "Expr"):
        drawMathExpr(canvas, sympify(resultRadStrings[2].get()), "e", angleCPos, 12)
    elif (CType == "Float"):
        canvas.create_text(*angleCPos, text=resultRadFloatStrings[2].get(), font=("", 10), anchor="e")
    elif (CType == "None"):
        CLine = False
    
    # 각도를 나타내는 선
    if (ALine):
        pos1 = APos + vecAB.normalize()*2*angleSize/3
        pos2 = APos + vecAC.normalize()*2*angleSize/3
        canvas.create_line(*pos1, *angleAPos, *pos2, smooth=True)
    if (BLine):
        pos1 = BPos - vecAB.normalize()*2*angleSize/3
        pos2 = BPos + vecBC.normalize()*2*angleSize/3
        canvas.create_line(*pos1, *angleBPos, *pos2, smooth=True)
    if (CLine):
        pos1 = CPos - vecAC.normalize()*2*angleSize/3
        pos2 = CPos - vecBC.normalize()*2*angleSize/3
        canvas.create_line(*pos1, *angleCPos, *pos2, smooth=True)

    # a b c 그리기
    # a
    aLine = True
    aType = sideDisplayTypeStrings[0].get()
    if (aType == "Char"):
        canvas.create_text(*aPos, text="a", font=("", 20), anchor="n") # a
    elif (aType == "Expr"):
        drawMathExpr(canvas, sympify(resultSideStrings[0].get()), "n", aPos, 15)
    elif (aType == "Float"):
        result = float(resultSideFloatStrings[0].get())
        if (result - int(result) == 0):
            aText = str(int(result))
        else:
            aText = resultSideFloatStrings[0].get()
        canvas.create_text(*aPos, text=aText, font=("", 20), anchor="n") # a
    elif (aType == "None"):
        aLine = False

    # b
    bLine = True
    bType = sideDisplayTypeStrings[1].get()
    if (bType == "Char"):
        canvas.create_text(*bPos, text="b", font=("", 20), anchor="w") # b
    elif (bType == "Expr"):
        bText = resultSideStrings[1].get()
        drawMathExpr(canvas, sympify(resultSideStrings[1].get()), "w", bPos, 15)
    elif (bType == "Float"):
        result = float(resultSideFloatStrings[1].get())
        if (result - int(result) == 0):
            bText = str(int(result))
        else:
            bText = resultSideFloatStrings[1].get()
        canvas.create_text(*bPos, text=bText, font=("", 20), anchor="w") # b
    elif (bType == "None"):
        bLine = False
    
    # c
    cLine = True
    cType = sideDisplayTypeStrings[2].get()
    if (cType == "Char"):
        canvas.create_text(*cPos, text="c", font=("", 20), anchor="e") # c
    elif (cType == "Expr"):
        drawMathExpr(canvas, sympify(resultSideStrings[2].get()), "e", cPos, 15)
    elif (cType == "Float"):
        result = float(resultSideFloatStrings[2].get())
        if (result - int(result) == 0):
            cText = str(int(result))
        else:
            cText = resultSideFloatStrings[2].get()
        canvas.create_text(*cPos, text=cText, font=("", 20), anchor="e") # c
    elif (cType == "None"):
        cLine = False

    # 변을 나타내는 점선 그리기
    if (aLine):
        canvas.create_line(*BPos, *aPos, *CPos, smooth=True, width=1, dash=2)
    if (bLine):
        canvas.create_line(*APos, *bPos, *CPos, smooth=True, width=1, dash=2)
    if (cLine):
        canvas.create_line(*APos, *cPos, *BPos, smooth=True, width=1, dash=2)

# 삼각형의 각도와 변의 길이 구하기
def getTriangle():
    global angleStrings, sideStrings, angles, sides

    for i in range(3):
        getAngle(i)
    for i in range(3):
        getSide(i)
    for i in range(3):
        getAngle(i)
    for i in range(3):
        getSide(i)

# 각도 구하기
def getAngle(index):
    global angles, sides
    a, b, c = sides[index], sides[(index+1)%3], sides[(index-1)%3]
    A, B, C = angles[index], angles[(index+1)%3], angles[(index-1)%3]

    # 이미 알때
    if (A != 0):
        return
    # 3변의 길이를 알때
    elif (sides.count(0) == 0):
        x = Symbol("x") # cosA
        eq = Eq((b**2 + c**2 - a**2) / (2*b*c), x) # 코사인법칙 식

        cosA = solve(eq)[0] # 코사인 값
        A = acos(cosA) # 라디안 각도
        angles[index] = simplify(A)
    # 나머지 각도 2개를 알때
    elif (angles.count(0) == 1):
        index = angles.index(0) # 모르는 각도 위치
        angle = pi - sum(angles) # 180 - 각도 2개의 합
        angles[index] = angle
    # 대변의 길이를 알고 다른 각의 크기와 그 각의 대변의 길이를 알때
    elif (a != 0 and ((b != 0 and B != 0) or (c != 0 and C != 0))):
        if (b != 0 and B != 0):
            twoR = b / sin(B)
        elif (c != 0 and C != 0):
            twoR = c / sin(C)
        
        x = Symbol("x") # sinA 미지수
        eq = Eq(a/twoR, x) # 사인법칙 식

        sinA = solve(eq)[0] # 사인 값
        A = asin(sinA) # 라디안 각도
        angles[index] = simplify(A)

# 변의 길이 구하기
def getSide(index):
    global angles, sides
    a, b, c = sides[index], sides[(index+1)%3], sides[(index-1)%3]
    A, B, C = angles[index], angles[(index+1)%3], angles[(index-1)%3]

    # 이미 알때
    if (a != 0):
        return
    # 각의 크기와 나머지 변 2개를 알때
    elif ((A != 0 or B != 0 or C != 0) and b != 0 and c != 0):
        x = Symbol("x") # a 미지수
        if (A != 0): # A각을 알때
            eq = Eq(b**2 + c**2 - 2*b*c*cos(A), x**2) # 코사인법칙 식
        elif (B != 0): # B각을 알때
            eq = Eq(x**2 + c**2 - 2*x*c*cos(B), b**2)
        elif (C != 0): # C각을 알때
            eq = Eq(x**2 + b**2 - 2*x*b*cos(C), c**2)

        if (A > pi/2 or min(solve(eq)) < 0):
            a = max(solve(eq))
        else:
            a = min(solve(eq))
        sides[index] = simplify(a)
    # 대각의 크기를 알고 다른 각의 크기와 그 각의 대변의 길이를 알때
    elif (A != 0 and ((b != 0 and B != 0) or (c != 0 and C != 0))):
        if (b != 0 and B != 0):
            twoR = b / sin(B)
        elif (c != 0 and C != 0):
            twoR = c / sin(C)
        
        x = Symbol("x") # a 미지수
        eq = Eq(twoR * sin(A), x) # 사인법칙 식

        a = max(solve(eq))
        sides[index] = simplify(a)

def clickEnterTypeButton():
    global angleEnterTypeString
    if (angleEnterTypeString.get() == "deg"):
        angleEnterTypeString.set("rad")
    elif (angleEnterTypeString.get() == "rad"):
        angleEnterTypeString.set("deg")
    else:
        raise "angleEnterType is rad or deg"

def saveImage():
    global canvas
    # 저장 위치 받기
    filePath = filedialog.asksaveasfilename(initialdir="d", title="이미지 저장", filetypes=(("*.png", "*png"),), defaultextension=".png")
    
    if (filePath == ""):
        return

    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()

    ImageGrab.grab().crop((x,y,x1,y1)).save(filePath)

def drawMathExpr(canvas, expr, anchor, pos, fontSize):
    # 수식 이미지 배열로 생성
    imageArray, b = parser.to_rgba("$"+latex(expr)+"$", color='black', fontsize=fontSize, dpi=100)
    # 배열을 이미지 객체로 변환
    img = Image.fromarray(imageArray)
    # tkinter에 맞는 이미지 타입으로 변환
    pimg = ImageTk.PhotoImage(img)
    # image가 객체가 사라지지 않게 저장
    canvas.images.append(pimg)
    # 사진 생성
    canvas.create_image(*pos, anchor=anchor, image=pimg)

def changeColor():
    global triangleColor
    color = colorchooser.askcolor()[1]
    triangleColor = color

class Vecotr:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vecotr(x, y)
    
    def __sub__(self, other):
        return self + -other
    
    def __mul__(self, n):
        x = self.x*n
        y = self.y*n
        return Vecotr(x, y)
    
    def __rmul__(self, n):
        x = self.x*n
        y = self.y*n
        return Vecotr(x, y)
    
    def __truediv__(self, n):
        x = self.x / n
        y = self.y / n
        return Vecotr(x, y)
    
    def __neg__(self):
        x = - self.x
        y = - self.y
        return Vecotr(x, y)
    
    def __getitem__(self, index):
        if (index == 0):
            return self.x
        elif (index == 1):
            return self.y
        else:
            raise StopIteration
        
    def __setitem__(self, index, value):
        if (index == 0):
            self.x = value
        elif (index == 1):
            self.y = value
        else:
            raise Exception
    
    def distance(self):
        return (self.x**2 + self.y**2)**0.5

    def normalize(self):
        return self / self.distance()

if (__name__ == "__main__"):
    main()