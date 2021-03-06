import pytest
import numpy as np
import pandas as pd
from pyleiades.energies import Energy

class TestEnergy:

    def test_ignore_case(self, testdata):
        nuc_test_data = testdata.iloc[7:].value
        nuc = Energy('Nuclear', data=testdata)
        nuc_energy_data = nuc.energy_data.value
        assert nuc_energy_data.equals(nuc_test_data)

    def test_invalid_energy(self, testdata):
        with pytest.raises(ValueError):
            Energy('test', data=testdata)

    def test_isolate_energy(self, testdata):
        nuc_test_data = testdata.iloc[7:].value
        nuc = Energy('nuclear', data=testdata)
        nuc_energy_data = nuc.energy_data.value
        assert nuc_energy_data.equals(nuc_test_data)

    def test_default_data(self, testdata, testvals):
        nuc_test_data = testdata.iloc[7:].value
        nuc = Energy('nuclear')
        nuc_energy_data = nuc.energy_data.value.values
        assert np.array_equal(nuc_energy_data, nuc_test_data)

    def test_monthly_data(self, testdata, testvals):
        nuc_test_data = np.concatenate([testvals[8:20], testvals[21:23]])
        nuc = Energy('nuclear', data=testdata)
        nuc_monthly_data = nuc.monthly_data.value.values
        assert np.array_equal(nuc_monthly_data, nuc_test_data)

    def test_yearly_data(self, testdata, testvals):
        nuc_test_data = np.array([testvals[7], testvals[20]])
        nuc = Energy('nuclear', data=testdata)
        nuc_yearly_data = nuc.yearly_data.value.values
        assert np.array_equal(nuc_yearly_data, nuc_test_data)

    def test_daterange_bounding_inputs(self, testdata, testvals):
        nuc_test_date_range = np.concatenate([testvals[10:20], testvals[21:22]])
        nuc = Energy('nuclear', data=testdata)
        nuc_date_range = nuc._daterange(nuc.monthly_data, '197303', '197401') \
                            .value.values
        assert np.array_equal(nuc_date_range, nuc_test_date_range)

    def test_daterange_bounding_defaults(self, testdata, testvals):
        nuc_test_date_range = np.concatenate([testvals[8:20], testvals[21:23]])
        nuc = Energy('nuclear', data=testdata)
        nuc_date_range = nuc._daterange(nuc.monthly_data, None, None) \
                            .value.values
        assert np.array_equal(nuc_date_range, nuc_test_date_range)

    def test_totals_monthly(self, testdata, testvals):
        nuc_test_totals = np.concatenate([testvals[8:20], testvals[21:23]])
        nuc = Energy('nuclear', data=testdata)
        nuc_monthly_totals = nuc.totals('monthly').value.values
        assert np.array_equal(nuc_monthly_totals, nuc_test_totals)

    def test_totals_yearly(self, testdata, testvals):
        valarray = testdata.value.values
        nuc_test_totals = np.array([testvals[7], testvals[20]])
        nuc = Energy('nuclear', data=testdata)
        nuc_yearly_totals = nuc.totals('yearly').value.values
        assert np.array_equal(nuc_yearly_totals, nuc_test_totals)

    def test_totals_cumulative(self, testdata, testvals):
        nuc_test_total = np.sum(np.array([testvals[7], testvals[20]]))
        nuc = Energy('nuclear', data=testdata)
        nuc_cumulative_total = nuc.totals('cumulative')
        assert nuc_cumulative_total == nuc_test_total

    def test_totals_invalid_freq(self, testdata):
        nuc = Energy('nuclear', data=testdata)
        with pytest.raises(ValueError):
            nuc_cumulative_total = nuc.totals('test')

    def test_maxima_month(self, testdata):
        nuc_test_max_month, nuc_test_max_val = pd.Period('197310', 'M'), 0.20
        nuc = Energy('nuclear', data=testdata)
        nuc_max_month, nuc_max_val = nuc.maxima('monthly')
        assert nuc_max_month == nuc_test_max_month
        assert nuc_max_val == nuc_test_max_val

    def test_minima_month(self, testdata):
        nuc_test_min_month, nuc_test_min_val = pd.Period('197303', 'M'), 0.09
        nuc = Energy('nuclear', data=testdata)
        nuc_min_month, nuc_min_val = nuc.minima('monthly')
        assert nuc_min_month == nuc_test_min_month
        assert nuc_min_val == nuc_test_min_val

    def test_extrema_maximum_month(self, testdata):
        nuc_test_max_month, nuc_test_max_val = pd.Period('197310', 'M'), 0.20
        nuc = Energy('nuclear', data=testdata)
        nuc_max_month, nuc_max_val = nuc.extrema('max', 'monthly')
        assert nuc_max_month == nuc_test_max_month
        assert nuc_max_val == nuc_test_max_val

    def test_extrema_minimum_month(self, testdata):
        nuc_test_min_month, nuc_test_min_val = pd.Period('197303', 'M'), 0.09
        nuc = Energy('nuclear', data=testdata)
        nuc_min_month, nuc_min_val = nuc.extrema('min', 'monthly')
        assert nuc_min_month == nuc_test_min_month
        assert nuc_min_val == nuc_test_min_val

    def test_extrema_maximum_year(self, testdata):
        valarray = testdata.value.values
        nuc_test_max_year, nuc_test_max_val = pd.Period('1973', 'Y'), 1.30
        nuc = Energy('nuclear', data=testdata)
        nuc_max_year, nuc_max_val = nuc.extrema('max', 'yearly')
        assert nuc_max_year == nuc_test_max_year
        assert nuc_max_val == nuc_test_max_val

    def test_extrema_minimum_year(self, testdata):
        nuc_test_min_year, nuc_test_min_val = pd.Period('1972', 'Y'), 0.60
        nuc = Energy('nuclear', data=testdata)
        nuc_min_year, nuc_min_val = nuc.extrema('min', 'yearly')
        assert nuc_min_year == nuc_test_min_year
        assert nuc_min_val == nuc_test_min_val

    def test_extrema_invalid_freq(self, testdata):
        nuc = Energy('nuclear', data=testdata)
        with pytest.raises(ValueError):
            nuc_cumulative_total = nuc.extrema('max', 'test')

    def test_extrema_invalid_ext(self, testdata):
        nuc = Energy('nuclear', data=testdata)
        with pytest.raises(ValueError):
            nuc_cumulative_total = nuc.extrema('test', 'yearly')
