#!/usr/bin/env python3

#Semestralni prace BI-SKJ
#Autor: Dominik Soukup (soukudom)

#exit code 1..pri detekci podivneho Time
#          2..detekce signalu, chyba argparseru
#          3..prazdny soubor nebo spatna prava, problem se stazenim, slozka nemuze byt vytvorena 
#          4..neplatny rozsah nejake osy
#          5..pri detekci spatneho casu
#          6..chyba argumetu
#          7..chyba konfig souboru
#          8..neni nainstalovan potrebny sw
#          9..ostatni

#import potrebnych balicku
from collections import defaultdict
from decimal import *
import argparse
import sys
import re
import os
import time
import datetime
import subprocess
import signal
import tempfile
import calendar
import shutil

#globalni promenne
args = None  #vyparsovany namespace ze vstupnich prepinacu
data = {}  #slovnik vstupnich parametru
data2 = defaultdict(list)  #slovnik pro tvorbu datovych souboru pro gnuplot
ymax = None  #maxim na ose Y
ymin = None  #minimum na ose Y
xmax = None  #maximum na ose X
xmin = None  #minimum na ose X
nol = 0  #pocet radek mergovanoho souboru
lim = 0  #limit na pocet pruchodu generujiciho cyklu
it = []  #poradove cislo jednotlivych obraku videa
lim2 = 0  #pocet pruchodu generujiciho cyklu na jeden snimek
numb = 0  #poradove cislo vysledne slozky
dl = 0  #pocet vstupnich souboru
gMove = list()  #list s vypoctenymi daty pro plot
solid = list()  #sytost barvy (odliseni souboru)
gnuplot = ""  #parametry gnuplotu
comm = ""  #prikaz pro vygenerovani obrazku
nos = 0  #kolik mezer obsahuje timeformat, number of spaces
lenNol = 0  #pocet cifer nol
confLine = {}  #slovnik s pozicemi radku v konfiguracnim souboru
wasInsert = defaultdict(int)  #slovnik s hodnotami zda byl zadan prepinac
multiplot = 0  #indikator prekryvu dat

#temp soubory
out = None  #merge soubor
outR = None  #otoceny merge soubor
out2 = None  #soubor, ze ktereho cte gnuplot
out2R = None  # otoceny soubor, ze ktereho cte gnuplot
directory = None  #tempfile.mkdtemp()

#temp pro web
web = list()


# \fn zvetsi poradove cislo obrazku
# \param nb: seznam s cisly posledniho obrazku
def iterator(nb):
    flag = 1
    for i in range(1, len(nb) + 1):
        tmp = nb[-i]
        if flag == 1:
            if tmp < 9:
                flag = 0
                nb[-i] = nb[-i] + 1
            else:
                nb[-i] = 0
        else:
            break


# \fn vytvori video
def createVideo():
    global data
    global numb
    global directory

    #pripraveni prikazu, ktery se bude spoustet
    ffmpeg = "ffmpeg -y -r {0} -f image2 -i \"{1}\"/obr%0" + str(
        lenNol) + "d.png \"{2}\"/video.mp4"

    print("\033[1mCreating video....", '\033[0m')
    subprocess.call(ffmpeg.format(data["fps"], directory,
                                  data["name"] + str(numb)),
                    shell=True,
                    stderr=subprocess.DEVNULL)

    print("\033[1mComplete!\nTotal time:", str(data["time"]),
          "s\nDestination:", data["name"] + str(numb), "\033[0m")


# \fn prevede seznam s cisly na ciselny retezec
# \param nb:    seznam s cisly posledniho obrazku
# \return co:   ciselny retezec
def printNumber(nb):
    co = ""
    for i in it:
        co += str(i)
    return co


# \fn vytvori slozku pro vysledne video
def createFolder():
    global numb
    #detekuje zda nazev obsahuje cestu
    if '/' in data["name"]:
        path, name = data["name"].rsplit('/', 1)
        cm = "ls '{0}' | grep '{1}'".format(path, name)
        ln = len(name) + 1
    else:
        cm = "ls | grep '^{0}'".format(data["name"])
        #pricteni 1 kvuli podtrzitku v nazvu
        ln = len(data["name"]) + 1
    #najde nazevy slozek zacinajici stejnym nazvem
    pom = subprocess.getoutput(cm)
    ar = pom.split('\n')
    #pokud existuje, najde nejvetsi poradove cislo slozky
    for i in ar:
        nm = i[ln:]
        if nm.isnumeric():
            if int(nm) > numb:
                numb = int(nm)
    if pom == "":
        numb = ""
    else:
        numb += 1
        numb = "_" + str(numb)
    try:
        subprocess.check_call(["mkdir", data["name"] + str(numb)],
                              stderr=subprocess.DEVNULL)
    except:
        print("\033[91m\033[1mName {0} of dir can not be create!\033[0m".format(
            data["name"]),
              file=sys.stderr)
        close(3)


# \fn nastavi sytosti pro ruzne soubory
def setSolid():
    global dl
    for i in range(0, dl):
        solid.append(1.00 - i * (1.00 / dl))


# \fn vypsani napovedy pri nespravnem vstupnim parametru
def usage(val):
    #parsovani jmena skriptu
    pom = sys.argv[0].split('./')
    print("""usage: """ + pom[1] +
          """ [-h] [-t TIMEFORMAT] [-X XMAX] [-x XMIN] [-Y YMAX] [-y YMIN]
               [-S SPEED] [-T TIME] []-F FPS [-c CRITICALVALUE] [-l LEGEND]
               [-g GNUPLOTPARAMS] [-e EFFECTPARAMS] [-f F] [-n NAME] [-E]
               input [input ...]
""" + pom[1] + """ : error: {0}""".format(val),
          file=sys.stderr)
    close(6)


# \fn vypsani chyby pri zpracovani konfiguracniho souboru
# \param val:   chybna hodnota
# \param line:  radek chybne hodnoty v konfiguracnim souboru
def configErr(val, line):
    global args
    print(
        "\033[91m\033[1mError: unrecognized value '{0}' in '{1}' at line {2} use -h or --help\033[0m".format(
            val, args.f, line),
        file=sys.stderr)
    close(6)


# \fn parsovani hodnoty retezce effectparams pro efekt vykreslovani
# \param ret:   retezec effectparams
# \return       soubory, ktere budou pouzity pri generovani video
def parse(ret):
    global out2, out2R

    if ret is not None:
        #odeleni prvni casti formatu effectparams
        tmp = ret[0].split(':', 1)
        tmp2 = tmp[0].split('=')
        #podle hodnoty nastaveni typovych souboru
        if tmp2[1] == '1':
            sb1 = out2.name
            sb2 = out2.name
        elif tmp2[1] == '2':
            sb1 = out2.name
            sb2 = out2R.name
        elif tmp2[1] == '3':
            sb1 = out2R.name
            sb2 = out2R.name
    #defaultni smer vykresleni
    else:
        sb1 = out2.name
        sb2 = out2.name
    return sb1, sb2


# \fn spocte pocet po sobe nejdoucich bilych znaku v retezci
# \param ret:   jakykoli retezec
# \return       pocet po sobe nejdoucich bilych znaku ve vstupnim retezci
def countSpace(ret):
    leng = 0
    ret = ret.strip()
    for i in range(0, len(ret) - 1):
        #pokud jsou vedle sebe dve mezery tak nezapocitavej
        if ret[i] == ' ' and ret[i + 1] == ' ':
            continue
        if data["timeformat"][i] == ' ':
            leng = leng + 1
    return leng


# \fn stazeni souboru z internetu
def downloadFile():
    global web
    global args
    global data

    #provedeni hluboke kopie
    tmpInput = list()
    for i in args.input:
        tmpInput.append(i)

    #counter kontrolovane pozice
    cnt = 0
    for i in tmpInput:
        if i.startswith("http"):
            print("\033[1mDownloading file..\033[0m")
            #tempfile pro webovy soubor
            tmp = tempfile.NamedTemporaryFile(delete=False)
            web.append(tmp)
            #vytvoreni prikazu
            pom = subprocess.call(["wget", "-q", i, "-O", tmp.name])
            args.input[cnt] = tmp.name
            #pokud pri stahovani nastala chyba
            if pom != 0:
                print(
                    "\033[91m\033[1mFile '{0}' downloading failed\033[0m".format(
                        i))
                #vymaz soubor
                del args.input[cnt]
                if data["ignoreerrors"] == True:
                    print("error suppressed (download fail)", file=sys.stderr)
                    if len(args.input) == 0:
                        print("\033[91m\033[1mNo more files available\033[0m")
                        close(3)
                    continue
                else:
                    close(3)
            cnt += 1


# \fn nastavi hodnotu XMAX pro konfiguraci gnuplotu
# \param para:  hodnota XMAX
# \param xmax:  maximalni hodnota na ose X
# \return       hodnota XMAX pro konfiguraci gnuplotu
def getXmax(para, xmax):
    if para == "auto":
        xdataM = ""
    elif para == "max":
        #prevod casoveho formatu na timestamp
        #zacatek epochy gnuplotu je 1.1. 2000, proto 1.1. 1970 - 1.1. 2000 = 946684800
        xdataM = float(calendar.timegm(xmax.utctimetuple())) - 946684800
        #pokud vyjde zaporna hodnota tak casovy format neobsahuje rok
        if xdataM < 0:
            tmp = datetime.datetime.strftime((xmax), (data["timeformat"]))
            tmp2 = datetime.datetime.strptime(("2000" + tmp),
                                              ("%Y" + data["timeformat"]))
            xdataM = float(calendar.timegm(tmp2.utctimetuple())) - 946684800

    else:
        #stejny prevod, ale nutne pretypovani na casovy format datetime.datetime
        tmp = datetime.datetime.strptime(para, data["timeformat"])
        xdataM = float(calendar.timegm(tmp.utctimetuple())) - 946684800
        if xdataM < 0:
            tmp = datetime.datetime.strptime(("2000" + para),
                                             ("%Y" + data["timeformat"]))
            xdataM = float(calendar.timegm(tmp.utctimetuple())) - 946684800

    return xdataM


# \fn nastavi hodnotu XMIN pro konfiguraci gnuplotu
# \param para:  hodnota XMIN
# \param xmin:  minimalni hodnota na ose X
# \return       hodnota XMIN pro konfiguraci gnuplotu
def getXmin(para, xmin):
    if para == "auto":
        xdatam = ""
    elif para == "min":
        #prevod casoveho formatu na timestamp
        #zacatek epochy gnuplotu je 1.1. 2000, proto 1.1. 1970 - 1.1. 2000 = 946684800
        xdatam = float(calendar.timegm(xmin.utctimetuple())) - 946684800
        #pokud vyjde zaporna hodnota tak casovy format neobsahuje rok
        if xdatam < 0:
            tmp = datetime.datetime.strftime((xmin), (data["timeformat"]))
            tmp2 = datetime.datetime.strptime(("2000" + tmp),
                                              ("%Y" + data["timeformat"]))
            xdatam = float(calendar.timegm(tmp2.utctimetuple())) - 946684800
    else:
        #stejny prevod, ale nutne pretypovani na casovy format datetime.datetime
        tmp = datetime.datetime.strptime(para, data["timeformat"])
        xdatam = float(calendar.timegm(tmp.utctimetuple())) - 946684800
        if xdatam < 0:
            tmp = datetime.datetime.strptime(("2000" + para),
                                             ("%Y" + data["timeformat"]))
            xdataM = float(calendar.timegm(tmp.utctimetuple())) - 946684800

    return xdatam


# \fn nastavi hodnotu YMAX pro konfiguraci gnuplotu
# \param para:  hodnota YMAX
# \param ymax:  maximalni hodnota na ose Y
# \return       hodnota YMAX pro konfiguraci gnuplotu
def getYmax(para, ymax):
    if para == "auto":
        ydataM = ""
    elif para == "max":
        ydataM = ymax
    else:
        ydataM = para
    return ydataM


# \fn nastavi hodnotu YMIN pro konfiguraci gnuplotu
# \param para:  hodnota YMIN
# \param ymin:  minimalni hodnota na ose Y
# \return       hodnota YMIN pro konfiguraci gnuplotu
def getYmin(para, ymin):
    if para == "auto":
        ydatam = ""
    elif para == "min":
        ydatam = ymin
    else:
        ydatam = para
    return ydatam


# \fn vymaze nepotrebne soubory a ukonci skript
# \param code: navratovy kod skriptu
def close(code):
    global out, outR, out2, out2R, web, directory
    global data 
    try:
        #pokud nastala chyba, vymaz adresar video
        if code != 0 and data["name"] is not None:
            if os.path.isdir(data["name"] + str(numb)):
                shutil.rmtree(data["name"] + str(numb))
        #vymaze temp soubory
        if os.path.isdir(directory):
            shutil.rmtree(directory)
        out.close()
        outR.close()
        out2.close()
        out2R.close()
        os.unlink(out.name)
        os.unlink(outR.name)
        os.unlink(out2.name)
        os.unlink(out2R.name)
        for i in web:
            i.close()
            os.unlink(i.name)
        sys.exit(code)
    except KeyError:
        sys.exit(code)
    except FileNotFoundError:
        sys.exit(code)
    except OSError:
        sys.exit(code)
    except ProcessLookupError:
        sys.exit(code)


# \fn zkontroluje rozsah vysledne hodnoty time
# \param para: retezec podezrelych hodnot
def checkPara(para):
    global data
    global nol

    if data["speed"] > nol:
        if data["ignoreerrors"] == False:
            print(
                "\033[91m\033[1mError: Speed value '{0}' is bigger than number of lines\033[0m".format(
                    data["speed"]),
                file=sys.stderr)
            close(1)
        else:
            data["speed"] = 1
            print("error suppressed (big speed)", file=sys.stderr)
    #pokud neni nastaveno ingnoreerrors, zeptej se na spravnost dat
    if data["time"] > 300:
        if data["ignoreerrors"] == False:
            print("speed=", data["speed"], ", time=", data["time"], ", fps=",
                  data["fps"])
            print("\033[1mSuspicious values: {0}\033[0m".format(para))
            print("\033[1mWould you like to make a change?\033[0m",
                  file=sys.stderr)
            answer = input("\033[1m[Y/n]\033[0m\n")
            if answer != "n":
                close(1)
        else:
            print("error suppressed (time)", file=sys.stderr)

    #pokud neni nastaveno ingnoreerrors, zeptej se na spravnost dat
    elif data["time"] < 5:
        if data["ignoreerrors"] == False:
            print("speed=", data["speed"], ", time=", data["time"], ", fps=",
                  data["fps"])
            print("\033[1mSuspicious values: {0}\033[0m".format(para))
            print("\033[1mWould you like to make a change?\033[0m",
                  file=sys.stderr)
            answer = input("\033[1m[Y/n]\033[0m\n")

            if answer != "n":
                close(1)
        else:
            print("error suppressed (time)", file=sys.stderr)


# \fn vypocte ze zadanych hodnot hodnoty: Time, Speed a Fps
def checkVal():
    global data

    if data["time"] == None and data["speed"] == None and data["fps"] == None:
        data["speed"] = 1
        data["fps"] = 25
        data["time"] = (nol / data["speed"]) / data["fps"]
        checkPara("time")

    elif data["time"] == None and data["fps"] == None and data["speed"] != None:
        data["fps"] = 25
        data["time"] = (nol / data["speed"]) / data["fps"]
        checkPara("speed")

    elif data["time"] == None and data["speed"] == None and data["fps"] != None:
        data["speed"] = 1
        data["time"] = (nol / data["speed"]) / data["fps"]
        checkPara("fps")

    elif data["time"] != None and data["speed"] == None and data["fps"] == None:
        data["speed"] = 1
        data["fps"] = int((nol / data["speed"]) / data["time"])
        checkPara("time")

    elif data["time"] == None and data["speed"] != None and data["fps"] != None:
        data["time"] = (nol / data["speed"]) / data["fps"]
        checkPara("speed, fps")

    elif data["time"] != None and data["speed"] != None and data["fps"] == None:
        data["fps"] = int((nol / data["speed"]) / data["time"])
        checkPara("speed, time")

    elif data["time"] != None and data["speed"] == None and data["fps"] != None:
        data["speed"] = int(nol / (data["time"] * data["fps"]))
        if data["speed"] == 0:
            if data["ignoreerrors"] == False:
                print(
                    "\033[91m\033[1mSpeed value is zero. Not possible.\033[0m",
                    file=sys.stderr)
                close(1)
            else:
                data["speed"] = 1
                data["time"] = (nol / data["speed"]) / data["fps"]
                print("error suppressed (zero speed)", file=sys.stderr)
        checkPara("time, fps")

    elif data["time"] != None and data["speed"] != None and data["fps"] != None:
        if data["time"] != int((nol / data["speed"]) / data["fps"]):
            if data["ignoreerrors"] == False:
                print("\033[91m\033[1mThese values are not acceptable\033[0m",
                      file=sys.stderr)
                close(1)
            else:
                data["time"] = (nol / data["speed"]) / data["fps"]


# \fn zpracuje konfiguracni soubor
def doConfig():
    global data
    global confLine
    global wasInsert
    try:
        with open(args.f, encoding='utf-8') as file:
            #cteni a parsovani prislusnich radku
            for lino, line in enumerate(file, start=1):
                line = line.strip()
                #odstraneni radkovych komentaru a prazdnych radku
                if re.match("(^#|^$)", line) is not None:
                    continue
                #odstraneni komentaru
                if re.search("#", line) is not None:
                    line = line[:line.index('#')].strip()

                key, *value = line.split()
                key = key.lower()
                #kontrola parametru
                if key == "timeformat" and wasInsert["-t"] == 0:
                    data[key] = ' '.join(value)
                elif key == "xmax" and wasInsert["-X"] == 0:
                    data[key] = ' '.join(value)
                    confLine[key] = lino
                elif key == "xmin" and wasInsert["-x"] == 0:
                    data[key] = ' '.join(value)
                    confLine[key] = lino
                elif key == "ymax" and wasInsert["-Y"] == 0:
                    data[key] = value[0]
                    confLine[key] = lino
                elif key == "ymin" and wasInsert["-y"] == 0:
                    data[key] = value[0]
                    confLine[key] = lino
                elif key == "speed" and wasInsert["-S"] == 0:
                    try:
                        data[key] = checkSTF(''.join(value))
                    except (argparse.ArgumentTypeError, ValueError) as e:
                        data[key] = ''.join(value)
                    confLine[key] = lino
                elif key == "time" and wasInsert["-T"] == 0:
                    try:
                        data[key] = checkSTF(''.join(value))
                    except (argparse.ArgumentTypeError, ValueError) as e:
                        data[key] = ''.join(value)
                    confLine[key] = lino
                elif key == "fps" and wasInsert["-F"] == 0:
                    try:
                        data[key] = checkSTF(''.join(value))
                    except (argparse.ArgumentTypeError, ValueError) as e:
                        data[key] = ''.join(value)
                    confLine[key] = lino
                elif key == "criticalvalue" and wasInsert["-c"] == 0:
                    if data[key] is None:
                        data[key] = value
                    else:
                        data[key].append(value)
                    confLine[key] = lino
                elif key == "legend" and wasInsert["-l"] == 0:
                    data[key] = ' '.join(value)
                    confLine[key] = lino
                elif key == "gnuplotparams" and wasInsert["-g"] == 0:
                    if data[key] is None:
                        data[key] = list()
                        confLine[key] = list()

                        data[key].append("set " + ' '.join(value))
                        confLine[key].append(lino)
                    else:
                        data[key].append("set " + ' '.join(value))
                        confLine[key].append(lino)
                elif key == "effectparams" and wasInsert["-e"] == 0:
                    data[key] = value
                    confLine[key] = lino
                elif key == "name" and wasInsert["-n"] == 0:
                    data[key] = ' '.join(value)
                    confLine[key] = lino
                elif key == "ignoreerrors" and wasInsert["-E"] == 0:
                    try:
                        confLine[key] = lino
                        data[key] = checkIgnoreErrors(value[0])
                    except ValueError:
                        configErr(data[key], lino)
    except PermissionError:
        print("\033[91m\033[1mError: permission denied '{0}'\033[0m".format(
            args.f),
              file=sys.stderr)
        close(3)
    except FileNotFoundError:
        print("\033[91m\033[1mError: file '{0}' does not exist\033[0m".format(
            args.f),
              file=sys.stderr)
        close(3)


# \fn zkontroluje spravnost dat
def checkData():
    global data
    global confLine
    for key in data.keys():
        if data[key] is None:
            continue
        else:
            if key == "xmax":
                try:
                    #kontrola formatu X
                    checkX()
                except ValueError:
                    if data["ignoreerrors"] == True:
                        print("error suppressed (xmax)", file=sys.stderr)
                        data[key] = "max"
                    else:
                        configErr(data[key], confLine[key])
            elif key == "xmin":
                try:
                    checkx()
                except ValueError:
                    if data["ignoreerrors"] == True:
                        print("error suppressed (xmin)", file=sys.stderr)
                        data[key] = "min"
                    else:
                        configErr(data[key], confLine[key])

            elif key == "ymax":
                try:
                    choiceCheckMax(data[key])
                except argparse.ArgumentTypeError:
                    if data["ignoreerrors"] == False:
                        configErr(data[key], confLine[key])
                    else:
                        print("error suppressed (ymax)", file=sys.stderr)
                        data[key] = "auto"
            elif key == "ymin":
                try:
                    choiceCheckMin(data[key])
                except argparse.ArgumentTypeError:
                    if data["ignoreerrors"] == False:
                        configErr(data[key], confLine[key])
                    else:
                        print("error suppressed (ymin)", file=sys.stderr)
                        data[key] = "auto"
            elif key == "speed":
                try:
                    checkSTF(data[key])
                except (argparse.ArgumentTypeError, ValueError) as e:
                    if data["ignoreerrors"] == False:
                        configErr(data[key], confLine[key])
                    else:
                        print("error suppressed (speed)", file=sys.stderr)
                        data[key] = None
            elif key == "time":
                try:
                    checkSTF(data[key])
                except (argparse.ArgumentTypeError, ValueError) as e:
                    if data["ignoreerrors"] == False:
                        configErr(data[key], confLine[key])
                    else:
                        print("error suppressed (time)", file=sys.stderr)
                        data[key] = None

            elif key == "fps":
                try:
                    checkSTF(data[key])
                except (argparse.ArgumentTypeError, ValueError) as e:
                    if data["ignoreerrors"] == False:
                        configErr(data[key], confLine[key])
                    else:
                        print("error suppressed (fps)", file=sys.stderr)
                        data[key] = None

            elif key == "gnuplotparams":
                for lin, val in enumerate(data[key], start=0):
                    try:
                        gnuplotCheck(val[4:])
                    except subprocess.CalledProcessError:
                        if data["ignoreerrors"] == False:
                            configErr(val[4:], confLine[key][lin])
                        else:
                            print("error suppressed (gnuplotparams)",
                                  file=sys.stderr)
                            data[key] = None
            elif key == "effectparams":
                try:
                    effectCheck(''.join(data[key]))
                except argparse.ArgumentTypeError:
                    if data["ignoreerrors"] == False:
                        configErr(data[key], confLine[key])
                    else:
                        print("error suppressed (effectparams)",
                              file=sys.stderr)
                        data[key] = None


# \fn nastavi defaultni hodnoty pokud nebyly zadany
# \param data: slovni s parametry
def setDefault(data):

    for key in data:
        if data[key] == None:
            if key == "timeformat":
                data[key] = "[%Y-%m-%d %H:%M:%S]"
            elif key == "xmax":
                data[key] = "max"
            elif key == "xmin":
                data[key] = "min"
            elif key == "ymax":
                data[key] = "auto"
            elif key == "ymin":
                data[key] = "auto"
            elif key == "ignoreerrors":
                data[key] = False
            elif key == "name":
                pom = sys.argv[0].split('./')
                data[key] = pom[1].split('.')[0]
            elif key == "legend":
                data[key] = ""


# \fn nastavi konfiguraci gnuplotu a plotu
def setGnuplot():
    global gnuplot
    global nos
    global multiplot

    plot = "plot "
    for i in range(0, dl):
        pos = 2 + nos + i
        #prikaz plot pro vykreslovani grafu
        if multiplot != 2:
            plot += """"{0}" using 1:(f($""" + str(pos) + """)):((i($""" + str(
                pos) + """))+ """ + str(
                    gMove[i][2]) + """) t "" w filledcurves closed fs transparent solid """ + str(
                        solid[i]) + """ noborder,\
"{1}" using 1:(((h($""" + str(pos) + """)))+ """ + str(
                            gMove[i][0]) + """):((g($""" + str(pos) + """))+ """ + str(
                                gMove[i][1]) + """) t "" w filledcurves closed fs transparent solid """ + str(
                                    solid[i]) + """ noborder,"""
        #prikaz plot pokud se data prekryvaji na rozne Xove souradnici
        if multiplot == 2:
            plot += """"{0}" using 1:""" + str(pos) + """:""" + str(
                pos + (dl - 1 - i) + (i) * 3 +
                3) + """ t "" w filledcurves closed fs transparent solid """ + str(
                    solid[i]) + """ noborder,\
"{1}" using 1:""" + str(pos + (dl - 1 - i) + (i) * 3 + 1) + """:""" + str(
                        pos + (dl - 1 - i) + (i) * 3 +
                        2) + """ t "" w filledcurves closed fs transparent solid """ + str(
                            solid[i]) + """ noborder,"""

    #priprava parametru gnuplotu
    gnuplot = """set terminal png
    f(x)=x
    g(x)=x*0.5
    h(x)=x*0.7
    i(x)=x*0.3
    set datafile missing "X"
    set xtics rotate by 90 right
    set style fill noborder
    set bmargin at screen 0.2
    set xdata time
    set format x "%H:%M"
    set yrange {3}
    set xrange {5}
    set title "{4}"
    set auto fix
    set timefmt "{2}" """
    if data["gnuplotparams"] is not None:
        data["gnuplotparams"].insert(0, gnuplot)
        gnuplot = '\n'.join(data["gnuplotparams"])

    #pripojeni prikazu plot (bez posledni carky)
    gnuplot += "\n" + plot[:-1]


# \fn vytvori jednotlive snimky video
def createPicture():
    global lim2
    global out, out2, outR, out2R, directory
    global data
    global lenNol
    flag = 0
    try:
        for i in range(1, lim + 1):
            #zvetsi cislo souboru a ulozi dopromenne
            iterator(it)
            pm = printNumber(it)

            #vypocet procentualni castni poctu zpracovanych radek souboru
            if flag == 1:
                print("\033[1m\033[1AMaking pictures....", int(
                    (lim2 / nol) * 100), '%\033[0m')
            else:
                print("\033[1mMaking pictures....", int(
                    (lim2 / nol) * 100), '%\033[0m')
                flag = 1

            #precte prvnich lim2 radku ze souboru a necha je vykreslit jako jeden snimek
            with open(out.name,
                      encoding='utf-8') as file, open(out2.name,
                                                      encoding='utf-8',
                                                      mode='w') as file2:
                [file2.write(next(file)) for x in range(1, lim2 + 1)]

            with open(outR.name,
                      encoding='utf-8') as file, open(out2R.name,
                                                      encoding='utf-8',
                                                      mode='w') as file2:
                [(file2.write(next(file))) for x in range(1, lim2 + 1)]

            subprocess.call(comm.format(directory, pm),
                            shell=True,
                            stderr=subprocess.DEVNULL)
            #pocet radku v nasledujicim snimku se zvetsuje podle parametru speed
            lim2 += data["speed"]
            if (lim2 > nol):
                lim2 = nol

        print("\033[1m\033[1AMaking pictures....", int(
            (lim2 / nol) * 100), '%\033[0m')
    except RuntimeError:
        close(9)


# \fn vytvori datove soubory pro gnuplot
def createGnuFiles():
    global nol, lenNol
    global out, outR
    global data2, data
    global it

    #serazeni klicu slovniku
    Sdata2 = sorted(data2)
    Rdata2 = reversed(Sdata2)
    with open(out.name, mode='w', encoding="utf-8") as file:
        for i in Sdata2:
            tmp = datetime.datetime.strftime(i, data["timeformat"])
            #poc_mezer=tmp.count(' ')
            for j in range(0, dl):
                tmp += ' ' + str(data2[i][j])
            for j in range(0, dl):
                #pridani hodnot pro prekryv mimo stejne hodnty osy X
                if data2[i][j] == 'X':
                    tmp += ' ' + str('X') + ' ' + str('X') + ' ' + str('X')
                else:
                    tmp += ' ' + str(data2[i][j] * Decimal(0.7) + gMove[j][0])
                    tmp += ' ' + str(data2[i][j] * Decimal(0.5) + gMove[j][1])
                    tmp += ' ' + str(data2[i][j] * Decimal(0.3) + gMove[j][2])
            tmp += '\n'
            nol += 1
            file.write(tmp)
        lenNol = len(str(nol))
        #tvorba delky cisla obrazku
        for j in range(0, lenNol):
            it.append(0)

        #otoceni souboru
        with open(outR.name, mode='w', encoding="utf-8") as file:
            for i in Rdata2:
                tmp = datetime.datetime.strftime(i, data["timeformat"]) + " "
                for j in range(0, dl):
                    tmp += ' ' + str(data2[i][j])
                for j in range(0, dl):
                    if data2[i][j] == 'X':
                        #pridani honot pro prekryv mimo stejne hodnoty X
                        tmp += ' ' + str('X') + ' ' + str('X') + ' ' + str('X')
                    else:
                        tmp += ' ' + str(data2[i][j] * Decimal(0.7) +
                                         gMove[j][0])
                        tmp += ' ' + str(data2[i][j] * Decimal(0.5) +
                                         gMove[j][1])
                        tmp += ' ' + str(data2[i][j] * Decimal(0.3) +
                                         gMove[j][2])
                tmp += '\n'
                file.write(tmp)


# \fn doplni platne hodnoty do pripravenoho slovniku
def fillData():
    global args
    global data
    global multiplot

    for no, i in enumerate(args.input, start=0):
        with open(i, encoding='utf-8') as file:
            for line in file:
                #odtraneni whitespacu
                line = line.strip()
                key, value = line.rsplit(' ', 1)
                value = value.strip()
                key = key.strip()
                key = datetime.datetime.strptime(key, data["timeformat"])
                #osetreni (vynechani dat) kdyz je zmensena osa X
                if data["xmin"] != "auto" and data["xmin"] != "min":
                    pom = datetime.datetime.strptime(data["xmin"],
                                                     data["timeformat"])
                    if key < pom:
                        continue
                if data["xmax"] != "auto" and data["xmax"] != "max":
                    pom = datetime.datetime.strptime(data["xmax"],
                                                     data["timeformat"])
                    if key > pom:
                        continue
                try:
                    value = Decimal(value)
                except InvalidOperation:
                    value = 'X'
                data2[key][no] = value


# \fn spoji data vstupnich souboru do jednoho souboru
def mergeFiles():
    global xmax
    global xmin
    global ymax
    global ymin
    global gMove
    global data
    global multiplot
    #seznamy s hodnotami pro posun krivek
    moveMulti = list()
    moveSimple = list()
    flag = 0
    flag2 = 0
    #lokalni promenne pro lokani rozsahy
    xlocal = 0
    xlocalM = 0
    localX = list()

    for no, i in enumerate(args.input, start=0):
        try:
            with open(i, encoding="utf-8") as file:
                for lino, line in enumerate(file, start=1):
                    #ostraneni whitespacu
                    line = line.strip()
                    key, value = line.rsplit(' ', 1)
                    value = value.strip()
                    key = key.strip()
                    #kontrola casoveho formatu
                    try:
                        key = datetime.datetime.strptime(key,
                                                         data["timeformat"])
                    except ValueError:
                        print(
                            "\033[91m\033[1mError: unrecognized value '{0}' for timeformat or unrecognized value '{1}' in data file at line '{2}' use -h or --help\033[0m".format(
                                data["timeformat"], key, lino),
                            file=sys.stderr)
                        close(5)
                    #osetreni (vynechani dat) kdyz je zmensena osa X

                    if data["xmin"] != "auto" and data["xmin"] != "min":
                        try:
                            pom = datetime.datetime.strptime(
                                data["xmin"], data["timeformat"])
                        except ValueError:
                            usage(
                                "unrecognized value '{0}' for X axis use -h or --help".format(
                                    data["xmin"],
                                    file=sys.stderr))

                        if key < pom:
                            flag2 = 2
                            continue
                    if data["xmax"] != "auto" and data["xmax"] != "max":
                        try:
                            pom = datetime.datetime.strptime(
                                data["xmax"], data["timeformat"])
                        except ValueError:
                            usage(
                                "unrecognized value '{0}' for X axis use -h or --help".format(
                                    data["xmax"],
                                    file=sys.stderr))

                        if key > pom:
                            continue

                #ochrana proti neplatnym datum
                    try:
                        value = Decimal(value)
                    except InvalidOperation:
                        if lino == 1:
                            print(
                                "\033[91m\033[1mError: line 1 in '{0}' is not accetable\033[0m".format(
                                    i))
                            close(5)
                        if not data2[key]:
                            for j in range(0, dl):
                                data2[key].append('X')
                        continue
                    #inicializace
                    if (lino == 1 and no == 0) or (flag == 0):
                        ymax = value
                        ymin = value
                        xmax = key
                        xmin = key
                        flag = 1
                        #vypocet hodnot pro vykreslovani grafu default
                        tmp = list()
                        h = value - (Decimal(0.7) * value)
                        tmp.append(h)
                        h = value - (Decimal(0.5) * value)
                        tmp.append(h)
                        h = value - (Decimal(0.3) * value)
                        tmp.append(h)
                        gMove.append(tmp)
                    if lino == 1 or flag2 == 2:
                        tmp = list()
                        #inicializace lokalnich hodnot
                        xlocalm = key
                        xlocalM = key
                        #vypocet hodnot pro vykreslovani po souborech i pro vykreslovani jako celku
                        if no != 0:
                            #hodnoty pro vykresleni po souborech
                            h = value - (Decimal(0.7) * value)
                            tmp.append(h)
                            h = value - (Decimal(0.5) * value)
                            tmp.append(h)
                            h = value - (Decimal(0.3) * value)
                            tmp.append(h)
                            moveMulti.append(tmp)
                            #hodnoty pro vykresleni jako celku
                            moveSimple += gMove
                        flag2 = 0
                    #zjistovani minim a maxim
                    if value > ymax:
                        ymax = value
                    if value < ymin:
                        ymin = value
                    if key > xmax:
                        xmax = key
                    if key < xmin:
                        xmin = key
                    if key < xlocalm:
                        xlocalm = key
                    if key > xlocalM:
                        xlocalM = key
                    if not data2[key]:
                        #detekce prekryvu hodnot, ktere nezacinaji na stejne hodnote osy X
                        for k in localX:
                            if key < k[1] and key > k[0]:
                                multiplot = 2
                        for j in range(0, dl):
                            data2[key].append('X')
                    else:
                        if multiplot != 2:
                            multiplot = 1
                    #ulozeni lokalnich minim pro kontrolu prekryvu
                    pom = (xlocalm, xlocalM)
                    localX.append(pom)
        except PermissionError:
            print(
                "\033[91m\033[1mError: permission denied '{0}'\033[0m".format(i),
                file=sys.stderr)
            close(3)
        except FileNotFoundError:
            print("\033[91m\033[1mError: file not found '{0}'\033[0m".format(i),
                  file=sys.stderr)
            close(3)
    #prirazeni prislusneho druhu vypoctu podle dat
    if multiplot == 0:
        gMove += moveSimple
    elif multiplot != 0:
        gMove += moveMulti
    fillData()
    createGnuFiles()


# \fn osetruje signal SIGINT
# \param signal: cislo signalu
# \param frame:  objekt zasobniku
def signal_int(signal, frame):
    print("\033[91m\033[1mInterupted\033[0m")
    close(2)


# \fn osetruje signal SIGTERM
# \param signal: cislo signalu
# \param frame:  objekt zasobniku
def signal_term(signal, frame):
    print("\033[91m\033[1mTerminated\033[0m")
    close(2)


# \fn kontroluje format pro Ymax
# \param choice:    zadana hodnota Ymax
# \return           hodnota Ymax
def choiceCheckMax(choice):
    try:
        return re.match("(^auto$|^max$|^-?[1-9][0-9]*$)", choice).group(0)
    except AttributeError:
        raise argparse.ArgumentTypeError(
            "invalid choice: '{0}' use -h or --help)".format(choice))


# \fn kontroluje format pro Ymin
# \param choice:    zadana hodnota Ymin
# \return           hodnota Ymin
def choiceCheckMin(choice):
    try:
        return re.match("(^auto$|^min$|^-?[1-9][0-9]*$)", choice).group(0)
    except AttributeError:
        raise argparse.ArgumentTypeError(
            "invalid choice: '{0}' use -h or --help)".format(choice))


# \fn kontroluje casovy format osy X vzhledem k timestampu
# \param choice:    zadana hodnota pro osu X
# \param time:      zadana hodnota pro timestamp
def choiceCheckTime(choice, time):
    datetime.datetime.strptime(choice, time)


# \fn kontroluje format hodnoty Critical
# \param val:   zadana hodnota Critical
# \return       hodnota Critical
def criticalCheck(val):
    try:
        return re.match("^[xy]=[0-9]+$", val).group(0)
    except KeyboardInterrupt:
        print("\033[91m\033[1mInterupted\033[0m")
        close(2)
    except AttributeError:
        raise argparse.ArgumentTypeError(
            "invalid argument '{0}' use -h or --help)".format(val))


# \fn kontroluje format hodnoty Ignoreerrors
# \param val:   zadana hodnota Ignoreerrors
# \return       hodnota Ignoreerrors
def checkIgnoreErrors(val):
    if val == "false" or val == "False":
        return False
    elif val == "true" or val == "True":
        return True
    else:
        raise ValueError


# \fn kontroluje format hodnoty Efectparams
# \param val:   zadana hodnota Efectparams
# \return       hodnota Efectparams
def effectCheck(val):
    try:
        #prvni musi byt hodnota smer a pak libovlne hodnoty podle zadani
        return re.match("((smer=[1-3]+)(:[a-z]+=[a-z0-9]+)*$)+", val).group(0)
    except KeyboardInterrupt:
        print("\033[91m\033[1mInterupted\033[0m")
        close(2)
    except AttributeError:
        raise argparse.ArgumentTypeError(
            "invalid argument '{0}' use -h or --help)".format(val))


# \fn kontroluje format parametru gnuplotu
# \param val: zadana hodnota parametru gnuplotu
def gnuplotCheck(val):
    try:
        subprocess.check_call(
            "printf 'set %s' '{0}'| gnuplot 2>>/dev/null".format(val),
            shell=True)
    except KeyboardInterrupt:
        print("\033[91m\033[1mInterupted\033[0m")
        close(2)
    except AttributeError:
        raise argparse.ArgumentTypeError(
            "invalid gnuplot argument '{0}' use -h or --help".format(val))


# \fn kontroluje format pro Xmax
def checkX():
    global data
    if data["xmax"] != "max" and data["xmax"] != "auto":
        choiceCheckTime(data["xmax"], data["timeformat"])


# \fn kontroluje format pro Xmin
def checkx():
    if data["xmin"] != "min" and data["xmin"] != "auto":
        choiceCheckTime(data["xmin"], data["timeformat"])


# \fn kontroluje format parametru pro Speed, Time a Fps
# \param val:   zadana hodnota pro parametr Speed, Time nebo Fps
# \return       hodnotu pro parametr Speed, Time nebo Fps
def checkSTF(val):
    val = int(val)
    if val < 1:
        raise argparse.ArgumentTypeError(
            "invalid value '{0}' use -h or --help".format(val))
    else:
        return val


# \fn testuje zda existuje program
# \param name: jmeno programu, ktery se otestuje
# \return      logicka hodnota zda soubor existuje nebo neexistuje
def exist(name):
    try:
        if name == "gnuplot":
            subprocess.Popen([name, "-V"],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL).communicate()
        else:
            subprocess.Popen([name],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL).communicate()
    except KeyboardInterrupt:
        print("\033[91m\033[1mInterupted\033[0m")
        close(2)
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True


# \fn kontroluje zda je soubor prazdny
# \param sb: seznam vstupnich souboru
def checkFile(sb):
    #provedeni hluboke kopie
    tmpInput = list()
    cnt = 0  #citac kontrolovane pozice
    for i in sb:
        tmpInput.append(i)

    try:
        for no, i in enumerate(tmpInput, start=0):
            #zkontrolluj velikost souboru
            if os.stat(i).st_size == 0 and data["ignoreerrors"] == True:
                print("error suppressed (empty file)", file=sys.stderr)
                del sb[cnt]
                cnt -= 1
            elif os.stat(i).st_size == 0 and data["ignoreerrors"] == False:
                print("\033[91m\033[1mError: File is empty\033[0m",
                      file=sys.stderr)
                close(3)
            cnt += 1
        if len(sb) == 0:
            print("\033[91m\033[1mNo more available files\033[0m",
                  file=sys.stderr)
            close(3)
    except KeyboardInterrupt:
        print("\033[91m\033[1mInterupted\033[0m")
        close(2)
    except FileNotFoundError:
        print(
            "\033[91m\033[1mError: file '{0}' does not exist\033[0m".format(i),
            file=sys.stderr)
        close(3)


# \fn kontroluje zda se zadane prepinace neopakuji
def checkRepeat():
    global wasInsert
    for i in sys.argv:
        if i.startswith("-"):
            if i == "-e":
                continue
            elif i == "-c":
                continue
            elif i == "-g":
                continue
            wasInsert[i] += 1
            if wasInsert[i] > 1:
                print(
                    "\033[91m\033[1mError: detect repeated switch '{0}' use -h or --help\033[0m".format(
                        i),
                    file=sys.stderr)
                close(6)

############################## VYKONNA CAST ##############################

#spusteni kontroly signalu
signal.signal(signal.SIGINT, signal_int)
signal.signal(signal.SIGTERM, signal_term)

#testovani potrebnych programu
if exist("ffmpeg") == False:
    print("\033[91m\033[1mProgram {0} is not installed\033[0m".format(name))
    close(8)
if exist("wget") == False:
    print("\033[91m\033[1mProgram {0} is not installed\033[0m".format(name))
    close(8)

if exist("gnuplot") == False:
    print("\033[91m\033[1mProgram {0} is not installed\033[0m".format(name))
    close(8)

#slouzi detekci vicenasobneho zadani prepinace
checkRepeat()

#parsovani vstupnich argumentu
parser = argparse.ArgumentParser()

parser.add_argument('-t', '--timeformat',
                    help='time in format strftime(3c)',
                    default=None)
parser.add_argument('-X', '--xmax', help='auto, max, value', default=None)
parser.add_argument('-x', '--xmin', help='auto, min, value', default=None)
parser.add_argument('-Y', '--ymax',
                    help='auto, max, value',
                    default=None,
                    type=choiceCheckMax)
parser.add_argument('-y', '--ymin',
                    help='auto, min, value',
                    default=None,
                    type=choiceCheckMin)
parser.add_argument('-S', '--speed',
                    help='number of records (int)',
                    default=None,
                    type=checkSTF)
parser.add_argument('-T', '--time',
                    help='duration (int)',
                    default=None,
                    type=checkSTF)
parser.add_argument('-F', '--fps',
                    help='fps (int)',
                    default=None,
                    type=checkSTF)
parser.add_argument('-c', '--criticalvalue',
                    help='critical value',
                    action='append',
                    default=None,
                    type=criticalCheck)
parser.add_argument('-l', '--legend', help='legend (text)', default=None)
parser.add_argument('-g', '--gnuplotparams',
                    help='gnuplot params',
                    default=None,
                    action='append',
                    type=gnuplotCheck)
parser.add_argument('-e', '--effectparams',
                    help='effect params (param=val)',
                    default=None,
                    action='append',
                    type=effectCheck)
parser.add_argument('-f', help='config file', default=None)
parser.add_argument('-n', '--name', help='name of directory', default=None)
parser.add_argument('-E', '--ignoreerrors',
                    help='ignore errors',
                    default=None,
                    action='store_true')
parser.add_argument("input", nargs='+', default=None)

args = parser.parse_args()

#vytvoreni tempu
out = tempfile.NamedTemporaryFile(delete=False)
outR = tempfile.NamedTemporaryFile(delete=False)
out2 = tempfile.NamedTemporaryFile(delete=False)
out2R = tempfile.NamedTemporaryFile(delete=False)
directory = tempfile.mkdtemp()

#zalozeni klicu slovniku
for i in args.__dict__:
    data[i] = None

#pokud je zadan configuracni soubor tak zpracuj
if args.f:
    doConfig()

#presun dat z argparse, aby byly platnejsi nez z konfiguracniho souboru
for i in args.__dict__:
    if args.__dict__[i] is not None:
        data[i] = args.__dict__[i]

        #defaultni hodnoty pro ty co nebyly zadany
setDefault(data)

#pomocna promena, aby gnuplot vedel, kde zacinaji Y data
nos = countSpace(data["timeformat"])

#kontrola fomatu pro X-ovou osu
if wasInsert["-X"] == 1:
    try:
        checkX()
    except KeyboardInterrupt:
        print("\033[91m\033[1mInterupted\033[0m")
        close(2)
    except ValueError:
        usage(
            "unrecognized value '{0}' for X axis or unrecognized value '{1}' for timeformat use -h or --help".format(
                data["xmax"], data["timeformat"],
                file=sys.stderr))

if wasInsert["-x"] == 1:
    try:
        checkx()
    except KeyboardInterrupt:
        print("\033[91m\033[1mInterupted\033[0m")
        close(2)
    except ValueError:
        usage(
            "unrecognized value '{0}' for X axis or unrecognized value '{1}' for timeformat use -h or --help".format(
                data["xmin"], data["timeformat"],
                file=sys.stderr))

if data["f"]:
    #kontrola zadanych dat
    checkData()

#vytvoreni slozky pro video
createFolder()

#stazeni souboru pokud jsou z internetu
downloadFile()

#kontrola prazdnosti souboru
checkFile(args.input)

#delka platnych vstupnich souboru
dl = len(args.input)

#spojeni dat datovych souboru
mergeFiles()

#kontrola hodnot time, fsp, speed
checkVal()

#sytost barvy pro soubro
setSolid()

#konfigurace gnuplot
setGnuplot()

#vytvareni poctu iteraci pro generovani snimku
lim = int(nol / data["speed"])
lim2 = data["speed"]

#testovani rozsahu dat
ydataM = getYmax(data["ymax"], ymax)
ydatam = getYmin(data["ymin"], ymin)

if ydataM == ydatam and (ydatam != "" or ydataM != ""):
    print("\033[91m\033[1mError: Bad range of Y axis '{0}:{1}'\033[0m".format(
        ydatam, ydataM),
          file=sys.stderr)
    close(4)

xdataM = getXmax(data["xmax"], xmax)
xdatam = getXmin(data["xmin"], xmin)

if xdatam == xdataM and (xdatam != "" or xdataM != ""):
    print("\033[91m\033[1mError: Bad range of X axis '{0}:{1}'\033[0m".format(
        xdatam, xdataM),
          file=sys.stderr)
    close(4)
#parsuj efekt
sb = parse(data["effectparams"])

#prikaz pro bash pro vytvoreni obrazku
comm = "printf \"%s\\n\" '" + gnuplot.format(
    sb[0], sb[1], data["timeformat"], "[" + str(ydatam) + ":" + str(ydataM) +
    "]", data["legend"], "[" + str(xdatam) + ":" + str(xdataM) +
    "]") + "'|gnuplot > \"{0}\"/obr{1}.png"

#vytvor Obrazek
createPicture()

#vytvori video
createVideo()

#odstrani temp soubory
close(0)
