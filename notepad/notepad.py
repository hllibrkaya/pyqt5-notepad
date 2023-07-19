import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPlainTextEdit, QToolBar, QVBoxLayout, \
    QAction, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFontDatabase, QIcon, QKeySequence
from PyQt5.QtPrintSupport import QPrintDialog


class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("./icons/notepad.ico"))
        self.screen_width, self.screen_height = self.geometry().width(), self.geometry().height()
        self.resize(self.screen_width * 3, self.screen_height * 3)

        self.filter_types = "Text Document (*.txt);; Python (*.py);; Markdown(*.md);; Html(*.html)"
        self.path = None

        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixed_font.setPointSize(12)

        main_layout = QVBoxLayout()

        # editor
        self.editor = QPlainTextEdit()
        self.editor.setFont(fixed_font)
        main_layout.addWidget(self.editor)

        # status bar
        self.status_bar = self.statusBar()

        # app container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # file menu
        # ************************
        file_menu = self.menuBar().addMenu("&File")

        # file toolbar
        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(100, 100))
        self.addToolBar(Qt.BottomToolBarArea, file_toolbar)

        # open, save, save as, print options
        open_file_action = self.create_action(self, "./icons/file_open.ico", "Open", "Open File",
                                              self.file_open)
        open_file_action.setShortcut(QKeySequence.Open)  # these are default shortcuts that module provided

        save_file_action = self.create_action(self, "./icons/save.ico", "Save", "Save File",
                                              self.file_save)
        save_file_action.setShortcut(QKeySequence.Save)

        save_file_as_action = self.create_action(self, "./icons/save_as.ico", "Save As", "Save File As",
                                                 self.file_save_as)
        save_file_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))

        print_action = self.create_action(self, "./icons/printer.ico", "Print", "Print File",
                                          self.print_file)
        print_action.setShortcut(QKeySequence.Print)

        file_menu.addActions([open_file_action, save_file_action, save_file_as_action, print_action])
        file_toolbar.addActions([open_file_action, save_file_action, save_file_as_action, print_action])

        # *******************

        # edit menu
        edit_menu = self.menuBar().addMenu("&Edit")

        # edit toolbar
        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(100, 100))
        self.addToolBar(Qt.BottomToolBarArea, edit_toolbar)

        # undo, redo, clear actions
        undo_action = self.create_action(self, "./icons/undo.ico", "Undo", "Undo", self.editor.undo)
        undo_action.setShortcut(QKeySequence.Undo)

        redo_action = self.create_action(self, "./icons/redo.ico", "Redo", "Redo", self.editor.redo)
        redo_action.setShortcut(QKeySequence.Redo)

        clear_action = self.create_action(self, "./icons/clear.ico", "Clear", "Clear",
                                          self.clear_contents)
        clear_action.setShortcut(QKeySequence("Ctrl+L"))
        edit_menu.addActions([undo_action, redo_action, clear_action])
        edit_toolbar.addActions([undo_action, redo_action, clear_action])

        edit_menu.addSeparator()
        edit_toolbar.addSeparator()

        # cut, copy, select all
        cut_action = self.create_action(self, "./icons/cut.ico", "Cut", "Cut", self.editor.cut)
        cut_action.setShortcut(QKeySequence.Cut)

        copy_action = self.create_action(self, "./icons/copy.ico", "Copy", "Copy", self.editor.copy)
        copy_action.setShortcut(QKeySequence.Copy)

        paste_action = self.create_action(self, "./icons/paste.ico", "Paste", "Paste", self.editor.paste)
        paste_action.setShortcut(QKeySequence.Paste)

        select_all_action = self.create_action(self, "./icons/select_all.ico", "Select All", "Select All",
                                               self.editor.selectAll)
        select_all_action.setShortcut(QKeySequence.SelectAll)

        edit_menu.addActions([cut_action, copy_action, paste_action, select_all_action])
        edit_toolbar.addActions([cut_action, copy_action, paste_action, select_all_action])

        edit_menu.addSeparator()
        edit_toolbar.addSeparator()

        # wrap text, screenshot actions
        wrap_text_action = self.create_action(self, "./icons/wrap_text.ico", "Wrap Text", "Wrap Text", self.wrap_text)
        wrap_text_action.setShortcut(QKeySequence("Ctrl+Alt+X"))
        screenshot_action = self.create_action(self, "./icons/screenshot.ico", "Screenshot", "Screenshot",
                                               self.screenshot)
        screenshot_action.setShortcut(QKeySequence("Ctrl+Shift+P"))
        edit_menu.addActions([wrap_text_action, screenshot_action])
        edit_toolbar.addActions([wrap_text_action, screenshot_action])

        # *****************

        self.update_title()

    def create_action(self, parent, icon_path, action_name, set_status_tip, triggered_method):
        action = QAction(QIcon(icon_path), action_name, parent)
        action.setStatusTip(set_status_tip)
        action.triggered.connect(triggered_method)
        return action

    def screenshot(self):
        screen = QApplication.primaryScreen()
        s_shot = screen.grabWindow(self.winId())
        s_shot.save("shot.jpg", "jpg")

    def wrap_text(self):
        self.editor.setLineWrapMode(not self.editor.lineWrapMode())

    def clear_contents(self):
        self.editor.setPlainText("")

    def print_file(self):
        print_dialog = QPrintDialog()
        if print_dialog.exec_():
            self.editor.print_(print_dialog.printer())

    def file_open(self):
        # second element is filetype, so it's unnecessary that's why it's assigned to underscore
        path, _ = QFileDialog.getOpenFileName(parent=self, caption="Open File", directory="", filter=self.filter_types)

        if path:
            try:
                with open(path, "r", encoding="utf8") as file:
                    text = file.read()
                    file.close()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()

    def file_save(self):
        if self.path is None:
            self.file_save_as()
        else:
            try:
                text = self.editor.toPlainText()
                with open(self.path, "w") as file:
                    file.write(text)
                    file.close()
            except Exception as e:
                self.dialog_message(str(e))

    def file_save_as(self):
        path, _ = QFileDialog.getSaveFileName(parent=self, caption="Save File As", directory="",
                                              filter=self.filter_types)
        text = self.editor.toPlainText()

        if not path:
            return
        else:
            try:
                with open(path, "w") as file:
                    file.write(text)
                    file.close()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.update_title()

    def update_title(self):
        self.setWindowTitle("{0} - Notepad".format(os.path.basename(self.path) if self.path else "Untitled"))

    def dialog_message(self, message):
        dialog = QMessageBox(self)
        dialog.setText(message)
        dialog.setIcon(QMessageBox.Critical)
        dialog.show()


app = QApplication(sys.argv)
notepad = Notepad()
notepad.show()
sys.exit(app.exec_())
