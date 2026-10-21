STYLE = """
QMainWindow { background: #081626; }
QWidget { color: #E7F1F9; font-family: 'Segoe UI', 'Helvetica Neue', sans-serif; font-size: 14px; }
QWidget#shell { background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #153A63,stop:0.4 #0d2138,stop:1 #081626); }
QLabel { background: transparent; }
QLabel#brand { font-size: 29px; font-weight: 600; letter-spacing: 3px; }
QLabel#eyebrow { color: #A8DFFF; font-size: 11px; letter-spacing: 2px; }
QLabel#muted { color: #afc6da; font-size: 12px; }
QLabel#tokenValue { font-size: 43px; color: #A8DFFF; font-weight: 600; }
QLabel#metricValue { font-size: 25px; font-weight: 600; }
QFrame#panel { background: rgba(21,58,99,110); border: 1px solid #365673; border-radius: 14px; }
QPlainTextEdit { background: #091a2c; border: 1px solid #365673; border-radius: 14px;
  padding: 18px; color: #E7F1F9; selection-background-color: #3178C6; font-size: 15px; }
QPlainTextEdit:focus { border: 1px solid #7db9e0; }
QPushButton, QComboBox { background: #173c60; border: 1px solid #487094;
  border-radius: 10px; padding: 9px 14px; min-height: 19px; }
QPushButton:hover, QComboBox:hover { background: #22517d; border-color: #A8DFFF; }
QPushButton:pressed { background: #3178C6; }
QPushButton:disabled { color: #738ba2; background: #11283e; border-color: #294157; }
QPushButton:focus, QComboBox:focus { border: 2px solid #A8DFFF; }
QPushButton#primary { background: #2767aa; border-color: #589cdc; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox QAbstractItemView { background: #153A63; color: #E7F1F9; selection-background-color: #3178C6; }
QProgressBar { background: #102b46; border: 0; border-radius: 2px; max-height: 3px; }
QProgressBar::chunk { background: #A8DFFF; }
QScrollBar:vertical { background: #0d2138; width: 12px; border-radius: 6px; }
QScrollBar::handle:vertical { background: #487094; min-height: 30px; border-radius: 6px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QToolTip { color: #E7F1F9; background: #153A63; border: 1px solid #487FA8; padding: 6px; }
QPushButton#modeButton { padding: 6px 14px; min-height: 18px; }
QPushButton#modeButton:checked { background: #2767aa; border-color: #A8DFFF; }
QScrollArea#contextScroll { background: transparent; border: none; }
QScrollArea#contextScroll > QWidget { background: transparent; }
QWidget#planningBody { background: #0c233b; border: 1px solid #365673; border-radius: 14px; }
QFrame#contextCard { background: rgba(21,58,99,150); border: 1px solid #365673; border-radius: 12px; }
QLabel#planningValue { color: #A8DFFF; font-size: 25px; font-weight: 600; }
QLabel#planningWarning { color: #FFC89C; font-size: 12px; }
QLabel#planningInterpretation { color: #E7F1F9; font-size: 13px; }
QLineEdit { background: #091a2c; color: #E7F1F9; border: 1px solid #487094; border-radius: 9px; padding: 8px 12px; }
QLineEdit:focus { border: 2px solid #A8DFFF; }
QLineEdit[invalid="true"] { border: 1px solid #FFC89C; }
QToolButton#tokenInformation { color: #A8DFFF; background: transparent; border: 1px solid #7DA9C9;
  border-radius: 10px; padding: 0; font-family: 'Segoe UI'; font-size: 13px; font-weight: 600; }
QToolButton#tokenInformation:hover { background: #22517d; border-color: #A8DFFF; }
QToolButton#tokenInformation:focus { background: #173c60; border: 2px solid #A8DFFF; }
"""
