import sys
import json
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QStackedWidget, QFormLayout, QLineEdit, QCheckBox,
    QPushButton, QMessageBox
)

from utils.constants import (
    PROVIDER_OPENAI,
    PROVIDER_GOOGLE,
    PROVIDER_DEEPSEEK
)

from utils.helper import KeyStore
from utils.provider import provider_manager

CONFIG_FILE = "translator_config.json"


class ModelConfigPage(QWidget):
    """单个模型的配置页"""
    def __init__(self, model_name: str, config_data: dict):
        super().__init__()
        self.model_name = model_name
        self.config_data = config_data

        layout = QVBoxLayout(self)

        # 是否启用
        self.enable_cb = QCheckBox(f"启用 {model_name}")
        layout.addWidget(self.enable_cb)

        # API Key 输入框
        form = QFormLayout()
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setMinimumWidth(300)
        form.addRow("API Key:", self.api_key_input)
        layout.addLayout(form)

        layout.addStretch()

        # 保存按钮
        self.save_btn = QPushButton("保存配置")
        self.save_btn.clicked.connect(self.save_config)
        layout.addWidget(self.save_btn)

        self.load_config()

    def load_config(self):
        # 从 JSON 读取启用状态
        self.enable_cb.setChecked(self.config_data.get(self.model_name, False))
        # 从 Keyring 读取 API Key
        api_key = KeyStore.get_key(self.model_name)
        if api_key:
            self.api_key_input.setText(api_key)

    def save_config(self):
        # 保存启用状态到 JSON
        self.config_data[self.model_name] = self.enable_cb.isChecked()
        save_json_config(self.config_data)

        # 保存 API Key 到 Keyring
        api_key = self.api_key_input.text().strip()
        if api_key:
            KeyStore.set_key(self.model_name, api_key)
        if self.config_data[self.model_name]:
            provider_manager.get_provider(self.model_name).enable()
        else:
            provider_manager.get_provider(self.model_name).disable()
        QMessageBox.information(self, "保存成功", f"{self.model_name} 配置已保存")


def load_json_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_json_config(data: dict):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("保存 JSON 配置失败:", e)


class TranslatorConfigWindow(QWidget):
    """主配置窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("翻译服务配置")
        self.resize(600, 250)

        # 加载 JSON 配置
        self.config_data = load_json_config()

        main_layout = QHBoxLayout(self)

        # 左侧模型选择列表
        self.model_list = QListWidget()
        self.model_names = [PROVIDER_GOOGLE, PROVIDER_OPENAI, PROVIDER_DEEPSEEK]
        self.model_list.addItems(self.model_names)
        main_layout.addWidget(self.model_list)

        # 右侧堆叠页面
        self.pages = QStackedWidget()
        self.model_pages = {}
        for name in self.model_names:
            page = ModelConfigPage(name, self.config_data)
            self.model_pages[name] = page
            self.pages.addWidget(page)
        main_layout.addWidget(self.pages)

        # 左右联动
        self.model_list.currentRowChanged.connect(self.pages.setCurrentIndex)
        # 默认选中第一个模型
        default_index = 0
        self.model_list.setCurrentRow(default_index)
