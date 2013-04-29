from PySide import QtGui

class Printer():
    def __init__(self):
        self.printer = QtGui.QPrinter()
        self.printer.setPageMargins(20, 20, 20, 20, QtGui.QPrinter.Millimeter)

        self.pdf = QtGui.QPrinter()
        self.pdf.setPageMargins(20, 20, 20, 20, QtGui.QPrinter.Millimeter)
        self.pdf.setOutputFormat(QtGui.QPrinter.PdfFormat)

    def print(self, document, output):
        dialog = QtGui.QPrintDialog(self.printer)
        if(dialog.exec_() == QtGui.QDialog.Accepted):
            self.pdf.setOutputFileName(output)
            document.print(self.printer)
            document.print(self.pdf)