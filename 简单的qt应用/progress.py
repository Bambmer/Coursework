# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progress.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QProgressBar,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(320, 240)
        self.start = QPushButton(Dialog)
        self.start.setObjectName(u"start")
        self.start.setGeometry(QRect(80, 170, 168, 26))
        self.label_tip = QLabel(Dialog)
        self.label_tip.setObjectName(u"label_tip")
        self.label_tip.setEnabled(False)
        self.label_tip.setGeometry(QRect(60, 110, 215, 31))
        self.label_tip.setScaledContents(False)
        self.label_tip.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_tip.setWordWrap(False)
        self.progressBar = QProgressBar(Dialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(60, 50, 221, 31))
        self.progressBar.setValue(24)

        self.retranslateUi(Dialog)
        self.start.clicked.connect(self.progressBar.reset)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.start.setText(QCoreApplication.translate("Dialog", u"\u5f00\u59cb", None))
        self.label_tip.setText(QCoreApplication.translate("Dialog", u"\u5df2\u722c\u53d6\u76ee\u6807\u7f51\u7ad9\u6570\u636e\u5e76\u4fdd\u5b58\u81f3data.csv\uff01", None))
    # retranslateUi

