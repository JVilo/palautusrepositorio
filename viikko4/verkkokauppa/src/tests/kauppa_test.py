import unittest
from unittest.mock import Mock, ANY, MagicMock
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.varasto_mock = Mock()
        
        self.pankki_mock.tilisiirto = MagicMock()
        

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        # palautetaan aina arvo 42
        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_kun_tilimaksu_varmistaa_oikeaasiaksa_oikeatili_oikea_summa_tilisiirrossa(self):
        
        self.viitegeneraattori_mock.uusi.return_value = 25

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 5

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 1)
            
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pirkko", "02468")

        self.pankki_mock.tilisiirto.assert_called_with("pirkko", 25, "02468", ANY, 1)

    def test_kaksi_eri_tuotetta_kun_tilimaksu_varmistaa_oikeaasiaksa_oikeatili_oikea_summa_tilisiirrossa(self):
        self.viitegeneraattori_mock.uusi.return_value = 30

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 5
            if tuote_id == 2:
                return 2

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 1)
            if tuote_id == 2:
                return Tuote(1, "kurkku",3)
            
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("pirkko", "02468")

        self.pankki_mock.tilisiirto.assert_called_with("pirkko", 30, "02468", ANY, 4)

    def test_kaksi_samaa_tuotetta_kun_tilimaksu_varmistaa_oikeaasiaksa_oikeatili_oikea_summa_tilisiirrossa(self):
        self.viitegeneraattori_mock.uusi.return_value = 30

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 5

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 1)
            
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pirkko", "02468")

        self.pankki_mock.tilisiirto.assert_called_with("pirkko", 30, "02468", ANY, 2)
    
    def test_kaksi_eri_tuotetta_toinen_loppu_varastosta_kun_tilimaksu_varmistaa_oikeaasiaksa_oikeatili_oikea_summa_tilisiirrossa(self):
        self.viitegeneraattori_mock.uusi.return_value = 20

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 0
            if tuote_id == 2:
                return 2

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 1)
            if tuote_id == 2:
                return Tuote(1, "kurkku",3)
            
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("pirkko", "02468")

        self.pankki_mock.tilisiirto.assert_called_with("pirkko", 20, "02468", ANY, 3)
    
    def test_Varmista_että_metodin_aloita_asiointi_kutsuminen_nollaa_edellisen_ostoksen_tiedot(self):
        self.viitegeneraattori_mock.uusi.return_value = 20

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 0
            if tuote_id == 2:
                return 2

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 1)
            if tuote_id == 2:
                return Tuote(1, "kurkku",3)
            
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.tilimaksu("pirkko", "02468")
        self.varasto_mock.assert_not_called()
        
        self.pankki_mock.tilisiirto.assert_called_with("pirkko", 20, "02468", ANY, 0)

    def test_Varmista_että_kauppa_pyytää_uuden_viitenumeron_jokaiselle_maksutapahtumalle(self):
        
        self.viitegeneraattori_mock = Mock(wraps=Viitegeneraattori())
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 2

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 1)
            if tuote_id == 2:
                return Tuote(1, "kurkku",3)
            
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)
        
        
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("pirkko", "02468")

        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 1)


        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("pirkko", "02468")

        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)



        


        


        