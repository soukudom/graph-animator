#!/usr/bin/env python3

import subprocess
import signal


def signal_int(signal, frame):
    pass


signal.signal(signal.SIGINT, signal_int)

#odebrani prav pro testovani
subprocess.call("chmod 000 testy/souborBezPrav.txt",shell=True)


#test1: Test pristupovych prav
input("\n\n\033[1mTest1: Test pristupovych prav\033[0m")
print('./color_magic.py testy/souborBezPrav.txt -t "%Y/%m/%d %H:%M:%S"\n')
args = ['./color_magic.py', 'testy/souborBezPrav.txt', '-t',
        '"%Y/%m/%d %H:%M:%S"']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",ret)

#test2: Test prazdnosti souboru
input("\n\n\033[1mTest2: Test prazdnosti souboru\033[0m")
print('./color_magic.py testy/souborPrazdny.txt -t "%Y/%m/%d %H:%M:%S"\n')
args = ['./color_magic.py', 'testy/souborPrazdny.txt']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",ret)

#test3: Test prazdnosti souboru s potlacenim chyb
input("\n\n\033[1mTest3: Test prazdnosti souboru s potlacenim chyb\033[0m")
print('./color_magic.py testy/souborPrazdny.txt -E\n')
args = ['./color_magic.py', 'testy/souborPrazdny.txt', '-E']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",ret)

#test4: Test zpracovani platneho datoveho souboru s nekolika prazdnymi soubory
input(
    "\n\n\033[1mTest4: Test prazdnosti platneho datoveho souboru s nekolika prazdnymi\033[0m")
print(
    './color_magic.py testy/souborPrazdny.txt testy/souborPrazdny.txt testy/sin.txt -t "%Y/%m/%d %H:%M:%S"\n')
args = ['./color_magic.py', 'testy/souborPrazdny.txt',
        'testy/souborPrazdny.txt', 'testy/sin.txt', '-t',
        '"%Y/%m/%d %H:%M:%S"']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test5: Test zpracovani platneho datoveho souboru s nekolika prazdnymi a s potlacenim chyb
input(
    "\n\n\033[1mTest5: Test prazdnosti platneho datoveho souboru s nekolika prazdnymi\033[0m")
print(
    './color_magic.py testy/souborPrazdny.txt testy/souborPrazdny.txt testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -E -S 5\n')
args = ['./color_magic.py', 'testy/souborPrazdny.txt',
        'testy/souborPrazdny.txt', 'testy/sin.txt', '-t',
        '"%Y/%m/%d %H:%M:%S"', '-E', '-S', '5']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

input("\033[1mTest5b\033[0m")
#prehozeni poradi souboru
print(
    '\n./color_magic.py testy/sin.txt testy/souborPrazdny.txt testy/souborPrazdny.txt -t "%Y/%m/%d %H:%M:%S" -E -S 5\n')
args = ['./color_magic.py', 'testy/sin.txt', 'testy/souborPrazdny.txt',
        'testy/souborPrazdny.txt', '-t', '"%Y/%m/%d %H:%M:%S"', '-E', '-S',
        '5']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))
input("\033[1mTest5c\033[0m")
#prehozeni poradi souboru
print(
    '\n./color_magic.py testy/souborPrazdny.txt testy/sin.txt testy/souborPrazdny.txt -t "%Y/%m/%d %H:%M:%S" -E -S 5 -e smer=2\n')
args = ['./color_magic.py', 'testy/souborPrazdny.txt', 'testy/sin.txt',
        'testy/souborPrazdny.txt', '-t', '"%Y/%m/%d %H:%M:%S"', '-E', '-S',
        '5', '-e', 'smer=2']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test6: Test kontroly casoveho formatu
input("\n\n\033[1mTest6: Test kontroly casoveho formatu\033[0m")
print('./color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%s"\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%s"']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",ret)

#test7: Test souboru s jednou radkou
input("\n\n\033[1mTest7: Test souboru s jednou radkou\033[0m")
print('./color_magic.py testy/souborJedenRadek.txt -t "%Y/%m/%d %H:%M:%S"\n')
args = ['./color_magic.py', 'testy/souborJedenRadek.txt', '-t',
        '"%Y/%m/%d %H:%M:%S"']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",ret)

#test8: Test povinnosti vstupniho datoveho souboru
input("\n\n\033[1mTest8: Test povinnosti vstupniho datoveho souboru\033[0m")
print('./color_magic.py -t "%Y/%m/%d %H:%M:%S"\n')
args = ['./color_magic.py', '-t', '"%Y/%m/%d %H:%M:%S"']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",ret)

#test9: Test casoveho formatu pro osu X
input("\n\n\033[1mTest9: Test casoveho formatu pro osu X\033[0m")
print('./color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -X "2009"\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-X', '2009']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",ret)

#zadani dalsich moznosti
input("\n\n\033[1mTest9b\033[0m")
print('./color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -X min\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-X', 'min']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",ret)

#zadani dalsich moznosti
input("\n\n\033[1mTest9c\033[0m")
print('./color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -x max\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-x', 'max']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",ret)

#test10: Test zmena rozsahu X-ove osy
input("\n\n\033[1mTest10: Test zmena rozsahu X-ove osy (zvetseni) \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -x "2009/05/11 04:00:00" -X "2009/05/12 12:12:12" -S 5 -e smer=3\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-X', '"2009/05/12 12:12:12"', '-x', '"2009/05/11 04:00:00"', '-S',
        '5', '-e', 'smer=3']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test10b: Test zmena rozsahu X-ove osy
input("\n\n\033[1mTest10b: Test zmena rozsahu X-ove osy (zmenseni) \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -x "2009/05/11 10:00:00" -X "2009/05/12 04:12:12" -S 5\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-X', '"2009/05/12 04:12:12"', '-x', '"2009/05/11 10:00:00"', '-S',
        '5']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test11: Test kontroly hodnot Time, Speed, Fps
input("\n\n\033[1mTest11: Test kontroly hodnot Time, Speed, Fps \033[0m")
print('./color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S -5\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '-5']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",ret)
#test11b: Test kontroly hodnot Time, Speed, Fps
input("\n\n\033[1mTest11b: Test kontroly hodnot Time, Speed, Fps \033[0m")
print('./color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -T a\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-T', 'a']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",ret)
#test11c: Test kontroly hodnot Time, Speed, Fps
input("\n\n\033[1mTest11c: Test kontroly hodnot Time, Speed, Fps \033[0m")
print('./color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -F 5a\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-F', '5a']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",ret)

#test12: Test kontroly rozsahu hodnot Time, Speed, Fps
input(
    "\n\n\033[1mTest12: Test kontroly rozsahu hodnot Time, Speed, Fps \033[0m")
print('./color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 200\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '200']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))
#test12b: Test kontroly rozsahu hodnot Time, Speed, Fps
input(
    "\n\n\033[1mTest12b: Test kontroly rozsahu hodnot Time, Speed, Fps \033[0m")
print('./color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -F 240\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-F', '240']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))
#test12c: Test kontroly rozsahu hodnot Time, Speed, Fps
input(
    "\n\n\033[1mTest12c: Test kontroly rozsahu hodnot Time, Speed, Fps \033[0m")
print('./color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -T 2\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-T', '2']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))
#test12d: Test kontroly rozsahu hodnot Time, Speed, Fps
input(
    "\n\n\033[1mTest12d: Test kontroly rozsahu hodnot Time, Speed, Fps \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -T 20 -F 24\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-T', '20', '-F', '24']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))
#test12e: Test kontroly rozsahu hodnot Time, Speed, Fps
input(
    "\n\n\033[1mTest12e: Test kontroly rozsahu hodnot Time, Speed, Fps \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -T 20 -F 24 -E\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-T', '20', '-F', '24', '-E']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))
#test12f: Test kontroly rozsahu hodnot Time, Speed, Fps
input(
    "\n\n\033[1mTest12f: Test kontroly rozsahu hodnot Time, Speed, Fps \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 1 -T 20 -F 72 -X auto -x auto\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '1', '-T', '20', '-F', '72', '-X', 'auto', '-x', 'auto']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))
#test12g: Test kontroly rozsahu hodnot Time, Speed, Fps
input(
    "\n\n\033[1mTest12g: Test kontroly rozsahu hodnot Time, Speed, Fps \033[0m")
print('./color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -T 20 -F 340\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-T', '20', '-F', '340']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))
#test12h: Test kontroly rozsahu hodnot Time, Speed, Fps
input(
    "\n\n\033[1mTest12h: Test kontroly rozsahu hodnot Time, Speed, Fps \033[0m")
print('./color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -T 20 -F 340 -E\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-T', '20', '-F', '340', '-E']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test13: Test nazvu slozky videa
input("\n\n\033[1mTest13: Test nazvu slozky videa \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -n "slozka s mezerou"\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-n', '"slozka s mezerou"']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test14: Test parametru efektu vykreslovani
input("\n\n\033[1mTest14: Test parametru efektu vykreslovani \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -e smer=1:xyz=abc:abc=a2b\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-e', 'smer=1:xyz=abc:abc=a2b']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))
#test14b: Test parametru efektu vykreslovani
input("\n\n\033[1mTest14b: Test parametru efektu vykreslovani \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -e smer=1=xyz=abc:abc=a2b\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-e', 'smer=1=xyz=abc:abc=a2b']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))
#test14c: Test parametru efektu vykreslovani
input("\n\n\033[1mTest14c: Test parametru efektu vykreslovani \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -e smXr=1:xyz=abc:abc=a2b\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-e', 'smXr=1:xyz=abc:abc=a2b']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test15: Test parametru Legend
input("\n\n\033[1mTest15: Test parametru Legend \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -l "legenda efektu"\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-l', '"legenda efektu"']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test16: Test vicenasobneho pouziti prepinace
input("\n\n\033[1mTest16: Test vicenasobneho pouziti prepinace \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -Y 150 -Y auto\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-Y', '150', '-Y', 'auto']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",ret)

#test16b: Test vicenasobneho pouziti prepinace (povolene opakovani)
input(
    "\n\n\033[1mTest16b: Test vicenasobneho pouziti prepinace (povolene opakovani) \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -Y 150 -e smer=2:smer=3 -e smer=1\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-Y', '150', '-e', 'smer=2:smer=3', '-e', 'smer=1']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test17: Test konfiguracniho souboru
input("\n\n\033[1mTest17: Test konfiguracniho souboru \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -f testy/configOK.txt \n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-f', 'testy/configOK.txt']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test18: Test platnosti prepinacu pred konfiguracnim souborem
input(
    "\n\n\033[1mTest18: Test platnosti prepinacu pred konfiguracnim souborem \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -f testy/configOK.txt -Y max -y min -X max -x min -e smer=3\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-f', 'testy/configOK.txt', '-Y', ' max', '-y', 'min', '-X',
        'max', '-x', 'min','-e','smer=3']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test19: Test existence konfiguracniho souboru
input("\n\n\033[1mTest19: Test existence konfiguracniho souboru \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -f testy/configKO.txt\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-f', 'testy/configKO.txt']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",ret)

#test20: Test prav konfiguracniho souboru
input("\n\n\033[1mTest20: Test prav konfiguracniho souboru \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -f testy/souborBezPrav.txt\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-f', 'testy/souborBezPrav.txt']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",ret)

#test21: Test hodnot v konfiguracnim souboru
input("\n\n\033[1mTest21: Test hodnot v konfiguracnim souboru\033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -f testy/configChyba.txt\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-f', 'testy/configChyba.txt']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test22: Test zadany konfiguracni soubor a chybnym prepinacem
input(
    "\n\n\033[1mTest22: Test zadany konfiguracni soubor s chybnym prepinacem\033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -f testy/configOK.txt -X xxx\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-f', 'testy/configOK.txt', '-X', 'xxx']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test23: Test stazeni souboru z internetu
input("\n\n\033[1mTest23: Test stazeni souboru z internetu\033[0m")
print(
    './color_magic.py https://users.fit.cvut.cz/~barinkl/data1 -t "[%H:%M:%S %d.%m.%Y]" -S 5\n')
args = ['./color_magic.py', '"https://users.fit.cvut.cz/~barinkl/data1"', '-t',
        '"[%H:%M:%S %d.%m.%Y]"', '-S', '5']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))
#test23b: Test stazeni neplatneho souboru z internetu
input("\n\n\033[1mTest23b: Test stazeni neplatneho souboru z internetu\033[0m")
print(
    './color_magic.py https://users.fit.cvut.cz/~barinkl/data1x -t "[%H:%M:%S %d.%m.%Y]" -S 5\n')
args = ['./color_magic.py', '"https://users.fit.cvut.cz/~barinkl/data1x"',
        '-t', '"[%H:%M:%S %d.%m.%Y]"', '-S', '5']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test23c: Test potlaceni neplatneho souboru z internetu
input(
    "\n\n\033[1mTest23c: Test potlaceni neplatneho souboru z internetu\033[0m")
print(
    './color_magic.py https://users.fit.cvut.cz/~barinkl/data1x -t "[%H:%M:%S %d.%m.%Y]" -S 5 -E\n')
args = ['./color_magic.py', '"https://users.fit.cvut.cz/~barinkl/data1x"',
        '-t', '"[%H:%M:%S %d.%m.%Y]"', '-S', '5', '-E']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test23d: Test stazeni vice souboru z internetu
input("\n\n\033[1mTest23d: Test stazeni vice souboru z internetu\033[0m")
print(
    './color_magic.py https://users.fit.cvut.cz/~barinkl/data1 https://users.fit.cvut.cz/~barinkl/data1 -t "[%H:%M:%S %d.%m.%Y]" -S 5\n')
args = ['./color_magic.py', '"https://users.fit.cvut.cz/~barinkl/data1"',
        '"https://users.fit.cvut.cz/~barinkl/data1"', '-t',
        '"[%H:%M:%S %d.%m.%Y]"', '-S', '5']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test23e: Test stazeni vice souboru z internetu s potlacenim chyby
input(
    "\n\n\033[1mTest23e: Test stazeni vice souboru z internetu s potlacenim chyby\033[0m")
print(
    './color_magic.py https://users.fit.cvut.cz/~barinkl/data1x https://users.fit.cvut.cz/~barinkl/data1 -t "[%H:%M:%S %d.%m.%Y]" -S 5 -E\n')
args = ['./color_magic.py', '"https://users.fit.cvut.cz/~barinkl/data1x"',
        '"https://users.fit.cvut.cz/~barinkl/data1"', '-t',
        '"[%H:%M:%S %d.%m.%Y]"', '-S', '5', '-E']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test23f: Test stazeni vice souboru z internetu s potlacenim chyby
input(
    "\n\n\033[1mTest23f: Test stazeni vice souboru z internetu s potlacenim chyby\033[0m")
print(
    './color_magic.py https://users.fit.cvut.cz/~barinkl/data1 https://users.fit.cvut.cz/~barinkl/data1x -t "[%H:%M:%S %d.%m.%Y]" -S 5 -E\n')
args = ['./color_magic.py', '"https://users.fit.cvut.cz/~barinkl/data1"',
        '"https://users.fit.cvut.cz/~barinkl/data1x"', '-t',
        '"[%H:%M:%S %d.%m.%Y]"', '-S', '5', '-E']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test23g: Test stazeni vice souboru z internetu + lokalni soubor
input(
    "\n\n\033[1mTest23g: Test stazeni vice souboru z internetu + lokalni soubor\033[0m")
print(
    './color_magic.py https://users.fit.cvut.cz/~barinkl/data1 https://users.fit.cvut.cz/~barinkl/data1 testy/webLocal.txt -t "[%H:%M:%S %d.%m.%Y]" -S 5\n')
args = ['./color_magic.py', '"https://users.fit.cvut.cz/~barinkl/data1"',
        '"https://users.fit.cvut.cz/~barinkl/data1"', 'testy/webLocal.txt',
        '-t', '"[%H:%M:%S %d.%m.%Y]"', '-S', '5']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test24: Test postupne navazujicich neprekryvajicich se souboru
input(
    "\n\n\033[1mTest24: Test postupne navazujicich neprekryvajicich se souboru\033[0m")
print(
    './color_magic.py testy/split/aa testy/split/ab testy/split/ac testy/split/ad testy/split/ae -t "%Y/%m/%d %H:%M:%S" -S 5 -e smer=2\n')
args = ['./color_magic.py', 'testy/split/aa', 'testy/split/ab',
        'testy/split/ac', 'testy/split/ad', 'testy/split/ae', '-t',
        '"%Y/%m/%d %H:%M:%S" ', '-S', '5', '-e', 'smer=2']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test25: Test vice nenavazujicich a neprekryvajicich se souboru
input(
    "\n\n\033[1mTest25: Test nenavazujicich a neprekryvajicich se souboru\033[0m")
print(
    './color_magic.py testy/split/aa testy/split/ac testy/split/ae -t "%Y/%m/%d %H:%M:%S" -S 5 -e smer=3\n')
args = ['./color_magic.py', 'testy/split/aa', 'testy/split/ac',
        'testy/split/ae', '-t', '"%Y/%m/%d %H:%M:%S" ', '-S', '5', '-e',
        'smer=3']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test26: Test jeden soubor s nesoumernymi casovymi hodnotami
input(
    "\n\n\033[1mTest26: Test jeden soubor s nesoumernymi casovymi hodnotami\033[0m")
print('./color_magic.py testy/split/concat -t "%Y/%m/%d %H:%M:%S" -S 5\n')
args = ['./color_magic.py', 'testy/split/concat', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test27: Test postupne navazujicich neprekryvajicich se souboru v neusporadanem poradi
input(
    "\n\n\033[1mTest27: Test postupne navazujicich neprekryvajicich se souboru v neusporadanem poradi\033[0m")
print(
    './color_magic.py testy/split/ac testy/split/aa testy/split/ad testy/split/ae testy/split/ab -t "%Y/%m/%d %H:%M:%S" -S 5\n')
args = ['./color_magic.py', 'testy/split/ac', 'testy/split/aa',
        'testy/split/ad', 'testy/split/ae', 'testy/split/ab', '-t',
        '"%Y/%m/%d %H:%M:%S" ', '-S', '5']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test28: Test prekryvajicich se dat
input("\n\n\033[1mTest28: Test prekryvajicich se dat\033[0m")
print(
    './color_magic.py testy/split/aa testy/split/ab testy/split450/ab testy/split450/ac -t "%Y/%m/%d %H:%M:%S" -S 5\n')
args = ['./color_magic.py', 'testy/split/aa', 'testy/split/ab',
        'testy/split450/ab', 'testy/split450/ac', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test28b: Test prekryvajicich se dat jine poradi
input("\n\n\033[1mTest28b: Test prekryvajicich se dat jine poradi\033[0m")
print(
    './color_magic.py testy/split450/aa testy/split/ab testy/split/ac testy/split/ad -t "%Y/%m/%d %H:%M:%S" -S 5 -e smer=2\n')
args = ['./color_magic.py', 'testy/split450/aa', 'testy/split/ab',
        'testy/split/ac', 'testy/split/ad', '-t', '"%Y/%m/%d %H:%M:%S" ', '-S',
        '5', '-e', 'smer=2']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test28c: Test prekryvajicich se dat mimo osu X
input("\n\n\033[1mTest28c: Test prekryvajicich se dat mimo osu X\033[0m")
print(
    './color_magic.py testy/split350/ab testy/split350/ad testy/split450/ac testy/split350/ac testy/prekryvMimoX.txt -t "%Y/%m/%d %H:%M:%S" -S 5\n')
args = ['./color_magic.py', 'testy/split350/ab', 'testy/split350/ad',
        'testy/split450/ac', 'testy/split350/ac', 'testy/prekryvMimoX.txt',
        '-t', '"%Y/%m/%d %H:%M:%S" ', '-S', '5']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test28d: Test prekryvajicich se dat mimo osu X jine poradi
input(
    "\n\n\033[1mTest28d: Test prekryvajicich se dat mimo osu X jine poradi\033[0m")
print(
    './color_magic.py testy/split350/ab testy/split350/ad testy/split450/ac testy/split350/aa testy/split350/ac testy/prekryvMimoX2.txt -t "%Y/%m/%d %H:%M:%S" -S 6 -Y max -y min\n')
args = ['./color_magic.py', 'testy/split350/ab', 'testy/split350/ad',
        'testy/split450/ac', 'testy/split350/aa', 'testy/split350/ac',
        'testy/prekryvMimoX2.txt', '-t', '"%Y/%m/%d %H:%M:%S" ', '-S', '6',
        '-Y', 'max', '-y', 'min']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test28e: Test prekryvajicich se dat mimo osu X jine poradi
input(
    "\n\n\033[1mTest28e: Test prekryvajicich se dat mimo osu X jine poradi\033[0m")
print(
    './color_magic.py testy/split350/ab testy/prekryvMimoXHalf.txt testy/split350/ad testy/split450/ac testy/split350/aa testy/split350/ac -t "%Y/%m/%d %H:%M:%S" -S 6 -Y max -y min\n')
args = ['./color_magic.py', 'testy/split350/ab', 'testy/prekryvMimoXHalf.txt',
        'testy/split350/ad', 'testy/split450/ac', 'testy/split350/aa',
        'testy/split350/ac', '-t', '"%Y/%m/%d %H:%M:%S" ', '-S', '6', '-Y',
        'max', '-y', 'min']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test29: Test data s neciselnymi hodnotami
input("\n\n\033[1mTest29: Test data s neciselnymi hodnotami \033[0m")
print('./color_magic.py testy/sinSotek.txt -t "%Y/%m/%d %H:%M:%S" -S 5\n')
args = ['./color_magic.py', 'testy/sinSotek.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test30: Test fungovani efektu
input("\n\n\033[1mTest30: fungovani efektu \033[0m")
print('./color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -e smer=2\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-e', 'smer=2']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))
#test30b: Test fungovani efektu
input("\n\n\033[1mTest30b: fungovani efektu \033[0m")
print('./color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -e smer=3\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-e', 'smer=3']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))
#test30c: Test fungovani efektu + casovy format
input("\n\n\033[1mTest30c: fungovani efektu + casovy format \033[0m")
print(
    './color_magic.py testy/random.data -t "%H:%M:%S" -S 5 -e smer=3 -X max -x min -Y max -y min\n')
args = ['./color_magic.py', 'testy/random.data', '-t', '"%H:%M:%S" ', '-S',
        '5', '-e', 'smer=3', '-X', 'max', '-x', 'min', '-Y', 'max', '-y',
        'min']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test31: Test pojmenovani slozky s cestou
input("\n\n\033[1mTest31: pojmenovani slozky s cestou \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -e smer=3 -n testy/vnejsi/vnitrni/animace\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-e', 'smer=3', '-n', 'testy/vnejsi/vnitrni/animace']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))

#test31b: Test pojmenovani slozky s cestou (verze 2)
input("\n\n\033[1mTest31b: pojmenovani slozky s cestou (verze 2) \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -e smer=3 -n testy/vnejsi/vnitrni/animace\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-e', 'smer=3', '-n', 'testy/vnejsi/vnitrni/animace']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))
#test31c: Test pojmenovani slozky s chybnou cestou
input("\n\n\033[1mTest3c1: pojmenovani slozky s chybnou cestou \033[0m")
print(
    './color_magic.py testy/sin.txt -t "%Y/%m/%d %H:%M:%S" -S 5 -e smer=3 -n testy/vnejsi/vnXXrni/animace\n')
args = ['./color_magic.py', 'testy/sin.txt', '-t', '"%Y/%m/%d %H:%M:%S" ',
        '-S', '5', '-e', 'smer=3', '-n', 'testy/vnejsi/vnXXrni/animace']

ret = subprocess.call(' '.join(args), shell=True)
print("return code:",abs(ret))
