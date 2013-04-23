# About
The program searches and prints addresses from the UCPH address book: http://www.ku.dk/vejviser/

# Todo
* [ ] Use a QValidator (regexp) on the case QLineEdit
* [ ] Allow the print menu to appear on clicking enter in the list
* [ ] Allow the use of alt-button to choose element
* [ ] Mark and select the first element (if any) in the list
* [ ] Improve the settings to show which folder i currently selected
* [ ] Run the GUI in a seperate thread to avoid freezing when searching
* [ ] Create an installer for the program
* [ ] Add an icon
* [ ] Possibly find a catchy name ;)

# Considerations
* Port the code to use TKInter instead to avoid having to use PyQT
* Clean up the way beautifulsoup is used and in general fix the dirty hacks in [adress_book.py](https://github.com/jfrdev/adresseprinter/blob/master/address_book.py)
* Move away from python completely and use C instead to improve performance
