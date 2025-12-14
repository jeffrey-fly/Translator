# from google import genai
#
# def main():
#     client = genai.Client()
#
#     response = client.models.generate_content(
#         model="gemini-2.5-flash", contents="翻译：hello,how are you?"
#     )
#     print(response.text)
#
# if __name__ == '__main__':
#     print("hello world")
#     main()

# app.py
"""
程序入口：负责创建 QApplication 并启动主窗口
"""
from services.translation.google_service import translate_text

import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # main()

    translated = translate_text("run", target_language="zh")
    print(translated)

