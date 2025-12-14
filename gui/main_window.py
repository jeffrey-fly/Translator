# ------------------------------
# main_window.py
"""
主窗口：Qt 翻译软件界面（仅 UI，不包含具体翻译实现）
"""
from services.translation.google_service import translate_text
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel,
    QComboBox,
    QMessageBox,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Translator")
        self.resize(800, 500)

        central = QWidget(self)
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        # 顶部：语言选择
        lang_layout = QHBoxLayout()
        main_layout.addLayout(lang_layout)

        self.src_lang = QComboBox()
        self.src_lang.addItems(["Auto", "English", "Chinese", "Japanese"])

        self.dst_lang = QComboBox()
        self.dst_lang.addItems(["Chinese", "English", "Japanese"])

        lang_layout.addWidget(QLabel("From:"))
        lang_layout.addWidget(self.src_lang)
        lang_layout.addWidget(QLabel("To:"))
        lang_layout.addWidget(self.dst_lang)
        lang_layout.addStretch()

        # 中间：输入 / 输出文本框
        text_layout = QHBoxLayout()
        main_layout.addLayout(text_layout, stretch=1)

        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText("Enter text to translate...")

        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)
        self.output_edit.setPlaceholderText("Translation result...")

        text_layout.addWidget(self.input_edit)
        text_layout.addWidget(self.output_edit)

        # 底部：按钮
        btn_layout = QHBoxLayout()
        main_layout.addLayout(btn_layout)

        self.translate_btn = QPushButton("Translate")
        self.clear_btn = QPushButton("Clear")

        btn_layout.addStretch()
        btn_layout.addWidget(self.translate_btn)
        btn_layout.addWidget(self.clear_btn)

        # 信号连接
        self.translate_btn.clicked.connect(self.on_translate)
        self.clear_btn.clicked.connect(self.on_clear)

    def on_translate(self):
        """
        翻译按钮回调（当前为占位实现）
        后续可在这里接入 OpenAI / Google / 本地模型
        """
        text = self.input_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Warning", "Input text is empty")
            return

        src = self.src_lang.currentText()
        dst = self.dst_lang.currentText()

        # TODO: 替换为真实翻译逻辑
        result = translate_text(text, target_language=dst)
        # result = f"[Mock Translation]\nFrom: {src} -> To: {dst}\n\n{text}"

        self.output_edit.setPlainText(result)

    def on_clear(self):
        self.input_edit.clear()
        self.output_edit.clear()
