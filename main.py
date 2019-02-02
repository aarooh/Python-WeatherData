# -*- coding: utf-8 -*- 
import svgwrite     
                                            
class saatieto:                                                 
    paivamaara = ""
    sademaara = 0
    keskilampo = 0
    alinlampo = 0
    ylinlampo = 0
    
def valikko():
    print()
    print("Säätietojen käsittely")
    print("*******************************************************")
    print("1) Lataa kaupungin säätiedot tiedostosta")
    print("2) Laske keskiarvo kuukauden lämpötiloista")
    print("3) Laske kuukauden lämpötilojen minimi ja maksimi")
    print("4) Tallenna kuukauden tiedot tiedostoon")
    print("5) Piirrä graafi kuukauden lämpötiloista kaupungissa")
    print("6) Lataa toiset säätiedot ja piirrä vertailugraafi")
    print("0) Lopeta")
    valinta = int(input("Valintasi: "))
    return valinta


def tietojenlataus():                                           
    kaupunki = input("Anna tiedostonimi: ")                     #Kysytään käyttäjältä .csv tiedosto
    kaupunkinimi = kaupunki[:-4].capitalize()                   
    tiedosto = open(kaupunki, "r", encoding = "utf-8")          
    lista = []                                                  #Alustetaan lista säätiedoille
    for rivi in tiedosto:
        rivi = rivi.split(";")
        tieto = saatieto()
        tieto.paivamaara = rivi[0]
        tieto.sademaara = rivi[1]
        tieto.keskilampo = rivi[2]
        tieto.alinlampo = rivi[3]
        tieto.ylinlampo = rivi[4]
        lista.append(tieto)
    tiedosto.close()
    lista.pop(0)
    print("Tiedoston luku onnistui.")
    return lista, kaupunkinimi                                  #Palautetaan lista ja kaupungin nimi pääohjelmaan
    
def keskiarvo(lista):                                          #Lasketaan keskilämpötila listan säätietojen avulla
    summa = 0                                                   
    lukumaara = 0                                              
    for arvo in lista:
        summa = summa + float(arvo.keskilampo)
        lukumaara = len(lista)
    keskiarvo = summa/lukumaara
    print("Kuukauden lämpötilan keskiarvo:", "{0:.1f}".format(keskiarvo))


def minimijamaksimi(lista):                                       #lasketaan minimi ja maksimi lämpötilat.              
    minmaxlista = []
    for arvo in lista:                                          
        minmaxlista.append(float(arvo.alinlampo))
        minmaxlista.append(float(arvo.ylinlampo))
    print("Kuukauden lämpötilan minimi:", min(minmaxlista))
    print("Kuukauden lämpötilan maksimi:", max(minmaxlista))


def tietojentallennus(lista, kaupunkinimi):                     #Tallennetaan tiedostoon säätiedot
    tiedostonnimi = input("Anna tiedostonimi: ")               
    tiedosto = open(tiedostonnimi, "w", encoding = "utf-8")
    
    #Kerätään tietoja tiedostoon tallennustavarten                                                            
    summa = 0
    lukumaara = 0
    for arvo in lista:
        summa = summa + float(arvo.keskilampo)
        lukumaara = len(lista)
    keskiarvo = summa/lukumaara
    minmaxlista = []
    for arvo in lista:
        minmaxlista.append(float(arvo.alinlampo))
        minmaxlista.append(float(arvo.ylinlampo))
    minimi = min(minmaxlista)
    maksimi = max(minmaxlista)
    
    tiedosto.write("Kuukauden säätilasto kaupungissa" + " " + kaupunkinimi + "\n")
    tiedosto.write("*******************************************************" + "\n")
    tiedosto.write("Kuukauden lämpötilan keskiarvo: " + "{0:.1f}".format(keskiarvo) + " celsiusastetta." + "\n")
    tiedosto.write("Kuukauden lämpötilan minimi: " + str(minimi) + " celsiusastetta." + "\n")
    tiedosto.write("Kuukauden lämpötilan maksimi: " + str(maksimi) + " celsiusastetta." + "\n")
    tiedosto.write("*******************************************************")
    tiedosto.close()
    print("Tallennus onnistui.")
    
def graafinpiirto(lista):    #Piirretään kuvaaja svg                                     
    keskilista = []                                              
    for arvo in lista:
         keskilista.append(float(arvo.keskilampo))
    csvtiedosto = open("kuvapisteet.csv", "w", encoding = "utf-8")
    kuvanimi = input("Anna svg-tiedoston nimi: ")
    
    kuva = svgwrite.Drawing(kuvanimi,  size = ("600px", "600px"))
    nelio = kuva.rect(
        (0, 0),
        (600, 600),
        fill = "white"
    )
    kuva.add(nelio)
    for i in range(0, 6):
        viiva = kuva.line(
            (0, (100 * i)),
            (600, (100 * i)),
            stroke = "black"
        )
        kuva.add(viiva)
        teksti = kuva.text(((-(100 * i) / 10) + 30),
           (0, i * 100),
            stroke = "green"
        )
        kuva.add(teksti)
        
    for n in range(0, len(keskilista)):                         
        x = keskilista[n]                                       
        if int(n + 1) < len(keskilista):
            graafi = kuva.line(((20 * n), ((30 - float(x)) * 10)),
                ((20 * (n + 1)), ((30 - float(keskilista[n + 1])) * 10)),
                stroke = "red"
            )
            kuva.add(graafi)
        if len(keskilista) - 1 > n:
            csvtiedosto.write(str(int((30 - float(x)) * 10)) + ",")
        else:
            csvtiedosto.write(str(int((30 - float(x)) * 10)) + "\n")
            
    kuva.save()
    csvtiedosto.close()
    print("Svg- ja csv-tiedostojen kirjoitus onnistui.")


def vertailugraafi(lista):
    verrattava = input("Anna vertailtavat säätiedot sisältävän tiedoston nimi: ")
    vertailutiedosto = open(verrattava, "r", encoding = "utf-8")
    kuvanimi = input("Anna svg-tiedoston nimi: ")
    csvtiedosto = open("kuvapisteet.csv", "w", encoding = "utf-8")


    apulista = []
    for rivi in vertailutiedosto:                                
        rivi = rivi.split(";")                                  
        vertailutieto = saatieto()
        vertailutieto.keskilampo = rivi[2]
        apulista.append(vertailutieto)
    apulista.pop(0)
    vertailutiedosto.close()
    
    vertailulista = []                                          
    for arvo1 in apulista:                                      
        vertailulista.append(float(arvo1.keskilampo))           
    keskilista = []
    for arvo2 in lista:
         keskilista.append(float(arvo2.keskilampo))
         
    kuva = svgwrite.Drawing(kuvanimi,  size = ("600px", "600px"))
    nelio = kuva.rect(
        (0, 0),
        (600, 600),
        fill = "white"
    )
    kuva.add(nelio)
    for i in range(0, 6):
        viiva = kuva.line(
            (0, (100 * i)),
            (600, (100 * i)),
            stroke = "black"
        )
        kuva.add(viiva)
        teksti = kuva.text(((-(100 * i) / 10) + 30),
           (0, i * 100),
            stroke = "green"
        )
        kuva.add(teksti)
        
    for n in range(0, len(keskilista)):                          
        x = keskilista[n]                                       
        if int(n + 1) < len(keskilista):
            kuvaaja = kuva.line(((20 * n), ((30 - float(x)) * 10)),
                ((20 * (n + 1)), ((30 - float(keskilista[n + 1])) * 10)),
                stroke = "red"
            )
            kuva.add(kuvaaja)
            
        if len(keskilista) - 1 > n:
            csvtiedosto.write(str(int((30 - float(x)) * 10)) + ",")
        else:
            csvtiedosto.write(str(int((30 - float(x)) * 10)) + "\n")
            
    for m in range(0, len(vertailulista)):
        y = vertailulista[m]
        if int(m + 1) < len(vertailulista):
            vertailukuvaaja = kuva.line(((20 * m), ((30 - float(y)) * 10)),
                ((20 * (m + 1)), ((30 - float(vertailulista[m + 1])) * 10)),
                stroke = "blue"
            )
            kuva.add(vertailukuvaaja)
            
        if len(vertailulista) - 1 > m:
            csvtiedosto.write(str(int((30 - float(y)) * 10)) + ",")
        else:
            csvtiedosto.write(str(int((30 - float(y)) * 10)) + "\n")
            
    kuva.save()
    csvtiedosto.close()
    print("Svg- ja csv-tiedostojen kirjoitus onnistui.")


def paaohjelma():                                               
    while True:
        valinta = valikko()
        if valinta == 0:
            print("Kiitos ohjelman käytöstä!")
            break
        elif valinta == 1:
            lista, kaupunkinimi = tietojenlataus()
        elif valinta == 2:
            keskiarvo(lista)
        elif valinta == 3:
            minimijamaksimi(lista)
        elif valinta == 4:
            tietojentallennus(lista, kaupunkinimi)
        elif valinta == 5:
            graafinpiirto(lista)
        elif valinta == 6:
            vertailugraafi(lista)
            
paaohjelma()
