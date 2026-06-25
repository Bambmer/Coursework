# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        if not mainWindow.objectName():
            mainWindow.setObjectName(u"mainWindow")
        mainWindow.resize(419, 349)
        self.centralwidget = QWidget(mainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(-1, 3, 411, 321))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_3 = QSpacerItem(20, 28, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(118, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 1, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.target_URL = QPushButton(self.widget)
        self.target_URL.setObjectName(u"target_URL")

        self.verticalLayout.addWidget(self.target_URL)

        self.data_get = QPushButton(self.widget)
        self.data_get.setObjectName(u"data_get")

        self.verticalLayout.addWidget(self.data_get)

        self.generate_excel = QPushButton(self.widget)
        self.generate_excel.setObjectName(u"generate_excel")

        self.verticalLayout.addWidget(self.generate_excel)

        self.generate_wordcloud = QPushButton(self.widget)
        self.generate_wordcloud.setObjectName(u"generate_wordcloud")

        self.verticalLayout.addWidget(self.generate_wordcloud)


        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(118, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 1, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 18, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(118, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 0, 1, 1)

        self.sucecess = QLabel(self.widget)
        self.sucecess.setObjectName(u"sucecess")
        self.sucecess.setEnabled(False)
        self.sucecess.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.sucecess, 3, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(118, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 38, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 4, 1, 1, 1)

        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(mainWindow)
        self.statusbar.setObjectName(u"statusbar")
        mainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.target_URL, self.data_get)
        QWidget.setTabOrder(self.data_get, self.generate_excel)
        QWidget.setTabOrder(self.generate_excel, self.generate_wordcloud)

        self.retranslateUi(mainWindow)
        self.target_URL.clicked.connect(mainWindow.get_URL)
        self.data_get.clicked.connect(mainWindow.data_get)
        self.generate_excel.clicked.connect(mainWindow.generate_excel)
        self.generate_wordcloud.clicked.connect(mainWindow.generate_wordcloud)

        QMetaObject.connectSlotsByName(mainWindow)
    # setupUi

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QCoreApplication.translate("mainWindow", u"MainWindow", None))
        self.target_URL.setText(QCoreApplication.translate("mainWindow", u"\u9009\u62e9\u76ee\u6807\u7f51\u7ad9", None))
        self.data_get.setText(QCoreApplication.translate("mainWindow", u"\u6570\u636e\u83b7\u53d6", None))
        self.generate_excel.setText(QCoreApplication.translate("mainWindow", u"\u751f\u6210\u7edf\u8ba1\u56fe", None))
        self.generate_wordcloud.setText(QCoreApplication.translate("mainWindow", u"\u751f\u6210\u8bcd\u4e91\u56fe", None))
        self.sucecess.setText(QCoreApplication.translate("mainWindow", u"\u6210\u529f\uff01", None))
    # retranslateUi

