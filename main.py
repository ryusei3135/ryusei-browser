import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar,
    QAction, QLineEdit, QTabWidget
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon


class Browser(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ryusei browser")
        self.resize(1200, 800)

        # ------------------------
        # タブウィジェット
        # ------------------------
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)

        self.setCentralWidget(self.tabs)

        # ------------------------
        # ツールバー
        # ------------------------
        self.init_toolbar()

        # 最初のタブ
        self.add_new_tab(QUrl("https://www.google.com"), "Home")

    # ========================
    # ツールバー
    # ========================
    def init_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # 戻る
        back_btn = QAction("←", self)
        back_btn.triggered.connect(
            lambda: self.current_browser().back()
        )
        toolbar.addAction(back_btn)

        # 進む
        forward_btn = QAction("→", self)
        forward_btn.triggered.connect(
            lambda: self.current_browser().forward()
        )
        toolbar.addAction(forward_btn)

        # 更新
        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(
            lambda: self.current_browser().reload()
        )
        toolbar.addAction(reload_btn)

        toolbar.addSeparator()

        # URLバー
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)

        toolbar.addSeparator()

        # 新規タブ
        new_tab_btn = QAction("+", self)
        new_tab_btn.triggered.connect(
            lambda: self.add_new_tab(QUrl("https://www.google.com"), "New Tab")
        )
        toolbar.addAction(new_tab_btn)

    # ========================
    # 新しいタブを追加
    # ========================
    def add_new_tab(self, qurl, label):

        browser = QWebEngineView()
        browser.setUrl(qurl)

        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)

        # タイトル変更
        browser.titleChanged.connect(
            lambda title, browser=browser:
            self.tabs.setTabText(
                self.tabs.indexOf(browser),
                title
            )
        )

        # URL変更
        browser.urlChanged.connect(
            lambda q, browser=browser:
            self.update_url_bar(q, browser)
        )

    # ========================
    # 現在のブラウザ取得
    # ========================
    def current_browser(self):
        return self.tabs.currentWidget()

    # ========================
    # URL移動
    # ========================
    def navigate_to_url(self):
        browser = self.current_browser()
        if not browser:
            return

        url = self.url_bar.text().strip()

        if not url.startswith("http"):
            url = "https://" + url

        browser.setUrl(QUrl(url))

    # ========================
    # URLバー更新
    # ========================
    def update_url_bar(self, q, browser=None):
        if browser != self.current_browser():
            return
        self.url_bar.setText(q.toString())

    # ========================
    # タブ変更時
    # ========================
    def current_tab_changed(self, index):
        browser = self.current_browser()
        if browser:
            self.update_url_bar(browser.url(), browser)

    # ========================
    # タブを閉じる
    # ========================
    def close_tab(self, index):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(index)


# ========================
# アプリ起動
# ========================
app = QApplication(sys.argv)

app.setWindowIcon(QIcon("icon.png"))

# QSS読み込み
try:
    with open("style.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())
except FileNotFoundError:
    pass

window = Browser()
window.show()

sys.exit(app.exec_())