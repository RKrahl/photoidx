"""A dialog window to show some informations on the current image.
"""

from PySide2 import QtCore, QtWidgets
from photoidx.exif import Exif


class ImageInfoDialog(QtWidgets.QDialog):

    def __init__(self, basedir):
        super().__init__()
        self.basedir = basedir

        infoLayout = QtWidgets.QGridLayout()
        cameraModelLabel = QtWidgets.QLabel("Camera model:")
        self.cameraModel = QtWidgets.QLabel()
        self.cameraModel.setTextFormat(QtCore.Qt.PlainText)
        infoLayout.addWidget(cameraModelLabel, 0, 0)
        infoLayout.addWidget(self.cameraModel, 0, 1)
        filenameLabel = QtWidgets.QLabel("File name:")
        self.filename = QtWidgets.QLabel()
        self.filename.setTextFormat(QtCore.Qt.PlainText)
        infoLayout.addWidget(filenameLabel, 1, 0)
        infoLayout.addWidget(self.filename, 1, 1)
        createDateLabel = QtWidgets.QLabel("Create date:")
        self.createDate = QtWidgets.QLabel()
        self.createDate.setTextFormat(QtCore.Qt.PlainText)
        infoLayout.addWidget(createDateLabel, 2, 0)
        infoLayout.addWidget(self.createDate, 2, 1)
        orientationLabel = QtWidgets.QLabel("Orientation:")
        self.orientation = QtWidgets.QLabel()
        self.orientation.setTextFormat(QtCore.Qt.PlainText)
        infoLayout.addWidget(orientationLabel, 3, 0)
        infoLayout.addWidget(self.orientation, 3, 1)
        gpsPositionLabel = QtWidgets.QLabel("GPS position:")
        self.gpsPosition = QtWidgets.QLabel()
        self.gpsPosition.setTextFormat(QtCore.Qt.RichText)
        self.gpsPosition.setOpenExternalLinks(True)
        infoLayout.addWidget(gpsPositionLabel, 4, 0)
        infoLayout.addWidget(self.gpsPosition, 4, 1)
        exposureTimeLabel = QtWidgets.QLabel("Exposure time:")
        self.exposureTime = QtWidgets.QLabel()
        self.exposureTime.setTextFormat(QtCore.Qt.PlainText)
        infoLayout.addWidget(exposureTimeLabel, 5, 0)
        infoLayout.addWidget(self.exposureTime, 5, 1)
        apertureLabel = QtWidgets.QLabel("F-number:")
        self.aperture = QtWidgets.QLabel()
        self.aperture.setTextFormat(QtCore.Qt.PlainText)
        infoLayout.addWidget(apertureLabel, 6, 0)
        infoLayout.addWidget(self.aperture, 6, 1)
        isoLabel = QtWidgets.QLabel("ISO speed rating:")
        self.iso = QtWidgets.QLabel()
        self.iso.setTextFormat(QtCore.Qt.PlainText)
        infoLayout.addWidget(isoLabel, 7, 0)
        infoLayout.addWidget(self.iso, 7, 1)
        focalLengthLabel = QtWidgets.QLabel("Focal length:")
        self.focalLength = QtWidgets.QLabel()
        self.focalLength.setTextFormat(QtCore.Qt.PlainText)
        infoLayout.addWidget(focalLengthLabel, 8, 0)
        infoLayout.addWidget(self.focalLength, 8, 1)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(infoLayout)
        mainLayout.addWidget(buttonBox, alignment=QtCore.Qt.AlignHCenter)
        self.setLayout(mainLayout)
        self.setWindowTitle("Image Info")

    def setinfo(self, item):
        exifdata = Exif(self.basedir / item.filename)
        self.cameraModel.setText(str(exifdata.cameraModel))
        self.filename.setText(str(item.filename))
        if item.createDate:
            self.createDate.setText(item.createDate.strftime("%a, %x %X"))
        else:
            self.createDate.setText(None)
        if item.orientation:
            self.orientation.setText(item.orientation)
        else:
            self.orientation.setText(None)
        pos = item.gpsPosition
        if pos:
            link = "<a href='%s'>%s</a>" % (pos.as_osmurl(), str(pos))
            self.gpsPosition.setText(link)
        else:
            self.gpsPosition.setText(None)
        self.exposureTime.setText(str(exifdata.exposureTime))
        self.aperture.setText(str(exifdata.aperture))
        self.iso.setText(str(exifdata.iso))
        self.focalLength.setText(str(exifdata.focalLength))
