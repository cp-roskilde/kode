# Snake

Her er de specifikke kodeblokke og logik, du skal bruge i PictoBlox for at få dit Snake-spil til at fungere. Vi opdeler det i tre dele: Slangehovedet, Kroppen og Maden.
------------------------------
## 1. Slangehovedet (Hovedlogik og styring)
Slangehovedet skal konstant bevæge sig fremad, oprette kloner af sig selv (som danner kroppen) og skifte retning med pilestasterne.
Bevægelse og krop (Placeres på Hoved-spriten):

* når der klikkes på det grønne flag
* sæt [Point v] til (0)
   * sæt retning til [90 v] (Peg til højre)
   * gå til x: (0) y: (0)
   * for evigt
   * gå (10) trin
      * opret klon af [mig selv v]
      * vent (0.1) sekunder
   
Styring med pilestaster (Placeres på Hoved-spriten):

* når der trykkes på tasten [pil op v] → sæt retning til [0 v]
* når der trykkes på tasten [pil ned v] → sæt retning til [180 v]
* når der trykkes på tasten [pil højre v] → sæt retning til [90 v]
* når der trykkes på tasten [pil venstre v] → sæt retning til [-90 v]

(Tip: For at undgå at slangen kan gå direkte baglæns ind i sig selv, kan du tilføje en hvis block, f.eks.: hvis ikke <retning = 180>, så sæt retning til 0 for pil op).
------------------------------
## 2. Slangens krop (Klon-styring)
Klonerne fungerer som slangens krop. De skal forsvinde efter et kort stykke tid. Jo flere point du har, jo længere skal klonerne blive på skærmen.
Placeres på Hoved-spriten:

* når jeg starter som klon
* vent ((0.2) + (Point * (0.1))) sekunder
   * slet denne klon

------------------------------
## 3. Maden (Æblet)
Maden skal placere sig et tilfældigt sted. Når slangen rører maden, skal den flytte sig, og du skal have et point.
Placeres på Mad-spriten:

* når der klikkes på det grønne flag
* gå til tilfældig placering
   * for evigt
   * hvis <rører [Slangehoved v]?> så
      * ændr [Point v] med (1)
         * gå til tilfældig placering
      
------------------------------
## 4. Game Over (Tab-betingelse)
Spillet skal stoppe, hvis slangen rammer kanten eller rører sin egen krop.
Placeres på Hoved-spriten (inde i din 'for evigt'-løkke):

* hvis <<rører [kant v]?> eller <rører farve [#FarvePåKroppen]>> så
* sig [Game Over!] i (2) sekunder
   * stop [alle v]


