from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys

def run_browser():
    app = QApplication([])
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Browser")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)
        
        self.web_view = QWebEngineView()
        self.web_view.setContextMenuPolicy(Qt.NoContextMenu)
        self.web_view.load(QUrl("https://www.google.com"))
        
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        
        self.forward_button = QPushButton("Forward")
        self.forward_button.clicked.connect(self.go_forward)
        
        self.reload_button = QPushButton("Reload")
        self.reload_button.clicked.connect(self.reload_page)
        
        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(self.go_home)
        
        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(self.back_button)
        toolbar_layout.addWidget(self.forward_button)
        toolbar_layout.addWidget(self.reload_button)
        toolbar_layout.addWidget(self.home_button)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self.web_view)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def go_back(self):
        self.web_view.back()
    
    def go_forward(self):
        self.web_view.forward()
    
    def reload_page(self):
        self.web_view.reload()
    
    def go_home(self):
        default_home_url = "https://www.google.com"
        self.web_view.load(QUrl(default_home_url))

if __name__ == "__main__":
    run_browser()
