from uploado import set_mi_tula, clean_information
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