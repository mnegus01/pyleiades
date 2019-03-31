import pytest
import numpy as np
from matplotlib import pyplot as plt
from pyleiades.visuals import Visual

class TestVisual:

    def test_include_energy(self, testdata):
        nuc_test_data = testdata.iloc[7:].value
        visual = Visual(data=testdata)
        visual.include_energy('nuclear', 'coal')
        nuc_energy_data = visual.energies[0].energy_data.value
        assert 'nuclear' == visual.energies[0].energy_type
        assert 'coal' == visual.energies[1].energy_type
        assert nuc_energy_data.equals(nuc_test_data)

    def test_linegraph_no_energies(self, testdata):
        visual = Visual(data=testdata)
        with pytest.raises(RuntimeError):
            ax = visual.linegraph('totals')

    def test_linegraph_invalid_subject(self, testdata):
        visual = Visual(data=testdata)
        visual.include_energy('nuclear')
        with pytest.raises(ValueError):
            ax = visual.linegraph('test')

    def test_linegraph_default_totals(self, testdata, testvals):
        nuc_test_totals = np.array([testvals[7], testvals[20]])
        visual = Visual(data=testdata)
        visual.include_energy('nuclear')
        ax = visual.linegraph('totals')
        nuc_default_totals = ax.lines[0].get_xydata().T[1]
        assert np.array_equal(nuc_default_totals, nuc_test_totals)

    def test_linegraph_yearly_totals(self, testdata, testvals):
        nuc_test_totals = np.array([testvals[7], testvals[20]])
        visual = Visual(data=testdata)
        visual.include_energy('nuclear')
        ax = visual.linegraph('totals', freq='yearly')
        nuc_yearly_totals = ax.lines[0].get_xydata().T[1]
        assert np.array_equal(nuc_yearly_totals, nuc_test_totals)

    def test_linegraph_monthly_totals(self, testdata, testvals):
        nuc_test_totals = np.concatenate([testvals[8:20], testvals[21:23]])
        visual = Visual(data=testdata)
        visual.include_energy('nuclear')
        ax = visual.linegraph('totals', freq='monthly')
        nuc_monthly_totals = ax.lines[0].get_xydata().T[1]
        assert np.array_equal(nuc_monthly_totals, nuc_test_totals)
