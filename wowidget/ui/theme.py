from pathlib import Path
from typing import Final

BACKGROUND_IMAGE_PATH: Final[Path] = (
    Path(__file__).resolve().parents[1] / "assets" / "ui" / "seasonal_background.jpeg"
)


APP_STYLESHEET: Final[str] = """
QWidget {
    color: #F5F2FF;
    font-family: "Segoe UI";
    font-size: 13px;
}

QMainWindow,
QStackedWidget,
QWidget#PlainPage {
    background-color: #11101A;
}

QLabel#PageTitle {
    color: #FFFFFF;
    font-size: 30px;
    font-weight: 700;
}

QLabel#PageSubtitle {
    color: #C9C4DA;
    font-size: 13px;
}

QLabel#SectionTitle {
    color: #FFFFFF;
    font-size: 17px;
    font-weight: 650;
}

QLabel#StateTitle {
    color: #FFFFFF;
    font-size: 20px;
    font-weight: 700;
}

QLabel#MutedLabel {
    color: #B7B1C9;
}

QLabel#StatusSuccess {
    color: #7FE6AE;
    font-weight: 600;
}

QLabel#StatusError {
    color: #FF8A9B;
    font-weight: 600;
}

QFrame#GlassCard,
QGroupBox {
    background-color: rgba(21, 18, 36, 218);
    border: 1px solid rgba(198, 158, 255, 82);
    border-radius: 16px;
}

QFrame#InnerCard {
    background-color: rgba(13, 12, 24, 205);
    border: 1px solid rgba(187, 164, 233, 65);
    border-radius: 12px;
}

QFrame#DividerLine {
    color: rgba(196, 164, 240, 72);
    background-color: rgba(196, 164, 240, 72);
    max-height: 1px;
    border: none;
}


QScrollArea#CharacterSummaryScroll {
    background: transparent;
    border: none;
}

QScrollArea#CharacterSummaryScroll > QWidget > QWidget {
    background: transparent;
}

QScrollArea#PortraitScroll {
    background: transparent;
    border: none;
}

QScrollArea#PortraitScroll > QWidget > QWidget {
    background: transparent;
}

QGroupBox {
    margin-top: 12px;
    padding: 18px 14px 14px 14px;
    font-size: 14px;
    font-weight: 650;
    color: #FFFFFF;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    padding: 0 6px;
    color: #E7D7FF;
}

QPushButton {
    min-height: 34px;
    padding: 0 16px;
    color: #FFFFFF;
    background-color: rgba(90, 62, 135, 215);
    border: 1px solid rgba(209, 173, 255, 100);
    border-radius: 10px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: rgba(116, 79, 170, 230);
    border-color: rgba(224, 194, 255, 170);
}

QPushButton:pressed {
    background-color: rgba(75, 48, 117, 235);
}

QPushButton:disabled {
    color: rgba(255, 255, 255, 95);
    background-color: rgba(65, 59, 76, 150);
    border-color: rgba(255, 255, 255, 35);
}

QPushButton#PrimaryButton {
    background-color: #7250B9;
    border-color: #C49BFF;
}

QPushButton#PrimaryButton:hover {
    background-color: #8661CE;
}

QPushButton#DangerButton {
    background-color: rgba(132, 42, 65, 220);
    border-color: rgba(255, 137, 159, 150);
}

QLineEdit,
QSpinBox,
QComboBox {
    min-height: 34px;
    padding: 0 10px;
    color: #FFFFFF;
    background-color: rgba(10, 9, 19, 220);
    border: 1px solid rgba(191, 164, 232, 75);
    border-radius: 9px;
    selection-background-color: #7E5BC8;
}

QLineEdit:focus,
QSpinBox:focus,
QComboBox:focus {
    border-color: #B98CFF;
}

QComboBox::drop-down {
    width: 26px;
    border: none;
}

QCheckBox {
    spacing: 9px;
    color: #EFEAFF;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 1px solid rgba(204, 177, 245, 120);
    background-color: rgba(10, 9, 19, 215);
}

QCheckBox::indicator:checked {
    background-color: #7D59C4;
    border-color: #C59CFF;
}

QSlider::groove:horizontal {
    height: 5px;
    border-radius: 2px;
    background: rgba(255, 255, 255, 62);
}

QSlider::sub-page:horizontal {
    background: #B77AE5;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    width: 16px;
    margin: -6px 0;
    border-radius: 8px;
    background: #F2D8FF;
    border: 2px solid #7E5BB7;
}


QFrame#CompactSummaryRow {
    background-color: rgba(15, 12, 28, 120);
    border: 1px solid rgba(199, 164, 247, 42);
    border-radius: 8px;
}

QFrame#CompactSummaryRow:hover {
    background-color: rgba(28, 21, 46, 175);
    border-color: rgba(204, 169, 255, 80);
}

QLabel#CompactSummaryLabel {
    color: #AAA3BE;
    font-size: 11px;
    font-weight: 600;
}

QLabel#CompactSummaryValue {
    color: #FFFFFF;
    font-size: 12px;
    font-weight: 700;
}

QFrame#SummaryStat {
    background-color: rgba(15, 12, 28, 175);
    border: 1px solid rgba(199, 164, 247, 48);
    border-radius: 10px;
}

QFrame#SummaryStat:hover {
    background-color: rgba(28, 21, 46, 200);
    border-color: rgba(204, 169, 255, 90);
}

QLabel#SummaryStatLabel {
    color: #AFA7C5;
    font-size: 10px;
    font-weight: 700;
}

QLabel#SummaryStatValue {
    color: #FFFFFF;
    font-size: 15px;
    font-weight: 650;
}

QScrollBar:vertical {
    width: 10px;
    margin: 18px 1px 5px 4px;
    background: transparent;
}

QScrollBar::handle:vertical {
    min-height: 38px;
    border-radius: 3px;
    background: rgba(193, 147, 255, 105);
}

QScrollBar::handle:vertical:hover {
    background: rgba(210, 172, 255, 165);
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
    background: transparent;
    border: none;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
}


QWidget#PlainPage QFrame#GlassCard {
    background-color: rgba(21, 18, 36, 232);
}

QWidget#PlainPage QLineEdit,
QWidget#PlainPage QComboBox {
    min-height: 36px;
}

QWidget#PlainPage QGroupBox {
    border-radius: 14px;
}

QWidget#PlainPage QPushButton {
    min-height: 36px;
}

QMessageBox {
    background-color: #161320;
}
"""
