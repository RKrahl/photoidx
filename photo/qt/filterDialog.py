"""A dialog window to change the filter options.
"""

from PySide import QtCore, QtGui
import photo.idxfilter
from photo.geo import GeoPosition


class GeoPosEdit(QtGui.QLineEdit):
    """A QLineEdit with a suitable size for a GeoPosition.
    """
    def sizeHint(self):
        sh = super(GeoPosEdit, self).sizeHint()
        fm = self.fontMetrics()
        postext = u"\u2014%s\u2014" % GeoPosition("90.0 S, 180.0 E").floatstr()
        sh.setWidth(fm.boundingRect(postext).width())
        return sh


class FilterOption(object):

    def __init__(self, criterion, parent):
        self.groupbox = QtGui.QGroupBox("Filter by %s" % criterion)
        self.groupbox.setCheckable(True)
        parent.addWidget(self.groupbox)

    def setOption(self, optionValue):
        self.groupbox.setChecked(optionValue is not None)

class TagFilterOption(FilterOption):

    def __init__(self, parent):
        super(TagFilterOption, self).__init__("tags", parent)
        self.entry = QtGui.QLineEdit()
        label = QtGui.QLabel("Tags:")
        label.setBuddy(self.entry)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.entry)
        self.groupbox.setLayout(layout)

    def setOption(self, taglist, negtaglist):
        super(TagFilterOption, self).setOption(taglist)
        if taglist is not None:
            tags = sorted(taglist)
            negtags = ["!%s" % t for t in sorted(negtaglist)]
            self.entry.setText(",".join(tags + negtags))

class SelectFilterOption(FilterOption):

    def __init__(self, parent):
        super(SelectFilterOption, self).__init__("selection", parent)
        self.buttonYes = QtGui.QRadioButton("selected")
        self.buttonNo = QtGui.QRadioButton("not selected")
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.buttonYes)
        layout.addWidget(self.buttonNo)
        self.groupbox.setLayout(layout)

    def setOption(self, select):
        super(SelectFilterOption, self).setOption(select)
        if select is not None:
            if select:
                self.buttonYes.setChecked(QtCore.Qt.Checked)
                self.buttonNo.setChecked(QtCore.Qt.Unchecked)
            else:
                self.buttonYes.setChecked(QtCore.Qt.Unchecked)
                self.buttonNo.setChecked(QtCore.Qt.Checked)

class DateFilterOption(FilterOption):

    def __init__(self, parent):
        super(DateFilterOption, self).__init__("date", parent)
        self.startEntry = QtGui.QLineEdit()
        startLabel = QtGui.QLabel("Start:")
        startLabel.setBuddy(self.startEntry)
        self.endEntry = QtGui.QLineEdit()
        endLabel = QtGui.QLabel("End:")
        endLabel.setBuddy(self.endEntry)
        layout = QtGui.QGridLayout()
        layout.addWidget(startLabel, 0, 0)
        layout.addWidget(self.startEntry, 0, 1)
        layout.addWidget(endLabel, 1, 0)
        layout.addWidget(self.endEntry, 1, 1)
        self.groupbox.setLayout(layout)

    def setOption(self, date):
        super(DateFilterOption, self).setOption(date)
        if date is not None:
            self.startEntry.setText(date[0].isoformat())
            self.endEntry.setText(date[1].isoformat())

class GPSFilterOption(FilterOption):

    def __init__(self, parent):
        super(GPSFilterOption, self).__init__("GPS position", parent)
        self.posEntry = GeoPosEdit()
        posLabel = QtGui.QLabel("Position:")
        posLabel.setBuddy(self.posEntry)
        self.radiusEntry = QtGui.QLineEdit()
        radiusLabel = QtGui.QLabel("Radius:")
        radiusLabel.setBuddy(self.radiusEntry)
        layout = QtGui.QGridLayout()
        layout.addWidget(posLabel, 0, 0)
        layout.addWidget(self.posEntry, 0, 1)
        layout.addWidget(radiusLabel, 1, 0)
        layout.addWidget(self.radiusEntry, 1, 1)
        self.groupbox.setLayout(layout)

    def setOption(self, gpspos, gpsradius):
        super(GPSFilterOption, self).setOption(gpspos)
        if gpspos is not None:
            self.posEntry.setText(gpspos.floatstr())
            self.radiusEntry.setText(str(gpsradius))

class ListFilterOption(FilterOption):

    def __init__(self, parent):
        super(ListFilterOption, self).__init__("explicit file names", parent)
        self.entry = QtGui.QLineEdit()
        label = QtGui.QLabel("Files:")
        label.setBuddy(self.entry)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.entry)
        self.groupbox.setLayout(layout)

    def setOption(self, filelist):
        super(ListFilterOption, self).setOption(filelist)
        if filelist is not None:
            self.entry.setText(" ".join(sorted(filelist)))


class FilterDialog(QtGui.QDialog):

    def __init__(self):
        super(FilterDialog, self).__init__()

        optionsLayout = QtGui.QVBoxLayout()

        self.tagFilterOption = TagFilterOption(optionsLayout)
        self.selectFilterOption = SelectFilterOption(optionsLayout)
        self.dateFilterOption = DateFilterOption(optionsLayout)
        self.gpsFilterOption = GPSFilterOption(optionsLayout)
        self.filelistFilterOption = ListFilterOption(optionsLayout)

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
        self.tagFilterOption.setOption(imgFilter.taglist, imgFilter.negtaglist)
        self.selectFilterOption.setOption(imgFilter.select)
        self.dateFilterOption.setOption(imgFilter.date)
        self.gpsFilterOption.setOption(imgFilter.gpspos, imgFilter.gpsradius)
        self.filelistFilterOption.setOption(imgFilter.filelist)

