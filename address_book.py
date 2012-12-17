import http.client
import urllib.request, urllib.parse, urllib.error
from codecs import Codec
from bs4 import BeautifulSoup
import datetime

MAXPOS=60

def get_contacts(name, dept, tlf, email, func):
    return _parse_contacts(_get_raw(name, dept, tlf, email, func, 'DK'))

def print_contact(cont, html, case_type, case_no):
    address = list(map(_strip, cont['Adresse'].split(':')))
    while len(address) < 3:
        address.append('')

    return html.format(
        cont['Navn'],
        address[0],
        address[1],
        address[2],
        cont['Lokation'],
        cont['Afdeling'],
        case_type,
        case_no,
        datetime.date.today().strftime('%d-%m-%Y'))

def _strip(str): return str.strip()

def _get_raw(name, dept, tlf, email, func, lang):
    host = 'www2.adm.ku.dk'
    pos = 0
    raw = ''
    conn = http.client.HTTPConnection(host)

    while pos < MAXPOS:
        body = urllib.parse.urlencode({
            'p_navn': name.encode('iso-8859-1'),
            'p_afdeling': dept.encode('iso-8859-1'),
            'p_telefon': tlf.encode('iso-8859-1'),
            'p_email': email.encode('iso-8859-1'),
            'p_funktion': func.encode('iso-8859-1'),
            'p_sprog': lang,
            'p_pos': pos
        })

        conn.request('POST', '/selv/pls/STB_WWW25.soegning_res4', body, {
            'Host': host
        })

        resp = conn.getresponse().read()
        soup = BeautifulSoup(resp)
        raw = raw + ''.join(soup.findAll(text=True))

        if soup.body.select('form') != []:
            pos = pos+10
        else: # No more pages set pos to be greater than MAXPOS
            pos = MAXPOS

    conn.close()
    return raw

def _parse_contacts(raw):
    lines = filter(None, map(_strip, raw.splitlines()))
    lines_res = []

    for line in lines:
        if 'Adresse' in line:
            address = line.split(':')[1].strip()
            line = next(lines)

            while line.startswith(':'):
                address = address + ' : ' + line.split(':')[1].strip()
                line = next(lines)
            lines_res[n]['Adresse'] = address

        if 'Navn' in line:
            n = len(lines_res)
            name = line.split(':')[1].strip()
            lines_res.append({'Navn':name})
            lines_res[n]['Adresse'] = ''
            lines_res[n]['Lokation'] = ''
            lines_res[n]['Afdeling'] = ''
            lines_res[n]['Telefon'] = ''

        elif ('Lokation' in line) or \
             ('Afdeling' in line) or \
             ('Telefon' in line):
            linelist = list(map(_strip, line.split(':')))
            if len(linelist) > 1 and len(linelist[1]) > 0:
                lines_res[n][linelist[0]] = linelist[1]

    return lines_res
