#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

# losowanie min
import random
import gi
# wymagamy biblioteki w wersji min 3.0
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# zmienna przechowujaca ilość min oraz rozmiar planszy
n = 3


class Plansza(Gtk.Grid):
    """Klasa implementujaca plansze gry."""

    def __init__(self, rodzic, rozmiar):
        """Konstruktor klasy plansza.

        Parameters:
            rodzic  - odnosnik do klasy, ktora utworzyla plansze
            rozmiar - rozmiar planszy
        """
        Gtk.Grid.__init__(self)

        self.rodzic = rodzic
        self.rozmiar = rozmiar
        self.generuj_plansze()

    def generuj_plansze(self):
        """Metoda generujaca plansze."""

        # Zmienna przechowujaca przyciski bedace polami planszy
        self.pola = []

        # utworzenie pól planszy
        for i in xrange(self.rozmiar):
            self.pola.append([])

            for j in xrange(self.rozmiar):
                b = Gtk.Button.new_with_label("")
                self.pola[i].append(b)
                self.attach(b, i, j, 1, 1)
                b.connect("clicked", self.kliknieto, j, i)

        self.set_column_homogeneous(True)
        self.set_row_homogeneous(True)

    def kliknieto(self, button, x, y):
        """Metoda wywolywana w momencie klikniecia na pole.

        Parameters:
            button  - przycisk jaki zostal wcisniety
            x, y    - pozycja przycisku
        """
        button.set_sensitive(False)

        # odwolanie do mechaniki gry ktora zostala zaimpelentowana
        # w klasie App
        self.rodzic.stan_pola(button, x, y)

    def reset_planszy(self):
        """Metoda resetujaca pola planszy."""
        for i in xrange(self.rozmiar):
            for j in xrange(self.rozmiar):
                self.pola[i][j].set_sensitive(True)
                self.pola[i][j].get_child().set_markup("")

    def ustaw_tekst(self, button, tekst):
        """Metoda odpowiedzialna za ustawienie label na polu.

        Parameters:
            button  - przycisk do ktorego ma zostac dodany tekst
            tekst   - tekst jaki ma zostac dodany do przycisku
        """
        kolory = {"default": "brown",
                  -1: "red",
                  0: "black",
                  1: "orange",
                  2: "orangered",
                  3: "tomato"}

        if tekst == -1:
            styl = '<span foreground="{}"><b>{}</b></span>'.format(kolory[tekst], "M")
        elif tekst > 3:
            styl = '<span foreground="{}"><b>{}</b></span>'.format(kolory["default"], tekst)
        else:
            styl = '<span foreground="{}"><b>{}</b></span>'.format(kolory[tekst], tekst)

        button.get_child().set_markup(styl)
        button.set_sensitive(False)

    def odslon_wszystkie(self):
        """Metoda odpowiedzialna za odsloniecie wszystkich pol planszy."""
        for i in xrange(self.rozmiar):
            for j in xrange(self.rozmiar):
                if (self.pola[i][j].get_sensitive() is True):
                    ilosc_min = self.rodzic.ile_min_w_poblizu(j, i)
                    self.ustaw_tekst(self.pola[i][j], ilosc_min)


class App(Gtk.Window):
    """Klasa glowna aplikacji tworzy okno i inicjalizuje gre."""

    def __init__(self):
        """Konstruktor klasy App."""

        Gtk.Window.__init__(self)
        # ustawienie tytulu okna oraz rozmiaru
        self.set_title("Saper")
        self.set_default_size(200, 200)

        self.connect("delete-event", Gtk.main_quit)

        box = Gtk.VBox()

        # utworzenie przycisku "Nowa gra"
        self.nowa = Gtk.Button.new_with_label("Nowa gra")
        self.nowa.connect("clicked", self.nowa_gra)

        box.pack_end(self.nowa, True, True, 0)

        # utworzenie planszy rozgrywki
        self.plansza = Plansza(self, n)

        box.pack_end(self.plansza, True, True, 0)

        self.add(box)

        self.show_all()

        # wylosowanie min
        self.losuj_miny()

    # implementacja mechaniki gry

    def nowa_gra(self, _):
        """Metoda odpowiedzialna za utworzenie nowej rozgrywki."""

        # ustawienie tytulu okna
        self.set_title("Saper")

        # zresetowanie ustawien przyciskow
        self.plansza.reset_planszy()

        # wylosowanie nowych pozycji min
        self.losuj_miny()

    def losuj_miny(self):
        """Metoda odpowiedzialna za wylosowanie min."""

        # zmienna przechowujaca informacje o ilosci pol bez miny
        self.bezpieczne_pola = n ** 2 - n

        # zmienna przechowujaca zbior pozycji min
        self.miny = set()

        # losowanie pozycji min
        for i in xrange(n):
            pozycja = (random.randint(0, n - 1),
                       random.randint(0, n - 1))

            # ponowne losowanie w przypadku gdy pozycja
            # miny znajduje sie juz w zbiorze
            while(pozycja in self.miny):
                pozycja = (random.randint(0, n - 1),
                           random.randint(0, n - 1))

            self.miny.add(pozycja)

    # W specyfikacji jest napisane by w momencie losowania min
    # zostaly wyliczone wartosci poszczegolnych pol
    # jednakze rozwiazanie to dla duzego rozmiaru planszy
    # jest nieefektywne gdyż musimy przechowywac informacje
    # o n^2 pol zatem rozmiar potrzebnej pamieci rosnie szybko
    # moje rozwiazanie polega na wyszukaniu min ktore sasiaduja
    # z danym polem
    def ile_min_w_poblizu(self, x, y):
        """Metoda wyliczajaca ilosc min.

        Metoda ta na biezaco wylicza ilosc min dla zadanej pozycji pola

        Parameters:
            x, y  - pozycja przycisku jaki zostal wcisniety

        Return:
            suma - ilosc min w poblizu zadanego pola
        """

        # jezeli pole jakie zostalo wcisniete okazuje sie mina zwracam -1
        if (x, y) in self.miny:
            return -1

        # zmienna przechowujaca ilosc min w poblizu pola
        suma = 0

        for i in xrange(x - 1, x + 2):
            for j in xrange(y - 1, y + 2):
                if i < 0 or j < 0:
                    continue
                if (i, j) in self.miny:
                    suma += 1

        return suma

    def stan_pola(self, button, x, y):
        """Metoda ktora aktualizuje stan wybranego pola.

        Parameters:
            button  - pole w postaci przycisku jakie zostalo wybrane
            x, y    - pozycja pola
        """

        # zmniejszenie ilosci bezpiecznych pol
        self.bezpieczne_pola -= 1

        # okreslenie ilosci min w poblizu wybranego pola
        ilosc_min = self.ile_min_w_poblizu(x, y)

        # jezeli natrafilismy na mine to gra sie konczy przegrana
        # jezeli ilosc bezpiecznych pol jest rowna 0
        # to gra konczy sie wygrana
        if ilosc_min == -1:
            # odsloniecie wszystkich pol
            self.plansza.odslon_wszystkie()

            # zwrocenie stosownego komunikatu
            self.przegrana()
        elif self.bezpieczne_pola == 0:
            # odsloniecie wszystkich pol
            self.plansza.odslon_wszystkie()

            # zwrocenie stosownego komunikatu
            self.wygrana()

        # ustawienie tekstu na wybranym polu
        self.plansza.ustaw_tekst(button, ilosc_min)

    def przegrana(self):
        """Metoda wywolywana w momencie przegranej."""
        self.set_title("PRZEGRANA!")

    def wygrana(self):
        """Metoda wywolywana w momencie wygranej."""
        self.set_title("WYGRANA!")

        # utworzenie okna popup z informacja o wygranej
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, "WYGRANA")
        dialog.run()
        dialog.destroy()

if __name__ == "__main__":
    a = App()
    Gtk.main()
