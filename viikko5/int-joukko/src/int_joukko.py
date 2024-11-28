KAPASITEETTI = 5
KASVATUSKOKO = 5


class IntJoukko:

    def _luo_lista(self, koko):
        return [0] * koko
    
    def __init__(self, kapasiteetti=KAPASITEETTI, kasvatuskoko=KASVATUSKOKO):
        if not isinstance(kapasiteetti, int) or kapasiteetti < 0:
            raise ValueError("Invalid capacity")
        if not isinstance(kasvatuskoko, int) or kasvatuskoko < 0:
            raise ValueError("Invalid increment size")
        
        self.kapasiteetti = kapasiteetti
        self.kasvatuskoko = kasvatuskoko
        self.alkioiden_lukumaara = 0
        self.ljono = self._luo_lista(self.kapasiteetti)


    def kuuluu(self, n):
        return n in self.ljono[:self.alkioiden_lukumaara]

    def lisaa(self, n):
        if not self.kuuluu(n):
            if self.alkioiden_lukumaara == len(self.ljono):
                self.ljono.extend([0] * self.kasvatuskoko)
            self.ljono[self.alkioiden_lukumaara] = n
            self.alkioiden_lukumaara += 1
            return True
        return False

    def poista(self, n):
        try:
            index = self.ljono.index(n, 0, self.alkioiden_lukumaara)
            self.ljono[index:self.alkioiden_lukumaara - 1] = self.ljono[index + 1:self.alkioiden_lukumaara]
            self.alkioiden_lukumaara -= 1
            return True
        except ValueError:
            return False

    def kopioi_lista(self, a, b):
        for index in range(0, len(a)):
            b[index] = a[index]

    def mahtavuus(self):
        return self.alkioiden_lukumaara

    def to_int_list(self):
        return self.ljono[:self.alkioiden_lukumaara]

    @staticmethod
    def yhdiste(a, b):
        result = IntJoukko()
        for num in a.to_int_list() + b.to_int_list():
            result.lisaa(num)
        return result

    @staticmethod
    def leikkaus(a, b):
        result = IntJoukko()
        a_set = set(a.to_int_list())
        for num in b.to_int_list():
            if num in a_set:
                result.lisaa(num)
        return result

    @staticmethod
    def erotus(a, b):
        result = IntJoukko()
        b_set = set(b.to_int_list())
        for num in a.to_int_list():
            if num not in b_set:
                result.lisaa(num)
        return result

    def __str__(self):
        if self.alkioiden_lukumaara == 0:
            return "{}"
        return "{" + ", ".join(map(str, self.to_int_list())) + "}"
