# Gra saper napisana w Pythonie

### ZASADY GRY
- Gra jest jednoosobowa.
- Gra odbywa się na planszy złożonej z n×n pól,
- Na początku komputer losuje n różnych położeń min oraz dla każdego pola uaktualnia informację, z iloma minami dane pole sąsiaduje (w poziomie, pionie oraz po ukosach).

Następnie rozpoczyna się rozgrywka:
- Użytkownik odsłania pola tak, aby nie natrafić na minę.
- Gra toczy się do momentu odkrycia wszystkich pól bez min (wygrana) lub do odkrycia pola z miną (przegrana).
- W sytuacji wygranej odsłaniane są wszystkie pola (ustawione na nieaktywne) oraz wyświetlane jest okno z informacją o wygranej
- Po natrafieniu na minę, użytkownik przegrywa, wszystkie pola są odsłaniane (oraz ustawione na nieaktywne).
- Przycisk Nowa gra umożliwia rozpoczęcie nowej rozgrywki (resetowanie początkowych ustawień min; przyciski stają się aktywne; okno aplikacji pozostaje to samo), nawet jeśli obecna gra nie jest ukończona.
- Gracz może wybrać dowolne pole, poprzez kliknięcie na nim myszką.
- Po kliknięciu na pole, wyświetla się jego zawartość (informacja o sąsiadujących minach, lub informacja o minie).

<br></br>
### INTERFEJS
- Plansza została zaimplementowana jako własna klasa Plansza, która dziedziczy bezpośrednio po Gtk.Table lub Gtk.Grid.
- Plansza zawiera n×n pól, a na nich w losowych miejscach n min.
- Pojedyncze pole planszy zostało zaimplementowane jako Gtk.Button.
- Przycisk może zostać użyty tylko raz. Wtedy, na labeli wyświetlana jest informacja o sąsiadujących minach, lub informacja o minie, formatowane w następujący sposób (do formatowania tekstu na lebeli skorzystałem z metody Gtk.Label.set_markup() oraz Pango markup):
  * dla miny: czerwona, pogrubiona litera M,
  * zero min w sąsiedztwie: czarna, pogrubiona liczba 0,
  * jedna mina w sąsiedztwie: pogrubiona liczba 1 w kolorze "orange",
  * dwie miny w sąsiedztwie: pogrubiona liczba 2 w kolorze "orangered",
  * trzy miny w sąsiedztwie: pogrubiona liczba 3 w kolorze "tomato",
  * cztery i więcej min w sąsiedztwie: pogrubiona liczba min w kolorze "brown".

<br></br>
### MECHANIKA GRY
- Mechanika aplikacji została zaimplementowana wewnątrz klasy App.
- Przycisk "Nowa gra" może zostać wciśnięty w każdej chwili i resetuje rozgrywkę.

<br></br>
> #### Uwaga
> Program będący rozwiązaniem musi składać się z pojedynczego pliku źródłowego. Program nie powinien zapisywać żadnych danych.
