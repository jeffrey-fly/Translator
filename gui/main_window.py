# ------------------------------
# main_window.py
"""
主窗口：Qt 翻译软件界面
"""
from PySide6.QtCore import QTranslator

from gui.config_window import TranslatorConfigWindow, load_json_config, KeyStore

from PySide6.QtGui import QAction
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

from services.translation.google_service import GoogleTranslator
from utils.constants import (
    PROVIDER_OPENAI,
    PROVIDER_GOOGLE,
    PROVIDER_DEEPSEEK
)

from utils.provider import ProviderManager, provider_manager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Translator")
        self.resize(800, 500)

        # 创建菜单栏
        menu_bar = self.menuBar()

        # 添加一个“配置”菜单
        config_menu = menu_bar.addMenu("配置")

        # 创建一个菜单动作
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.open_settings)

        # 添加到菜单
        config_menu.addAction(settings_action)

        config_menu.addSeparator()
        config_menu.addAction("退出", self.close)

        self.config_window = None

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

        self.provider_manager = ProviderManager()
        self.json_config_data = load_json_config()
        for p in provider_manager.providers.values():
            enable = self.json_config_data.get(p.name, False)
            if enable:
                p.enable()
            else:
                p.disable()
        self.translator = None

    def open_settings(self):
        if self.config_window is None:
            self.config_window = TranslatorConfigWindow()

        self.config_window.show()
        self.config_window.raise_()  # 提到最前
        self.config_window.activateWindow()  # 获取焦点

    def on_translate(self):
        """
        翻译按钮回调（当前为占位实现）
        后续可在这里接入 OpenAI / Google / 本地模型
        """
        providers_name = provider_manager.enabled_providers()
        first_provider = providers_name[0] if providers_name else None
        if not first_provider:
            QMessageBox.warning(self, "Warning", "please config first")
            return

        if not self.translator:
            if first_provider == PROVIDER_GOOGLE:
                self.translator = GoogleTranslator(provider_manager.get_provider(PROVIDER_GOOGLE).key)

        if not self.translator:
            QMessageBox.warning(self, "Warning", "no provider")
            return

        text = self.input_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Warning", "Input text is empty")
            return

        src = self.src_lang.currentText()
        dst = self.dst_lang.currentText()

        # TODO: 替换为真实翻译逻辑
        # result = translate_text(text, dst, src)
        result = self.translator.translate(text, dst, src)

        self.output_edit.setPlainText(result)

    def on_clear(self):
        self.input_edit.clear()
        self.output_edit.clear()
