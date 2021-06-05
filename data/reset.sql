-- SQLite

DROP TABLE IF EXISTS Film;
DROP TABLE IF EXISTS Zalen;
DROP TABLE IF EXISTS Verkoop;
DROP TABLE IF EXISTS Vertoning;

CREATE TABLE IF NOT EXISTS Film (
	ID_Film INTEGER PRIMARY KEY AUTOINCREMENT,
	Titel TEXT,
	Duur INT,
	'3Dbeschikbaar' BOOLEAN,
	KNT BOOLEAN,
	IMDB_ID TEXT,
	Poster_link TEXT,
	Beschrijving TEXT
);

CREATE TABLE IF NOT EXISTS Zalen (
	ID_Zalen INTEGER PRIMARY KEY AUTOINCREMENT,
	'3Dmogelijk' BOOLEAN,
	Plaatsen INTEGER
);

CREATE TABLE IF NOT EXISTS Verkoop (
	Verkoop_ID INTEGER PRIMARY KEY AUTOINCREMENT,
	ID_Vertoning INTEGER,
	Tickets_kids INTEGER,
	Tickets_standaard INTEGER,
	Prijs REAL,

	FOREIGN KEY (ID_Vertoning) REFERENCES Vertoning (ID_Vertoning)
);

CREATE TABLE IF NOT EXISTS Vertoning (
	ID_Vertoning INTEGER PRIMARY KEY AUTOINCREMENT,
	ID_Film INTEGER,
	Datum TEXT,
	Moment TEXT,
	'3D' BOOLEAN,
	ID_Zaal INTEGER,

	FOREIGN KEY (ID_Film) REFERENCES Film (ID_Film),
	FOREIGN KEY (ID_Zaal) REFERENCES Zalen (ID_Zaal)
);

-- SQLite

INSERT INTO Zalen ("3Dmogelijk", Plaatsen)
VALUES 

(
TRUE, 20
),
(
TRUE, 20
),
(
TRUE, 20
),
(
TRUE, 25
),
(
TRUE, 18
),
(
FALSE, 15
),
(
FALSE, 15
)

;

-- SQLite

INSERT INTO Vertoning (ID_Film, Datum, Moment, '3D', ID_Zaal)
VALUES 
(
4,"05/06/2021", "23:59",0,1
),

(
9,"05/06/2021", "23:59",0,2
),

(
14,"05/06/2021", "23:59",0,3
),

(
17,"05/06/2021", "23:59",1,4
),

(
20,"05/06/2021", "23:59",0,5
),

(
29,"05/06/2021", "23:59",0,6
),

(
1,"05/06/2021", "10:00",0,7
),

(
2,"05/06/2021", "14:00",0,7
),


(
3,"05/06/2021", "17:00",0,7
),

(
4,"05/06/2021", "20:00",0,7
)



;

-- SQLite

INSERT INTO Verkoop (ID_Vertoning, Tickets_kids, Tickets_standaard, Prijs)
VALUES 

(
"1", "2", "2", "32"
),

(
"1", "0", "4", "36"
),

(
"1", "0", "4", "36"
),

(
"1", "0", "4", "36"
),

(
"1", "0", "6", "54"
),

(
"2", "0", "1", "9"
),

(
"2", "0", "2", "18"
),

(
"2", "0", "3", "27"
),

(
"2", "0", "1", "9"
),

(
"2", "0", "3", "27"
),

(
"2", "0", "2", "18"
),

(
"2", "0", "4", "36"
),

(
"2", "0", "2", "18"
),

(
"2", "0", "2", "18"
),

(
"3", "4", "2", "46"
),

(
"3", "4", "2", "46"
),

(
"3", "4", "3", "55"
),

(
"3", "4", "2", "46"
),

(
"4", "0", "5", "45"
),

(
"4", "0", "4", "36"
),

(
"4", "0", "4", "36"
),

(
"4", "0", "2", "18"
),

(
"4", "0", "2", "18"
),

(
"4", "0", "2", "18"
),

(
"4", "0", "2", "18"
),

(
"4", "0", "2", "18"
),

(
"4", "0", "2", "18"
),

(
"5", "0", "2", "18"
),

(
"5", "0", "2", "18"
),

(
"5", "0", "3", "27"
),

(
"5", "0", "1", "9"
),

(
"5", "0", "1", "9"
),

(
"5", "0", "2", "18"
),

(
"5", "0", "1", "9"
),

(
"5", "0", "2", "18"
),

(
"5", "0", "1", "9"
),

(
"5", "0", "1", "9"
),

(
"5", "0", "2", "18"
),

(
"6", "2", "2", "32"
),

(
"6", "2", "0", "14"
),

(
"6", "3", "2", "39"
),

(
"6", "2", "2", "32"
),

(
"7", "2", "1", "23"
),

(
"7", "2", "1", "23"
),


(
"7", "2", "1", "23"
),


(
"7", "2", "1", "23"
)
;

-- SQLite

INSERT INTO Film (Titel, Duur, "3Dbeschikbaar", KNT, IMDB_ID, Poster_link, Beschrijving)
VALUES (
"Forrest Gump", "142", FALSE, FALSE, "tt0109830", "https://image.tmdb.org/t/p/original/h5J4W4veyxMXDMjeNxZI46TsHOb.jpg", "De film vertelt het verhaal van de simpele Forrest Gump. Zijn lage IQ weerhoudt hem er niet van om een grote rol te spelen bij diverse belangrijke gebeurtenissen in de Amerikaanse geschiedenis. Zo zien we hem in Vietnam vechten, Elvis en JFK ontmoeten, enzovoorts."
),
(
"Saving Private Ryan", "169", FALSE, TRUE, "tt0120815", "https://image.tmdb.org/t/p/original/1wY4psJ5NVEhCuOYROwLH2XExM2.jpg", "Tijdens de invasie van de Geallieerden in Normandië sterven twee broers. Een derde broer sterft gelijktijdig in Nieuw Guinea, bij het vechten tegen de Japanners. Als bekend wordt dat een vierde broer vermist is geraakt op het Franse platteland, wordt een missie gestart om hem veilig thuis te krijgen."
),

(
"The Shawshank Redemption", "142", FALSE, TRUE, 'tt0111161', "https://image.tmdb.org/t/p/original/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg", "Andy Dufresne betrapt zijn vrouw met een ander en wordt vervolgens beschuldigd van de moord op zijn vrouw en haar minnaar. Hij houdt vol dat hij onschuldig is, maar krijgt toch tweemaal levenslang in de strenge gevangenis Shawshank."
),

(
"Toy Story", "81", FALSE, FALSE, "tt0114709", "https://image.tmdb.org/t/p/original/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg", "Cowboy Woody is al jaren het favoriete speelgoed van Andy. Wanneer de jongen voor zijn verjaardag de blitse astronautenpop Buzz Lightyear krijgt, wordt Woody naar de achtergrond verdrongen. De twee stukken speelgoed wedijveren om de gunst van de jongen en zetten door hun geruzie de hele kinderkamer in rep en roer. Als Buzz door toedoen van Woody uit het raam valt, krijgt Woody hiervan de schuld van de rest van het speelgoed. Hij gaat naar buiten om Buzz proberen te redden."
),

(
"Catch Me If You Can", "141", FALSE, FALSE, "tt0264464", "https://image.tmdb.org/t/p/original/ctjEj2xM32OvBXCq8zAdK3ZrsAj.jpg", "Hij doet zich voor als arts, hoogleraar, advocaat en piloot, en niemand twijfelt ooit aan zijn kunnen. Maar intussen licht Frank, amper twintig jaar oud, iedereen op en verdwijnt hij keer op keer zonder een spoor achter te laten. Tot de politie een internationale klopjacht opent."
),

(
"The Green Mile", "189", FALSE, TRUE, "tt0120689", "https://image.tmdb.org/t/p/original/sOHqdY1RnSn6kcfAHKu28jvTebE.jpg", "Nu Paul Edgecomb zijn dagen slijt in een bejaardentehuis, kijkt hij terug op zijn leven als gevangenisbewaker. Jarenlang heeft hij dienst gedaan in de 'Dodengang' van de Cold Mountain gevangenis. Paul denkt vooral terug aan 1935."
),

(
"The Dark Knight", "152", FALSE, TRUE, "tt0468569", "https://image.tmdb.org/t/p/original/qJ2tW6WMUDux911r6m7haRef0WH.jpg", "Bruce Wayne, alias Batman, en Lt. James Gordon bundelen hun krachten met de nieuw aangewezen Officier van Justitie Harvey Dent. Samen proberen zij de chaos tegen te gaan die Gotham momenteel teistert, veroorzaakt door niemand minder dan Batmans ergste vijand, The Joker."
),

(
"Cast Away", "144", FALSE, FALSE, "tt0162222", "https://image.tmdb.org/t/p/original/6Zp6oj4QxpYFFvrVtb4kGc7r0jK.jpg", "Chuck Noland is een hooggeplaatste functionaris bij FedEx die zijn werk boven zijn privéleven stelt. Terwijl hij met een vrachtvliegtuig meevliegt komt het vliegtuig in een storm terecht. Als dan een deel van de lading ontploft, stort het vliegtuig in de Stille Oceaan neer."
),

(
"The Silence of the Lambs", "118", FALSE, TRUE, "tt0102926", "https://image.tmdb.org/t/p/original/rplLJ2hPcOQmkFhTqUte0MkEaO2.jpg", "Clarice Starling, een jonge FBI-agente, wordt op een zaak van een psychopatische seriemoordenaar gezet. Om een beter inzicht te krijgen in de zieke geest van de moordenaar besluit ze met een andere psychopaat, Dr. Hannibal 'The Cannibal' Lecter, te gaan praten."
),

(
"Braveheart", "178", FALSE, TRUE, "tt0112573", "https://image.tmdb.org/t/p/original/or1gBugydmjToAEq7OZY0owwFk.jpg", "Het einde van de 13e eeuw: William Wallace is een Schotse rebel die een verzet leidt tegen de wrede Engelse heerser Edward the Longshanks. Als klein jongetje zag William zijn vader en broer vermoord worden in een poging om Schotland te bevrijden.  "
),

(
"The Lord of the Rings - The Return of the King", "201", FALSE, FALSE, "tt0167260", "https://image.tmdb.org/t/p/original/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg", "De hobbits Sam en Frodo beginnen samen met Gollum aan het laatste deel van hun reis richting Mordor, om daar te proberen in het hol van de leeuw de machtige Ene Ring te vernietigen. De legers van Gondor proberen ondertussen de stad Minas Tirith te 
beschermen tegen Sauron's legers."
),

(
"The Lord of the Rings - The Fellowship of the Ring", "178", FALSE, FALSE, "tt0120737", "https://image.tmdb.org/t/p/original/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg", "Een eeuwenoude ring, die jaren zoek is geweest, wordt gevonden en komt bij toeval terecht bij de kleine Hobbit Frodo. Als de tovenaar Gandalf erachter komt dat deze ring eigenlijk de Ene Ring is waar de slechte Sauron naar op zoek is, gaat Frodo samen met Gandalf, een Dwerg, een Elf, twee Mensen en drie andere Hobbits op een groots avontuur om deze te vernietigen.      "
),

(
"The Lord of the Rings - The Two Towers", "179", FALSE, FALSE, "tt0167261", "https://image.tmdb.org/t/p/original/rrGlNlzFTrXFNGXsD7NNlxq4BPb.jpg", "De hobbits Frodo en Sam trekken verder richting Mordor om hun taak, het vernietigen van de machtige Ene Ring waar de slechte Sauron naar op zoek is, te volbrengen. Hierbij krijgen ze hulp uit onverwachte hoek."
),

(
"Back to the Future", "116", FALSE, FALSE, "tt0088763", "https://image.tmdb.org/t/p/original/7lyBcpYB0Qt8gYhXYaEZUNlNQAv.jpg", "Marty McFly  reist terug naar 1955 met een tot tijdmachine omgebouwde DeLorean van Doc Emmett Brown. Hij zorgt er per ongeluk voor dat zijn moeder verliefd op hem wordt in plaats van op zijn vader."
),

(
"Die Hard", "131", FALSE, TRUE, "tt0095016", "https://image.tmdb.org/t/p/original/yFihWxQcmqcaBR31QM6Y8gT6aYV.jpg", "De enige reden waarom de New Yorkse agent in Los Angeles zit, is dat hij de kerst bij zijn kinderen wil zijn. Hij bevindt zich op een feestje van het werk van zijn ex-vrouw als een stel Duitse terroristen controle over de wolkenkrabber neemt om een kluis met zeven sloten te openen."
),

(
"Scarface", "170", FALSE, TRUE, "tt0086250", "https://image.tmdb.org/t/p/original/xFocqbDze8zWuf7GolkpS2M17V8.jpg", "Scarface vertelt het verhaal van Tony Montana, een Cubaanse bootvluchteling die zich langzaam op weet te werken in het cocaïne-circuit van Florida. Na een tijdje de klusjes van anderen opgelost te hebben, begint hij zijn eigen imperium op te bouwen."
),

(
"The Shining", "115", TRUE, TRUE, "tt0081505", "https://image.tmdb.org/t/p/original/b6ko0IKC8MdYBBPkkA1aBPLe2yz.jpg", "Jack Torrance is een schrijver met een writer's block. Wanneer hij wordt aangenomen voor een baan als huismeester van het prestigieuze Overlook Hotel, dat zich op een afgelegen plek in de bergen van Colorado bevindt, ziet hij dit als de ideale kans om inspiratie op te doen en zijn boek af te maken."
),

(
"Alien", "122", FALSE, TRUE, "tt2316204", "https://image.tmdb.org/t/p/original/sRITPlHYjHiOLQXr0sFxVz5TPmj.jpg", "De bemanning van het kolonieschip Covenant is op weg naar een verre planeet aan de andere kant van de Melkweg. Ze ontdekken daar, wat zij denken, een onbekend paradijs, maar wat eigenlijk een duistere gevaarlijke wereld is. De enige bewoner blijkt de 'synthetische' David (Michael Fassbender) te zijn, een overlevende van de gedoemde Prometheus expeditie."
),

(
"Terminator 2: Judgment Day", "137", FALSE, TRUE, "tt0103064", "https://image.tmdb.org/t/p/original/wy0XcYDGngA4ppIrKDZrqC7z0jm.jpg", "Het is tien jaar geleden dat Sarah Connor het doelwit was van een moordlustige Terminator-robot uit de toekomst. Haar zoon John zal ooit de verzetsleider worden die het opneemt tegen supercomputer Skynet."
),

(
"The Sixth Sense", "107", FALSE, TRUE, "tt0167404", "https://image.tmdb.org/t/p/original/fIssD3w3SvIhPPmVo4WMgZDVLID.jpg", "Dr. Malcolm Crowe is een vooraanstaand kinderpsycholoog, die wordt gekweld door de pijnlijke herinnering aan een geestesziek patiëntje, dat hij in het verleden niet heeft kunnen helpen."
),

(
"Inception", "148", FALSE, FALSE, "tt1375666", "https://image.tmdb.org/t/p/original/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg", "Dom Cobb is een meesterdief, gespecialiseerd in het “stelen” van waardevolle geheimen in de droomstaat van een mens, wanneer de geest het kwetsbaarst is."
),

(
"Full Metal Jacket", "116", FALSE, TRUE, "tt0093058", "https://image.tmdb.org/t/p/original/kMKyx1k8hWWscYFnPbnxxN4Eqo4.jpg", "Het eerste deel van de film volgt een groep militairen die door Sgt. Hartman op onmenselijke wijze klaargestoomd worden voor de Vietnam oorlog. Het tweede deel van de film laat zien hoe één van deze militairen, Joker, de oorlog verslaat als reporter, tijdens het Tet-offensief."
),

(
"GoodFellas", "145", FALSE, TRUE, "tt0099685", "https://image.tmdb.org/t/p/original/6QMSLvU5ziIL2T6VrkaKzN2YkxK.jpg", "Henry Hill wil al van jongs af aan bij de maffia. Gangster Jimmy 'The Gent' Conway staat in hoog aanzien bij zijn misdaadcollega's. Hij neemt de jonge Henry onder zijn hoede en leert hem alle fijne kneepjes van het gangstervak."
),

(
"Jurassic Park", "127", FALSE, FALSE, "tt0107290", "https://image.tmdb.org/t/p/original/9i3plLl89DHMz7mahksDaAo7HIS.jpg", "Wetenschappers slagen er in om dinosauriërs te klonen uit een druppel dino-bloed afkomstig uit een mug. De ondernemende miljonair John Hammond wil de gekloonde dino's aan het publiek laten zien en bouwt daarvoor een gigantisch thema-park."
),

(
"Good Will Hunting", "126", FALSE, FALSE, "tt0119217", "https://image.tmdb.org/t/p/original/bABCBKYBK7A5G1x0FzoeoNfuj2.jpg", "Als docenten ontdekken dat een doelloze conciërge ook een wiskundig genie blijkt te zijn, helpt een therapeut de jongeman zijn belemmerende problemen te overwinnen."
),

(
"Star Wars: Episode VI - Return of the Jedi", "134", FALSE, FALSE, "tt0086190", "https://image.tmdb.org/t/p/original/mDCBQNhR6R0PVFucJl0O4Hp5klZ.jpg", "Na Han Solo uit de handen van Jabba the Hutt gered te hebben, voltooit Luke z'n Jedi-training bij Yoda. De Keizer bouwt een nieuwe Death Star, en dit keer overziet hij zelf de bouw hiervan. Luke gaat de confrontatie met Darth Vader en de Keizer aan, terwijl z'n vrienden op de maan van Endor met hulp van de Ewoks de keizerlijke troepen te lijf gaan."
),

(
"The Terminator", "107", FALSE, TRUE, "tt0088247", "https://image.tmdb.org/t/p/original/qvktm0BHcnmDpul4Hz01GIazWPr.jpg", "n de toekomst vindt er een wereldoorlog plaats tussen de mensen en de machines. De machines sturen een Terminator terug in de tijd. Deze cyborg heeft maar één missie: het doden van Sarah Connor, omdat haar ongeboren zoon zal uitgroeien tot de leider van het menselijk verzet."
),

(
"Indiana Jones and the Last Crusade", "127", FALSE, FALSE, "tt0097576", "https://image.tmdb.org/t/p/original/acgJPtbeXdBaKYAUVdfYLVwKzAC.jpg", "Al sedert 1912 zit Indiana Jones een bende achterna die een kostbaar kruis hebben gestolen. Nu het hem uiteindelijk gelukt is het juweel te bemachtigen en aan historicus Brody te overhandigen, kan hij opnieuw zijn baan als leraar oppikken."
),

(
"The Princess Bride", "98", FALSE, FALSE, "tt0093779", "https://image.tmdb.org/t/p/original/whF3YddFYSwJNuHEvi5lpsnty2l.jpg", "Het verhaal speelt zich af in het fictieve land Florin. Prinses Buttercup wordt verliefd op de stalknecht Wesley. Het jonge stel zweert elkaar eeuwige trouw. Maar dan wordt Wesley tijdens een zeereis vermoord door een bende piraten. Buttercup gelooft stellig dat zij nooit meer van iemand anders zal houden."
),

(
"Groundhog Day", "101", FALSE, FALSE, "tt0107048", "https://image.tmdb.org/t/p/original/gCgt1WARPZaXnq523ySQEUKinCs.jpg", "Phil Connors is een chagrijnige weerman die naar Punxsutawney wordt gestuurd om daar het jaarlijkse 'Groundhog Day' te verslaan. Hij wordt daar ingesneeuwd en tot zijn grote verrassing wordt hij de volgende dag wakker en is het weer dezelfde dag."
),

(
"Home Alone", "84", FALSE, FALSE, "tt13677540", "https://image.tmdb.org/t/p/original/lL2Ri3PHs9V1ot3V8ZUvrtFgj9h.jpg", "Met Kerst vertrekt de familie McCallister samen met een oom en tante en hun kinderen voor een paar dagen naar Parijs. Oom en tante overnachten met hun kinderen bij de McCallisters en het hele huis is vol, terwijl iedereen koortsachtig aan het inpakken is. In de drukte is iedereen kortaangebonden en Kevins oudere broer Buzz plaagt hem. Als Kevin boos wordt en zijn zelfbeheersing verliest, wordt hij voor straf naar boven gestuurd. De volgende ochtend vertrekt de familie laat, ze hebben zich verslapen en ze hebben dan haast en vergeten in alle drukte Kevin."
),

(
"The Departed", "151", FALSE, TRUE, "tt0407887", "https://image.tmdb.org/t/p/original/kWWAt2FMRbqLFFy8o5R4Zr8cMAb.jpg", "Colin Sullivan werkt voor de grote en beruchte gangster Frank Costello en krijgt de taak te infiltreren in het politiekorps van Boston. Tegelijkertijd werkt undercover-agent Billy Costigan zich op in de wereld van Costello en probeert diens vertrouwen te winnen."
),

(
"The Lion King", "89", FALSE, FALSE, "tt0110357", "https://image.tmdb.org/t/p/original/jq3z51D9uXmc5tsFOwpbFwz4F2y.jpg", "In Afrika wordt de jonge leeuw Simba geboren als zoon van de leeuwenkoning Mufasa. Dat zint Mufasa's jaloerse broer Scar absoluut niet, die nu niet langer de eerste troonopvolger is. Terwijl Simba een onbezorgde jeugd geniet in zijn vaders koninkrijk, smeedt Scar samen met een groep hyena's een plan om zowel Mufasa als Simba uit de weg te ruimen, en zo zelf de macht te kunnen grijpen."
),

(
"Finding Nemo", "100", FALSE, FALSE, "tt0266543", "https://image.tmdb.org/t/p/original/eHuGQ10FUzK1mdOY69wF5pGgEf5.jpg", "De clownvis Marlin leidt samen met zijn enige zoon Nemo een veilig leventje in het Great Barrier Reef bij Australië. Wanneer Nemo onverwachts weggehaald wordt van zijn thuis, en in het aquarium van een tandarts belandt, is het aan Marlin om hem te redden."
),

(
"Rocky", "119", FALSE, TRUE, "tt0075148", "https://image.tmdb.org/t/p/original/i5xiwdSsrecBvO7mIfAJixeEDSg.jpg", "Rocky Balboa is een tweederangs bokser uit Philadelphia. Hij is een mislukking: hij woont in een afgedankt appartement en als bijbaantje is hij een inner van schulden. Ook probeert hij indruk te maken op de ietwat verlegen Adrian, zijn grote liefde."
),

(
"The Exorcist", "122", FALSE, TRUE, "tt0070047", "https://image.tmdb.org/t/p/original/4ucLGcXVVSVnsfkGtbLY4XAius8.jpg", "Bij opgravingen in Noord-Irak vindt priester-archeoloog Merrin een duivelsbeeldje. Net op hetzelfde moment wordt in Georgetown actrice Chris McNeil opgeschrikt door vreemde geluiden in de kamer van haar twaalfjarig dochtertje Regan."
),

(
"Ghostbusters", "108", FALSE, FALSE, "tt1289401", "https://image.tmdb.org/t/p/original/wJmWliwXIgZOCCVOcGRBhce7xPS.jpg", "Erin Gilbert, een wetenschapper aan de universiteit van Columbia, heeft samen met Abby Yates een boek geschreven genaamd 'Ghosts from our Past: Both Literally and Figuratively – The Study of Paranormal Knowing'. De twee hebben elkaar jaren niet gesproken maar worden bij elkaar gebracht door een man die hulp zoekt bij de bestrijding van spoken. Samen met Jillian, een collega van Abby, besluiten ze een bedrijf op te richten dat gespecialiseerd is in het vernietigen van paranormale verschijningen."
),

(
"The Breakfast Club", "97", FALSE, FALSE, "tt0088847", "https://image.tmdb.org/t/p/original/c0bdxKVRevkw50LOnk6B8d3e4s.jpg", "Een club studenten moet 's ochtends nablijven. Niemand heeft een vriend aan een ander, en ieder zit er om verschillende redenen. De opdracht die ze krijgen is het schrijven van een opstel, onder doodse stilte en zonder van plaats te veranderen."
),

(
"The Incredibles", "115", FALSE, FALSE, "tt0317705", "https://image.tmdb.org/t/p/original/2LqaLgk4Z226KkgPJuiOQ58wvrm.jpg", "Bob Parr en zijn vrouw Helen behoorden vroeger tot de groep van 's werelds grootste misdaadbestrijders. Levens redden en het kwaad bestrijden was hun dagelijks werk. Maar vijftien jaar later zijn ze gedwongen om als gewone burgers te leven en zich terug te trekken in een buitenwijk. Ze wonen daar als ""normaal"" gezin met hun drie kinderen, Violet, Dash en Jack Jack."
),

(
"Indiana Jones Raiders of the Lost Ark", "115", FALSE, FALSE, "tt0082971", "https://image.tmdb.org/t/p/original/ceG9VzoRAVGwivFU403Wc3AHRys.jpg", "Indiana Jones heeft maar één levensdoel: de wereld afreizen op zoek naar archeologische rijkdommen. Hij is een avonturier die voor niets terugschrikt om zijn doel te bereiken en zijn concurrenten te verslaan."
),

(
"Gladiator", "155", FALSE, TRUE, "tt0172495", "https://image.tmdb.org/t/p/original/ehGpN04mLJIrSnxcZBMvHeG0eDc.jpg", "De Romeinse generaal Maximus wordt ter dood veroordeeld door Commodus, de boosaardige troonopvolger van Marcus Aurelius. Maximus kan op het nippertje ontsnappen, maar zijn vrouw en zoon worden bruut vermoord."
),

(
"The Goonies", "114", FALSE, FALSE, "tt0089218", "https://image.tmdb.org/t/p/original/eBU7gCjTCj9n2LTxvCSIXXOvHkD.jpg", "De Goonies, een stel jonge tieners, vinden de plattegrond van de piraat Eénoog Willy en ze gaan meteen op jacht. Deze plattegrond leidt namelijk naar een schat. Al snel komen ze in een kilometerslang gangenstelsel terecht en beleven de gekste avonturen."
),

(
"E.T. the Extra-Terrestrial", "115", FALSE, FALSE, "tt0083866", "https://image.tmdb.org/t/p/original/an0nD6uq6byfxXCfk6lQBzdL2J1.jpg", "De tienjarige Elliott woont samen met zijn moeder, broer en zusje in een bosrijke buitenwijk van Los Angeles. Op een dag ontdekt hij in de tuin een buitenaards wezentje. Elliott en het wezentje schrikken zich eerst te pletter, maar sluiten dan vriendschap."
),

(
"Stand by Me", "95", FALSE, FALSE, "tt3331846", "https://image.tmdb.org/t/p/original/jArnRnllnxbvE2CEV8jc2hhwweS.jpg", "Nobita 'Noby' Nobi zit in de 4e klas van de middelbare school. Hij krijgt voortdurend onvoldoendes vanwege zijn luiheid en wordt altijd gepest door zijn klasgenoten Suneo 'Sneech' Honekawa en Takeshi 'Big G' Goda. Zijn achter-achterkleinzoon uit de 22e eeuw, Sewashi, die hem elke dag toekijkt reist naar Nobita's tijd in gezelschap van zijn robotkat Doraemon."
),

(
"Ferris Bueller's Day Off", "103", FALSE, FALSE, "tt0091042", "https://image.tmdb.org/t/p/original/kKhvDqvxaXSJXWjVKjCTeHvNKd3.jpg", "Voor de negende keer achter elkaar spijbelt Ferris Bueller van school. Dit keer moet hij een zeer slim excuus bedenken terwijl zijn zus er alles aan doet om hem door de mand te laten vallen. Ook de rector is zijn spijbelen spuugzat en wil er persoonlijk een einde aan maken."
),

(
"Rain Man", "133", FALSE, FALSE, "tt0095953", "https://image.tmdb.org/t/p/original/8L6EMburnnVx8cvQmhGgC826JNc.jpg", "Als de vader van de yuppie Charlie overlijdt, erft hij een oldtimer en een rozentuin. Hij komt tevens tot de ontdekking dat hij nog een broer heeft. Raymond is autistisch, maar is wel in staat om ingewikkelde wiskundige vraagstukken op te lossen."
),

(
"Dead Poets Society", "128", FALSE, FALSE, "tt0097165", "https://image.tmdb.org/t/p/original/ai40gM7SUaGA6fthvsd87o8IQq4.jpg", "Keating doceert in 1959 Engels aan een deftige kostschool voor jongens waar ijzeren discipline heerst. Zijn filosofie 'the purpose of education is to think for yourself' valt in slechte aarde bij de staf en de ouders, maar maakt hem razend populair bij de leerlingen."
),

(
"Enter The Dragon", "102", FALSE, FALSE, "tt0070034", "https://image.tmdb.org/t/p/original/zN7OOSARMLVzl9xJqkW2CcZ3xhY.jpg", "Lee wordt door de geheime dienst binnengehaald om aan een vechtsporttoernooi mee te doen, op een eiland geregeerd door een drugsdealer. Lee krijgt de opdracht hem uitschakelen, maar er mogen geen wapens op het eiland zijn."
),

(
"The Foreigner", "114", FALSE, FALSE, "tt1615160", "https://image.tmdb.org/t/p/original/rwM4hzrmc5HiWfQD9ls9DL4QgGl.jpg", "Wanneer Quan een restaurant begint in een buitenwijk van Londen, kan hij niet vermoeden dat hij een beroep zal moeten doen op de guerrillatechnieken die hij juist wilde vergeten. Zijn vrouw en dochter komen namelijk om bij een bomaanslag van Ierse terroristen."
),

(
"Lionheart", "105", FALSE, FALSE, "tt0100029", "https://image.tmdb.org/t/p/original/r9blY8BJR4FkWpvdbmmWuxPSc7z.jpg", "adat zijn broer in Los Angeles is vermoord door een rivaliserende misdaadbende, ontvlucht Lyon Gaultier in een verre uithoek van Noord-Afrika het Franse Vreemdelingenlegioen. Op de hielen gezeten door twee officieren van het Legioen, vindt hij zijn weg naar de V.S., waar hij kennismaakt met de wereld van illegale freefight."
)
;