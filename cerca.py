#!/usr/bin/python3
# -*- coding: utf-8 -*- 

#------------------------------------------------
#                                               |
# Practica Realitzada per: FERRAN NOGUERA VALL  |
#                                               |
#------------------------------------------------

import sys
import csv
import math
import unicodedata
import urllib.request
import operator
import re
import argparse

from ast import literal_eval
from datetime import datetime, timedelta
from html.parser import HTMLParser


parser = argparse.ArgumentParser()
parser.add_argument("--key",help="Use --key [Values]")
parser.add_argument("--date",help="Use --key [Dates]")



actestotals=[]
actesfiltrats = []
allbic = []
allpark = []


class park:
  def afegir_nom(self,dades):
    self.nom = dades
  def afegir_longitud(self,dades):
    self.longitud = dades
  def afegir_latitud(self,dades):
    self.latitud = dades
    
class parkHTMLParser(HTMLParser):
  cpark = park()
  ctag = ""
  def handle_starttag(self,tag,attrs):
    self.ctag = tag
    if tag == 'row':
      self.cpark = park()
  def handle_endtag(self,tag):
    self.ctag = ""
    if tag == 'row':
      allpark.append(self.cpark)
      
  def unknown_decl(self,data):
    if self.ctag == 'name':
      self.cpark.afegir_nom(data[6:])
    if self.ctag == 'gmapx':
      self.cpark.afegir_latitud(data[6:])
    if self.ctag == 'gmapy':
      self.cpark.afegir_longitud(data[6:])

url = 'http://www.bcn.cat/tercerlloc/Aparcaments.xml'
p = urllib.request.urlopen(url)
parkread = p.read().decode('utf-8')
p.close()

parkHTML = parkHTMLParser()
parkHTML.feed(parkread)



class bicing: 
    def afegir_idd(self,dades):
        self.idd = dades
    def afegir_latitud(self,dades):
        self.latitud = dades
    def afegir_longitud(self,dades):
        self.longitud = dades
    def afegir_bicis(self,dades):
        self.bicis = dades
    def afegir_places(self,dades):
        self.places = dades
        
class bicingHTMLParser(HTMLParser):

    cbic = bicing()
    ctag = ""

    def handle_starttag(self, tag, attrs):
        self.ctag = tag
        if tag == 'station':
            self.cbic = bicing()

    def handle_endtag(self, tag):
        self.ctag = ""
        if tag == 'station':
            allbic.append(self.cbic)

    def handle_data(self, data):
        if self.ctag == 'id':
            self.cbic.afegir_idd(data)
        if self.ctag == 'lat':
            self.cbic.afegir_latitud(data)
        if self.ctag == 'long':
            self.cbic.afegir_longitud(data)
        if self.ctag == 'bikes':
            self.cbic.afegir_bicis(data)
        if self.ctag == 'slots':
            self.cbic.afegir_places(data)

url = 'http://wservice.viabicing.cat/v1/getstations.php?v=1'
b = urllib.request.urlopen(url)
bicread = b.read().decode('utf-8')
b.close()

bicHTML = bicingHTMLParser()
bicHTML.feed(bicread)


class acte(object):
  name = ""
  address = ""
  date_ini = ""
  date_fi = ""
  hour = ""
  latitud = ""
  longitud = ""
  barri = ""
  
  def afegir_name(self, dades):
    self.name = dades    
  def afegir_address(self, dades):
    self.address = dades    
  def afegir_dataini(self, dades):
    self.date_ini = dades 
  def afegir_datafi(self, dades):
    self.date_fi = dades
  def afegir_hora(self, dades):
    self.hour = dades
  def afegir_latitud(self, dades):
    self.latitud = dades 
  def afegir_longitud(self, dades):
    self.longitud = dades   
  def afegir_barri(self, dades):
    self.barri = dades
      
class acteHTMLParser(HTMLParser):
  cacte = acte()
  ctag = ""
  
  def handle_starttag(self, tag, attrs):
    self.ctag = tag
    if tag == 'row':
      self.cacte = acte()      
      
  def handle_endtag(self,tag):
    self.ctag = ""
    if tag == 'row':
      actestotals.append(self.cacte)
      
  def unknown_decl(self,data):
    if self.ctag == 'name':
      self.cacte.afegir_name(data[6:])
    if self.ctag == 'address':
      self.cacte.afegir_address(data[6:])
    if self.ctag == 'date':
      self.cacte.afegir_dataini(data[6:])
      self.cacte.afegir_datafi(data[6:])
    if self.ctag == 'begindate':
      self.cacte.afegir_dataini(data[6:])
    if self.ctag == 'enddate':
      self.cacte.afegir_datafi(data[6:])
    if self.ctag == 'proxhour':
      self.cacte.afegir_hora(data[6:])
    if self.ctag == 'gmapx':
      self.cacte.afegir_latitud(data[6:])
    if self.ctag == 'gmapy':
      self.cacte.afegir_longitud(data[6:])
    if self.ctag == 'barri':
      self.cacte.afegir_barri(data[6:])
      
url = 'http://www.bcn.cat/tercerlloc/agenda_cultural.xml'
a = urllib.request.urlopen(url)
actread = a.read().decode('utf-8')
a.close()

actHTML = acteHTMLParser()
actHTML.feed(actread)
      

def byesigns(nom):
  return(re.sub('[^0-9a-zA-Z]+', ' ', nom))

def byeaccents(nom):
  return(''.join((c
                  for c in unicodedata.normalize('NFD', nom) 
                  if unicodedata.category(c) != 'Mn')))
  
      
def evaluarestr(nom1,nom2,nom3,comp):
  if isinstance(comp, str):
    added = " "+comp+" "
    un =byeaccents(added.lower()) in byesigns(byeaccents(nom3.lower()))
    if un:
      return un
    un =byeaccents(added.lower()) in byesigns(byeaccents(nom1.lower()))
    if un:
      return un
    un =byeaccents(added.lower()) in byesigns(byeaccents(nom2.lower()))
    return un
    
  if isinstance(comp, list):
    for k in comp:
      if not evaluarestr(nom1,nom2,nom3, k):
        return False
    return True
  if isinstance(comp, tuple):
    for l in comp:
      if evaluarestr(nom1,nom2,nom3, l):
        return True
    return False


def interval(ini,fi,actual, i):
  if (ini<=actual<=fi):
    return True
  compare = actual + timedelta(days=i)
  if (actual > fi and compare <=fi):
    return True
  if (actual < ini and compare >=ini):
    return True
  return False

def evaluarmesdunadata(ini,fi,rest):
  if isinstance(rest,str):
    rest = datetime.strptime(rest, "%d/%m/%Y")
    return ini<=rest<=fi
  if isinstance(rest,tuple):
    act = datetime.strptime(rest[0], "%d/%m/%Y")
    if interval(ini,fi,act,rest[1]):
      return True
    if interval(ini,fi,act,rest[2]):
      return True   
  if isinstance(rest,list):
    for x in rest:
      if evaluarmesdunadata(ini,fi,x):
        return True
    return False
  return False


ordenar = False
filtrar = False
onemore = False
if(len(sys.argv) == 1):
  actesfiltrats = actestotals
if(len(sys.argv) == 3):
  filtrar = True
  fderest = eval("sys.argv[1]")
  restriccio = eval(sys.argv[2])
if(len(sys.argv) == 5):
  filtrar = True
  onemore = True
  fderest = eval("sys.argv[1]")
  restriccio = eval(sys.argv[2])
  fderest2 = eval("sys.argv[3]")
  restriccio2 = eval(sys.argv[4])
  
if (filtrar):
  for acttractant in actestotals:
      nomact = " "+acttractant.name+" "
      nomaddress = " "+acttractant.address+" "
      nombarri = " "+acttractant.barri+" "
      datatractini = acttractant.date_ini
      datatractfi = acttractant.date_fi
      if onemore:
        candidate = []
        if (fderest == "--key"):
          if evaluarestr(nomact,nomaddress,nombarri,restriccio):
            candidate = acttractant
        if (fderest == "--date"):
          ordenar = True 
          s = 'Acte Permanent'
          if datatractini == s or datatractfi == s:
            candidate = acttractant
          else:
            if datatractini == datatractfi:
              comps = datetime.strptime(datatractini, "%d/%m/%Y")
              if evaluarmesdunadata(comps,comps,restriccio):
                candidate = acttractant
            else:
              comps = datetime.strptime(datatractini, "%d/%m/%Y")
              compe = datetime.strptime(datatractfi, "%d/%m/%Y")
              if evaluarmesdunadata(comps,compe,restriccio):
                candidate = acttractant
      
      
        if (fderest2 == "--key"):
          if evaluarestr(nomact,nomaddress,nombarri,restriccio2):
            if candidate == acttractant:
              actesfiltrats.append(candidate)
        if (fderest2 == "--date"):
          ordenar = True 
          s = 'Acte Permanent'
          if datatractini == s or datatractfi == s:
            if candidate == acttractant:
              actesfiltrats.append(candidate)
          else:
            if datatractini == datatractfi:
              comps = datetime.strptime(datatractini, "%d/%m/%Y")
              if evaluarmesdunadata(comps,comps,restriccio2):
                if candidate == acttractant:
                  actesfiltrats.append(candidate)
            else:
              comps = datetime.strptime(datatractini, "%d/%m/%Y")
              compe = datetime.strptime(datatractfi, "%d/%m/%Y")
              if evaluarmesdunadata(comps,compe,restriccio2):
                if candidate == acttractant:
                  actesfiltrats.append(candidate)
      
  
      else:
        if (fderest == "--key"):
          if evaluarestr(nomact,nomaddress,nombarri,restriccio):
            actesfiltrats.append(acttractant)
        if (fderest == "--date"):
          ordenar = True 
          s = 'Acte Permanent'
          if datatractini == s or datatractfi == s:
            actesfiltrats.append(acttractant)
          else:
            if datatractini == datatractfi:
              comps = datetime.strptime(datatractini, "%d/%m/%Y")
              if evaluarmesdunadata(comps,comps,restriccio):
                actesfiltrats.append(acttractant)
            else:
              comps = datetime.strptime(datatractini, "%d/%m/%Y")
              compe = datetime.strptime(datatractfi, "%d/%m/%Y")
              if evaluarmesdunadata(comps,compe,restriccio):
                actesfiltrats.append(acttractant)

if ordenar:
  actesfiltrats=sorted(
    actesfiltrats,
    key=operator.attrgetter('date_ini')
    )


def diskm(lat1, long1, lat2, long2):
  pararads = math.pi/180.0
  
  phi1 = (90.0 - lat1)*pararads
  phi2 = (90.0 - lat2)*pararads
 
  theta1 = long1*pararads
  theta2 = long2*pararads
 
  cos = (math.sin(phi1)
         * math.sin(phi2)
         * math.cos(theta1 - theta2) 
         + math.cos(phi1)*math.cos(phi2)
         )
  
  arc = math.acos( cos ) *6373
  return arc



f = open('taula actes.html', 'w')
f.write("""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 10px;
}
table tr:nth-child(even) {
    background-color: #eee;
}
table tr:nth-child(odd) {
   background-color:#fff;
}
</style>
</head>
<body>

<table style="width:100%">""")

sl = """
"""
f.write(sl+"<tr>")

header = [
  "Nom",
  "Adreça",
  "Barri",
  "Dia Inici",
  "Dia Fi",
  "Hora",
  "Bicing amb Aparcament",
  "Bicing amb bicis disponibles",
  "Parking"
  ]

for data in header:
  f.write(sl+"""<th style="min-width:150px">"""+data+"</th>")
f.write(sl+"</tr>")


for r in actesfiltrats:
  bicparking = []
  bicdisponibles = []
  if r.latitud == "":
    r.latitud = "0.0"
  if r.longitud == "":
    r.longitud = "0.0"
  latact = float(r.latitud)
  lonact = float(r.longitud)
  for b in allbic:
    distancia = diskm(latact,lonact,float(b.latitud),float(b.longitud))
    if (0.5 >= distancia):
      if int(b.bicis) > 0:
        bicdisponibles.append((distancia,b.idd))
      if int(b.places) > 0:
        bicparking.append((distancia,b.idd))
  bicparking.sort()
  bicparking = bicparking[0:5]
  bicdisponibles.sort()
  bicdisponibles = bicdisponibles[0:5]
  parkdisponible = []
  for p in allpark:
    distp = diskm(latact,lonact,float(p.latitud),float(p.longitud))
    if (0.5 >= distp):
      parkdisponible.append((distp,p.nom))
  parkdisponible.sort()
  parkdisponible = parkdisponible[0:5]
  f.write(sl+"<tr>")
  f.write(sl+"<td>"+r.name+"</td>")
  f.write(sl+"<td>"+r.address+"</td>")
  f.write(sl+"<td>"+r.barri+"</td>")
  f.write(sl+"<td>"+r.date_ini+"</td>")
  f.write(sl+"<td>"+r.date_fi+"</td>")
  f.write(sl+"<td>"+r.hour+"</td>")
  count = 0
  f.write(sl+"<td>")
  for parquing in bicparking:
    if count != 0:
      f.write(sl+"<br>")
    f.write(parquing[1])
    count += 1
  f.write(sl+"</td>"+sl+"<td>")
  count = 0
  for parquing in bicdisponibles:
    if count != 0:
      f.write(sl+"<br>")
    f.write(parquing[1])
    count += 1
  f.write(sl+"</td>"+sl+"<td>")
  count = 0
  for par in parkdisponible:
    if count != 0:
      f.write(sl+" //")
      f.write(sl+"<br>")
    f.write(par[1])
    count+=1
  f.write(sl+"</td>"+sl+"</tr>")
f.write(sl+"</table>"+sl+sl+"</body>"+sl+"</html>")
f.close    
      