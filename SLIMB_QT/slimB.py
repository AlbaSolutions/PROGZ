#import sys
#from PyQt5 import uic
#from PyQt5.QtWidgets import QApplication
#
#
#def back(self):
#    print("we went back")
#
#def forward(self):
#    print("we went forward")
#
#def Refresh(self):
#    print("we refreshed")
#
#app = QApplication(sys.argv)
#
## If you saved the template in `templates/main_window.ui`
#ui = uic.loadUi("slimb.ui")
#ui.show()

# Then you can access the objects from the UI
# For example, if you had a label named label1
#ui.butBack.clicked.connect(back)
#ui.butForward.clicked.connect(forward)
#ui.butRefresh.clicked.connect(Refresh)





import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import slimbUI



class SlimBApp(QtWidgets.QMainWindow,slimbUI.Ui_SLIMB):
    def __init__(self, parent=None,homePage):
        super(SlimBApp, self).__init__(parent)
        self.setupUi(self,homePage)
        self.butBack.clicked.connect(self.back)#conntect()
        self.butForward.clicked.connect(self.forward)
        self.butRefresh.clicked.connect(self.Refresh)

    def back(self):
        print("we went back")

    def forward(self):
        print("we went forward")

    def Refresh(self):
        print("we refreshed")





def main():
    app = QApplication(sys.argv)
    form = SlimBApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
