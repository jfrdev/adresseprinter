# About
The program searches and prints addresses from the UCPH address book: http://www.ku.dk/vejviser/

# Bugs
* ~~Some addresses does not show correctly (e.g. Daniel Noesgaard which becomes one line and with an extra newline afterwards)~~
    * Not completely fixed but since the error lies with the user using the address field wrong, nothing more can be done
    * Newlines are removed
    * Addresses containing a comma will be kept that way since we have no way of knowing wheter it was intentional or a mistake

# Todo
* [x] Use a QValidator (regexp) on the case QLineEdit
* [x] Mark and select the first element (if any) in the list
* [x] Improve the settings to show which folder is currently selected
* [x] Create an installer for the program
* [x] Add an icon
* [ ] Allow the print menu to appear on clicking enter in the list
* [ ] Allow the use of alt-button to choose element
* [ ] Run the GUI in a seperate thread to avoid freezing when searching
* [ ] Possibly find a catchy name ;)

# Considerations
* Port the code to use TKInter instead to avoid having to use PyQT
* Clean up the way beautifulsoup is used and in general fix the dirty hacks in [AdressBook.py](https://github.com/jfrdev/adresseprinter/blob/master/AddressBook.py)
* Move away from python completely and use C instead to improve performance (This is an entire project in itself)
