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
#from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import slimbUI



class SlimBApp(QMainWindow,slimbUI.Ui_SLIMB):
    def __init__(self, homepage,parent=None):
        super(SlimBApp, self).__init__(parent)
        self.setupUi(self,homepage)
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
    form = SlimBApp('http://mrfgmw.cgi.int/FORKS/MRFG')
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
