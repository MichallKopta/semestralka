import random

class Predmet:
    #rodic pro predmety

    def __init__(self, nazev, popis):
        self.nazev = nazev
        self.popis = popis

    def pouzij(self, hrac):
        #rodic pro metodu pouzij
        print(f"Použil jsi {self.nazev}, ale nic se nestalo.")

    def __str__(self):
        return f"{self.nazev} – {self.popis}"


class Zbran(Predmet):
    #zvysuje utok

    def __init__(self, nazev, bonus_utok):
        super().__init__(nazev, f"Zvyšuje útok o {bonus_utok}")
        self.bonus_utok = bonus_utok

    def pouzij(self, hrac):
        hrac.utok += self.bonus_utok
        print(f"Vybavil jsi se zbraní {self.nazev}! Útok +{self.bonus_utok} → celkem {hrac.utok}")


class Lektvar(Predmet):
    #obnova zivotu

    def __init__(self, nazev, leceni):
        super().__init__(nazev, f"Obnoví {leceni} životů")
        self.leceni = leceni

    def pouzij(self, hrac):
        pred = hrac.zivoty
        hrac.zivoty = min(hrac.max_zivoty, hrac.zivoty + self.leceni)
        skutecne = hrac.zivoty - pred
        print(f"Vypil jsi {self.nazev}! Obnoven {skutecne} HP → {hrac.zivoty}/{hrac.max_zivoty}")


class Artefakt(Predmet):
    #zvysuje obranu

    def __init__(self, nazev, bonus_obrana):
        super().__init__(nazev, f"Zvyšuje obranu o {bonus_obrana}")
        self.bonus_obrana = bonus_obrana

    def pouzij(self, hrac):
        hrac.obrana += self.bonus_obrana
        print(f"Aktivoval jsi artefakt {self.nazev}! Obrana +{self.bonus_obrana} → celkem {hrac.obrana}")

#inventar

class Inventar:
    def __init__(self):
        self.predmety = []  #predmety v invetari

    def pridej(self, predmet):
        self.predmety.append(predmet)
        print(f"Získal jsi: {predmet.nazev}")

    def zobraz(self):
        if not self.predmety:
            print("  (prázdný inventář)")
        for i, p in enumerate(self.predmety):
            print(f"  [{i}] {p}")

    def pouzij_predmet(self, index, hrac):
        if 0 <= index < len(self.predmety):
            predmet = self.predmety.pop(index)
            predmet.pouzij(hrac)
        else:
            print("Neplatný výběr.") #spatne zadany index

    def je_prazdny(self):
        return len(self.predmety) == 0


class Postava:
    #parent pro hrace a nepritele

    def __init__(self, jmeno, zivoty, utok, obrana):
        self.jmeno = jmeno
        self.max_zivoty = zivoty
        self.zivoty = zivoty
        self.utok = utok
        self.obrana = obrana

    def utoc_na(self, cil):
        #univerzal utok
        poskozeni = max(1, self.utok - cil.obrana + random.randint(-2, 4))
        cil.zivoty -= poskozeni
        return poskozeni

    def dostan_poskozeni(self, hodnota):
        #snizuje zivoty
        self.zivoty = max(0, self.zivoty - hodnota)

    def je_nazivu(self):
        #vraci true/false
        return self.zivoty > 0

    def stav(self):
        return f"{self.jmeno}: {self.zivoty}/{self.max_zivoty} HP | {self.utok} ATK | {self.obrana} DEF"


class Hrac(Postava):
    #dite, rozsiruje o par moznosti

    def __init__(self, jmeno, zivoty, utok, obrana):
        super().__init__(jmeno, zivoty, utok, obrana)
        self.inventar = Inventar()
        self.xp = 0
        self.level = 1
        self.xp_limit = 30          # XP potřebné pro level-up
        self.pocet_nepriatel = 0    # statistika
        self.pocet_mistnosti = 0    # statistika

    def ziskej_xp(self, hodnota):
        #prida xp a dlasi level
        self.xp += hodnota
        print(f"Získal jsi {hodnota} XP! (celkem {self.xp}/{self.xp_limit})")
        if self.xp >= self.xp_limit:
            self.level_up()

    def level_up(self):
        #zvyseni levelu
        self.xp -= self.xp_limit
        self.level += 1
        self.xp_limit = int(self.xp_limit * 1.5)
        bonus_hp = 10
        bonus_utok = 2
        self.max_zivoty += bonus_hp
        self.zivoty = min(self.zivoty + bonus_hp, self.max_zivoty)
        self.utok += bonus_utok
        print(f"\nLEVEL UP! Dosáhl jsi levelu {self.level}!")
        print(f"   Max HP +{bonus_hp}, Útok +{bonus_utok}")

    def zobraz_stav(self):
        #prehled
        print(f"\n{'─'*40}")
        print(f"  {self.jmeno} (Level {self.level}) | XP {self.xp}/{self.xp_limit}")
        print(f"{self.zivoty}/{self.max_zivoty} HP  | {self.utok} ATK | {self.obrana} DEF")
        print(f"{'─'*40}")



class Valecnik(Hrac):

    def __init__(self, jmeno):
        super().__init__(jmeno, zivoty=80, utok=14, obrana=5)
        self.typ = "Válečník"

    def specialni_schopnost(self, cil):
        #specialniutok
        poskozeni = (self.utok * 2) - cil.obrana
        poskozeni = max(1, poskozeni)
        cil.zivoty -= poskozeni
        print(f"{self.jmeno} použil DRTIVÝ ÚDER na {cil.jmeno} za {poskozeni} poškození!")
        return poskozeni


class Mag(Hrac):


    def __init__(self, jmeno):
        super().__init__(jmeno, zivoty=55, utok=18, obrana=2)
        self.typ = "Mág"
        self.many = 3  #pocet specialnich utoku

    def specialni_schopnost(self, cil):
        if self.many <= 0:
            print("Nemáš dostatek many! Útočíš normálně.")
            return self.utoc_na(cil)
        poskozeni = self.utok + random.randint(5, 10) #ignor obrany
        cil.zivoty -= poskozeni
        self.many -= 1
        print(f"{self.jmeno} seslal OHNIVOU KOULI na {cil.jmeno} za {poskozeni} poškození! (many: {self.many})")
        return poskozeni


class Lovec(Hrac):

    def __init__(self, jmeno):
        super().__init__(jmeno, zivoty=65, utok=12, obrana=4)
        self.typ = "Lovec"
        self.sance_uhyb = 0.25  #25%

    def specialni_schopnost(self, cil):
        poskozeni = self.utok + random.randint(3, 8)
        cil.zivoty -= poskozeni
        print(f"{self.jmeno} vystřelil PŘESNÝ VÝSTŘEL na {cil.jmeno} za {poskozeni} poškození!")
        return poskozeni

    def zkus_uhnout(self):
        #vraci true/false
        return random.random() < self.sance_uhyb


class Nepritel(Postava):

    def __init__(self, jmeno, zivoty, utok, obrana, xp_odmena):
        super().__init__(jmeno, zivoty, utok, obrana)
        self.xp_odmena = xp_odmena  #xp za porazeni


class Goblin(Nepritel):
    def __init__(self):
        super().__init__("Goblin", zivoty=25, utok=7, obrana=1, xp_odmena=10)
        self.emoji = "👺"


class Kostlivec(Nepritel):
    def __init__(self):
        super().__init__("Kostlivec", zivoty=35, utok=10, obrana=3, xp_odmena=15)
        self.emoji = "💀"


class Troll(Nepritel):
    def __init__(self):
        super().__init__("Troll", zivoty=55, utok=13, obrana=5, xp_odmena=25)
        self.emoji = "👹"


class Boss(Nepritel):

    def __init__(self):
        super().__init__("Temný pán", zivoty=100, utok=18, obrana=8, xp_odmena=50)
        self.emoji = "👑"

    def dvojity_utok(self, hrac):
        #utoci 2x
        p1 = max(1, self.utok - hrac.obrana + random.randint(-2, 3))
        p2 = max(1, self.utok - hrac.obrana + random.randint(-2, 3))
        hrac.zivoty -= (p1 + p2)
        print(f"{self.jmeno} zaútočil DVAKRÁT: {p1} + {p2} = {p1+p2} poškození!")
        return p1 + p2


class Souboj:
    #logika souboje

    def __init__(self, hrac, nepritel):
        self.hrac = hrac
        self.nepritel = nepritel

    def proved(self):
        #spousti souboj, vraci true/flase
        h = self.hrac
        n = self.nepritel
        emoji = getattr(n, 'emoji', '👾')

        print(f"\nSouboj: {h.jmeno} vs {emoji} {n.jmeno}!")
        print(f"  {n.stav()}")

        while h.je_nazivu() and n.je_nazivu():
            print(f"\nTy: {h.zivoty}/{h.max_zivoty} HP  |  {emoji} {n.jmeno}: {n.zivoty}/{n.max_zivoty} HP")
            print("  Akce: [1] Útok  [2] Speciální  [3] Předmět  [4] Útěk")
            volba = input("  > ").strip()

            if volba == "1":
                #normalní utok
                pos = h.utoc_na(n)
                print(f"Zasáhl jsi za {pos} poškození!")

            elif volba == "2":
                #speciálni schopnost
                h.specialni_schopnost(n)

            elif volba == "3":
                #pouziti predmetu z inventare
                if h.inventar.je_prazdny():
                    print("  Inventář je prázdný!")
                    continue
                print("  Inventář:")
                h.inventar.zobraz()
                try:
                    idx = int(input("  Vyber číslo předmětu: "))
                    h.inventar.pouzij_predmet(idx, h)
                except ValueError:
                    print("  Neplatný vstup.")
                    continue

            elif volba == "4":
                #utek (50%)
                if random.random() < 0.5:
                    print("Podařilo se ti utéct!")
                    return False
                else:
                    print("Útěk se nezdařil!")

            else:
                print("  Neznámá akce, zkus znovu.")
                continue

            #utok nepritele
            if n.je_nazivu():
                #dodge
                if isinstance(h, Lovec) and h.zkus_uhnout():
                    print(f"Uhnul jsi útoku {n.jmeno}!")
                elif isinstance(n, Boss):
                    n.dvojity_utok(h)
                else:
                    pos_n = n.utoc_na(h)
                    print(f"{n.jmeno} tě zasáhl za {pos_n} poškození!")

        #po soubaji
        if h.je_nazivu():
            print(f"\nPorazil jsi {n.jmeno}!")
            h.ziskej_xp(n.xp_odmena)
            h.pocet_nepriatel += 1
            return True
        else:
            print(f"\n{n.jmeno} tě porazil...")
            return False


class Hra:
    #data pro hru a rizeni


    MOZNE_PREDMETY = [
        Zbran("Rezavý meč", bonus_utok=3),
        Zbran("Elfský luk", bonus_utok=5),
        Lektvar("Malý lektvar", leceni=15),
        Lektvar("Velký lektvar", leceni=30),
        Artefakt("Amulet síly", bonus_obrana=3),
        Artefakt("Dračí štít", bonus_obrana=5),
    ]

    def __init__(self):
        self.hrac = None
        self.bezi = True





    def vytvor_postavu(self):
        #tvorba postavy
        print("\n" + "="*45)
        print("DOBRODRUŽSTVÍ V KOBCE")
        print("="*45)
        jmeno = input("\nZadej jméno svého dobrodruha: ").strip() or "Hrdina" #pokud nic nenapise da Hrdina

        print("\nVyber typ postavy:")
        print("  [1] Válečník  – silný útočník s hodně HP")
        print("  [2] Mág       – mocná magie, ale slabý")
        print("  [3] Lovec     – rychlý, šance na úhyb")
        volba = input("> ").strip()

        if volba == "1":
            self.hrac = Valecnik(jmeno)
        elif volba == "2":
            self.hrac = Mag(jmeno)
        elif volba == "3":
            self.hrac = Lovec(jmeno)
        else:
            print("Neplatná volba, vytvářím Válečníka.")
            self.hrac = Valecnik(jmeno)

        print(f"\nVítej, {self.hrac.jmeno} – {self.hrac.typ}!")
        print(f"   {self.hrac.stav()}")


    def vygeneruj_udalost(self):
        #random vybere jaka mistnost bude dalsi
        if self.hrac.pocet_mistnosti >= 23 and random.random() < 0.2:
            return "boss"
        nahodne = random.random()
        if nahodne < 0.45:
            return "souboj"
        elif nahodne < 0.65:
            return "predmet"
        elif nahodne < 0.80:
            return "past"
        elif nahodne < 0.90:
            return "odpocinek"
        else:
            return "bonus_xp"

    def vygeneruj_nepritele(self):
        #random nepritel
        level = self.hrac.level
        if level <= 1:
            return Goblin()
        elif level <= 2:
            return random.choice([Goblin(), Kostlivec()])
        else:
            return random.choice([Kostlivec(), Troll()])

    def vygeneruj_predmet(self):
        #random predmet
        return random.choice(self.MOZNE_PREDMETY)

    def udalost_souboj(self):
        nepritel = self.vygeneruj_nepritele()
        souboj = Souboj(self.hrac, nepritel)
        vysledek = souboj.proved()
        if not self.hrac.je_nazivu():
            self.bezi = False

    def udalost_boss(self):
        print("\nPřed tebou se zjevuje TEMNÝ PÁN!")
        boss = Boss()
        souboj = Souboj(self.hrac, boss)
        vysledek = souboj.proved()
        if vysledek:
            print("\nPorazil jsi Temného pána! VYHRÁVÁŠ!")
            self.bezi = False
            self.konec(vyhral=True)
        else:
            self.bezi = False

    def udalost_predmet(self):
        predmet = self.vygeneruj_predmet()
        print(f"\nNalezl jsi předmět: {predmet}")
        print("  [1] Vzít si ho  [2] Nechat ležet")
        volba = input("  > ").strip()
        if volba == "1":
            self.hrac.inventar.pridej(predmet)

    def udalost_past(self):
        poskozeni = random.randint(5, 15)
        print(f"\nŠlápl jsi do pasti! Ztratil jsi {poskozeni} HP.")
        self.hrac.dostan_poskozeni(poskozeni)
        if not self.hrac.je_nazivu():
            self.bezi = False

    def udalost_odpocinek(self):
        leceni = random.randint(10, 25)
        self.hrac.zivoty = min(self.hrac.max_zivoty, self.hrac.zivoty + leceni)
        print(f"\nNašel jsi bezpečné místo k odpočinku. Obnovil jsi {leceni} HP → {self.hrac.zivoty}/{self.hrac.max_zivoty}")

    def udalost_bonus_xp(self):
        bonus = random.randint(8, 20)
        print(f"\nNalezl jsi starý svitek. Získáváš {bonus} XP!")
        self.hrac.ziskej_xp(bonus)



    def herni_smycka(self):
        #loop kterej ridi hru
        input("\nStiskni ENTER a vydej se do kobky...")

        while self.bezi and self.hrac.je_nazivu():
            self.hrac.pocet_mistnosti += 1
            cislo = self.hrac.pocet_mistnosti
            print(f"\n\n{'='*45}")
            print(f"Místnost č. {cislo}")
            print(f"{'='*45}")
            self.hrac.zobraz_stav()

            udalost = self.vygeneruj_udalost()

            if udalost == "souboj":
                self.udalost_souboj()
            elif udalost == "boss":
                self.udalost_boss()
                break
            elif udalost == "predmet":
                self.udalost_predmet()
            elif udalost == "past":
                self.udalost_past()
            elif udalost == "odpocinek":
                self.udalost_odpocinek()
            elif udalost == "bonus_xp":
                self.udalost_bonus_xp()

            if not self.hrac.je_nazivu():
                self.konec(vyhral=False)
                break

            if self.bezi:
                input("\n[ENTER] – pokračuj do další místnosti...")


    def konec(self, vyhral):
        
        h = self.hrac
        print(f"\n\n{'='*45}")
        if vyhral:
            print("VÍTĚZSTVÍ!")
        else:
            print("GAME OVER")
        print(f"{'='*45}")
        print(f"  Postava:           {h.jmeno} – {h.typ}")
        print(f"  Dosažený level:    {h.level}")
        print(f"  Poražení nepřátelé:{h.pocet_nepriatel}")
        print(f"  Prošlé místnosti:  {h.pocet_mistnosti}")
        print(f"{'='*45}\n")

    def spust(self):
        #nejdrive vytvori postavu a nasledne hru
        self.vytvor_postavu()
        self.herni_smycka()

#spusteni programu

if __name__ == "__main__":
    hra = Hra()   # instance hry
    hra.spust()







