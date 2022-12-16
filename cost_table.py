from qgis.PyQt.QtWidgets import *
from .cost_table_dialog import Ui_dlgCosts

class DlgCosts(QDialog, Ui_dlgCosts):
    def __init__(self):
        super(DlgCosts, self).__init__()
        self.setupUi(self)

        self.tblCosts.setColumnWidth(0,130)

