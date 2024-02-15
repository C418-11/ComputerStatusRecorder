

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from UI.BaseWidgets import GetScale
from UI.tools import showException


class CustomQMenuBar(QMenuBar):
    def __init__(self, *args, move, **kwargs):
        super().__init__(*args, **kwargs)

        self._move_func = move

        self.base_position = None

    @showException
    def mousePressEvent(self, event, *_):
        # noinspection PyUnresolvedReferences
        if event.button() == Qt.LeftButton:
            self.base_position = event.pos()
            event.accept()

    @showException
    def mouseMoveEvent(self, event, *_):
        # noinspection PyUnresolvedReferences
        if event.buttons() == Qt.LeftButton and not self.isMaximized():
            self._move_func(event.globalPos() - self.base_position)
            event.accept()


class UiMain:
    def __init__(self, widget: GetScale):
        super().__init__()
        self.Widget = widget
        self.Widget.reference_size = QSize(640, 480)
        self.Widget.resize(640, 480)
        self.Widget.setMinimumSize(640, 480)

        self.TopTab: QTabWidget | None = None
        self.TopTab_Widget: QWidget | None = None

        self.CtrlBar: QWidget | None = None
        self.MenuBar: CustomQMenuBar | None = None

        self.MaxNormalButton: QPushButton | None = None
        self.MinButton: QPushButton | None = None
        self.ExitButton: QPushButton | None = None

        self.top_tabs = []

    def append(self, widget: QWidget):
        self.TopTab.addTab(widget, widget.objectName())
        self.top_tabs.append(widget)

    def _MaxNormalSlot(self):
        if self.Widget.isMaximized():
            self.Widget.showNormal()
            self.MaxNormalButton.setText(u"Max")
        else:
            self.Widget.showMaximized()
            self.MaxNormalButton.setText(u"Normal")

    def setupUi(self):
        self.TopTab = QTabWidget(self.Widget)
        self.TopTab.setObjectName(u"TopTab")

        self.TopTab_Widget = QWidget()
        self.TopTab_Widget.setObjectName(u"TopTab_Widget")

        self.CtrlBar = QWidget(self.Widget)
        self.CtrlBar.setObjectName(u"CtrlBar")

        self.MenuBar = CustomQMenuBar(self.CtrlBar, move=self.Widget.move)
        self.MenuBar.setObjectName(u"Menu")

        # noinspection PyUnresolvedReferences
        self.MenuBar.triggered.connect(lambda action: print(action.text()))

        self.ExitButton = QPushButton(self.CtrlBar)
        self.ExitButton.setObjectName(u"ExitButton")

        self.MaxNormalButton = QPushButton(self.CtrlBar)
        self.MaxNormalButton.setObjectName(u"MaxNormalButton")

        self.MinButton = QPushButton(self.CtrlBar)
        self.MinButton.setObjectName(u"MinButton")

        QWidget.setTabOrder(self.MenuBar, self.MinButton)
        QWidget.setTabOrder(self.MinButton, self.MaxNormalButton)
        QWidget.setTabOrder(self.MaxNormalButton, self.ExitButton)

        self.ReTranslateUi()

        # noinspection PyUnresolvedReferences
        self.ExitButton.clicked.connect(self.Widget.close)
        # noinspection PyUnresolvedReferences
        self.MinButton.clicked.connect(self.Widget.showMinimized)
        # noinspection PyUnresolvedReferences
        self.MaxNormalButton.clicked.connect(self._MaxNormalSlot)

        self.TopTab.setCurrentIndex(0)

        self.Widget.scaleChanged.connect(self.AutoResize)

        QMetaObject.connectSlotsByName(self.Widget)

    @showException
    def AutoResize(self, x_scale: float, y_scale: float):
        self.CtrlBar.resize(self.Widget.width(), int(25 * y_scale))

        self.ExitButton.resize(int(60 * x_scale), self.CtrlBar.height())
        self.MinButton.resize(int(60 * x_scale), self.CtrlBar.height())
        self.MaxNormalButton.resize(int(60 * x_scale), self.CtrlBar.height())

        self.ExitButton.move(self.Widget.width() - self.ExitButton.width(), 0)
        self.MaxNormalButton.move(self.ExitButton.x() - self.MaxNormalButton.width(), 0)
        self.MinButton.move(self.MaxNormalButton.x() - self.MinButton.width(), 0)

        self.MenuBar.resize(self.MinButton.x(), self.CtrlBar.height())

        self.TopTab.resize(self.Widget.width(), self.Widget.height() - self.CtrlBar.height())
        self.TopTab.move(0, self.CtrlBar.height())

        for tab in self.top_tabs:
            try:
                tab.ReScale(x_scale, y_scale)
            except AttributeError:
                pass

    def ReTranslateUi(self):
        self.Widget.setWindowTitle(QCoreApplication.translate("MainUi", u"StatusRecorder", None))
        self.ExitButton.setText(QCoreApplication.translate("MainUi", u"Exit", None))
        self.MinButton.setText(QCoreApplication.translate("MainUi", u"Min", None))
        if self.Widget.isMaximized():
            self.MaxNormalButton.setText(QCoreApplication.translate("MainUi", u"Normal", None))
        else:
            self.MaxNormalButton.setText(QCoreApplication.translate("MainUi", u"Max", None))


def test():
    app = QApplication(sys.argv)
    widget = GetScale()
    ui = UiMain(widget)
    ui.setupUi()

    sub_sub = [1, 2, 3, 4, 5, 6]

    for name in ["CPU", "Memory", "Network", "Disk"]:
        tab = QTabWidget(ui.TopTab_Widget)
        tab.setObjectName(name)
        for x in sub_sub:
            tab.addTab(QWidget(), str(x))
        ui.append(tab)

    # noinspection PyUnresolvedReferences
    widget.setWindowFlags(Qt.CustomizeWindowHint)
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    test()
