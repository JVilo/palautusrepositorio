from enum import Enum
from tkinter import ttk, constants, StringVar


class Komento(Enum):
    SUMMA = 1
    EROTUS = 2
    NOLLAUS = 3
    KUMOA = 4


class Kayttoliittyma:
    def __init__(self, sovelluslogiikka, root):
        self._sovelluslogiikka = sovelluslogiikka
        self._root = root

        self._komennot = {
            Komento.SUMMA: self._summa,
            Komento.EROTUS: self._erotus,
            Komento.NOLLAUS: self._nollaus,
            Komento.KUMOA: self._kumoa
            
        }
        self.history = []

    def kaynnista(self):
        self._arvo_var = StringVar()
        self._arvo_var.set(self._sovelluslogiikka.arvo())
        self._syote_kentta = ttk.Entry(master=self._root)

        tulos_teksti = ttk.Label(textvariable=self._arvo_var)

        summa_painike = ttk.Button(
            master=self._root,
            text="Summa",
            command=lambda: self._suorita_komento(Komento.SUMMA)
        )

        erotus_painike = ttk.Button(
            master=self._root,
            text="Erotus",
            command=lambda: self._suorita_komento(Komento.EROTUS)
        )

        self._nollaus_painike = ttk.Button(
            master=self._root,
            text="Nollaus",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.NOLLAUS)
        )

        self._kumoa_painike = ttk.Button(
            master=self._root,
            text="Kumoa",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.KUMOA)
        )

        tulos_teksti.grid(columnspan=4)
        self._syote_kentta.grid(columnspan=4, sticky=(constants.E, constants.W))
        summa_painike.grid(row=2, column=0)
        erotus_painike.grid(row=2, column=1)
        self._nollaus_painike.grid(row=2, column=2)
        self._kumoa_painike.grid(row=2, column=3)
    
    def _lue_syote(self):
        return self._syote_kentta.get()

    def _suorita_komento(self, komento):
        arvo = 0
        try:
            arvo = int(self._syote_kentta.get())
        except ValueError:
            pass
            
        if komento != Komento.KUMOA:
            self.history.append((komento, arvo))

        self._komennot[komento](arvo)
        print(komento)
        

        self._kumoa_painike["state"] = constants.NORMAL

        if self._sovelluslogiikka.arvo() == 0:
            self._nollaus_painike["state"] = constants.DISABLED
        else:
            self._nollaus_painike["state"] = constants.NORMAL

        self._syote_kentta.delete(0, constants.END)
        self._arvo_var.set(self._sovelluslogiikka.arvo())

    def _summa(self, arvo):
        print(arvo,"arvo")
        print(self._sovelluslogiikka.arvo(), "sovelluslog")
        self._sovelluslogiikka.plus(arvo)

    def _erotus(self, arvo):
        self._sovelluslogiikka.miinus(arvo)

    def _nollaus(self, arvo):
        self._sovelluslogiikka.nollaa()

    def _kumoa(self, arvo):
        if not self.history:
            return
        last_command, last_value = self.history.pop()
        if last_command == Komento.SUMMA:
            self._sovelluslogiikka.miinus(last_value)
        elif last_command == Komento.EROTUS:
            self._sovelluslogiikka.plus(last_value)
    

        
