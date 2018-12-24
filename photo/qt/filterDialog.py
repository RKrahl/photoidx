"""A dialog window to change the filter options.
"""

from PySide import QtCore, QtGui
import photo.idxfilter


class FilterDialog(QtGui.QDialog):

    def __init__(self):
        super(FilterDialog, self).__init__()

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | 
                                           QtGui.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(buttonBox, alignment=QtCore.Qt.AlignHCenter)
        self.setLayout(mainLayout)
        self.setWindowTitle("Filter options")

    def setfilter(self, imgFilter):
        pass
