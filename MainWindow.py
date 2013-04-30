import sys
import os
import codecs

from PySide import QtNetwork, QtCore, QtGui, QtXml, QtWebKit

import UiLoader
import AddressBook
import Printer

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        self.webpage = QtWebKit.QWebPage()
        self.document = self.webpage.mainFrame()
        self.settings = QtCore.QSettings('Adresseprinter')
        self.dir = self.settings.value('pdf_dir', os.path.expanduser('~') + os.sep + 'Desktop')
        self.contacts = {}
        self.printer = Printer.Printer()
        self.addressbook = AddressBook.AddressBook()

        self.file = codecs.open('data/template.html')
        self.html_template = self.file.read().decode('utf-8')
        self.file.close()

        QtGui.QMainWindow.__init__(self, parent)
        self.ui = UiLoader.loadUi('data/gui.ui', self)
        self.statusText = QtGui.QLabel("PDF gemmes i: \"" + self.dir + "\"")
        self.ui.statusBar.addWidget(self.statusText, 1)
        self.ui.caseText.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("\d*")))
        self.addSignals()

    def addSignals(self):
        QtCore.QObject.connect(self.ui.searchButton,
                QtCore.SIGNAL('clicked()'), self.search)
        QtCore.QObject.connect(self.ui.nameText,
                QtCore.SIGNAL("returnPressed()"), self.search)
        QtCore.QObject.connect(self.ui.deptText,
                QtCore.SIGNAL("returnPressed()"), self.search)
        QtCore.QObject.connect(self.ui.phoneText,
                QtCore.SIGNAL("returnPressed()"), self.search)
        QtCore.QObject.connect(self.ui.emailText,
                QtCore.SIGNAL("returnPressed()"), self.search)
        QtCore.QObject.connect(self.ui.funcText,
                QtCore.SIGNAL("returnPressed()"), self.search)

        QtCore.QObject.connect(self.ui.actionPDF,
                QtCore.SIGNAL('triggered()'), self.setPdfDir)

        QtCore.QObject.connect(self.ui.printButton,
                QtCore.SIGNAL('clicked()'), self.printAddress)
        QtCore.QObject.connect(self.ui.caseText,
                QtCore.SIGNAL("returnPressed()"), self.printAddress)

    def setPdfDir(self):
        self.dir = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if self.dir:
            self.settings.setValue('pdf_dir', self.dir)
            self.statusText.setText("PDF gemmes i: \"" + self.dir + "\"")

    def printAddress(self):
        index = self.ui.contactList.currentRow()
        html = self.addressbook.printContact(
            self.contacts[index],
            self.html_template,
            self.ui.caseBox.currentText(),
            self.ui.caseText.text()
            )
        self.document.setHtml(html)
        self.printer.print(self.document,
                           self.dir +
                           os.sep +
                           self.ui.caseBox.currentText() +
                           self.ui.caseText.text() +
                           '.pdf')

    def search(self):
        self.contacts = self.addressbook.getContacts(
                        self.ui.nameText.text(),
                        self.ui.deptText.text(),
                        self.ui.phoneText.text(),
                        self.ui.emailText.text(),
                        self.ui.funcText.text()
                        )
        self.clearSearch()
        self.drawList()
        if self.ui.contactList.count() > 0:
            self.ui.contactList.setCurrentRow(0)

    def clearSearch(self):
        self.ui.nameText.clear()
        self.ui.deptText.clear()
        self.ui.phoneText.clear()
        self.ui.emailText.clear()
        self.ui.funcText.clear()

    def drawList(self):
        self.ui.contactList.clear()
        for contact in self.contacts:
            self.ui.contactList.addItem(
                'Navn: ' + contact['Navn'] + '\n' +
                'Adresse: ' + contact['Adresse'] + '\n' +
                'Afdeling: ' + contact['Afdeling'] + '\n' +
                'Telefon: ' + contact['Telefon'])

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    QtGui.qApp = app
    myapp = MainWindow()
    myapp.show()
    app.exec_()
    QtGui.qApp = None