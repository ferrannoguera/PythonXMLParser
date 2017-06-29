#!/usr/bin/python3

import sys
import urllib.request

from html.parser import HTMLParser

allactes=[] 


#rest = eval (sys.argv[1])

class acte: 

    def afegir_nom(self,nom):
        self.nom = nom
        
        
# creem una subclasse i sobreescribim el metodes del han
class MHTMLParser(HTMLParser):
  cact = acte()
  ctag = ""
  def handle_starttag(self, tag, attrs):
    self.ctag = tag
    if tag == 'street':
      print ("Start tag: ", tag)

  def handle_endtag(self, tag):
    self.ctag = ""
    if tag == 'street':
      print ("End tag: ", tag)
  
  #def handle_data(self, data):
    #if self.ctag == 'height':
      #print ("Data: ", data)
    
  def unknown_decl(self, data):
    if self.ctag == 'street':
      print (data[6:])
         

         
f = urllib.request.urlopen('http://wservice.viabicing.cat/v1/getstations.php?v=1')
agenda = f.read().decode('utf-8')
f.close()

agendaHTML = MHTMLParser()
agendaHTML.feed(agenda)


print (allactes)



# creem una subclasse i sobreescribim el metodes del han class MHTMLParser(HTMLParser): cact = acte() ctag = "" def handle_starttag(self, tag, attrs): self.ctag = tag if tag == 'street': self.cact = acte() #print ("Start tag: ", tag) def handle_endtag(self, tag): self.ctag = "" if tag == 'street': allactes.append(self.cact) #print ("End tag: ", tag) #def handle_data(self, data): #if self.ctag == 'height': #print ("Data: ", data) def unknown_decl(self, data): if self.ctag == 'street': self.cact.afegir_nom(data[6:])