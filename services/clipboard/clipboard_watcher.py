

class ClipboardWatcher(QObject):
    textChanged = pyqtSignal(str)

    def __init__(self, app):
        super().__init__()
        self.clipboard = app.clipboard()
        self.clipboard.dataChanged.connect(self.on_change)

    def on_change(self):
        text = self.clipboard.text()
        self.textChanged.emit(text)