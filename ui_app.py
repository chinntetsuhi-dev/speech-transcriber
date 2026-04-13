import sys
from dataclasses import dataclass
from typing import Dict
import os

from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QAction, QFont
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
    nav_speakers: str
    nav_export: str
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
    speaker_group: str
    speaker_hint: str
    export_group: str
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


STRINGS: Dict[str, UIStrings] = {
    "zh": UIStrings(
        title="语音转写与说话人识别工具",
        choose_language="选择界面语言",
        language_hint="请选择启动语言。后续可以在设置页扩展语言切换。",
        confirm="进入程序",
        nav_home="首页",
        nav_transcribe="转写",
        nav_speakers="说话人",
        nav_export="导出",
        nav_settings="设置",
        welcome_title="项目控制台",
        welcome_body="当前版本以语音识别为核心，后续可继续扩展结构化工业数据提取、导出和分析模块。",
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
        speaker_group="说话人映射（预留扩展）",
        speaker_hint="未来可在这里把 SPEAKER_00、SPEAKER_01 映射成真实姓名。",
        export_group="导出与集成（预留扩展）",
        developer_group="开发者声明",
        watermark="Internal Build",
        developer_statement="开发者声明：本程序当前为本地开发版本，识别结果仅供辅助整理与研究测试使用，请勿将未核对内容直接视为正式记录。",
        status_ready="状态：就绪",
        status_no_file="请先选择文件。",
        menu_file="文件",
        menu_exit="退出",
        about_title="关于",
        about_body="这是一个以语音识别为核心的工业信息采集原型系统。",
        splash_title="正在加载系统",
        splash_body="欢迎使用。\n正在初始化界面与识别模块，请稍候……",
    ),
    "ja": UIStrings(
        title="音声文字起こし・話者識別ツール",
        choose_language="表示言語を選択",
        language_hint="起動時の言語を選んでください。設定ページで後から拡張できる構成にしています。",
        confirm="開始する",
        nav_home="ホーム",
        nav_transcribe="文字起こし",
        nav_speakers="話者",
        nav_export="出力",
        nav_settings="設定",
        welcome_title="プロジェクトコントロール",
        welcome_body="現段階では音声認識を中核とし、今後は構造化データ抽出や工業向け解析機能へ拡張できます。",
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
        speaker_group="話者マッピング（拡張予定）",
        speaker_hint="将来ここで SPEAKER_00 / SPEAKER_01 を実名へ対応付けできます。",
        export_group="出力・連携（拡張予定）",
        developer_group="開発者声明",
        watermark="Internal Build",
        developer_statement="開発者声明：本ソフトは現在ローカル開発版です。認識結果は補助用途と検証用途を前提とし、未確認のまま正式記録として扱わないでください。",
        status_ready="状態：待機中",
        status_no_file="先にファイルを選択してください。",
        menu_file="ファイル",
        menu_exit="終了",
        about_title="このアプリについて",
        about_body="これは音声認識を中核とした工業情報収集の原型システムです。",
        splash_title="システムを読み込み中",
        splash_body="ようこそ。\n画面と認識モジュールを初期化しています。少々お待ちください……",
    ),
    "en": UIStrings(
        title="Speech Transcription & Speaker Tool",
        choose_language="Choose interface language",
        language_hint="Select the startup language. The settings area is structured for future expansion.",
        confirm="Enter",
        nav_home="Home",
        nav_transcribe="Transcription",
        nav_speakers="Speakers",
        nav_export="Export",
        nav_settings="Settings",
        welcome_title="Project Console",
        welcome_body="This version focuses on speech recognition as the core. Later it can expand toward structured industrial data extraction and analysis.",
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
        speaker_group="Speaker mapping (reserved)",
        speaker_hint="Later you can map SPEAKER_00 and SPEAKER_01 to real names here.",
        export_group="Export & integration (reserved)",
        developer_group="Developer statement",
        watermark="Internal Build",
        developer_statement="Developer statement: this program is currently a local development build. Outputs are intended for assisted drafting and testing only and should be reviewed before formal use.",
        status_ready="Status: ready",
        status_no_file="Please choose a file first.",
        menu_file="File",
        menu_exit="Exit",
        about_title="About",
        about_body="This is an industrial information capture prototype centered on speech recognition.",
        splash_title="Loading system",
        splash_body="Welcome.\nInitializing interface and recognition modules. Please wait...",
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
        progress.setRange(0, 0)  # 无限动画

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
        self.resize(1180, 760)
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
        body.setSizes([190, 900])

        self.stack.addWidget(self._build_home_page())
        self.stack.addWidget(self._build_transcribe_page())
        self.stack.addWidget(self._build_speakers_page())
        self.stack.addWidget(self._build_export_page())
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
            self.s.nav_speakers,
            self.s.nav_export,
            self.s.nav_settings,
        ])
        self.nav_list.setCurrentRow(1)  # 默认打开“转写”
        self.nav_list.currentRowChanged.connect(self.stack.setCurrentIndex)
        layout.addWidget(self.nav_list, 1)

        return frame

    def _build_home_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(8)
        layout.addWidget(PageHeader(self.s.welcome_title, self.s.welcome_body))

        grid = QGridLayout()
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(8)

        card1 = self._info_card(self.s.input_group, self.s.selected_file)
        card2 = self._info_card(self.s.keyword_group, self.s.keyword_hint)
        card3 = self._info_card(self.s.speaker_group, self.s.speaker_hint)
        card4 = self._info_card(self.s.export_group, "TXT / JSON / SRT / future industrial extensions")

        grid.addWidget(card1, 0, 0)
        grid.addWidget(card2, 0, 1)
        grid.addWidget(card3, 1, 0)
        grid.addWidget(card4, 1, 1)

        layout.addLayout(grid)
        layout.addStretch(1)
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

    def _build_speakers_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(8)
        layout.addWidget(PageHeader(self.s.nav_speakers, self.s.speaker_hint))

        box = QGroupBox(self.s.speaker_group)
        box_layout = QVBoxLayout(box)
        note = QLabel(self.s.speaker_hint)
        note.setWordWrap(True)
        self.speaker_editor = QPlainTextEdit()
        self.speaker_editor.setPlaceholderText("SPEAKER_00 = ...\nSPEAKER_01 = ...")
        box_layout.addWidget(note)
        box_layout.addWidget(self.speaker_editor)
        layout.addWidget(box)
        layout.addStretch(1)
        return page

    def _build_export_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(8)
        layout.addWidget(PageHeader(self.s.nav_export, "Reserved area for future export templates and packaging options."))

        box = QGroupBox(self.s.export_group)
        box_layout = QVBoxLayout(box)
        export_note = QLabel("Future expansion points: TXT / JSON / SRT export, report templates, packaging settings, batch mode.")
        export_note.setWordWrap(True)
        export_editor = QPlainTextEdit()
        export_editor.setPlaceholderText("Export presets and integrations will be placed here later.")
        box_layout.addWidget(export_note)
        box_layout.addWidget(export_editor)
        layout.addWidget(box)
        layout.addStretch(1)
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
        window.nav_list.setCurrentRow(1)  # 默认切到“转写”页

    QTimer.singleShot(1400, finish_loading)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()