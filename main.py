import random
from pprint import pprint
import json
import re
import logging

LEADERBOARD_SOUBOR = "leaderboard.json"
karty = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
barvy = ['S', 'K', 'P', 'L']

hodnoty_karet = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10,
                 "K": 10}
# balicek = [[{'hodnota': hodnota, 'barva': barva}for hodnota in hodnoty] for barva in barvy]
# print(balicek)
balicek = []
bonbony_celkem = 1000
bonbony_max = 1000


def pravidla():  # soupis pravidel
    print('''
    - V blackjacku hrajete proti dealerovi.
    - Po nastavení sázky dostanete dvě karty.
    - Dealer dostane dvě karty, ale odhalí pouze jednu z nich.
    - Pokud se hodnota vašich prvních dvou karet sčítá na 21, máte blackjack.
    - Ve vašem tahu, pokud nedostanete blackjack nebo nezkrachujete, budete požádáni, abyste buď brali, stáli nebo
     dali doubledown pokud možno.
    - Braním dostanete další kartu.
    - Stání končí váš tah.
    - Pokud je součet vašich karet v jakémkoli okamžiku vyšší než 21, zkrachujete a automaticky prohrajete.
    - Pokud na konci kola máte vyšší skóre než dealer a nezkrachovali jste, vyhráváte.
    - Pokud máte nižší skóre než dealer nebo dealer má blackjack a vy ne, kolo prohrajete.
    - Pokud máte vy a dealer stejné skóre nebo jste oba získali blackjack, pak je to remíza (push).
    - Blackjack se vyplácí 3:2.
        Výhra se vyplácí 1:1.
        Remíza vám vrátí vaši sázku.
        Když prohrajete, prohrajete svou sázku
    - Double down je akce provedená na začátku vašeho tahu, když máte 2 karty. Ddvojnásobíte svou sázku, ale 
    získáte pouze jednu poslední kartu, než váš tah automaticky skončí.''')


def update_leaderboard(in_nick, bonbony, upd_leaderboard=[]):  # update leaderboardu
    in_leaderboard = False
    for i in upd_leaderboard:
        if i["nick"] == in_nick:
            in_leaderboard = True
            i["bonbony"] = bonbony
            break
    if not in_leaderboard:
        upd_leaderboard.append({"nick": in_nick, "bonbony": bonbony})

    # bubble sort
    for i in range(len(upd_leaderboard) - 1):
        swapped = False
        for x in range(len(upd_leaderboard) - 1):
            if upd_leaderboard[x]["bonbony"] < upd_leaderboard[x + 1]["bonbony"]:
                swapped = True
                upd_leaderboard[x], upd_leaderboard[x + 1] = upd_leaderboard[x + 1], upd_leaderboard[x]
        if not swapped:
            break

    ulozit_soubor(LEADERBOARD_SOUBOR, upd_leaderboard)


def ulozit_soubor(soubor, info):  # ukladani dat do leaderboardu
    with open(soubor, "w+") as soubor:
        try:
            in_json = json.dumps(info)
            soubor.write(in_json)
        except json.encoder.JSONEncoder as e:
            raise IOError("Něco je špatně, sprav mě prosím")


def dostat_soubor(soubor):  # hledani souboru pro leaderboard
    try:
        with open(soubor, "r") as soubor:
            try:
                out_json = json.loads(soubor.read())
                return out_json
            except json.decoder.JSONDecodeError:
                raise IOError(f"Sprav mě prosím. Něco je špatně se souborem {soubor}")
    except FileNotFoundError:
        raise IOError(f"Ups, nedokázal jsem najít soubor {soubor}")


def leaderboard():
    leaderboard = dostat_soubor(LEADERBOARD_SOUBOR)
    for i in leaderboard:
        print(i["nick"], " " * 10, i["bonbony"])


def hrac_plus_karta(hrac_karty, hrac_skore):  # prida hracovi kartu
    hrac_karta = random.choice(balicek)  # davani random karty hraci
    hrac_karty.append(hrac_karta)
    balicek.remove(hrac_karta)

    hrac_skore += hrac_karta["hodnota"]  # updatovani hracova skore
    return hrac_karty, hrac_skore


def dealer_plus_karta(dealer_karty, dealer_skore):  # prida dealerovi kartu
    dealer_karta = random.choice(balicek)
    dealer_karty.append(dealer_karta)
    balicek.remove(dealer_karta)

    dealer_skore += dealer_karta["hodnota"]  # updatovani dealerova skore
    return dealer_karty, dealer_skore


def hra(balicek, in_nick, bonbony_max, hodnoty_karet):
    global bonbony_celkem
    while True:
        bonbony = input(f"kolik chceš vsadit bonbonů? máš {bonbony_celkem} bonbonu")
        if bonbony.isdigit() and int(bonbony) > 0:
            if int(bonbony) > bonbony_celkem:
                pprint("nelze vsadit vice bonbonu nez mas v kapse")
            else:
                bonbony = int(bonbony)
                break
    # karty pro hrace a dealera
    hrac_karty = []
    dealer_karty = []

    # skore hrace a dealera
    hrac_skore = 0
    dealer_skore = 0

    while len(hrac_karty) < 2:  # rozdavani karet hraci
        hrac_karty, hrac_skore = hrac_plus_karta(hrac_karty, hrac_skore)
        if len(hrac_karty) == 2:  # kdyz hodnota obou prvnich karet danych hraci je A tak jedno ma hodnotu 11 a druhe 1
            if hrac_karty[0]["hodnota"] == 11 and hrac_karty[1]["hodnota"] == 11:
                hrac_karty[0]["hodnota"] = 1
                hrac_skore -= 10

        pprint("Hráčovi karty: ")
        pprint(hrac_karty)
        print("hráčovo skore = ", hrac_skore)
        print("hracovy bonbony", bonbony)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        dealer_karty, dealer_skore = dealer_plus_karta(dealer_karty, dealer_skore)

    if len(dealer_karty) == 2:  # kdyz hodnota obou 1. karet danych dealerovi je A tak jedno ma hodnotu 11 a druhe 1
        if dealer_karty[0]["hodnota"] == 11 and dealer_karty[1]["hodnota"] == 11:
            dealer_karty[0]["hodnota"] = 1
            dealer_skore -= 10

    pprint("Dealerovy karty: ")
    pprint(dealer_karty[0])
    print("dealorovo skore = ", dealer_skore - dealer_karty[1]["hodnota"])
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    if hrac_skore == 21:
        pprint("WOHOOO BLACKJACK")
        pprint("VYHRAL JSI TY HAZARDERE")
        bonbony_celkem += bonbony * 1.5
        return
    if hrac_skore > 21:
        pprint("SORRY KAMO, PROHRAL JSI")
        bonbony_celkem -= bonbony
        return

    while hrac_skore < 21:  # hrac zadava jestli chce stat, double down nebo brat kartu
        volba = input("Zadej B pro braní dalsí karty S pro stání nebo D pro DoubleDown").upper()
        if len(volba) != 1 or volba not in ["S", "B", "D"]:
            print("DOBREJ POKUS, TROUBO")  # kdyz zada jine pismenko ney b,s,d

        if volba == 'B':
            hrac_karty, hrac_skore = hrac_plus_karta(hrac_karty, hrac_skore)
            a = 0
            while a < len(hrac_karty):
                if hrac_karty[a]["hodnota"] == 11 and hrac_karty[a]["hodnota"] == 11 or hrac_karty[a]["hodnota"] == 11 \
                        and hrac_karty[a]["hodnota"] == 10:
                    hrac_karty[a]["hodnota"] = 1
                    hrac_skore -= 10
                a += 1

            pprint("Dealerovy karty: ")
            print(dealer_karty[0])
            print("dealorovo skore = ", dealer_skore - dealer_karty[-1]["hodnota"])
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            pprint("Hráčovi karty: ")
            pprint(hrac_karty)
            print("hráčovo skore = ", hrac_skore)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        if volba == 'S':  # kdyz zada s
            break

        if volba == 'D':  # kdyz zada d
            hrac_karty, hrac_skore = hrac_plus_karta(hrac_karty, hrac_skore)
            bonbony = bonbony * 2
            break

    pprint("Hráčovi karty: ")
    pprint(hrac_karty)
    print("hráčovo skore = ", hrac_skore)
    print("hracovy bonbony", bonbony)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    print("DEALER ODHLUJE SVE KARTY")

    pprint("Dealerovy karty: ")
    print(dealer_karty, False)
    print("dealorovo skore = ", dealer_skore)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    while dealer_skore < 17:
        pprint("DEALER SI BERE KARTU....")
        dealer_karty, dealer_skore = dealer_plus_karta(dealer_karty, dealer_skore)
        a = 0
        while a < len(dealer_karty):  # kdyz ma dealer 2 a nebo a a eso
            if dealer_karty[a]["hodnota"] == 11 and dealer_karty[a]["hodnota"] == 11 \
                    or dealer_karty[a]["hodnota"] == 11 \
                    and dealer_karty[a]["hodnota"] == 10:
                dealer_karty[a]["hodnota"] = 1
                hrac_skore -= 10
            a += 1
        pprint("Hráčovi karty: ")
        pprint(hrac_karty)
        print("hráčovo skore = ", hrac_skore)
        print("hracovy bonbony", bonbony)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        pprint("Dealerovy karty: ")
        print(dealer_karty)
        print("dealorovo skore = ", dealer_skore)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    if hrac_skore == 21:
        pprint("WOHOOO BLACKJACK")
        pprint("VYHRAL JSI TY HAZARDERE")
        bonbony_celkem += bonbony * 1.5

    elif hrac_skore > 21:
        pprint("SORRY KAMO, PROHRAL JSI")
        bonbony_celkem -= bonbony

    elif dealer_skore > 21:
        pprint("DEALER PROHRAVA! VYHRAL JSI TY HAZARDERE")
        bonbony_celkem += bonbony

    elif dealer_skore == hrac_skore:
        print("REMIZA")

    elif dealer_skore == 21:
        pprint("DEALER MA BLACKJACK! PROHRAL JSI")
        bonbony_celkem -= bonbony

    elif hrac_skore > dealer_skore:
        print("VYHRAL JSI TY HAZARDERE")
        bonbony_celkem += bonbony

    else:
        print("DEALER VYHRAL")
        bonbony_celkem -= bonbony

    if bonbony_celkem < 1:
        print("Spadl jsi na 0 bonbonu. ALE babicka ti dala 200 bonbonu, takze muzes hrat dal")
        bonbony_celkem = 200

    if bonbony_celkem > bonbony_max:
        bonbony_max = bonbony_celkem
        update_leaderboard(in_nick, bonbony_max, dostat_soubor(LEADERBOARD_SOUBOR))


for barva in barvy:

    for karta in karty:
        # karty v balicku
        balicek.append({"barva": barva, "karta": karta, "hodnota": hodnoty_karet[karta]})
        # balicek.append(karta(barvy[barva], karta, hodnoty_karet[karta]))

while True:  # zadavani jmena
    nick = input("Co je jméno tvé dobrodruhu? => ")
    if nick.isspace() or len(nick) < 1 or re.fullmatch('[^a-z0-9_A-Z-]', nick) or len(nick) > 20:
        continue
    else:
        break
while True:  # hlavni menu
    print("-" * 30)
    akce = input('''Zdravim te pri hre Blackjack
        prosim zvol si, co chceš dělat
    1. Začít hru
    2. Síň slávy
    3. Pravidla
    4. Ukončit hru
    ''')
    if akce == "1":
        hra(balicek, nick, bonbony_max, hodnoty_karet)

    elif akce == "2":
        leaderboard()

    elif akce == "3":
        pravidla()
    elif akce == "4":
        quit()
    else:
        continue


