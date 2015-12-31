"""A dialog window to set and remove tags.
"""

from __future__ import division
import math
from PySide import QtCore, QtGui


class TagSelectDialog(QtGui.QDialog):

    def __init__(self, taglist):
        super(TagSelectDialog, self).__init__()

        self.taglist = set(taglist)
        self.checkLayout = QtGui.QGridLayout()
        self.tagCheck = {}
        ncol = int(math.ceil(math.sqrt(len(self.taglist)/10)))
        nrow = int(math.ceil(len(self.taglist)/ncol))
        c = 0
        for t in sorted(self.taglist):
            cb = QtGui.QCheckBox(t)
            self.checkLayout.addWidget(cb, c % nrow, c // nrow)
            self.tagCheck[t] = cb
            c += 1

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | 
                                           QtGui.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(self.checkLayout)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("Select tags")

    def setCheckedTags(self, tags):
        for t in self.taglist:
            state = QtCore.Qt.Checked if t in tags else QtCore.Qt.Unchecked
            self.tagCheck[t].setCheckState(state)

    def checkedTags(self):
        return { t for t in self.taglist if self.tagCheck[t].isChecked() }
