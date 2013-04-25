import sys
import os
import codecs
from PySide import QtCore, QtGui, QtNetwork, QtWebKit
from PySide.QtUiTools import QUiLoader

import address_book

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = QUiLoader().load('data/gui.ui', self)
        self.contacts = {}
        self.webpage = QtWebKit.QWebPage()
        self.document = self.webpage.mainFrame()
        self.printer = QtGui.QPrinter()
        self.printer.setPageMargins(20,20,20,20,QtGui.QPrinter.Millimeter)

        self.pdf = QtGui.QPrinter()
        self.pdf.setPageMargins(20,20,20,20,QtGui.QPrinter.Millimeter)
        self.pdf.setOutputFormat(QtGui.QPrinter.PdfFormat)

        self.settings = QtCore.QSettings('Adresseprinter')
        self.dir = self.settings.value('pdf_dir')
        self.ui.statusBar.showMessage("PDF is saved in: \"" + self.dir + "\"")

        self.file = codecs.open('data/template.html')
        self.html_template = self.file.read().decode('utf-8')
        self.file.close()

        self.regex = QtCore.QRegExp("\d*")
        self.validator=QtGui.QRegExpValidator(self.regex, self.ui.caseText)

        self.ui.caseText.setValidator(self.validator)

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
                QtCore.SIGNAL('clicked()'), self.print)
        QtCore.QObject.connect(self.ui.caseText,
                QtCore.SIGNAL("returnPressed()"), self.print)

    def setPdfDir(self):
        self.dir = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.settings.setValue('pdf_dir', self.dir)
        self.statusBar.showMessage("PDF is saved in: \"" + self.dir + "\"")

    def print(self):
        index = self.ui.contactList.currentRow()
        html = address_book.print_contact(
            self.contacts[index],
            self.html_template,
            self.ui.caseBox.currentText(),
            self.ui.caseText.text()
            )
        self.document.setHtml(html)
        dialog = QtGui.QPrintDialog(self.printer, self)
        if(dialog.exec_() == QtGui.QDialog.Accepted):
            self.pdf.setOutputFileName(
                self.dir +
                os.sep +
                self.ui.caseBox.currentText() +
                self.ui.caseText.text() +
                '.pdf')
            self.document.print(self.pdf)
            self.document.print(self.printer)

    def search(self):
        self.contacts = address_book.get_contacts(
                        self.ui.nameText.text(),
                        self.ui.deptText.text(),
                        self.ui.phoneText.text(),
                        self.ui.emailText.text(),
                        self.ui.funcText.text()
                        )
        self.clear_search()
        self.draw_list()
        if self.ui.contactList.count() > 0:
            self.ui.contactList.setCurrentRow(0)

    def clear_search(self):
        self.ui.nameText.clear(),
        self.ui.deptText.clear(),
        self.ui.phoneText.clear(),
        self.ui.emailText.clear(),
        self.ui.funcText.clear()


    def draw_list(self):
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