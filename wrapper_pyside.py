import sys
import os
import codecs

from PySide import QtNetwork, QtCore, QtGui, QtXml
from PySide.QtCore import Slot, QMetaObject, QSettings, QRegExp, QObject
from PySide.QtUiTools import QUiLoader
from PySide.QtGui import QApplication, QMainWindow, QPrinter, QRegExpValidator, QFileDialog, QPrintDialog, QDialog, qApp
from PySide.QtWebKit import QWebPage
from PySide.QtUiTools import QUiLoader

import address_book

class UiLoader(QUiLoader):
    def __init__(self, baseinstance):
        QUiLoader.__init__(self, baseinstance)
        self.baseinstance = baseinstance

    def createWidget(self, class_name, parent=None, name=''):
        if parent is None and self.baseinstance:
            # supposed to create the top-level widget, return the base instance
            # instead
            return self.baseinstance
        else:
            # create a new widget for child widgets
            widget = QUiLoader.createWidget(self, class_name, parent, name)
            if self.baseinstance:
                # set an attribute for the new child widget on the base
                # instance, just like PyQt4.uic.loadUi does.
                setattr(self.baseinstance, name, widget)
            return widget

def loadUi(uifile, baseinstance=None):
    loader = UiLoader(baseinstance)
    widget = loader.load(uifile)
    QMetaObject.connectSlotsByName(widget)
    return widget

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = loadUi('data/gui.ui', self)
        self.contacts = {}
        self.webpage = QWebPage()
        self.document = self.webpage.mainFrame()
        self.printer = QPrinter()
        self.printer.setPageMargins(20, 20, 20, 20, QPrinter.Millimeter)

        self.pdf = QPrinter()
        self.pdf.setPageMargins(20, 20, 20, 20, QPrinter.Millimeter)
        self.pdf.setOutputFormat(QPrinter.PdfFormat)

        self.settings = QSettings('Adresseprinter')
        self.dir = self.settings.value('pdf_dir', os.path.expanduser('~') + os.sep + 'Desktop' + os.sep)
        self.ui.statusBar.showMessage("PDF is saved in: \"" + self.dir + "\"")

        self.file = codecs.open('data/template.html')
        self.html_template = self.file.read().decode('utf-8')
        self.file.close()

        self.regex = QRegExp("\d*")
        self.validator = QRegExpValidator(self.regex, self.ui.caseText)

        self.ui.caseText.setValidator(self.validator)

        self.addSignals()

    def addSignals(self):
        QObject.connect(self.ui.searchButton,
                QtCore.SIGNAL('clicked()'), self.search)
        QObject.connect(self.ui.nameText,
                QtCore.SIGNAL("returnPressed()"), self.search)
        QObject.connect(self.ui.deptText,
                QtCore.SIGNAL("returnPressed()"), self.search)
        QObject.connect(self.ui.phoneText,
                QtCore.SIGNAL("returnPressed()"), self.search)
        QObject.connect(self.ui.emailText,
                QtCore.SIGNAL("returnPressed()"), self.search)
        QObject.connect(self.ui.funcText,
                QtCore.SIGNAL("returnPressed()"), self.search)

        QObject.connect(self.ui.actionPDF,
                QtCore.SIGNAL('triggered()'), self.setPdfDir)

        QObject.connect(self.ui.printButton,
                QtCore.SIGNAL('clicked()'), self.print)
        QObject.connect(self.ui.caseText,
                QtCore.SIGNAL("returnPressed()"), self.print)

    def setPdfDir(self):
        self.dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
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
        dialog = QPrintDialog(self.printer, self)
        if(dialog.exec_() == QDialog.Accepted):
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
    app = QApplication(sys.argv)
    QtGui.qApp = app
    myapp = MainWindow()
    myapp.show()
    app.exec_()
    QtGui.qApp = None