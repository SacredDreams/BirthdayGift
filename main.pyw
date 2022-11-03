from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import webbrowser
import time

class main:
    def __init__(self):
        """
        设置初始值、属性、变量
        """
        self.main_ui = None                                                         # 主窗口
        self.help_ui = None                                                         # 帮助窗口
        self.birthday_ui = None                                                     # 生日图片窗口
        self.result = None                                                           # 确认是否结束进程的结果
        self.count = 0                                                              # 点击“打开”按钮累计的次数
        self.condition = 15                                                         # 设置需要点击“打开”按钮的次数
        self.state = False                                                          # 为False时，不更换pushButton_3的链接
        self.url = "https://github.com/SacredDreams/BirthdayGift"                   # 项目地址
        self.logs_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())           # 获取日志文件的名称信息
        self.logs_output_list = []                                                  # help页面中读取本地日志信息生成的列表
        self.main_ui = QUiLoader().load("resources\\ui\\main.ui")                   # 加载主页面
        self.main_ui.pushButton.clicked.connect(self.turn_to_page_2)                # “开始”按钮，链接第二页
        self.main_ui.pushButton_2.clicked.connect(self.help)                        # “帮助”按钮，启动帮助窗口
        self.main_ui.pushButton_8.clicked.connect(self.turn_to_page_1)              # “上一页”按钮，切换至第一页
        self.main_ui.pushButton_8.setEnabled(False)                                 # “上一页”按钮，禁用
        self.build_connects()                                                       # 与“操作页面”的scrollArea的所有按钮建立连接

        # 绘制窗口弧角（main_ui）
        self.bmp = QBitmap(900, 600)
        self.bmp.fill()
        self.Painter = QPainter(self.bmp)
        self.Painter.setPen(Qt.NoPen)
        self.Painter.setBrush(Qt.black)
        self.Painter.drawRoundedRect(self.bmp.rect(), 10, 10)
        self.main_ui.setMask(self.bmp)

        # 绘制窗口阴影（main_ui）
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setOffset(10, 10)         # 设置偏移量
        self.shadow.setBlurRadius(20)       # 设置阴影半径
        self.shadow.setColor(Qt.black)       # 设置阴影颜色
        self.main_ui.setGraphicsEffect(self.shadow)

        with open("resources\\ClickTimes", "r") as file:                            # 从ClickTimes文件中读出需要点击“打开”按钮的次数
            self.condition = int(file.readlines()[0])

        with open("logs\\%s" % self.logs_time, "a") as file:                        # 创建并写入日志
            file.write("[%s] Start running..." % time.strftime("%H:%M:%S", time.localtime()))         # 程序开始执行
            file.write("\n[%s] Building connects..." % time.strftime("%H:%M:%S", time.localtime()))   # 连接PushButtons
            file.write("\n[%s] Loaded main window..." % time.strftime("%H:%M:%S", time.localtime()))  # 已加载主窗口

    def help(self):
        """
        帮助页面的窗口
        """
        self.help_ui = QUiLoader().load("resources\\ui\\help.ui")
        self.help_ui.show()
        with open("logs\\%s" % self.logs_time, "a") as file:                                          # 写入日志
            file.write("\n[%s] Loaded help window..." % time.strftime("%H:%M:%S", time.localtime()))  # 已加载主窗口
        with open("logs\\%s" % self.logs_time, "r") as file:                        # 读取日志
            self.logs_output_list = file.readlines()                                       # 存入日志列表
            for i in self.logs_output_list:
                self.help_ui.textEdit.append(i.replace("\n", ""))                   # 输出日志
        self.help_ui.pushButton.clicked.connect(self.tip)                           # “获取更多信息”按钮，其实是提示
        self.help_ui.pushButton_2.clicked.connect(self.open_url)                    # “打开项目地址”按钮，浏览器中打开
        self.help_ui.pushButton_3.clicked.connect(self.close_windows)               # “结束程序”按钮，关闭所有窗口

    def birthday(self):
        """
        生日贺卡页面
        """
        self.birthday_ui = QUiLoader().load("resources\\ui\\birthday.ui")
        self.birthday_ui.show()
        # 绘制窗口弧角（birthday_ui）
        self.birthday_ui.setMask(self.bmp)

        with open("logs\\%s" % self.logs_time, "a") as file:        # 写入日志
            file.write(
                "\n[%s] Loaded birthday window..."
                % time.strftime("%H:%M:%S", time.localtime())
            )                                                       # 已加载birthday

            try:                                                    # 将日志添加到输出
                self.help_ui.textEdit.append(
                    "[%s] Loaded birthday window..."
                    % time.strftime("%H:%M:%S", time.localtime())
                )
            except AttributeError:
                pass

    def turn_to_page_1(self):
        """
        切换到首页
        """
        self.main_ui.pushButton_8.setEnabled(False)                                 # “上一页”按钮，禁用
        self.main_ui.stackedWidget.setCurrentIndex(0)                               # 切换至第一页，index=0

        with open("logs\\%s" % self.logs_time, "a") as file:                                          # 写入日志
            file.write("\n[%s] Switched to page 1..." % time.strftime("%H:%M:%S", time.localtime()))  # 已切换至第一页

        try:                                                                                          # 将日志添加到输出
            self.help_ui.textEdit.append(
                "[%s] Switched to page 1..."
                % time.strftime("%H:%M:%S", time.localtime())
            )
        except AttributeError:
            pass

    def turn_to_page_2(self):
        """
        切换到执行页面，即第二页
        """
        self.main_ui.pushButton_8.setEnabled(True)                                  # “上一页”按钮，启用
        self.main_ui.stackedWidget.setCurrentIndex(1)                               # 切换至第二页，index=1

        with open("logs\\%s" % self.logs_time, "a") as file:                                           # 写入日志
            file.write("\n[%s] Switched to page 2..." % time.strftime("%H:%M:%S", time.localtime()))   # 已切换至第二页

        try:                                                                                           # 将日志添加到输出
            self.help_ui.textEdit.append(
                "[%s] Switched to page 2..."
                % time.strftime("%H:%M:%S", time.localtime())
            )
        except AttributeError:
            pass

    def close_windows(self):
        """
        帮助中“结束进程”按钮的执行内容
        """
        self.result = QMessageBox.question(self.help_ui, "提示", "你确认要结束此进程吗？")
        if str(self.result) == "PySide2.QtWidgets.QMessageBox.StandardButton.Yes":            # 判断用户点击yes或no

            with open("logs\\%s" % self.logs_time, "a") as file:                              # 写入日志
                file.write(
                    "\n[%s] Exited... (main > close_windows)"
                    % time.strftime("%H:%M:%S", time.localtime())
                )                                                                             # 程序结束运行

            try:                                                                              # 将日志添加到输出
                self.help_ui.textEdit.append(
                    "[%s] Exited... (main > close_windows)"
                    % time.strftime("%H:%M:%S", time.localtime())
                )
            except AttributeError:
                pass

            time.sleep(1)

            self.main_ui.close()
            self.help_ui.close()
            try:
                self.birthday_ui.close()
            except AttributeError:
                pass

    def open_url(self):
        """
        打开项目链接
        """
        webbrowser.open(self.url)

        with open("logs\\%s" % self.logs_time, "a") as file:                                      # 写入日志
            file.write("\n[%s] Url has opened..." % time.strftime("%H:%M:%S", time.localtime()))  # 成功打开项目链接地址

        try:                                                                                      # 将日志添加到输出
            self.help_ui.textEdit.append(
                "[%s] Url has opened..."
                % time.strftime("%H:%M:%S", time.localtime())
            )
        except AttributeError:
            pass

    def tip(self):
        """
        帮助页面中“显示更多帮助”的按钮显示的内容
        """
        QMessageBox.information(self.help_ui, "提示", " 举  “头”  望  “明月”  ......    ")        # 帮助窗口中的提示

        with open("logs\\%s" % self.logs_time, "a") as file:                                       # 写入日志
            file.write("\n[%s] Clue has showed..." % time.strftime("%H:%M:%S", time.localtime()))  # 提示已显示

        try:                                                                                       # 将日志添加到输出
            self.help_ui.textEdit.append(
                "[%s] Clue has showed..."
                % time.strftime("%H:%M:%S", time.localtime())
            )
        except AttributeError:
            pass

    def sum(self):
        """
        此方法为 除了可以 改变为“明月”的按钮 所调用的方法，点击除了“明月”以外的所有按钮都会连接到这里
        """
        if self.state is False:                           # 判断是否为False，False则不允许切入birthday页面
            self.count += 1                               # 每点击一次就将self.count加1

            with open("logs\\%s" % self.logs_time, "a") as file:                                        # 写入日志
                file.write(
                    "\n[%s] Clicked PushButton %s/%s..."
                    % (time.strftime("%H:%M:%S", time.localtime()), self.count, self.condition)
                )                                                                                       # 点击次数/总次数

            try:                                                                                        # 将日志添加到输出
                self.help_ui.textEdit.append(
                    "[%s] Clicked PushButton %s/%s..."
                    % (time.strftime("%H:%M:%S", time.localtime()), self.count, self.condition)
                )
            except AttributeError:
                pass

            if self.count == self.condition:              # 设置self.count的最大值为ClickTimes文件中的值
                self.state = True                         # 允许切入birthday的页面
                self.main_ui.pushButton_3.setText("明月")  # 将第一行第一个“打开”按钮设置成“明月”，提示见上↑

                with open("logs\\%s" % self.logs_time, "a") as file:    # 写入日志
                    file.write(
                        "\n[%s] State has transformed into True..."
                        % time.strftime("%H:%M:%S", time.localtime())
                    )                                                   # 已加载主窗口
                    file.write(
                        "\n[%s] PushButton has modified..."
                        % time.strftime("%H:%M:%S", time.localtime())
                    )                                                   # 修改PushButton

                try:                                                    # 将日志添加到输出
                    self.help_ui.textEdit.append(
                        "[%s] State has transformed into True..."
                        % time.strftime("%H:%M:%S", time.localtime())
                    )
                    self.help_ui.textEdit.append(
                        "[%s] PushButton has modified..."
                        % time.strftime("%H:%M:%S", time.localtime())
                    )
                except AttributeError:
                    pass

            if self.count == self.condition / 2:          # 当self.count为ClickTimes文件中值的一半时，显示提示
                self.main_ui.label_4.setText("找找有没有提示~")

                with open("logs\\%s" % self.logs_time, "a") as file:                                         # 写入日志
                    file.write("\n[%s] Text has modified..." % time.strftime("%H:%M:%S", time.localtime()))  # 修改Label

                try:                                                                                     # 将日志添加到输出
                    self.help_ui.textEdit.append(
                        "[%s] Text has modified..."
                        % time.strftime("%H:%M:%S", time.localtime())
                    )
                except AttributeError:
                    pass

    def sum_(self):
        """
        此方法为 可以 改变为“明月”的按钮 所调用的方法，只有点击“明月”按钮才会链接到这里并进入birthday页面
        """
        if self.count == self.condition:
            self.main_ui.close()
            self.birthday()

            with open("logs\\%s" % self.logs_time, "a") as file:            # 写入日志
                file.write(
                    "\n[%s] Main window has closed... (main > sum_)"
                    % time.strftime("%H:%M:%S", time.localtime())
                )                                                           # 已加载主窗口

            try:                                                            # 将日志添加到输出
                self.help_ui.textEdit.append(
                    "[%s] Main window has closed... (main > sum_)"
                    % time.strftime("%H:%M:%S", time.localtime())
                )
            except AttributeError:
                pass

        else:
            self.sum()

    def build_connects(self):                                           # 给所有“打开”按钮建立链接
        """
        与操作页面中scrollArea中的所有按钮建立连接
        """
        self.main_ui.pushButton_3.clicked.connect(self.sum_)
        self.main_ui.pushButton_4.clicked.connect(self.sum)
        self.main_ui.pushButton_5.clicked.connect(self.sum)
        self.main_ui.pushButton_6.clicked.connect(self.sum)
        self.main_ui.pushButton_7.clicked.connect(self.sum)
        # 此处 pushButton编号 非连续
        self.main_ui.pushButton_98.clicked.connect(self.sum)
        self.main_ui.pushButton_99.clicked.connect(self.sum)
        self.main_ui.pushButton_100.clicked.connect(self.sum)
        self.main_ui.pushButton_101.clicked.connect(self.sum)
        self.main_ui.pushButton_102.clicked.connect(self.sum)
        self.main_ui.pushButton_103.clicked.connect(self.sum)
        self.main_ui.pushButton_104.clicked.connect(self.sum)
        self.main_ui.pushButton_105.clicked.connect(self.sum)
        self.main_ui.pushButton_106.clicked.connect(self.sum)
        self.main_ui.pushButton_107.clicked.connect(self.sum)
        self.main_ui.pushButton_108.clicked.connect(self.sum)
        self.main_ui.pushButton_109.clicked.connect(self.sum)
        self.main_ui.pushButton_110.clicked.connect(self.sum)
        self.main_ui.pushButton_111.clicked.connect(self.sum)
        self.main_ui.pushButton_112.clicked.connect(self.sum)
        self.main_ui.pushButton_113.clicked.connect(self.sum)
        self.main_ui.pushButton_114.clicked.connect(self.sum)
        self.main_ui.pushButton_115.clicked.connect(self.sum)
        self.main_ui.pushButton_116.clicked.connect(self.sum)
        self.main_ui.pushButton_117.clicked.connect(self.sum)
        self.main_ui.pushButton_118.clicked.connect(self.sum)
        self.main_ui.pushButton_119.clicked.connect(self.sum)
        self.main_ui.pushButton_120.clicked.connect(self.sum)
        self.main_ui.pushButton_121.clicked.connect(self.sum)
        self.main_ui.pushButton_122.clicked.connect(self.sum)
        self.main_ui.pushButton_123.clicked.connect(self.sum)
        self.main_ui.pushButton_124.clicked.connect(self.sum)
        self.main_ui.pushButton_125.clicked.connect(self.sum)
        self.main_ui.pushButton_126.clicked.connect(self.sum)
        self.main_ui.pushButton_127.clicked.connect(self.sum)
        self.main_ui.pushButton_128.clicked.connect(self.sum)
        self.main_ui.pushButton_129.clicked.connect(self.sum)
        self.main_ui.pushButton_130.clicked.connect(self.sum)
        self.main_ui.pushButton_131.clicked.connect(self.sum)
        self.main_ui.pushButton_132.clicked.connect(self.sum)
        self.main_ui.pushButton_133.clicked.connect(self.sum)
        self.main_ui.pushButton_134.clicked.connect(self.sum)
        self.main_ui.pushButton_135.clicked.connect(self.sum)
        self.main_ui.pushButton_136.clicked.connect(self.sum)
        self.main_ui.pushButton_137.clicked.connect(self.sum)
        self.main_ui.pushButton_138.clicked.connect(self.sum)
        self.main_ui.pushButton_139.clicked.connect(self.sum)
        self.main_ui.pushButton_140.clicked.connect(self.sum)
        self.main_ui.pushButton_141.clicked.connect(self.sum)
        self.main_ui.pushButton_142.clicked.connect(self.sum)
        self.main_ui.pushButton_143.clicked.connect(self.sum)
        self.main_ui.pushButton_144.clicked.connect(self.sum)
        self.main_ui.pushButton_145.clicked.connect(self.sum)
        self.main_ui.pushButton_146.clicked.connect(self.sum)
        self.main_ui.pushButton_147.clicked.connect(self.sum)
        self.main_ui.pushButton_148.clicked.connect(self.sum)
        self.main_ui.pushButton_149.clicked.connect(self.sum)
        self.main_ui.pushButton_150.clicked.connect(self.sum)
        self.main_ui.pushButton_151.clicked.connect(self.sum)
        self.main_ui.pushButton_152.clicked.connect(self.sum)
        self.main_ui.pushButton_153.clicked.connect(self.sum)
        self.main_ui.pushButton_154.clicked.connect(self.sum)
        self.main_ui.pushButton_155.clicked.connect(self.sum)
        self.main_ui.pushButton_156.clicked.connect(self.sum)
        self.main_ui.pushButton_157.clicked.connect(self.sum)
        self.main_ui.pushButton_158.clicked.connect(self.sum)
        self.main_ui.pushButton_159.clicked.connect(self.sum)
        self.main_ui.pushButton_160.clicked.connect(self.sum)
        self.main_ui.pushButton_161.clicked.connect(self.sum)
        self.main_ui.pushButton_162.clicked.connect(self.sum)
        self.main_ui.pushButton_163.clicked.connect(self.sum)
        self.main_ui.pushButton_164.clicked.connect(self.sum)
        self.main_ui.pushButton_165.clicked.connect(self.sum)
        self.main_ui.pushButton_166.clicked.connect(self.sum)
        self.main_ui.pushButton_167.clicked.connect(self.sum)
        self.main_ui.pushButton_168.clicked.connect(self.sum)
        self.main_ui.pushButton_169.clicked.connect(self.sum)
        self.main_ui.pushButton_170.clicked.connect(self.sum)
        self.main_ui.pushButton_171.clicked.connect(self.sum)
        self.main_ui.pushButton_172.clicked.connect(self.sum)
        self.main_ui.pushButton_173.clicked.connect(self.sum)
        self.main_ui.pushButton_174.clicked.connect(self.sum)
        self.main_ui.pushButton_175.clicked.connect(self.sum)
        self.main_ui.pushButton_176.clicked.connect(self.sum)
        self.main_ui.pushButton_177.clicked.connect(self.sum)
        self.main_ui.pushButton_178.clicked.connect(self.sum)
        self.main_ui.pushButton_179.clicked.connect(self.sum)
        self.main_ui.pushButton_180.clicked.connect(self.sum)
        self.main_ui.pushButton_181.clicked.connect(self.sum)
        self.main_ui.pushButton_182.clicked.connect(self.sum)
        self.main_ui.pushButton_183.clicked.connect(self.sum)
        self.main_ui.pushButton_184.clicked.connect(self.sum)
        self.main_ui.pushButton_185.clicked.connect(self.sum)
        self.main_ui.pushButton_186.clicked.connect(self.sum)
        self.main_ui.pushButton_187.clicked.connect(self.sum)
        self.main_ui.pushButton_188.clicked.connect(self.sum)
        self.main_ui.pushButton_189.clicked.connect(self.sum)
        self.main_ui.pushButton_190.clicked.connect(self.sum)
        self.main_ui.pushButton_191.clicked.connect(self.sum)
        self.main_ui.pushButton_192.clicked.connect(self.sum)
        self.main_ui.pushButton_193.clicked.connect(self.sum)
        self.main_ui.pushButton_194.clicked.connect(self.sum)
        self.main_ui.pushButton_195.clicked.connect(self.sum)
        self.main_ui.pushButton_196.clicked.connect(self.sum)
        self.main_ui.pushButton_197.clicked.connect(self.sum)
        self.main_ui.pushButton_198.clicked.connect(self.sum)
        self.main_ui.pushButton_199.clicked.connect(self.sum)
        self.main_ui.pushButton_200.clicked.connect(self.sum)
        self.main_ui.pushButton_201.clicked.connect(self.sum)
        self.main_ui.pushButton_202.clicked.connect(self.sum)
        self.main_ui.pushButton_203.clicked.connect(self.sum)
        self.main_ui.pushButton_204.clicked.connect(self.sum)
        self.main_ui.pushButton_205.clicked.connect(self.sum)
        self.main_ui.pushButton_206.clicked.connect(self.sum)
        self.main_ui.pushButton_207.clicked.connect(self.sum)
        self.main_ui.pushButton_208.clicked.connect(self.sum)
        self.main_ui.pushButton_209.clicked.connect(self.sum)
        self.main_ui.pushButton_210.clicked.connect(self.sum)
        self.main_ui.pushButton_211.clicked.connect(self.sum)
        self.main_ui.pushButton_212.clicked.connect(self.sum)
        # 此处 pushButton编号 非连续
        self.main_ui.pushButton_218.clicked.connect(self.sum)
        self.main_ui.pushButton_219.clicked.connect(self.sum)
        self.main_ui.pushButton_220.clicked.connect(self.sum)
        self.main_ui.pushButton_221.clicked.connect(self.sum)
        self.main_ui.pushButton_222.clicked.connect(self.sum)
        self.main_ui.pushButton_223.clicked.connect(self.sum)
        self.main_ui.pushButton_224.clicked.connect(self.sum)
        self.main_ui.pushButton_225.clicked.connect(self.sum)
        self.main_ui.pushButton_226.clicked.connect(self.sum)
        self.main_ui.pushButton_227.clicked.connect(self.sum)
        self.main_ui.pushButton_228.clicked.connect(self.sum)
        self.main_ui.pushButton_229.clicked.connect(self.sum)
        self.main_ui.pushButton_230.clicked.connect(self.sum)
        self.main_ui.pushButton_231.clicked.connect(self.sum)
        self.main_ui.pushButton_232.clicked.connect(self.sum)
        self.main_ui.pushButton_233.clicked.connect(self.sum)
        self.main_ui.pushButton_234.clicked.connect(self.sum)
        self.main_ui.pushButton_235.clicked.connect(self.sum)
        self.main_ui.pushButton_236.clicked.connect(self.sum)
        self.main_ui.pushButton_237.clicked.connect(self.sum)
        self.main_ui.pushButton_238.clicked.connect(self.sum)
        self.main_ui.pushButton_239.clicked.connect(self.sum)
        self.main_ui.pushButton_240.clicked.connect(self.sum)
        self.main_ui.pushButton_241.clicked.connect(self.sum)
        self.main_ui.pushButton_242.clicked.connect(self.sum)
        self.main_ui.pushButton_243.clicked.connect(self.sum)
        self.main_ui.pushButton_244.clicked.connect(self.sum)
        self.main_ui.pushButton_245.clicked.connect(self.sum)
        self.main_ui.pushButton_246.clicked.connect(self.sum)
        self.main_ui.pushButton_247.clicked.connect(self.sum)

if __name__ == "__main__":
    app = QApplication()
    main = main()           # 实例化main类
    main.main_ui.show()     # 最先显示主窗口main_ui
    app.exec_()