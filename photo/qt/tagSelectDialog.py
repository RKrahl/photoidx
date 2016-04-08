"""A dialog window to set and remove tags.
"""

from __future__ import division
import math
from PySide import QtCore, QtGui


class TagSelectDialog(QtGui.QDialog):

    def __init__(self, taglist):
        super(TagSelectDialog, self).__init__()

        self.checkLayout = QtGui.QGridLayout()
        self.settags(taglist)

        self.entry = QtGui.QLineEdit()
        self.entry.returnPressed.connect(self.newtag)
        entryLabel = QtGui.QLabel("New tag:")
        entryLabel.setBuddy(self.entry)
        entryLayout = QtGui.QHBoxLayout()
        entryLayout.addWidget(entryLabel)
        entryLayout.addWidget(self.entry)

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | 
                                           QtGui.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(self.checkLayout)
        mainLayout.addLayout(entryLayout)
        mainLayout.addWidget(buttonBox, alignment=QtCore.Qt.AlignHCenter)
        self.setLayout(mainLayout)
        self.setWindowTitle("Select tags")

    def settags(self, tags):
        self.taglist = set(tags)
        self.tagCheck = {}
        # We need to rearrange the checkbox widgets in
        # self.checkLayout.  To this end, remove all old checkboxes
        # first, store those to be retained to self.tagCheck and then
        # add the new set of checkboxes to self.checkLayout, reusing
        # those in self.tagCheck.
        while True:
            child = self.checkLayout.takeAt(0)
            if not child:
                break
            cb = child.widget()
            t = cb.text()
            if t in self.taglist:
                self.tagCheck[t] = cb
        if len(self.taglist) > 0:
            ncol = int(math.ceil(math.sqrt(len(self.taglist)/10)))
            nrow = int(math.ceil(len(self.taglist)/ncol))
            c = 0
            for t in sorted(self.taglist):
                if t not in self.tagCheck:
                    self.tagCheck[t] = QtGui.QCheckBox(t)
                cb = self.tagCheck[t]
                self.checkLayout.addWidget(cb, c % nrow, c // nrow)
                c += 1

    def newtag(self):
        t = self.entry.text()
        if t not in self.taglist:
            self.taglist.add(t)
            self.settags(self.taglist)
        self.tagCheck[t].setCheckState(QtCore.Qt.Checked)
        self.adjustSize()
        self.entry.setText("")

    def setCheckedTags(self, tags):
        for t in self.taglist:
            state = QtCore.Qt.Checked if t in tags else QtCore.Qt.Unchecked
            self.tagCheck[t].setCheckState(state)

    def checkedTags(self):
        return { t for t in self.taglist if self.tagCheck[t].isChecked() }
