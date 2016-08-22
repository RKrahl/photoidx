"""A dialog window to show some informations on the current image.
"""

from PySide import QtCore, QtGui


class ImageInfoDialog(QtGui.QDialog):

    def __init__(self):
        super(ImageInfoDialog, self).__init__()

        infoLayout = QtGui.QGridLayout()
        filenameLabel = QtGui.QLabel("File name:")
        self.filename = QtGui.QLabel()
        self.filename.setTextFormat(QtCore.Qt.PlainText)
        infoLayout.addWidget(filenameLabel, 0, 0)
        infoLayout.addWidget(self.filename, 0, 1)
        createDateLabel = QtGui.QLabel("Create date:")
        self.createDate = QtGui.QLabel()
        self.createDate.setTextFormat(QtCore.Qt.PlainText)
        infoLayout.addWidget(createDateLabel, 1, 0)
        infoLayout.addWidget(self.createDate, 1, 1)
        orientationLabel = QtGui.QLabel("Orientation:")
        self.orientation = QtGui.QLabel()
        self.orientation.setTextFormat(QtCore.Qt.PlainText)
        infoLayout.addWidget(orientationLabel, 2, 0)
        infoLayout.addWidget(self.orientation, 2, 1)
        gpsPositionLabel = QtGui.QLabel("GPS position:")
        self.gpsPosition = QtGui.QLabel()
        self.gpsPosition.setTextFormat(QtCore.Qt.PlainText)
        infoLayout.addWidget(gpsPositionLabel, 3, 0)
        infoLayout.addWidget(self.gpsPosition, 3, 1)

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(infoLayout)
        mainLayout.addWidget(buttonBox, alignment=QtCore.Qt.AlignHCenter)
        self.setLayout(mainLayout)
        self.setWindowTitle("Image Info")

    def setinfo(self, item):
        self.filename.setText(item.filename)
        if item.createDate:
            self.createDate.setText(item.createDate.strftime("%a, %x %X"))
        else:
            self.createDate.setText(None)
        if item.orientation:
            self.orientation.setText(item.orientation)
        else:
            self.orientation.setText(None)
        if item.gpsPosition:
            self.gpsPosition.setText(unicode(item.gpsPosition))
        else:
            self.gpsPosition.setText(None)
