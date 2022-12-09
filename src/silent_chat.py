import pyautogui  # 操纵鼠标和键盘的API
import time
import xlrd
import pyperclip
import uuid
import pytesseract
from PIL import Image
from conversation import ConversationBot
from config import config

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

#定义鼠标事件

#pyautogui库其他用法 https://blog.csdn.net/qingfengxd1/article/details/108270159


def mouseClick(clickTimes, lOrR, img, reTry):
    img = 'imgs/' + img
    if reTry == 1:  # 重试直到成功一次
        while True:
            location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
            if location is not None:
                pyautogui.click(location.x,
                                location.y,
                                clicks=clickTimes,
                                interval=0.2,
                                duration=0.2,
                                button=lOrR)
                break
            # print(img)
            # print("未找到匹配图片,0.1秒后重试")
            time.sleep(0.1)
    elif reTry == -1:  # 一直重复
        while True:
            location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
            if location is not None:
                pyautogui.click(location.x,
                                location.y,
                                clicks=clickTimes,
                                interval=0.2,
                                duration=0.2,
                                button=lOrR)
            time.sleep(0.1)
    elif reTry > 1:  # 重试 i + 1 次
        i = 1
        while i < reTry + 1:
            location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
            if location is not None:
                pyautogui.click(location.x,
                                location.y,
                                clicks=clickTimes,
                                interval=0.2,
                                duration=0.2,
                                button=lOrR)
                print("重复")
                i += 1
            time.sleep(0.1)
    elif reTry == 0:  # 仅仅执行一次
        location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
        if location is not None:
            pyautogui.click(location.x,
                            location.y,
                            clicks=clickTimes,
                            interval=0.2,
                            duration=0.2,
                            button=lOrR)
        time.sleep(0.1)


# 数据检查
# cmdType.value  1.0 左键单击    2.0 左键双击  3.0 右键单击  4.0 输入  5.0 等待  6.0 滚轮
# ctype     空：0
#           字符串：1
#           数字：2
#           日期：3
#           布尔：4
#           error：5
def dataCheck(sheet1):
    checkCmd = True
    #行数检查
    if sheet1.nrows < 2:
        print("没数据啊哥")
        checkCmd = False
    #每行数据检查
    i = 1
    while i < sheet1.nrows:
        # 第1列 操作类型检查
        cmdType = sheet1.row(i)[0]
        if cmdType.ctype != 2 or (cmdType.value != 1.0 and cmdType.value != 2.0
                                  and cmdType.value != 3.0 and
                                  cmdType.value != 4.0 and cmdType.value != 5.0
                                  and cmdType.value != 6.0
                                  and cmdType.value != 7.0):
            print('第', i + 1, "行,第1列数据有毛病")
            checkCmd = False
        # 第2列 内容检查
        cmdValue = sheet1.row(i)[1]
        # 读图点击类型指令，内容必须为字符串类型
        if cmdType.value == 1.0 or cmdType.value == 2.0 or cmdType.value == 3.0:
            if cmdValue.ctype != 1:
                print('第', i + 1, "行,第2列数据有毛病")
                checkCmd = False
        # 输入类型，内容不能为空
        if cmdType.value == 4.0:
            if cmdValue.ctype != 0:
                print('第', i + 1, "行,第2列数据有毛病")
                checkCmd = False
        # 等待类型，内容必须为数字
        if cmdType.value == 5.0:
            if cmdValue.ctype != 2:
                print('第', i + 1, "行,第2列数据有毛病")
                checkCmd = False
        # 滚轮事件，内容必须为数字
        if cmdType.value == 6.0:
            if cmdValue.ctype != 2:
                print('第', i + 1, "行,第2列数据有毛病")
                checkCmd = False
        i += 1
    return checkCmd


#任务
def mainWork(img):
    i = 1
    while i < sheet1.nrows:
        #取本行指令的操作类型
        cmdType = sheet1.row(i)[0]
        if cmdType.value == 1.0:
            #取图片名称
            img = sheet1.row(i)[1].value
            reTry = 1
            if sheet1.row(i)[2].ctype == 2 and sheet1.row(i)[2].value != 0:
                reTry = sheet1.row(i)[2].value
            mouseClick(1, "left", img, reTry)
            print("单击左键", img)
        #2代表双击左键
        elif cmdType.value == 2.0:
            #取图片名称
            img = sheet1.row(i)[1].value
            #取重试次数
            reTry = 1
            if sheet1.row(i)[2].ctype == 2 and sheet1.row(i)[2].value != 0:
                reTry = sheet1.row(i)[2].value
            mouseClick(2, "left", img, reTry)
            print("双击左键", img)
        #3代表右键
        elif cmdType.value == 3.0:
            #取图片名称
            img = sheet1.row(i)[1].value
            #取重试次数
            reTry = 1
            if sheet1.row(i)[2].ctype == 2 and sheet1.row(i)[2].value != 0:
                reTry = sheet1.row(i)[2].value
            mouseClick(1, "right", img, reTry)
            print("右键", img)
        #4代表进行一次会话，一次会话维持100s
        elif cmdType.value == 4.0:
            # 初始化聊天机器人
            conversation_bot = ConversationBot(config, None, None)
            first_chat = True
            # 获取当前屏幕的尺寸
            width, height = pyautogui.size()
            t = 0
            while t < 100:
                response = None

                if first_chat:
                    first_chat = False
                    response = '你好，我的主人现在不在使用微信，我是一个人工智能，我可以在能力范围内陪你聊天，或者回答你的一些问题。请注意，因为我的主人是个笨蛋，所以我只能读懂单行文字，而且不能一次性读取多条消息。我的记忆大概有100s左右，如果100s左右没收到你的消息，那么我会忘了我们曾经聊过天。那么，让我们开始对话吧。'

                else:
                    # 寻找聊天气泡的位置
                    box = pyautogui.locateOnScreen('imgs/bubble.png',
                                                   confidence=0.85,
                                                   region=(0, 0, width,
                                                           height))
                    if box:
                        # 截取屏幕左上角 (a, b) 到右下角 (c, d) 的区域
                        screenshot = pyautogui.screenshot(region=(box.left,
                                                                  box.top,
                                                                  width,
                                                                  box.height))
                        # 使用 pytesseract 库识别图像中的文字
                        text = pytesseract.image_to_string(screenshot,
                                                           lang='chi_sim')
                        print('识别内容为：', text)
                        try:
                            conversation_bot.action(text)
                            response = conversation_bot.response
                        except Exception:
                            response = '糟糕，我的大脑暂时无法工作了，可能是 OpenAI 那边出了一些问题~我没法和你聊天啦！如果你继续和我讲话，我可能随机给你讲个笑话或者段子。'
                        # 输出识别结果
                        print('回复内容为：', response)

                if response:
                    # 发送识别结果:
                    pyperclip.copy(response)
                    location = pyautogui.locateCenterOnScreen('imgs/send.png',
                                                              confidence=0.9)
                    if location is not None:
                        t = 0
                        pyautogui.hotkey('ctrl', 'v')
                        pyautogui.click(location.x,
                                        location.y,
                                        clicks=1,
                                        interval=0.2,
                                        duration=0.2,
                                        button='left')
                    else:
                        print('没有找到发送按钮，出错了')
                print(f'还有{100-t}s关闭会话')
                t += 1
                time.sleep(1)

        #5代表等待
        elif cmdType.value == 5.0:
            #取图片名称
            waitTime = sheet1.row(i)[1].value
            time.sleep(waitTime)
            print("等待", waitTime, "秒")
        #6代表滚轮
        elif cmdType.value == 6.0:
            #取图片名称
            scroll = sheet1.row(i)[1].value
            pyautogui.scroll(int(scroll))
            print("滚轮滑动", int(scroll), "距离")
        #7代表进行一次判断是否单击
        elif cmdType.value == 7.0:
            #取图片名称
            img = sheet1.row(i)[1].value
            mouseClick(1, "left", img, 0)
            print("单击左键", img)
        i += 1


if __name__ == '__main__':
    file = 'cmd/cmd.xls'
    #打开文件
    wb = xlrd.open_workbook(filename=file)
    #通过索引获取表格sheet页
    sheet1 = wb.sheet_by_index(0)
    print('欢迎使用自动回复机器人~')
    #数据检查
    checkCmd = dataCheck(sheet1)
    if checkCmd:
        key = input('选择功能: 1.只回复一次 2.循环回复 \n')
        if key == '1':
            #循环拿出每一行指令
            mainWork(sheet1)
        elif key == '2':
            while True:
                mainWork(sheet1)
                time.sleep(0.1)
                print("等待0.1秒")
    else:
        print('输入有误或者已经退出!')
