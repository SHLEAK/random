from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
class BrowserTab(QWidget):
    def __init__(self, url="https://www.google.com"):
        super().__init__()
        layout = QVBoxLayout()
        self.web_view = QWebEngineView()
        self.web_view.setContextMenuPolicy(Qt.NoContextMenu)
        self.web_view.load(QUrl(url))
        layout.addWidget(self.web_view)
        self.setLayout(layout)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Browser")
        self.setGeometry(100, 100, 2278, 1473)
        self.setFixedSize(2278, 1473)
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.new_tab_button = QPushButton("+")
        self.new_tab_button.clicked.connect(self.add_new_tab)
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        self.forward_button = QPushButton("Forward")
        self.forward_button.clicked.connect(self.go_forward)
        self.reload_button = QPushButton("Reload")
        self.reload_button.clicked.connect(self.reload_page)
        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(self.go_home)
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)
        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(self.new_tab_button)
        toolbar_layout.addWidget(self.back_button)
        toolbar_layout.addWidget(self.forward_button)
        toolbar_layout.addWidget(self.reload_button)
        toolbar_layout.addWidget(self.home_button)
        toolbar_layout.addWidget(self.url_bar)
        main_layout = QVBoxLayout()
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self.tab_widget)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.add_new_tab()
    def add_new_tab(self):
        tab = BrowserTab()
        index = self.tab_widget.addTab(tab, "New Tab")
        self.tab_widget.setCurrentIndex(index)
        tab.web_view.loadStarted.connect(self.update_url_bar)
        tab.web_view.loadFinished.connect(self.update_url_bar)
    def close_tab(self, index):
        self.tab_widget.removeTab(index)
    def load_url(self):
        current_tab = self.tab_widget.currentWidget()
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url  # Add the default protocol (http://) if the URL has no protocol
        current_tab.web_view.load(QUrl(url))
    def update_url_bar(self):
        current_tab = self.tab_widget.currentWidget()
        url = current_tab.web_view.url().toString()
        self.url_bar.setText(url)
    def go_back(self):
        current_tab = self.tab_widget.currentWidget()
        current_tab.web_view.back()
    def go_forward(self):
        current_tab = self.tab_widget.currentWidget()
        current_tab.web_view.forward()
    def reload_page(self):
        current_tab = self.tab_widget.currentWidget()
        current_tab.web_view.reload()
    def go_home(self):
        default_home_url = "https://www.google.com"  # Change this to your desired default home page URL
        current_tab = self.tab_widget.currentWidget()
        current_tab.web_view.load(QUrl(default_home_url))
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
