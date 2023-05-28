import random
import csv

#Definiera värden för valutorna och valörerna
Valuta = {"Två":2, "Tre":3, "Fyra":4, "Fem":5, "Sex":6, "Sju":7, "åtta":8, "Nio":9, "Tio":10, "Knäckt":10, "Dam":10, "Kung":10, "Ess":11}
Valör = {"Hjärter", "Spader", "Ruter", "Klöver"}

#Definierar globala variabler för spelet
playing = True
skip = False
split_check = False
hand1 = True
hand2 = True
hand1_end = False
hand2_end = False
första_rundan = True

#Klassen Spelare
class Spelare:

    def __init__(self, namn):
        self.namn = namn
        self.tot_vinst = 0

    def __str__(self):
        return self.namn
    
    #Funktion för spelarens vinst
    def vinst(self):
        self.tot_vinst = spelare_chips.total - 100
        if self.tot_vinst > 0:
            print("\nGrattis", self.namn, "du har vunnit", self.tot_vinst,"kr. Tack för att du spelade!")
        elif self.tot_vinst < 0:
            print("\nTyvärr", self.namn, "du har förlorat", self.tot_vinst * -1,"kr. Tack för att du spelade!")
        else:
            print("\n", self.namn, "du har gått jämt ut. Tack för att du spelade!")
        self.sort()
    
    def no_money(self):
        self.tot_vinst = spelare_chips.total - 100
        print("\n", self.namn,"du har lyckets med att bli av med alla dina pengar. Tack för att du spelade!. Bättre lycka nästa gång.")
        self.sort()
    
    #Sortera topplistan baserat på vinsten
    def sort(self):
        filename = "scoreboard.csv"
        with open(filename, "r") as file:
            reader = csv.reader(file)
            data = list(reader)
            data.append([self.namn, self.tot_vinst])
            
            data = [(row[0], float(row[1])) for row in data]
            
            insertion_sort(data)
            
            with open (filename, "w", newline="") as file:
                writer = csv.writer(file)
                for row in data:
                    writer.writerow(row)

#Hjälpfunktion för sorteringsalgoritmen sort
def insertion_sort(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and key[1] > data[j][1]:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key

#Visa highscore listan
def highscore():
    filename = 'scoreboard.csv'
    print("\n------------------------------------------")
    print("Detta är highscore listan:")
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
        for i in data:
            print(i[0:2])
    print("------------------------------------------")
    if nytt_spel.lower()[0] != "n":
        input("Tryck enter för att gå tillbaka till menyn.")

#Regler för spelet
def regler():
    print("------------------------------------------")
    
    print("\nMålet med blackjack är att få 21 poäng eller så nära 21 poäng som möjligt utan att gå över 21 poäng.")
    print("Efter att du har stannat kommer dealern dra kort tills hans kort är värda 17 eller mer.\n")
    
    print("Hit - Få ett till kort.")
    print("Stand - Stanna med de kort du har. (Du får inte ett till kort)")
    print("Double - Dubbla din insats och få ett till sista kort.")
    print("Split - Om du får två kort med samma valör kan du splitta dem och spela med två händer.")
    print("Insurance - Om dealerns första kort är ett ess kan du välja att satsa upp till hälften av din insats på att dealern får blackjack.")
    print("give up - Om du inte gillar dina kort kan du ge upp och få hälften av din insats tillbaka under första rundan.")
    print("Charlie - Om du får 5 kort utan att gå över 21 vinner du automatiskt.")
    print("Highscore - Se topplistan.")
    print("------------------------------------------\n")
    input("Tryck enter för att gå tillbaka till menyn.")

class Kort:

    def __init__(self, valör, valuta):
        self.valör = valör
        self.valuta = valuta

    def __str__(self):
        return self.valör + " " + self.valuta

class Kortlek:

    def __init__(self):
        self.kortlek = []
        for valör in Valör:
            for valuta in Valuta:
                self.kortlek.append(Kort(valör, valuta))

    def __str__(self):
        kortlek = ""
        for kort in self.kortlek:
            kortlek += '\n' + kort.__str__()
        return "Kortleken har:" + kortlek
    
    def shuffle(self):
        random.shuffle(self.kortlek)
        
    def deal(self):
        kort = self.kortlek.pop()
        print(kort)
        return kort
    
    def deal_hidden(self):
        kort = self.kortlek.pop()
        return kort

class Hand:

    def __init__(self):
        self.hand = []
        self.hand_value = 0
        self.aces = 0
        self.item_count = 0

    def __str__(self):
        hand = ""
        for kort in self.hand:
            hand += '\n' + kort.__str__()
        return "Handen har:" + hand
    
    def __getitem__(self, index):
        return self.hand[index]

    #Lägger till ett kort i handen
    def add_card(self, kort):
        self.hand.append(kort)
        self.hand_value += Valuta[kort.valuta]
        self.item_count += 1
        if kort.valuta == "Ess":
            self.aces += 1

    #Kollar om det finns ett ess i handen och om det finns om det är värt 1 eller 11
    def adjust_for_ace(self):
        while self.hand_value > 21 and self.aces:
            self.hand_value -= 10
            self.aces -= 1

class chips:

    def __init__(self):
        self.total = 100
        self.bet = 0
        self.bet_insurance = 0

    #Vinner mot dealern
    def win_bet(self):
        self.total += self.bet
        self.total -= self.bet_insurance

    #Förlorar mot dealern
    def lose_bet(self):
        self.total -= self.bet
        self.total -= self.bet_insurance

def take_bet(chips):
    while True:
        try:
            print("Du har", chips.total)
            chips.bet = int(input("Hur mycket vill du satsa? "))
            print("")
        except ValueError:
            print("Du måste betta ett nummer.")
        else:
            if chips.bet > chips.total:
                print("Du har inte så mycket pengar. Du har bara", chips.total)
            else:
                break

#Lägger till ett kort samt printar ut det i konsollen
def hit(kortlek, hand):
    hand.add_card(kortlek.deal())
    if hand == dealer_hand:
        print("Dealern fick kortet", hand.hand[hand.item_count - 1], "tryck enter för att fortsätta.")
        input(">> ")
    else:
        print("Du fick kortet", hand.hand[hand.item_count - 1], "tryck enter för att fortsätta.")
        input(">> ")
    hand.adjust_for_ace()

#Slutar spelet och visar resultatet
def stand(hand):
    switch(hand)
    print("Du har valt att stanna.\n")

#Dubblar bettet och får ett sista kort
def double_down(kortlek, hand, chips):
    chips.bet = chips.bet * 2
    hit(kortlek, hand)

#Ger upp och får tillbaka hälften av bettet
def give_up(spelare, chips):
    global skip
    skip = True
    end(spelare)
    switch(spelare)
    chips.bet = chips.bet / 2
    chips.lose_bet()
    print("Du har valt att ge upp. Därmed får du tillbaka hälften av din insats.")

def insurance(spelare, dealer, chips):
    if dealer.hand[1].valuta == "Ess" and spelare.item_count == 2:
        print("--------------------------------------------------")
        print("Du kan välja att försäkra dig mot att dealern får blackjack. Det vill säga, eftersom dealern visar ett ess kan du bett upp till hälften av ditt bett i försäkring.\nDu vinner det bettet om dealern får 21 på två kort.")
        print("--------------------------------------------------")
        while True:
            try:
                insurance = int(input("Hur mycket vill du lägga undan som försäkring?: "))
            except ValueError:
                print("Du måste skriva ett nummer")
            else:
                if insurance == "":
                    print("Du måste skria någonting.")
                    continue
                elif insurance == 0:
                    break
                elif insurance > chips.total:
                    print("Du har inte så mycket pengar. Du har bara", chips.total)
                    continue
                elif insurance > chips.bet / 2:
                    print("Du kan som mest ha hälften av ditt bett som försäkring. Ditt orginalbett är", chips.bet)
                    continue
                elif insurance <= chips.bet / 2:
                    chips.bet_insurance = insurance
                    break

#Splittar handen till två händer
def split(kortlek):
    global playing
    global skip
    global split_check
    skip = True
    split_check = True
    print("\nDu har valt att splitta.\nDu har nu två händer.")
    spelare_hand2 = Hand()
    spelare_chips2.bet = spelare_chips.bet
    spelare_hand.hand_value -= Valuta[spelare_hand.hand[1].valuta]
    spelare_hand2.hand_value += Valuta[spelare_hand.hand[1].valuta]
    spelare_hand2.hand.append(spelare_hand[1])
    spelare_hand.hand.remove(spelare_hand[1])
    spelare_hand.add_card(kortlek.deal_hidden())
    spelare_hand2.add_card(kortlek.deal_hidden())
    spelare_hand.item_count = 2
    spelare_hand2.item_count = 2
    spelare_hand.adjust_for_ace()
    spelare_hand2.adjust_for_ace()
    
    #Din första hand körs
    while hand1 == True:
        print("\nFörsta handen:\n")
        show_some(spelare_hand, dealer_hand)
        hit_or_stand(kortlek, spelare_hand, spelare_chips)
        check_bust_hidden(spelare_hand, dealer_hand, spelare_chips)
        charlie(spelare_hand, spelare_chips)
        playing = False

    #Andra handen körs
    while hand2 == True:
        print("\nAndra handen:\n")
        show_some(spelare_hand2, dealer_hand)
        hit_or_stand(kortlek, spelare_hand2, spelare_chips2)
        check_bust(spelare_hand2, dealer_hand, spelare_chips2)
        charlie(spelare_hand2, spelare_chips2)
        playing = False

    if spelare_hand.hand_value <= 21 or spelare_hand2.hand_value <= 21 and hand1_end == False or hand2_end == False:
        input("Tryck enter för att se dealerns kort.")
    if spelare_hand.hand_value <= 21 and hand1_end == False:
        input("\nDealerns kort mot din första hand.")
        check_vinst(spelare_hand, dealer_hand, spelare_chips)
    if spelare_hand2.hand_value <= 21 and hand2_end == False:
        input("\nDealerns kort mot din andra hand.")
        check_vinst(spelare_hand2, dealer_hand, spelare_chips2)

#Funktion som gör att du vinner om du får 5 kort utan att gå över 21
def charlie(hand, chips):
    global skip
    if hand.item_count == 5 and hand.hand_value <= 21:
        print("Du har fått 5 kort utan att gå över 21. Du vinner på grund av Charlie-regeln.")
        switch(hand)
        end(hand)
        skip = True
        chips.win_bet()

def hit_or_stand(kortlek, hand, chips):
    insurance(hand, dealer_hand, spelare_chips)
    while True:
        #Checkar om man kan splitta
        if hand.item_count == 2 and hand.hand[0].valuta == hand.hand[1].valuta and chips.total >= chips.bet*2 and split_check == False:
            hs = input("\nHit, Stand, Double down, Split, give up\n")
            if hs == "":
                continue
            elif hs.lower() == "split":
                split(kortlek)
            elif hs.lower()[0] == "h":
                show_player(hand)
                hit(kortlek, hand)
                print()
            elif hs.lower() == "stand":
                stand(hand)
            elif hs.lower()[0] == "d":
                if chips.bet * 2 > chips.total:
                    print("Du har inte tillräckligt med pengar för att dubbla.")
                else:
                    print("Du har valt att dubbla ditt bett.\nDu kommer få ett sista kort. Tryck enter för att se ditt sista kort")
                    input(">> ")
                    show_player(hand)
                    double_down(kortlek, hand, chips)
                    switch(hand)
            elif hs.lower()[0] == "g":
                give_up(hand, chips)
            else:
                print("Försök igen.")
                continue
            
        #Om första rundan utan att kunna splitta
        elif hand.item_count == 2:
            hs = input("\nHit, Stand, Double down, give up\n")
            if hs == "":
                continue
            elif hs.lower()[0] == "h":
                show_player(hand)
                hit(kortlek, hand)
                print()
            elif hs.lower()[0] == "s":
                stand(hand)
            elif hs.lower()[0] == "d":
                if chips.bet * 2 > chips.total:
                    print("Du har inte tillräckligt med pengar för att dubbla.")
                else:
                    print("Du har valt att dubbla ditt bett.\nDu kommer få ett sista kort. Tryck enter för att se ditt sista kort")
                    input(">> ")
                    show_player(hand)
                    double_down(kortlek, hand, chips)
                    switch(hand)
            elif hs.lower()[0] == "g":
                give_up(hand, chips)
            else:
                print("Försök igen.")
                continue
            break
        
        #Det som kommer upp efter första rundan
        else:
            hs = input("\nHit, Stand, Double down\n")
            if hs == "":
                continue
            elif hs.lower()[0] == "h":
                show_player(hand)
                hit(kortlek, hand)
                print()
            elif hs.lower()[0] == "s":
                stand(hand)
            elif hs.lower()[0] == "d":
                if chips.bet * 2 > chips.total:
                    print("Du har inte tillräckligt med pengar för att dubbla.")
                else:
                    print("Du har valt att dubbla ditt bett.\nDu kommer få ett sista kort. Tryck enter för att se ditt sista kort")
                    input(">> ")
                    show_player(hand)
                    double_down(kortlek, hand, chips)
                    switch(hand)
            else:
                print("Försök igen.")
                continue
            break

#Det som gör att man byter från första handen till andra handen när man splittar
def switch(hand):
    global playing
    global hand1
    global hand2
    playing = False
    if hand == spelare_hand:
        hand1 = False
    elif hand != spelare_hand:
        hand2 = False

# Det som gör att handen räknas som klar
def end(hand):
    global hand1_end
    global hand2_end
    if hand == spelare_hand:
        hand1_end = True
    elif hand != spelare_hand:
        hand2_end = True

#Visar de olika händerna
def show_player(spelare):
    print("\nSpelarens hand:")
    for i in range(len(spelare.hand)):
        print("", spelare.hand[i])

def show_dealer(dealer):
    print("dealerns hand:")
    for i in range(len(dealer.hand)):
        print("", dealer.hand[i])

def show_some(spelare, dealer):
    print("dealerns hand:")
    print(" <kort dolt>")
    print('', dealer.hand[1])
    print("\nSpelarens hand:", *spelare.hand, sep='\n ')
    
def show_all(spelare, dealer):
    print("dealerns hand:", *dealer.hand, sep='\n ')
    print("dealerns hand =", dealer.hand_value)
    print("\nSpelarens hand:", *spelare.hand, sep='\n ')
    print("Spelarens hand =", spelare.hand_value)

#Vad som händer om man går över 21
def player_bust(spelare, dealer, chips):
    input("Du har kommit över 21, tryck enter för att se resultatet.\n")
    show_all(spelare, dealer)
    print("Spelaren har gått över 21. dealern vinner.")
    chips.lose_bet()

#Vad som händer om man går över 21 fast dealerns hand vissas inte
def player_bust_hidden(spelare, dealer, chips):
    input("Du har kommit över 21, tryck enter för att se korten.")
    show_some(spelare, dealer)
    input("Tryck enter för att fortsätta till andra handen\n")
    chips.lose_bet()

#Du ser vad denna gör :p
def player_wins(spelare, dealer, chips):
    show_all(spelare, dealer)
    print("Spelaren har vunnit!")
    chips.win_bet()

def dealer_busts(spelare, dealer, chips):
    show_all(spelare, dealer)
    print("dealern har gått över 21. Spelaren vinner.")
    chips.win_bet()

def dealer_wins(spelare, dealer, chips):
    show_all(spelare, dealer)
    print("dealern har vunnit!")
    #Om du har försäkrat dig och dealern får blackjack körs denna kod
    if dealer.hand_value == 21 and dealer.item_count == 2 and chips.bet_insurance > 0:
        print("Dealern har fått blackjack efter två kort. Men du får tillbaka ditt försäkringsbett 2/1. Du får tillbaka", chips.bet_insurance)
        chips.total += chips.bet_insurance * 2
        input("Tryck enter för att fortsätta")
    chips.lose_bet()

#Det blir lika
def push(spelare, dealer):
    show_all(spelare, dealer)
    print("dealern och spelaren har lika mycket. Det är oavgjort.")

def check_vinst(spelare, dealer, chips):
    if spelare.hand_value <= 21:
        print("\nDealerns hand:", *dealer.hand, sep='\n')
        #Det som gör att dealern drar kort tills den har 17 eller mer
        while dealer.hand_value < 17:
            input("\nTryck enter för att se nästa kort\n")
            show_dealer(dealer)
            hit(kortlek, dealer)
        input("Tryck enter för att se resultatet\n")
        
        #Vad som händer när någon har vunnit
        if dealer.hand_value > 21:
            dealer_busts(spelare, dealer, chips)
        elif dealer.hand_value > spelare.hand_value:
            dealer_wins(spelare, dealer, chips)
        elif dealer.hand_value < spelare.hand_value:
            player_wins(spelare, dealer, chips)
        else:
            push(spelare, dealer)

#Tittar varje runda om spelaren har gått över 21
def check_bust(spelare, dealer, chips):
    global playing
    if spelare.hand_value > 21:
        switch(spelare)
        player_bust(spelare, dealer, chips)
        
def check_bust_hidden(spelare, dealer, chips):
    global playing
    if spelare.hand_value > 21:
        switch(spelare)
        player_bust_hidden(spelare, dealer, chips)

#Om du har splitat ska du få vinsten/förlusten för båda händerna
def combine_total():
    spelare_chips.total += spelare_chips2.total
    spelare_chips.total -= 100

#Resetar det viktiga om du vill spela igen
def reset():
    global spelare_chips2
    global skip
    global split_check
    global playing
    global hand1
    global hand2
    global hand1_end
    global hand2_end

    spelare_chips2 = chips()
    playing = True
    skip = False
    split_check = False
    hand1 = True
    hand2 = True
    hand1_end = False
    hand2_end = False
    print()

spelare_chips2 = chips()
spelare_chips = chips()

while True:
    print("Vill du spela, titta till highscoren, titta till reglerna eller avsluta? (spela/highscore/regler/avsluta)")
    svar = input(">> ")
    if svar == "":
        print("Du måste skriva någonting.\n")
        continue
    elif svar.lower()[0] == "s":
        print()
    elif svar.lower()[0] == "h":
        highscore()
        continue
    elif svar.lower()[0] == "r":
        regler()
        continue
    elif svar.lower()[0 == "a"]:
        print("Tack för att du spelade. Hejdå!")
        break
    else:
        print("\nSvara med spela eller titta\n")
        continue

    #Gör så att man får skriva in namn och se målet med spelet
    if första_rundan == True:
        första_rundan = False
        print("Välkommen till BlackJack! Försök att komma så nära 21 som möjligt utan att gå över.\nMålet är att känna så mycket pengar så möjligt. Du har", spelare_chips.total, "att spela med.\nKungar, damer och knäckter är värd 10. Ess är värd 1 eller 11.")
        print("--------------------------------------------------")
        namn = input("Vad heter du? ")
        spelare = Spelare(namn)

    kortlek = Kortlek()
    kortlek.shuffle()
    
    take_bet(spelare_chips)

    spelare_hand = Hand()
    dealer_hand = Hand()

    spelare_hand.add_card(kortlek.deal_hidden())
    spelare_hand.add_card(kortlek.deal_hidden())
    dealer_hand.add_card(kortlek.deal_hidden())
    dealer_hand.add_card(kortlek.deal_hidden())

    #Spelet körs tills man har valt stand, give up, bustat eller fått 21.
    while playing == True:
        show_some(spelare_hand, dealer_hand)
        hit_or_stand(kortlek, spelare_hand, spelare_chips)
        if skip == False:
            check_bust(spelare_hand, dealer_hand, spelare_chips)
        charlie(spelare_hand, spelare_chips)

    #Checkar vem som vann
    if skip == False:
        if spelare_hand.hand_value <= 21:
            input("Tryck enter för att se dealerns kort.")
            check_vinst(spelare_hand, dealer_hand, spelare_chips)

    combine_total()
    print("\nDu har totalt", spelare_chips.total, "kr.")

    #Vad som händer efter rundan är slut
    if spelare_chips.total == 0:
        print("Du har slut på pengar och kan därför inte fortsätta spela. Bättre lycka nästa gång")
        nytt_spel = "no money"
        spelare.no_money()
        highscore()
        break

    else:
        nytt_spel = input("\nVill du spela igen? Skriv 'ja' eller 'nej' ")
        if nytt_spel == "":
            print("\nEftersom du inte skrev någonting tog jag beslutet för dig att du ville spela en runda till. Hoppas det går bra :p.")
            input("\nTryck Enter\n")
            reset()
            continue
        elif nytt_spel.lower()[0] == "j":
            reset()
            continue
        elif nytt_spel.lower()[0] == "n":
            spelare.vinst()
            highscore()
            break
        else:
            print("\nDetta är inte ett av valen som du var given.\nEftersom du ignorerade valmöjligheterna kastas du in i en ny runda.\nHa det så rolligt :p")
            input("\nTryck Enter\n")
            reset()
            continue