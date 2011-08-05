# coding=UTF-8
from bellum.meta import MGI, MGID
from bellum.landarmy.defcon.objects import Unit, Weapon, INFANTRY, ARMOR, SUPPORT
from bellum.landarmy.defcon.specials import IgnoresDebris, WKM, PartyArtillery, Grenades, Tarpit, DebrisMaker, WhatAMess, Markerlights, OwnPace, DefensiveDrones, SuicideExplosion

UNIT_STATS = \
(   # Party
    (                   # Offense
        (
            Unit(0.9, 0.8, 1, INFANTRY, False, (Weapon(0.65, 0, INFANTRY), Weapon(0.02, 0, ARMOR, poc=0))),          # Rekrut
            Unit(0.8, 0.75, 1, INFANTRY, False, (Weapon(0.65, 0, INFANTRY, poc=0.95), Weapon(0.02, 0, ARMOR, poc=0.05))), # Bojec
            Unit(0.7, 0.65, 2, INFANTRY, False, (
                    Weapon(0.6, 0, INFANTRY, aos=2, specialRules=(IgnoresDebris(),)),
                                                )),           # mortars
            Unit(0.8, 0.7, 3, ARMOR, False, (
                    Weapon(0.7, 0.02, INFANTRY, poc=0.95, specialRules=(WKM(), )),
                    Weapon(0.4, 0, ARMOR, poc=0.05),
                                                )),             # BTR
            Unit(1, 1, 1, INFANTRY, False, (
                    Weapon(0.6, 0, INFANTRY, poc=0.8, aos=2),
                    Weapon(0.5, 0, ARMOR, poc=0.2),
                                                )),             # Kaemowiec
            Unit(0.8, 0.6, 1, ARMOR, True, (
                    Weapon(0.6, 0, INFANTRY, aos=3),
                    Weapon(0.7, 0, ARMOR),
                                                )),             # Żbik
            Unit(1, 1, 1, SUPPORT, False, (), specialRules=(PartyArtillery(),)),      # Artillery
            Unit(1, 1, 2, SUPPORT, False, (Weapon(1, 1, INFANTRY),)),            # Sniper
            Unit(0.8, 0.7, 2, ARMOR, False, (
                    Weapon(0.7, 0.2, ARMOR, poc=0.9),
                    Weapon(0.5, 0, INFANTRY, poc=0.1),
                                                )),                 # Howitzer
            Unit(0.7, 0.6, 3, ARMOR, False, (
                    Weapon(0.2, 0, INFANTRY, specialRules=(Grenades(4),)),
                                                )),             # Hacker
        ),
        (               # Defense
            Unit(1, 1, 1, INFANTRY, False, (Weapon(0.65, 0, INFANTRY), Weapon(0.02, 0, ARMOR, poc=0))),      # Rekrut
            Unit(0.95, 0.9, 1, INFANTRY, False, (Weapon(0.65, 0, INFANTRY, poc=0.95), Weapon(0.02, 0, ARMOR, poc=0.05))), # Bojec
            Unit(0.8, 0.8, 1, INFANTRY, False, (
                    Weapon(0.55, 0, INFANTRY, specialRules=(IgnoresDebris(),)),
                                                )),           # mortars
            Unit(0.9, 0.8, 3, ARMOR, False, (
                    Weapon(0.7, 0, INFANTRY, poc=0.95, specialRules=(WKM(), )),
                    Weapon(0.3, 0, ARMOR, poc=0.05),
                                                )),             # BTR
            Unit(0.5, 0.4, 1, INFANTRY, False, (
                    Weapon(0.6, 0, INFANTRY, poc=0.8, aos=2),
                    Weapon(0.5, 0, ARMOR, poc=0.2),
                                                )),             # Kaemowiec
            Unit(0.9, 0.7, 1, ARMOR, True, (
                    Weapon(0.6, 0, INFANTRY, aos=2),
                    Weapon(0.6, 0, ARMOR),
                                                )),             # Żbik
            Unit(1, 1, 1, SUPPORT, False, (), specialRules=(PartyArtillery(),)),      # Artillery
            Unit(1, 1, 2, SUPPORT, False, (Weapon(1, 1, INFANTRY),)),            # Sniper
            Unit(0.8, 0.8, 2, ARMOR, False, (
                    Weapon(0.7, 0.2, ARMOR, poc=0.9),
                    Weapon(0.5, 0, INFANTRY, poc=0.1),
                                                )),                 # Howitzer
            Unit(0.7, 0.6, 3, ARMOR, False, (
                    Weapon(0.2, 0.05, INFANTRY, specialRules=(Grenades(4),)),
                                                )),             # Hacker
        )
    ),
        # Magnuss
    (                   # Offense
        (
            Unit(0.8, 0.7, 2, INFANTRY, False, (
                    Weapon(0.5, 0, INFANTRY),
                    Weapon(0.02, 0, ARMOR, poc=0),
                                ), specialRules=(Tarpit(),)),                         # Obrońca
            Unit(0.7, 0.65, 2, INFANTRY, False, (
                    Weapon(0.8, 0.07, INFANTRY),
                    Weapon(0.08, 0.05, ARMOR, poc=0),
                                ), specialRules=(DebrisMaker(1.5),)),                   # Captain
            Unit(0.7, 0.8, 2, INFANTRY, False, (
                    Weapon(0.8, 0.05, INFANTRY, aos=2),
                    Weapon(0.1, 0.1, INFANTRY, poc=0),
                                )),                                 # Niszczyciel
            Unit(0.6, 0.6, 1, ARMOR, True, (
                    Weapon(0.5, 0, INFANTRY, aos=2),
                    Weapon(0.7, 0.1, ARMOR),
                                )),                             # graviton
            Unit(0.65, 0.4, 1, ARMOR, False, (Weapon(0.2, 0, INFANTRY, aos=3),)),                     # transporter
            Unit(0.8, 0.7, 1, INFANTRY, False, (Weapon(0.8, 0.7, INFANTRY),)),          # leśnik
            Unit(0.7, 0.5, 1, ARMOR, False, (
                    Weapon(1, 1, INFANTRY, poc=0),
                    Weapon(1, 1, ARMOR)
                                )),                                 # laser tank
            Unit(0.75, 0.6, 3, INFANTRY, False, (
                    Weapon(0.8, 0.2, INFANTRY, poc=0.7),
                    Weapon(0.6, 0.1, ARMOR, poc=0.3),
                                ), specialRules=(DebrisMaker(2), Markerlights(1))),             # maguss
            Unit(1, 1, 1, SUPPORT, False, ()),     # sphere
            Unit(1, 1, 1, SUPPORT, False, (
                    Weapon(1, 1, INFANTRY, aos=5, poc=0.5, specialRules=(WhatAMess(2),)),
                    Weapon(1, 1, ARMOR, aos=2, poc=0.5)
                                )),                                     # nadprzestrzenna
        ),
        (               # Defense
            Unit(0.8, 0.7, 2, INFANTRY, False, (
                    Weapon(0.5, 0, INFANTRY),
                    Weapon(0.02, 0, ARMOR, poc=0),
                                ), specialRules=(Tarpit(),)),                         # Obrońca
            Unit(0.7, 0.65, 2, INFANTRY, False, (
                    Weapon(0.8, 0.07, INFANTRY),
                    Weapon(0.08, 0.05, ARMOR, poc=0),
                                ), specialRules=(DebrisMaker(1.5),)),                   # Captain
            Unit(0.7, 0.8, 2, INFANTRY, False, (
                    Weapon(0.8, 0.05, INFANTRY, aos=2),
                    Weapon(0.1, 0.1, INFANTRY, poc=0),
                                )),                                 # Niszczyciel
            Unit(0.6, 0.55, 1, ARMOR, True, (
                    Weapon(0.5, 0, INFANTRY, aos=2),
                    Weapon(0.7, 0.1, ARMOR),
                                )),                             # graviton
            Unit(0.5, 0.4, 1, ARMOR, False, (Weapon(0.2, 0, INFANTRY, aos=3),)),       # transporter
            Unit(0.5, 0.4, 1, INFANTRY, False, (Weapon(1, 1, INFANTRY),)),          # leśnik
            Unit(0.7, 0.5, 1, ARMOR, False, (
                    Weapon(1, 1, INFANTRY, poc=0),
                    Weapon(1, 1, ARMOR)
                                )),                                 # laser tank
            Unit(0.7, 0.6, 3, INFANTRY, False, (
                    Weapon(0.8, 0.2, INFANTRY, poc=0.7),
                    Weapon(0.6, 0.1, ARMOR, poc=0.3),
                                ), specialRules=(DebrisMaker(2), Markerlights(1))),             # maguss
            Unit(1, 1, 1, SUPPORT, False, ()),     # sphere
            Unit(1, 1, 1, SUPPORT, False, (
                    Weapon(1, 1, INFANTRY, aos=5, poc=0.5, specialRules=(WhatAMess(2),)),
                    Weapon(1, 1, ARMOR, aos=2, poc=0.5)
                                )),                                     # nadprzestrzenna
        )
    ),
            # Teknishon
    (                   # Offense
        (
            Unit(0.3, 0.4, 1, INFANTRY, False, ()),     # cel
            Unit(0.9, 0.85, 1, INFANTRY, False, (
                    Weapon(0.7, 0, INFANTRY),
                    Weapon(0.05, 0, ARMOR, poc=0),
                                )),                 # strzelec
            Unit(0.9, 0.8, 1, INFANTRY, False, (), specialRules=(DebrisMaker(1),)),     # forcefield
            Unit(0.7, 0.7, 2, INFANTRY, True, (
                    Weapon(0.1, 0, INFANTRY, aos=10),
                    Weapon(0.6, 0, ARMOR),
                                )),                     # P-armor
            Unit(0.6, 0.5, 2, ARMOR, True, (
                    Weapon(0.7, 0.2, ARMOR, aos=2),
                    Weapon(0.6, 0.1, INFANTRY, aos=10),
                                ), specialRules=(OwnPace(),)),      # x-mech
            Unit(0.7, 0.6, 1, ARMOR, False, (), specialRules=(DefensiveDrones(),)),     # nosiciel dronów
            Unit(0.8, 0.7, 1, ARMOR, False, ()),                # landmine. Offensive? duh.
            Unit(1, 1, 1, SUPPORT, False, (), specialRules=(Markerlights(2),)),     # łowcy
            Unit(0.7, 0.6, 1, ARMOR, True, (
                    Weapon(0.7, 0, ARMOR),
                    Weapon(0.5, 0.05, INFANTRY, aos=5),
                                )),                                 # transformator
            Unit(0.7, 0.6, 1, ARMOR, False, (
                    Weapon(0.2, 0, INFANTRY, specialRules=(Grenades(5),)),
                                )),         # strzelba
        ),
        (               # Defense
            Unit(0.3, 0.4, 1, INFANTRY, False, ()),     # cel
            Unit(0.6, 0.5, 1, INFANTRY, False, (
                    Weapon(0.9, 0, INFANTRY),
                    Weapon(0.08, 0, ARMOR, poc=0),
                                )),                 # strzelec
            Unit(0.4, 0.3, 1, INFANTRY, False, (), specialRules=(DebrisMaker(1),)),
            Unit(0.7, 0.6, 2, INFANTRY, True, (
                    Weapon(0.1, 0, INFANTRY, aos=10),
                    Weapon(0.65, 0, ARMOR),
                                )),                     # P-armor
            Unit(0.5, 0.4, 2, ARMOR, True, (
                    Weapon(1, 1, ARMOR, aos=2),
                    Weapon(0.6, 0.1, INFANTRY, aos=10),
                                ), specialRules=(OwnPace(),)),      # x-mech
            Unit(0.6, 0.5, 1, ARMOR, False, (), specialRules=(DefensiveDrones(),)),     # nosiciel dronów
            Unit(0.4, 0.3, 1, ARMOR, False, (
                    Weapon(1, 1, ARMOR, specialRules=(SuicideExplosion(),)),
                                )),                 # landmine
            Unit(1, 1, 1, SUPPORT, False, (), specialRules=(Markerlights(2),)),     # łowcy
            Unit(0.6, 0.6, 1, ARMOR, False, (
                    Weapon(1, 1, ARMOR, aos=2, poc=0.5, specialRules=(WKM(),)),
                    Weapon(1, 1, INFANTRY, aos=3, poc=0.5, specialRules=(WKM(),)),
                                )),                                 # transformator
            Unit(0.6, 0.6, 1, ARMOR, False, (
                    Weapon(0.2, 0, INFANTRY, specialRules=(Grenades(5),)),
                                )),         # strzelba
        )
    ),
)

UNIT_DESCRIPTIONS = \
( # Party
    (
        u'Żółtodziób miernie skuteczny przeciw piechocie\nZwalcza piechotę. Łatwo ginie.',
        u'Podstawowy piechur Partii\nMocniejszy od Rekruta, podobnie skuteczny',
        u'To moździerz. Czego tu się spodziewać?\nSkuteczny przeciw okopanej piechocie',
        u'Ciężki transporter opancerzony\nNiszczy zasłonę wroga strzelając do piechoty',
        u'Obronny karabin maszynowy\nJednostka obronna ogólnego przeznaczenia',
        u'Ciężki czołg szturmowy\nSkuteczny w ataku przeciw wszystkim typom jednostek',
        u'Wali we wszystko co się rusza(lub nie)\nDewastuje zasłonę wroga',
        u'Bardzo celny\nDoskonałe wsparcie przeciwpiechotne',
        u'Niszczyciel pojazdów\nBardzo dobrzy przeciwko pojazdom',
        u'Lekka artyleria przeciwpiechotna\nSkutecznie zwalcza okopaną piechotę',
    ),
    # Magnuss
    (
        u'Lekki żołnierz piechoty\nŚredni przeciw piechocie, zmniejsza skuteczność wrogiej broni maszynowej',
        u'Osłaniający dowódca przeciw piechocie\nDodaje zasłonę, dobrze zwalcza piechotę',
        u'Ciężki karabin Magnuss\nPrzygważdża piechotę, celnie miażdżąc piechotę',
        u'Lekka platforma przeciwpancerna\nSkuteczna przeciw pojazdom',
        u'Wytrzymały transporter\nSkraca czas ruchu armii. Przygważdża piechotę',
        u'Obronny snajper\nSkutecznie zwalcza piechotę gdy broni terenu',
        u'Pośredni skuteczny pojazd przeciwpancerny\nDoskonały przeciw pojazdom',
        u'Skuteczny dowódca przeciw wszystkim jednostkom\nWspomaga celność, tworzy zasłonę, dobrze walczy',
        u'Przyśpieszacz pojazdów\nSkaraca czas ruchu armii',
        u'Ciężkie działo obszarowe\nMasakruje jednostki wroga, dodając im jednak zasłony',
    ),
        # Teknishon
    (
        u'Dron obronny\nNie atakuje, wytrzymały, broni jednostki piechoty',
        u'Pośredni piechur obronny\nBardzo dobry strzelec obronny',
        u'Dron obronny\nGeneruje pole siłowe, dodając zasłonę',
        u'Ciężka piechota przygważdżająco-przeciwpancerna\nPrzygważdża wrogie jednostki i celnie zwalcza wrogi pancerz',
        u'Ciężki mech obronny\nStrzela co dwie tury, masakrując jednostki wroga',
        u'Mobilna fabryka obronnych dronów\nProdukuje drony, które pochłaniają strzały wroga',
        u'Dron ofensywny\nPodlatuje do wrogich pojazdów i wysadza je',
        u'Lekka piechota obserwacji\nPrzesyła namiary do innych jednostek, poprawiając celność wojsk',
        u'Ciężki czołg transformujący\nW ataku wielozadaniowy czołg, w obronie ciężka artyleria',
        u'Inteligetny miotacz granatów\nMiota granatami skutecznymi na okopaną piechotę'
    )
)

UNIT_BASECLASS = \
(       # Party
    (
        INFANTRY,
        INFANTRY,
        INFANTRY,
        ARMOR,
        INFANTRY,
        ARMOR,
        SUPPORT,
        SUPPORT,
        ARMOR,
        ARMOR
    ),
        # Magnuss
    (
        INFANTRY,
        INFANTRY,
        INFANTRY,
        INFANTRY,
        ARMOR,
        INFANTRY,
        ARMOR,
        INFANTRY,
        SUPPORT,
        SUPPORT,
    ),
        # Techno
    (
        INFANTRY,
        INFANTRY,
        INFANTRY,
        INFANTRY,
        ARMOR,
        ARMOR,
        ARMOR,
        SUPPORT,
        ARMOR,
        ARMOR,
    ),
)

UNIT_NAMES =  \
( # Party
    (
        u'Rekrut',
        u'Bojec',
        u'Moździerz',
        u'BTR',
        u'Kaem',
        u'Żbik',
        u'Artyleria',
        u'Snajper',
        u'Haubica',
        u'Siekacz',
    ),
    # Magnuss
    (
        u'Obrońca',
        u'Kapitan',
        u'Niszczyciel',
        u'Grawiton',
        u'Transporter',
        u'Leśnik',
        u'Czołg laserowy',
        u'Magus',
        u'Kula',
        u'N-Armatka',
    ),
        # Teknishon
    (
        u'Cel',
        u'Strzelec',
        u'Pole siłowe',
        u'Zbroja P',
        u'Mech X',
        u'Nosiciel dronów',
        u'Mina lądowa',
        u'Łowcy',
        u'Transformator',
        u'Strzelba'
    )
)

def getVerbose(garrison, race):
    vs = []
    for i in xrange(0, MGID+1):
        if garrison[i] > 0:
            vs.append(u' '+unicode(garrison[i])+u' '+UNIT_NAMES[race][i])
    return u','.join(vs)[1:]

def getStatTable(race):
    return UNIT_STATS[race]