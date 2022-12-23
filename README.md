
# Koszt mapy zasadniczej - wtyczka QGIS3

Wtyczka QGIS do określania prawdopodobnego kosztu pozyskania wektorowej mapy zasadniczej.
Koszt określany jest na podstawie załącznika do [ustawy z dnia 17 maja 1989r. - prawo geodezyjne i kartograficzne](https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU19890300163/U/D19890163Lj.pdf) oraz [obieszczenia Ministra Rozwoju i Technologii z dnia 25 października 2022 r. w sprawie ogłoszenia obowiązujących od dnia 1 stycznia 2023 r. stawek opłat za udostępnianie materiałów państwowego zasobu geodezyjnego i kartograficznego](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WMP20220001038).

W celu obliczenia prawdopodobnego kosztu mapy zasadniczej należy wskazać warstwę poligonową z zakresem zamawianej mapy. 

## Instalacja 

Aby zainstalować wtyczkę, należy ściągnąć ją w formacie .zip, a następnie w QGIS wybrać menu *Wtyczki -> Zarządzanie wtyczkami -> Instaluj z pliku ZIP*, wskazać lokalizację ściągniętego pliku i kliknąć "Zainstaluj wtyczkę".  

## Szczegóły obliczeniowe
Zgodnie z załącznikiem do prawa geodezyjnego i kartograficznego, przy zamawianiu kopii zasadniczej stosuje się współczynniki korygujące:

 1. CL – ze względu na cel, w jakim wykorzystywane będą udostępniane materiały zasobu; określa się go zaznaczając odpowiednie pole we wniosku o udostępnienie materiałów powiatowego zasobu geodezyjnego i
    kartograficznego. Do celów wtyczki przyjęto opcję "dla dowolnych potrzeb", gdzie współczynnik CL=2;

    

 2. LR – ze względu na liczbę jednostek rozliczeniowych (Ljr) udostępnianych materiałów zasobu; Dla mapy zasadniczej w postaci wektorowej współczynnik jednostką rozliczeniową jest hektar (ha). LR
    przyjmuje wartość:    
    
	- 1,0 – dla Ljr nie większej niż L1 = 10 (obszarów nie większych niż 10ha);
	- 0,8 – dla Ljr w przedziale 11–100 (obszarów w przedziale wielkości 11-100 ha);
	- 0,6 – dla Ljr większej od L2 = 100 (obszarów większych niż 100 ha)

 3. SU – ze względu na sposób udostępniania materiałów zasobu; W przypadku jednorazowego udostępniania materiałów zasobu współczynnik SU stosuje się w wysokości:

	- 1,0 – w przypadku udostępniania materiałów zasobu na zewnętrznym nośniku danych elektronicznych lub w postaci plików danych przekazywanych drogą
elektroniczną albo w postaci drukowanej;
	- 0,8 – w przypadku udostępniania materiałów zasobu w postaci elektronicznej za pomocą usług sieciowych. Do celów niniejszej wtyczki przyjęto wartość SU=1

4. PD – w przypadku gdy przedmiotem udostępnienia jest dająca się wyodrębnić część materiału zasobu, dla którego określona jest stawka podstawowa - dla map zasadniczych zawsze PD = 1

5. AJ – w przypadku, gdy udostępniany materiał zasobu zawiera informacje nieaktualne lub o cechach zmniejszających przydatność użytkową tego materiału. W przypadku mapy zasadniczej współczynnik AJ jest zależny od skali udostępnianej mapy. AJ przyjmuje wartość:
	- 1,0 – dla mapy zasadniczej w skalach 1:500;
	-  0,8 – dla mapy zasadniczej w skalach 1:1000;
	-  0,5 – dla mapy zasadniczej w skalach 1:2000;
	-  0,3 – dla mapy zasadniczej w skalach 1:5000.
W niniejszej wtyczce obliczany jest koszt mapy dla każdej z możliwych skal.

6. Sp - stawka podstawowa - dla mapy zasadniczej w wersji wektorowej, zgodnie z obwieszczeniem Ministra Rozwoju, Pracy i Technologii z dnia 1 października 2021 r. w sprawie ogłoszenia obowiązujących od dnia 1 stycznia 2022 r. stawek opłat za udostępnianie materiałów państwowego zasobu geodezyjnego i kartograficznego, wynosi 21,53 

Dla obszarów mniejszych niż 10ha (o liczbie jednostek rozliczeniowych (Lrj) mniejszej niż 10) wysokość opłaty za udostępnienie mapy (Wop) oblicza się wg. wzoru:

Wop = Sp × Ljr × CL × SU × PD × AJ

po podstawieniu znanych zmiennych: 

Wop = 21,53 × Ljr × 2 × 1 × 1 × AJ

gdzie Ljr jest liczbą jednostek rozliczeniowych udostępnianych materiałów zasobu, tzn. wielkością mapy w hektarach.

Dla obszarów większych niż 10ha i mniejszych niż 100 ha (o liczbie jednostek rozliczeniowych (Lrj) większej niż 10, ale mniejszej niż 100) wysokość opłaty za udostępnienie mapy (Wop) oblicza się wg. wzoru:

Wop = Sp × [L1 + (Ljr – L1) × LR1] x CL × SU × PD × AJ

po podstawieniu znanych zmiennych: 

Wop = Sp × [10 + (Ljr – 10) × 0,8] x 2 × 1 × 1 × AJ

Dla obszarów większych niż 100ha (o liczbie jednostek rozliczeniowych (Lrj) większej niż 100) wysokość opłaty za udostępnienie mapy (Wop) oblicza się wg. wzoru:

Wop = Sp × [L1 + (L2 – L1) × LR1 + (Ljr – L2) × LR2] x CL × SU × PD × AJ

po podstawieniu znanych zmiennych: 

Wop = Sp × 10 + 90 × 0,8 + (Ljr – 100) × 0,6] x 2 × 1 × 1 × AJ.

## Zastrzeżenie

Autor wtyczki nie bierze odpowiedzialności za działanie wtyczki i ewentualne błędne wyniki. Wtyczka jest open source, każdy może własnoręcznie zweryfikować kod.

Ponadto, koszt pozyskiwanych map zasadniczych może różnić się w zależności od powiatu. Niektóre PODGiKi nie dysponują mapami w wersji wektorowej i udostępniają mapy rastrowe, których koszt jest obliczany w odmienny sposób; oprócz tego pomiędzy poszczególnymi powiatami występują różnice w interpretacji prawa geodezyjnego i kartograficznego wpływające na koszt pozyskania map. Przykładem może być przypadek liczenia kosztu map "od nowa" w każdej gminie (tzn. naliczając od początku liczbę Ljr wpływającą na współczynnik LR), w przypadku pozyskiwania map z więcej niż jednej gminy danego powiatu.

Autor: Grzegorz Warszycki
opti33@gmail.com
https://www.linkedin.com/in/grzegorz-warszycki/

