import sys
from dataclasses import dataclass
from typing import Dict
import os

from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QAction, QFont, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QProgressBar,
    QRadioButton,
    QSplitter,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QDialog,
    QSizePolicy,
    QScrollArea,
)

from backend.pipeline import SpeechPipeline


@dataclass
class UIStrings:
    title: str
    choose_language: str
    language_hint: str
    confirm: str
    nav_home: str
    nav_transcribe: str
    nav_analysis: str
    nav_keywords: str
    nav_settings: str
    welcome_title: str
    welcome_body: str
    input_group: str
    choose_file: str
    selected_file: str
    keyword_group: str
    keyword_hint: str
    start_button: str
    stop_button: str
    progress_ready: str
    progress_running: str
    preview_group: str
    log_group: str
    analysis_group: str
    analysis_hint: str
    keyword_detect_group: str
    keyword_detect_hint: str
    developer_group: str
    watermark: str
    developer_statement: str
    status_ready: str
    status_no_file: str
    menu_file: str
    menu_exit: str
    about_title: str
    about_body: str
    splash_title: str
    splash_body: str
    system_overview_group: str
    system_overview_hint: str
    image_missing_text: str


STRINGS: Dict[str, UIStrings] = {
    "zh": UIStrings(
        title="工业语音识别与分析系统",
        choose_language="选择界面语言",
        language_hint="请选择启动语言。后续可以在设置页扩展语言切换。",
        confirm="进入程序",
        nav_home="首页",
        nav_transcribe="转写",
        nav_analysis="数据分析",
        nav_keywords="关键词检出",
        nav_settings="设置",
        welcome_title="工业系统总览",
        welcome_body="首页展示工业系统概况图。今后语音系统提取出的设备状态、异常提示与关键结果，可直接映射到该图中进行显示。",
        input_group="输入文件",
        choose_file="选择音频/视频文件",
        selected_file="当前文件：未选择",
        keyword_group="关键词提示",
        keyword_hint="输入人名、地名、术语，使用逗号分隔。",
        start_button="开始处理",
        stop_button="停止（预留）",
        progress_ready="就绪",
        progress_running="处理中...",
        preview_group="结果预览",
        log_group="运行日志",
        analysis_group="数据分析（预留扩展）",
        analysis_hint="今后基于语音系统提取出的信息，在此页面中进行异常检测、安全分析、趋势判断与数据库连接等扩展。",
        keyword_detect_group="关键词检出（预留扩展）",
        keyword_detect_hint="今后将把识别出的锅炉、反应釜、阀门、压力、温度等关键词按频次或类别在此列出排序。",
        developer_group="开发者声明",
        watermark="CZF PROJECT",
        developer_statement="开发者声明：本程序当前为本地开发版本，识别结果仅供辅助整理与研究测试使用，请勿将未核对内容直接视为正式记录。",
        status_ready="状态：就绪",
        status_no_file="请先选择文件。",
        menu_file="文件",
        menu_exit="退出",
        about_title="关于",
        about_body="这是一个以语音识别为核心、面向工业信息采集与分析的原型系统。",
        splash_title="正在加载系统",
        splash_body="欢迎使用。\n感謝你對陳哲飛的支持，请稍候……",
        system_overview_group="工业系统总览图",
        system_overview_hint="该图用于展示工业系统整体概况。后续识别出的异常、报警、设备状态等信息将映射到此处。",
        image_missing_text="未找到系统总览图。\n请将参考图放到：assets/process_overview.jpg",
    ),
    "ja": UIStrings(
        title="工業音声認識・分析システム",
        choose_language="表示言語を選択",
        language_hint="起動時の言語を選んでください。設定ページで後から拡張できる構成にしています。",
        confirm="開始する",
        nav_home="ホーム",
        nav_transcribe="文字起こし",
        nav_analysis="データ分析",
        nav_keywords="キーワード検出",
        nav_settings="設定",
        welcome_title="工業システム全体図",
        welcome_body="ホームでは工業システムの概況図を表示します。今後、音声システムから抽出された設備状態、異常情報、重要結果をこの図へ反映できる構成です。",
        input_group="入力ファイル",
        choose_file="音声 / 動画ファイルを選択",
        selected_file="選択中のファイル：未選択",
        keyword_group="キーワード補助",
        keyword_hint="人名・地名・専門用語をカンマ区切りで入力してください。",
        start_button="処理開始",
        stop_button="停止（拡張予定）",
        progress_ready="待機中",
        progress_running="処理中...",
        preview_group="結果プレビュー",
        log_group="実行ログ",
        analysis_group="データ分析（拡張予定）",
        analysis_hint="今後、音声システムから得られた情報に基づき、異常検知、安全分析、傾向把握、データベース連携などをこの画面に追加します。",
        keyword_detect_group="キーワード検出（拡張予定）",
        keyword_detect_hint="今後、ボイラー、反応槽、バルブ、圧力、温度などの検出キーワードをカテゴリまたは頻度順に表示します。",
        developer_group="開発者声明",
        watermark="CZF PROJECT",
        developer_statement="開発者声明：本ソフトは現在ローカル開発版です。認識結果は補助用途と検証用途を前提とし、未確認のまま正式記録として扱わないでください。",
        status_ready="状態：待機中",
        status_no_file="先にファイルを選択してください。",
        menu_file="ファイル",
        menu_exit="終了",
        about_title="このアプリについて",
        about_body="これは音声認識を中核とし、工業情報収集と分析へ拡張可能な原型システムです。",
        splash_title="システムを読み込み中",
        splash_body="ようこそ。\n画面と認識モジュールを初期化しています。少々お待ちください……",
        system_overview_group="工業システム全体図",
        system_overview_hint="この図は工業システムの全体構成表示用です。将来、異常、警報、設備状態などをここへ反映します。",
        image_missing_text="システム全体図が見つかりません。\n参考図を assets/process_overview.jpg に配置してください。",
    ),
    "en": UIStrings(
        title="Industrial Speech Recognition & Analysis System",
        choose_language="Choose interface language",
        language_hint="Select the startup language. The settings area is structured for future expansion.",
        confirm="Enter",
        nav_home="Home",
        nav_transcribe="Transcription",
        nav_analysis="Data Analysis",
        nav_keywords="Keyword Detection",
        nav_settings="Settings",
        welcome_title="Industrial System Overview",
        welcome_body="The home page displays a high-level industrial system overview diagram. Later, abnormal states, alarms, and extracted equipment information from speech data can be mapped onto this figure.",
        input_group="Input file",
        choose_file="Choose audio/video file",
        selected_file="Current file: none",
        keyword_group="Keyword hints",
        keyword_hint="Enter names, places, and terms separated by commas.",
        start_button="Start",
        stop_button="Stop (reserved)",
        progress_ready="Ready",
        progress_running="Processing...",
        preview_group="Result preview",
        log_group="Run log",
        analysis_group="Data Analysis (reserved)",
        analysis_hint="Later, this page will support anomaly detection, safety analysis, trend analysis, and database integration based on extracted speech information.",
        keyword_detect_group="Keyword Detection (reserved)",
        keyword_detect_hint="Later, detected keywords such as boiler, reactor, valve, pressure, and temperature will be listed and sorted here.",
        developer_group="Developer statement",
        watermark="CZF PROJECT",
        developer_statement="Developer statement: this program is currently a local development build. Outputs are intended for assisted drafting and testing only and should be reviewed before formal use.",
        status_ready="Status: ready",
        status_no_file="Please choose a file first.",
        menu_file="File",
        menu_exit="Exit",
        about_title="About",
        about_body="This is a prototype system centered on speech recognition and designed for future industrial information capture and analysis.",
        splash_title="Loading system",
        splash_body="Welcome.\nInitializing interface and recognition modules. Please wait...",
        system_overview_group="Industrial System Overview Diagram",
        system_overview_hint="This figure is reserved for industrial system overview display. Later, alarms, faults, and extracted equipment states can be mapped here.",
        image_missing_text="Overview image not found.\nPlease place the reference image at: assets/process_overview.jpg",
    ),
}


class LanguageDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Language")
        self.setModal(True)
        self.selected_language = "zh"
        self.resize(360, 220)
        self.setStyleSheet("""
            QDialog { background: #dcdcdc; }
            QLabel { color: #111111; }
            QGroupBox {
                border: 1px solid #7f7f7f;
                margin-top: 6px;
                background: #efefef;
            }
            QRadioButton { spacing: 8px; }
            QPushButton {
                background: #d6d6d6;
                border: 1px solid #6d6d6d;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background: #c8c8c8;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Select Language / 言語選択 / 选择语言")
        title.setStyleSheet("font-size: 16px; font-weight: 700;")
        layout.addWidget(title)

        hint = QLabel("Choose the startup language.")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        box = QGroupBox()
        box_layout = QVBoxLayout(box)
        self.group = QButtonGroup(self)

        options = [
            ("zh", "中文"),
            ("ja", "日本語"),
            ("en", "English"),
        ]

        for code, label in options:
            btn = QRadioButton(label)
            if code == "zh":
                btn.setChecked(True)
            self.group.addButton(btn)
            btn.code = code
            box_layout.addWidget(btn)

        layout.addWidget(box)

        confirm = QPushButton("Continue")
        confirm.setMinimumHeight(34)
        confirm.clicked.connect(self.accept_language)
        layout.addWidget(confirm)

    def accept_language(self):
        for btn in self.group.buttons():
            if btn.isChecked():
                self.selected_language = btn.code
                break
        self.accept()


class LoadingDialog(QDialog):
    def __init__(self, s: UIStrings):
        super().__init__()
        self.setWindowTitle("Loading")
        self.setModal(True)
        self.setFixedSize(420, 220)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.setStyleSheet("""
            QDialog {
                background: #d4d4d4;
            }
            QFrame {
                background: #efefef;
                border: 1px solid #707070;
            }
            QLabel {
                color: #111111;
            }
            QProgressBar {
                border: 1px solid #707070;
                background: #ffffff;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background: #8c8c8c;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        panel = QFrame()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(18, 18, 18, 18)
        panel_layout.setSpacing(12)

        title = QLabel(s.splash_title)
        title.setStyleSheet("font-size: 18px; font-weight: 700;")
        body = QLabel(s.splash_body)
        body.setWordWrap(True)

        progress = QProgressBar()
        progress.setRange(0, 0)

        panel_layout.addWidget(title)
        panel_layout.addWidget(body)
        panel_layout.addStretch(1)
        panel_layout.addWidget(progress)

        layout.addWidget(panel)


class PageHeader(QFrame):
    def __init__(self, title: str, body: str):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background: #ececec;
                border: 1px solid #7a7a7a;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #111111;")
        body_label = QLabel(body)
        body_label.setWordWrap(True)
        body_label.setStyleSheet("color: #333333;")

        layout.addWidget(title_label)
        layout.addWidget(body_label)


class ScaledImageLabel(QLabel):
    def __init__(self, image_path: str, fallback_text: str):
        super().__init__()
        self.image_path = image_path
        self.fallback_text = fallback_text
        self._pixmap = QPixmap()
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(520)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("""
            QLabel {
                background: #ffffff;
                border: 1px solid #7a7a7a;
                color: #444444;
            }
        """)
        self.load_image()

    def load_image(self):
        if os.path.exists(self.image_path):
            self._pixmap = QPixmap(self.image_path)
            if not self._pixmap.isNull():
                self._update_scaled_pixmap()
                return

        self.setText(self.fallback_text)
        self.setWordWrap(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self._pixmap.isNull():
            self._update_scaled_pixmap()

    def _update_scaled_pixmap(self):
        scaled = self._pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.setPixmap(scaled)


class MainWindow(QMainWindow):
    def __init__(self, language: str):
        super().__init__()
        self.lang = language
        self.s = STRINGS[language]
        self.current_file_path = ""

        self.hf_token = os.getenv("HF_TOKEN")
        self.ffmpeg_bin = r"D:\ffmpeg\ffmpeg-8.1-full_build-shared\bin"

        self.pipeline = SpeechPipeline(
            hf_token=self.hf_token,
            ffmpeg_bin=self.ffmpeg_bin,
        )

        self.setWindowTitle(self.s.title)
        self.resize(1280, 820)
        self._apply_retro_style()
        self._build_menu()
        self._build_ui()
        self.statusBar().showMessage(self.s.status_ready)

    def _apply_retro_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background: #d9d9d9;
            }
            QWidget {
                font-size: 12px;
                color: #111111;
            }
            QMenuBar, QMenu, QStatusBar {
                background: #e3e3e3;
                color: #111111;
            }
            QFrame {
                background: #efefef;
                border: 1px solid #7f7f7f;
            }
            QGroupBox {
                background: #efefef;
                border: 1px solid #7f7f7f;
                margin-top: 8px;
                font-weight: 700;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px 0 4px;
            }
            QPushButton {
                background: #d6d6d6;
                border: 1px solid #6f6f6f;
                padding: 6px 10px;
                min-height: 28px;
            }
            QPushButton:hover {
                background: #c8c8c8;
            }
            QPushButton:pressed {
                background: #bdbdbd;
            }
            QListWidget, QPlainTextEdit, QTextEdit {
                background: #ffffff;
                border: 1px solid #7a7a7a;
            }
            QProgressBar {
                border: 1px solid #707070;
                background: #ffffff;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background: #909090;
            }
        """)

    def _build_menu(self):
        file_menu = self.menuBar().addMenu(self.s.menu_file)
        exit_action = QAction(self.s.menu_exit, self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(8)

        header = self._build_top_banner()
        root.addWidget(header)

        body = QSplitter(Qt.Horizontal)
        body.setChildrenCollapsible(False)
        root.addWidget(body, 1)

        self.stack = QStackedWidget()

        nav = self._build_navigation()
        body.addWidget(nav)
        body.addWidget(self.stack)
        body.setSizes([190, 980])

        self.stack.addWidget(self._build_home_page())
        self.stack.addWidget(self._build_transcribe_page())
        self.stack.addWidget(self._build_analysis_page())
        self.stack.addWidget(self._build_keyword_detect_page())
        self.stack.addWidget(self._build_settings_page())

        footer = self._build_footer()
        root.addWidget(footer)

    def _build_top_banner(self) -> QWidget:
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: #cfcfcf;
                border: 1px solid #707070;
            }
        """)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(12, 10, 12, 10)

        left = QVBoxLayout()
        title = QLabel(self.s.title)
        title.setStyleSheet("font-size: 18px; font-weight: 700;")
        subtitle = QLabel(self.s.language_hint)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #333333;")
        left.addWidget(title)
        left.addWidget(subtitle)

        right = QLabel(self.s.watermark)
        right.setStyleSheet("font-size: 13px; font-weight: 700; color: #444444;")
        right.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout.addLayout(left, 1)
        layout.addWidget(right)
        return frame

    def _build_navigation(self) -> QWidget:
        frame = QFrame()
        frame.setMinimumWidth(170)
        frame.setMaximumWidth(220)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        title = QLabel("MENU")
        title.setStyleSheet("font-size: 13px; font-weight: 700; color: #222222;")
        layout.addWidget(title)

        self.nav_list = QListWidget()
        self.nav_list.setSpacing(2)
        self.nav_list.setIconSize(QSize(16, 16))
        self.nav_list.addItems([
            self.s.nav_home,
            self.s.nav_transcribe,
            self.s.nav_analysis,
            self.s.nav_keywords,
            self.s.nav_settings,
        ])
        self.nav_list.setCurrentRow(0)
        self.nav_list.currentRowChanged.connect(self.stack.setCurrentIndex)
        layout.addWidget(self.nav_list, 1)

        return frame

    def _build_home_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(8)
        layout.addWidget(PageHeader(self.s.welcome_title, self.s.welcome_body))

        overview_box = QGroupBox(self.s.system_overview_group)
        overview_layout = QVBoxLayout(overview_box)
        overview_note = QLabel(self.s.system_overview_hint)
        overview_note.setWordWrap(True)

        image_path = os.path.join("assets", "process_overview.jpg")
        self.system_image = ScaledImageLabel(image_path, self.s.image_missing_text)

        overview_layout.addWidget(overview_note)
        overview_layout.addWidget(self.system_image, 1)

        log_box = QGroupBox(self.s.log_group)
        log_layout = QVBoxLayout(log_box)
        home_log_note = QLabel("首页日志窗口预留给工业系统状态日志。今后语音系统提取出的异常、报警、关键词与分析结果会在这里滚动显示。")
        home_log_note.setWordWrap(True)
        self.home_log_text = QPlainTextEdit()
        self.home_log_text.setReadOnly(True)
        self.home_log_text.setMaximumHeight(150)
        self.home_log_text.setPlainText(
            "[INFO] 系统总览页已加载。\n"
            "[INFO] 当前页面为工业系统概况图框架。\n"
            "[INFO] 后续将由语音系统提取出的信息驱动该页。"
        )

        log_layout.addWidget(home_log_note)
        log_layout.addWidget(self.home_log_text)

        layout.addWidget(overview_box, 1)
        layout.addWidget(log_box)
        return page

    def _build_transcribe_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(8)
        layout.addWidget(PageHeader(self.s.nav_transcribe, self.s.welcome_body))

        content = QSplitter(Qt.Horizontal)
        content.setChildrenCollapsible(False)
        layout.addWidget(content, 1)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(8)

        input_box = QGroupBox(self.s.input_group)
        input_layout = QVBoxLayout(input_box)
        self.file_label = QLabel(self.s.selected_file)
        self.file_label.setWordWrap(True)
        choose_btn = QPushButton(self.s.choose_file)
        choose_btn.clicked.connect(self.choose_file)
        input_layout.addWidget(self.file_label)
        input_layout.addWidget(choose_btn)
        left_layout.addWidget(input_box)

        keyword_box = QGroupBox(self.s.keyword_group)
        keyword_layout = QVBoxLayout(keyword_box)
        self.keyword_input = QTextEdit()
        self.keyword_input.setPlaceholderText(self.s.keyword_hint)
        self.keyword_input.setMaximumHeight(90)
        keyword_layout.addWidget(self.keyword_input)
        left_layout.addWidget(keyword_box)

        action_box = QGroupBox("RUN")
        action_layout = QHBoxLayout(action_box)
        start_btn = QPushButton(self.s.start_button)
        start_btn.clicked.connect(self.start_processing)
        stop_btn = QPushButton(self.s.stop_button)
        stop_btn.setEnabled(False)
        action_layout.addWidget(start_btn)
        action_layout.addWidget(stop_btn)
        left_layout.addWidget(action_box)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setFormat(self.s.progress_ready)
        left_layout.addWidget(self.progress)
        left_layout.addStretch(1)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(8)

        preview_box = QGroupBox(self.s.preview_group)
        preview_layout = QVBoxLayout(preview_box)
        self.preview_text = QPlainTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setPlaceholderText("Recognition results will appear here.")
        preview_layout.addWidget(self.preview_text)

        log_box = QGroupBox(self.s.log_group)
        log_layout = QVBoxLayout(log_box)
        self.log_text = QPlainTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(170)
        log_layout.addWidget(self.log_text)

        right_layout.addWidget(preview_box, 1)
        right_layout.addWidget(log_box)

        content.addWidget(left_panel)
        content.addWidget(right_panel)
        content.setSizes([360, 760])
        return page

    def _build_analysis_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(8)
        layout.addWidget(PageHeader(self.s.nav_analysis, self.s.analysis_hint))

        top_box = QGroupBox(self.s.analysis_group)
        top_layout = QVBoxLayout(top_box)
        top_note = QLabel(self.s.analysis_hint)
        top_note.setWordWrap(True)

        self.analysis_text = QPlainTextEdit()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setPlaceholderText(
            "这里预留给后续的数据分析结果。\n"
            "例如：\n"
            "- 异常检测\n"
            "- 安全分析\n"
            "- 趋势判断\n"
            "- 数据库联动结果\n"
        )

        top_layout.addWidget(top_note)
        top_layout.addWidget(self.analysis_text)

        bottom_box = QGroupBox("分析模块占位")
        bottom_layout = QGridLayout(bottom_box)

        card1 = self._info_card("异常检测", "基于语音提取出的状态词、设备词和上下文信息，后续在这里进行异常判定。")
        card2 = self._info_card("安全分析", "根据识别到的报警、故障和关键描述，预留安全分析与风险提示区域。")
        card3 = self._info_card("趋势分析", "后续可将提取数据按时间维度进行趋势对比与演化分析。")
        card4 = self._info_card("数据库连接", "未来可接入数据库，对历史记录、状态数据和分析结果进行持久化。")

        bottom_layout.addWidget(card1, 0, 0)
        bottom_layout.addWidget(card2, 0, 1)
        bottom_layout.addWidget(card3, 1, 0)
        bottom_layout.addWidget(card4, 1, 1)

        layout.addWidget(top_box, 1)
        layout.addWidget(bottom_box)
        return page

    def _build_keyword_detect_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(8)
        layout.addWidget(PageHeader(self.s.nav_keywords, self.s.keyword_detect_hint))

        box = QGroupBox(self.s.keyword_detect_group)
        box_layout = QVBoxLayout(box)

        note = QLabel(self.s.keyword_detect_hint)
        note.setWordWrap(True)

        self.keyword_detect_text = QPlainTextEdit()
        self.keyword_detect_text.setReadOnly(True)
        self.keyword_detect_text.setPlaceholderText(
            "这里将来用于列出识别出的关键词并排序。\n\n"
            "示例：\n"
            "1. 锅炉\n"
            "2. 反应釜\n"
            "3. 阀门\n"
            "4. 温度\n"
            "5. 压力"
        )

        box_layout.addWidget(note)
        box_layout.addWidget(self.keyword_detect_text)

        side_box = QGroupBox("检出分类占位")
        side_layout = QGridLayout(side_box)
        side_layout.addWidget(self._info_card("设备类", "锅炉、反应釜、换热器、阀门等"), 0, 0)
        side_layout.addWidget(self._info_card("状态类", "异常、报警、故障、泄漏等"), 0, 1)
        side_layout.addWidget(self._info_card("参数类", "温度、压力、流量、液位等"), 1, 0)
        side_layout.addWidget(self._info_card("动作类", "开启、关闭、检查、调整等"), 1, 1)

        layout.addWidget(box, 1)
        layout.addWidget(side_box)
        return page

    def _build_settings_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(8)
        layout.addWidget(PageHeader(self.s.nav_settings, self.s.about_body))

        developer_box = QGroupBox(self.s.developer_group)
        developer_layout = QVBoxLayout(developer_box)
        statement = QTextEdit()
        statement.setPlainText(self.s.developer_statement)
        statement.setReadOnly(True)
        developer_layout.addWidget(statement)
        layout.addWidget(developer_box)
        layout.addStretch(1)
        return page

    def _build_footer(self) -> QWidget:
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: #dcdcdc;
                border: 1px solid #7a7a7a;
            }
        """)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 6, 10, 6)

        watermark = QLabel(self.s.watermark)
        watermark.setStyleSheet("font-weight: 700; color: #444444;")
        statement = QLabel(self.s.developer_statement)
        statement.setWordWrap(True)
        statement.setStyleSheet("color: #444444;")

        layout.addWidget(watermark)
        layout.addWidget(statement, 1)
        return frame

    def _info_card(self, title: str, body: str) -> QWidget:
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 10, 12, 10)
        label_title = QLabel(title)
        label_title.setStyleSheet("font-size: 13px; font-weight: 700;")
        label_body = QLabel(body)
        label_body.setWordWrap(True)
        label_body.setStyleSheet("color: #333333;")
        layout.addWidget(label_title)
        layout.addWidget(label_body)
        return frame

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.s.choose_file,
            "",
            "Media Files (*.mp3 *.mp4 *.wav *.m4a *.flac *.aac *.mov)"
        )
        if not file_path:
            return

        self.current_file_path = file_path

        prefix = self.s.selected_file
        if "：" in prefix:
            prefix = prefix.split("：")[0]
            self.file_label.setText(f"{prefix}：{file_path}")
        else:
            prefix = prefix.split(":")[0]
            self.file_label.setText(f"{prefix}: {file_path}")

        self.log("Selected file: " + file_path)
        self.statusBar().showMessage(self.s.status_ready)

    def get_keywords(self):
        raw = self.keyword_input.toPlainText().strip()
        if not raw:
            return []
        return [k.strip() for k in raw.split(",") if k.strip()]

    def start_processing(self):
        if not self.current_file_path:
            QMessageBox.warning(self, self.s.title, self.s.status_no_file)
            return

        self.progress.setValue(5)
        self.progress.setFormat(self.s.progress_running)
        self.preview_text.clear()
        self.log_text.clear()

        self.log("Start processing...")
        self.log("Input file: " + self.current_file_path)

        keywords = self.get_keywords()
        if keywords:
            self.log("Keywords: " + ", ".join(keywords))
        else:
            self.log("Keywords: None")

        self.statusBar().showMessage(self.s.progress_running)

        try:
            self.progress.setValue(15)

            result = self.pipeline.run(
                input_path=self.current_file_path,
                keywords=keywords,
                temp_dir="temp",
                output_dir="output",
            )

            self.progress.setValue(80)

            preview_lines = []
            for seg in result["segments"]:
                preview_lines.append(
                    f"[{seg['start']:.2f}-{seg['end']:.2f}] {seg['speaker']}: {seg['text']}"
                )

            self.preview_text.setPlainText("\n".join(preview_lines))

            self.log("Language: " + str(result["language"]))
            self.log("TXT saved: " + result["txt_file"])
            self.log("JSON saved: " + result["json_file"])
            self.log("Done.")

            self.home_log_text.appendPlainText("[INFO] 语音系统完成一次识别任务。")
            self.home_log_text.appendPlainText("[INFO] 后续可在此页映射设备状态与异常提示。")

            self.progress.setValue(100)
            self.progress.setFormat(self.s.progress_ready)
            self.statusBar().showMessage(self.s.status_ready)

        except Exception as e:
            self.progress.setValue(0)
            self.progress.setFormat(self.s.progress_ready)
            self.statusBar().showMessage("Error")
            self.log("ERROR: " + str(e))
            QMessageBox.critical(self, self.s.title, f"处理失败：\n{e}")

    def log(self, text: str):
        self.log_text.appendPlainText(text)


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei UI", 10))

    dialog = LanguageDialog()
    if dialog.exec() != QDialog.Accepted:
        sys.exit(0)

    loading = LoadingDialog(STRINGS[dialog.selected_language])
    loading.show()
    app.processEvents()

    window = MainWindow(dialog.selected_language)

    def finish_loading():
        loading.close()
        window.show()
        window.nav_list.setCurrentRow(0)

    QTimer.singleShot(1400, finish_loading)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()