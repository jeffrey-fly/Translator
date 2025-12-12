#
# class MainWindow(QMainWindow):
#     def __init__(self, translation_service):
#         super().__init__()
#         self.translator = translation_service
#
#     def on_translate_clicked(self):
#         text = self.text_input.toPlainText()
#         result = self.translator.translate(text)
#         self.result_area.setPlainText(result)