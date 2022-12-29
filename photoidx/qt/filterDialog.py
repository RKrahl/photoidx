"""A dialog window to change the filter options.
"""

import datetime
from PySide2 import QtCore, QtWidgets
import photoidx.idxfilter
from photoidx.geo import GeoPosition


class GeoPosEdit(QtWidgets.QLineEdit):
    """A QLineEdit with a suitable size for a GeoPosition.
    """
    def sizeHint(self):
        sh = super().sizeHint()
        fm = self.fontMetrics()
        postext = "\u2014%s\u2014" % GeoPosition("90.0 S, 180.0 E").floatstr()
        sh.setWidth(fm.boundingRect(postext).width())
        return sh


class FilterOption(object):

    def __init__(self, criterion, parent):
        self.groupbox = QtWidgets.QGroupBox("Filter by %s" % criterion)
        self.groupbox.setCheckable(True)
        parent.addWidget(self.groupbox)

    def getOption(self):
        raise NotImplementedError

    def setOption(self, optionValue):
        self.groupbox.setChecked(optionValue is not None)

class TagFilterOption(FilterOption):

    def __init__(self, parent):
        super().__init__("tags", parent)
        self.entry = QtWidgets.QLineEdit()
        label = QtWidgets.QLabel("Tags:")
        label.setBuddy(self.entry)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.entry)
        self.groupbox.setLayout(layout)

    def getOption(self):
        if self.groupbox.isChecked():
            return { 'tags': self.entry.text() }
        else:
            return {}

    def setOption(self, taglist, negtaglist):
        super().setOption(taglist)
        if taglist is not None:
            tags = sorted(taglist)
            negtags = ["!%s" % t for t in sorted(negtaglist)]
            self.entry.setText(",".join(tags + negtags))

class SelectFilterOption(FilterOption):

    def __init__(self, parent):
        super().__init__("selection", parent)
        self.buttonYes = QtWidgets.QRadioButton("selected")
        self.buttonNo = QtWidgets.QRadioButton("not selected")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.buttonYes)
        layout.addWidget(self.buttonNo)
        self.groupbox.setLayout(layout)

    def getOption(self):
        if self.groupbox.isChecked():
            return { 'select': bool(self.buttonYes.isChecked()) }
        else:
            return {}

    def setOption(self, select):
        super().setOption(select)
        if select is not None:
            if select:
                self.buttonYes.setChecked(QtCore.Qt.Checked)
                self.buttonNo.setChecked(QtCore.Qt.Unchecked)
            else:
                self.buttonYes.setChecked(QtCore.Qt.Unchecked)
                self.buttonNo.setChecked(QtCore.Qt.Checked)

class DateFilterOption(FilterOption):

    def __init__(self, parent):
        super().__init__("date", parent)
        self.startEntry = QtWidgets.QLineEdit()
        startLabel = QtWidgets.QLabel("Start:")
        startLabel.setBuddy(self.startEntry)
        self.endEntry = QtWidgets.QLineEdit()
        endLabel = QtWidgets.QLabel("End:")
        endLabel.setBuddy(self.endEntry)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(startLabel, 0, 0)
        layout.addWidget(self.startEntry, 0, 1)
        layout.addWidget(endLabel, 1, 0)
        layout.addWidget(self.endEntry, 1, 1)
        self.groupbox.setLayout(layout)

    def getOption(self):
        if self.groupbox.isChecked():
            startdate = self.startEntry.text()
            enddate = self.endEntry.text()
            if enddate:
                datestr = "%s--%s" % (startdate, enddate)
            else:
                datestr = startdate
            return { 'date': photoidx.idxfilter.strpdate(datestr) }
        else:
            return {}

    def setOption(self, date):
        super().setOption(date)
        if date is not None:
            self.startEntry.setText(date[0].isoformat())
            self.endEntry.setText(date[1].isoformat())

class GPSFilterOption(FilterOption):

    def __init__(self, parent):
        super().__init__("GPS position", parent)
        self.posEntry = GeoPosEdit()
        posLabel = QtWidgets.QLabel("Position:")
        posLabel.setBuddy(self.posEntry)
        self.radiusEntry = QtWidgets.QLineEdit()
        radiusLabel = QtWidgets.QLabel("Radius:")
        radiusLabel.setBuddy(self.radiusEntry)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(posLabel, 0, 0)
        layout.addWidget(self.posEntry, 0, 1)
        layout.addWidget(radiusLabel, 1, 0)
        layout.addWidget(self.radiusEntry, 1, 1)
        self.groupbox.setLayout(layout)

    def getOption(self):
        if self.groupbox.isChecked():
            return { 'gpspos': GeoPosition(self.posEntry.text()), 
                     'gpsradius': float(self.radiusEntry.text()) }
        else:
            return {}

    def setOption(self, gpspos, gpsradius):
        super().setOption(gpspos)
        if gpspos is not None:
            self.posEntry.setText(gpspos.floatstr())
            self.radiusEntry.setText(str(gpsradius))

class ListFilterOption(FilterOption):

    def __init__(self, parent):
        super().__init__("explicit file names", parent)
        self.entry = QtWidgets.QLineEdit()
        label = QtWidgets.QLabel("Files:")
        label.setBuddy(self.entry)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.entry)
        self.groupbox.setLayout(layout)

    def getOption(self):
        if self.groupbox.isChecked():
            return { 'files': self.entry.text().split() }
        else:
            return {}

    def setOption(self, filelist):
        super().setOption(filelist)
        if filelist is not None:
            self.entry.setText(" ".join(sorted(str(p) for p in filelist)))


class FilterDialog(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()

        mainLayout = QtWidgets.QVBoxLayout()

        self.tagFilterOption = TagFilterOption(mainLayout)
        self.selectFilterOption = SelectFilterOption(mainLayout)
        self.dateFilterOption = DateFilterOption(mainLayout)
        self.gpsFilterOption = GPSFilterOption(mainLayout)
        self.filelistFilterOption = ListFilterOption(mainLayout)

        btn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        buttonBox = QtWidgets.QDialogButtonBox(btn)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        mainLayout.addWidget(buttonBox, alignment=QtCore.Qt.AlignHCenter)

        self.setLayout(mainLayout)
        self.setWindowTitle("Filter options")

    def setfilter(self, imgFilter):
        self.imgFilter = imgFilter
        self.tagFilterOption.setOption(imgFilter.taglist, imgFilter.negtaglist)
        self.selectFilterOption.setOption(imgFilter.select)
        self.dateFilterOption.setOption(imgFilter.date)
        self.gpsFilterOption.setOption(imgFilter.gpspos, imgFilter.gpsradius)
        self.filelistFilterOption.setOption(imgFilter.filelist)

    def accept(self):
        filterArgs = {}
        filterArgs.update(self.tagFilterOption.getOption())
        filterArgs.update(self.selectFilterOption.getOption())
        filterArgs.update(self.dateFilterOption.getOption())
        filterArgs.update(self.gpsFilterOption.getOption())
        filterArgs.update(self.filelistFilterOption.getOption())
        self.imgFilter = photoidx.idxfilter.IdxFilter(**filterArgs)
        super().accept()
