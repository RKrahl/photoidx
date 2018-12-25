"""A dialog window to change the filter options.
"""

from PySide import QtCore, QtGui
import photo.idxfilter


class FilterDialog(QtGui.QDialog):

    def __init__(self):
        super(FilterDialog, self).__init__()

        optionsLayout = QtGui.QVBoxLayout()

        self.tagCheck = QtGui.QCheckBox("Filter by tags")
        self.tagEntry = QtGui.QLineEdit()
        tagLabel = QtGui.QLabel("Tags:")
        tagLabel.setBuddy(self.tagEntry)
        tagLayout = QtGui.QHBoxLayout()
        tagLayout.addWidget(tagLabel)
        tagLayout.addWidget(self.tagEntry)
        optionsLayout.addWidget(self.tagCheck)
        optionsLayout.addLayout(tagLayout)

        self.selectCheck = QtGui.QCheckBox("Filter by selection")
        self.selectButtonYes = QtGui.QRadioButton("selected")
        self.selectButtonNo = QtGui.QRadioButton("not selected")
        selectLayout = QtGui.QHBoxLayout()
        selectLayout.addWidget(self.selectButtonYes)
        selectLayout.addWidget(self.selectButtonNo)
        optionsLayout.addWidget(self.selectCheck)
        optionsLayout.addLayout(selectLayout)

        self.dateCheck = QtGui.QCheckBox("Filter by date")
        self.dateStartEntry = QtGui.QLineEdit()
        dateStartLabel = QtGui.QLabel("Start:")
        dateStartLabel.setBuddy(self.dateStartEntry)
        self.dateEndEntry = QtGui.QLineEdit()
        dateEndLabel = QtGui.QLabel("End:")
        dateEndLabel.setBuddy(self.dateEndEntry)
        dateLayout = QtGui.QGridLayout()
        dateLayout.addWidget(dateStartLabel, 0, 0)
        dateLayout.addWidget(self.dateStartEntry, 0, 1)
        dateLayout.addWidget(dateEndLabel, 1, 0)
        dateLayout.addWidget(self.dateEndEntry, 1, 1)
        optionsLayout.addWidget(self.dateCheck)
        optionsLayout.addLayout(dateLayout)

        self.gpsCheck = QtGui.QCheckBox("Filter by GPS position")
        self.gpsPosEntry = QtGui.QLineEdit()
        gpsPosLabel = QtGui.QLabel("Position:")
        gpsPosLabel.setBuddy(self.gpsPosEntry)
        self.gpsRadiusEntry = QtGui.QLineEdit()
        gpsRadiusLabel = QtGui.QLabel("Radius:")
        gpsRadiusLabel.setBuddy(self.gpsRadiusEntry)
        gpsLayout = QtGui.QGridLayout()
        gpsLayout.addWidget(gpsPosLabel, 0, 0)
        gpsLayout.addWidget(self.gpsPosEntry, 0, 1)
        gpsLayout.addWidget(gpsRadiusLabel, 1, 0)
        gpsLayout.addWidget(self.gpsRadiusEntry, 1, 1)
        optionsLayout.addWidget(self.gpsCheck)
        optionsLayout.addLayout(gpsLayout)

        self.filelistCheck = QtGui.QCheckBox("Filter by explicit file names")
        self.filelistEntry = QtGui.QLineEdit()
        filelistLabel = QtGui.QLabel("Files:")
        filelistLabel.setBuddy(self.filelistEntry)
        filelistLayout = QtGui.QHBoxLayout()
        filelistLayout.addWidget(filelistLabel)
        filelistLayout.addWidget(self.filelistEntry)
        optionsLayout.addWidget(self.filelistCheck)
        optionsLayout.addLayout(filelistLayout)

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | 
                                           QtGui.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(optionsLayout)
        mainLayout.addWidget(buttonBox, alignment=QtCore.Qt.AlignHCenter)
        self.setLayout(mainLayout)
        self.setWindowTitle("Filter options")

    def setfilter(self, imgFilter):
        if imgFilter.taglist is not None:
            self.tagCheck.setCheckState(QtCore.Qt.Checked)
            tags = sorted(imgFilter.taglist)
            negtags = ["!%s" % t for t in sorted(imgFilter.negtaglist)]
            self.tagEntry.setText(",".join(tags + negtags))
        else:
            self.tagCheck.setCheckState(QtCore.Qt.Unchecked)
            self.tagEntry.setText("")
        if imgFilter.select is not None:
            self.selectCheck.setCheckState(QtCore.Qt.Checked)
            if imgFilter.select:
                self.selectButtonYes.setChecked(QtCore.Qt.Checked)
                self.selectButtonNo.setChecked(QtCore.Qt.Unchecked)
            else:
                self.selectButtonYes.setChecked(QtCore.Qt.Unchecked)
                self.selectButtonNo.setChecked(QtCore.Qt.Checked)
        else:
            self.selectCheck.setCheckState(QtCore.Qt.Unchecked)
        if imgFilter.date is not None:
            self.dateCheck.setCheckState(QtCore.Qt.Checked)
            self.dateStartEntry.setText(imgFilter.date[0].isoformat())
            self.dateEndEntry.setText(imgFilter.date[1].isoformat())
        else:
            self.dateCheck.setCheckState(QtCore.Qt.Unchecked)
            self.dateStartEntry.setText("")
            self.dateEndEntry.setText("")
        if imgFilter.gpspos is not None:
            self.gpsCheck.setCheckState(QtCore.Qt.Checked)
            self.gpsPosEntry.setText(imgFilter.gpspos.floatstr())
            self.gpsRadiusEntry.setText(str(imgFilter.gpsradius))
        else:
            self.gpsCheck.setCheckState(QtCore.Qt.Unchecked)
            self.gpsPosEntry.setText("")
            self.gpsRadiusEntry.setText("")
        if imgFilter.filelist is not None:
            self.filelistCheck.setCheckState(QtCore.Qt.Checked)
            self.filelistEntry.setText(" ".join(sorted(imgFilter.filelist)))
        else:
            self.filelistCheck.setCheckState(QtCore.Qt.Unchecked)
            self.filelistEntry.setText("")
