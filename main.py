import random
from pprint import pprint

karty = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
barvy = ['S', 'K', 'P', 'L']

hodnoty_karet = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10,
                 "K": 10}
# balicek = [[{'hodnota': hodnota, 'barva': barva}for hodnota in hodnoty] for barva in barvy]
# print(balicek)
balicek = []

for barva in barvy:

    for karta in karty:
        # karty v balicku
        balicek.append({"barva": barva, "karta": karta, "hodnota": hodnoty_karet[karta]})
        # balicek.append(karta(barvy[barva], karta, hodnoty_karet[karta]))


def hra(balicek):
    global hodnoty_karet

    # karty pro hrace a dealera
    hrac_karty = []
    dealer_karty = []

    # skore hrace a dealera
    hrac_skore = 0
    dealer_skore = 0

    while len(hrac_karty) < 2:  # rozdavani karet hraci
        hrac_karta = random.choice(balicek)
        hrac_karty.append(hrac_karta)
        balicek.remove(hrac_karta)

        hrac_skore += hrac_karta["hodnota"]  # updatovani hracova skore

        if len(hrac_karty) == 2:  # kdyz hodnota obou prvnich karet danych hraci je A tak jedno ma hodnotu 11 a druhe 1
            if hrac_karty[0]["hodnota"] == 11 and hrac_karty[1]["hodnota"] == 11:
                hrac_karty[0]["hodnota"] = 1
                hrac_skore -= 10

        pprint("Hráčovi karty: ")
        pprint(hrac_karty)
        print("hráčovo skore = ", hrac_skore)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    dealer_karta = random.choice(balicek)
    dealer_karty.append(dealer_karta)
    balicek.remove(dealer_karta)

    dealer_skore += dealer_karta["hodnota"]  # updatovani dealerova skore

    if len(dealer_karty) == 2:  # kdyz hodnota obou prvnich karet danych dealerovi je A tak jedno ma hodnotu 11 a druhe 1
        if dealer_karty[0]["hodnota"] == 11 and dealer_karty[1]["hodnota"] == 11:
            dealer_karty[0]["hodnota"] = 1
            dealer_skore -= 10

    pprint("Dealerovy karty: ")
    if len(dealer_karty) == 1:
        pprint(dealer_karty[0])
        print("dealorovo skore = ", dealer_skore)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    else:
        print(dealer_karty[:-1], True)
        print("dealorovo skore = ", dealer_skore - dealer_karty[:-1]["hodnota"])
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    if hrac_skore == 21:
        pprint("WOHOOO BLACKJACK")
        pprint("VYHRAL JSI TY ZKURVENEJ HAZARDERE")
        return
    if hrac_skore > 21:
        pprint("SORRY KAMO, PROHRAL JSI")

    while hrac_skore < 21:
        volba = input("Zadej B pro braní dalsí karty nebo S pro stání").upper()
        if len(volba) != 1 or volba not in ["S", "B"]:
            print("DOBREJ POKUS, VOLE")

        if volba == 'B':
            hrac_karta = random.choice(balicek)  # davani random karty hraci
            hrac_karty.append(hrac_karta)
            balicek.remove(hrac_karta)

            hrac_skore += hrac_karta["hodnota"]  # updatovani hracova skore

            a = 0
            while a < len(hrac_karty):
                if hrac_karty[a]["hodnota"] == 11 and hrac_karty[a]["hodnota"] == 11 or hrac_karty[a]["hodnota"] == 11 and hrac_karty[a]["hodnota"] == 10:
                    hrac_karty[a]["hodnota"] = 1
                    hrac_skore -= 10
                a += 1

            pprint("Dealerovy karty: ")
            print(dealer_karty[:-1], True)
            print("dealorovo skore = ", dealer_skore - dealer_karty[:-1]["hodnota"])
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            pprint("Hráčovi karty: ")
            pprint(hrac_karty, False)
            print("hráčovo skore = ", hrac_skore)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        if volba == 'S':
            break

    pprint("Hráčovi karty: ")
    pprint(hrac_karty, False)
    print("hráčovo skore = ", hrac_skore)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    print("DEALER ODHLUJE SVE KARTY")

    pprint("Dealerovy karty: ")
    print(dealer_karty, False)
    print("dealorovo skore = ", dealer_skore)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    if hrac_skore == 21:
        pprint("WOHOOO BLACKJACK")
        pprint("VYHRAL JSI TY ZKURVENEJ HAZARDERE")
        quit()

    if hrac_skore > 21:
        pprint("SORRY KAMO, PROHRAL JSI")
        quit()

    input()

    while dealer_skore < 17:

        pprint("DEALER SI BERE KARTU....")

        dealer_karta = random.choice(balicek)
        dealer_karty.append(dealer_karta)
        balicek.remove(dealer_karta)

        dealer_skore += dealer_karta["hodnota"]  # updatovani dealerova skore

        a = 0
        while a < len(hrac_karty):
            if hrac_karty[a]["hodnota"] == 11 and hrac_karty[a]["hodnota"] == 11 or hrac_karty[a]["hodnota"] == 11 and \
                    hrac_karty[a]["hodnota"] == 10:
                hrac_karty[a]["hodnota"] = 1
                hrac_skore -= 10
            a += 1

        pprint("Hráčovi karty: ")
        pprint(hrac_karty, False)
        print("hráčovo skore = ", hrac_skore)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        pprint("Dealerovy karty: ")
        print(dealer_karty[:-1], True)
        print("dealorovo skore = ", dealer_skore - dealer_karty[:-1]["hodnota"])
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    if dealer_skore > 21:
        pprint("DEALER PROHRAVA! VYHRAL JSI TY ZKURVENEJ HAZARDERE")
        quit()

    if dealer_skore == 21:
        pprint("DEALER MA BLACKJACK! PROHRAL JSI")
        quit()

    if dealer_skore == hrac_skore:
        print("REMIZA")

    elif hrac_skore > dealer_skore:
        print("VYHRAL JSI TY ZKURVENEJ HAZARDERE")

    else:
        print("DEALER VYHRAL")


hra(balicek)
