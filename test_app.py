from app import name_archivo, get_fincaraiz_results
from datetime import datetime
import pytest
import unittest


new_year = datetime(2020, 1, 1)
now = datetime.now()
date_hoy=str(now.strftime("%Y-%m-%d"))
date_tomorrow=datetime(2024, 12, 3)

@pytest.mark.parametrize(
    'input_x, expected',
    [
        (new_year, 'landing_casas_2020-01-01 00:00:00.html'),
        (date_hoy, 'landing_casas_2023-03-12.html'),
        (date_tomorrow, 'landing_casas_2024-12-03 00:00:00.html')
    ]
)
def test_name_archivo(input_x, expected):
    assert name_archivo(input_x)==expected
    


class TestGetFincaraizResults(unittest.TestCase):

    def setUp(self):
        # Código de configuración previo a cada prueba
        self.url = 'https://casas.mitula.com.co/searchRE/op-1/tipo-Casa/q-Chapinero--Cundinamarca'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    def test_response_status_code(self):
        # Comprobamos que el código de estado de la respuesta es 200 (OK)
        response = get_fincaraiz_results(self.url, self.headers)
        self.assertEqual(response.status_code, 200)

    def test_response_content(self):
        # Comprobamos que el contenido de la respuesta es del tipo esperado
        response = get_fincaraiz_results(self.url, self.headers)
        self.assertIsInstance(response.content, bytes)

if __name__ == '__main__':
    unittest.main()
    
