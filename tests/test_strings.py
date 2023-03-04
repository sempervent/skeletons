"""Test the skeletons init."""
import pytest

from skeletons.strings import FString, LString


# pylint: disable=invalid-name
def test_FString():
    """Test the FString class."""
    # pylint: enable=invalid-name
    fstr = FString(fstr='a {a}', a='string')
    assert str(fstr) == 'a string'
    fstr = FString('string', fstr='a {a}')
    assert str(fstr) == 'a string'
    fstr = FString(fstr='a {a}')
    assert fstr.render('string') == 'a string'
    assert fstr.render(a='string') == 'a string'
    with pytest.raises(ValueError):
        fstr = FString('arg1', fstr='a {a}', a='kwarg1')
    with pytest.raises(ValueError):
        fstr.render('arg1', a='kwarg1')


# pylint: disable=invalid-name
def test_LString():
    """Test the LString class."""
    # pylint: enable=invalid-name
    # flake8: noqa F821
    # pylint: disable=undefined-variable
    lstr = LString('a', exp=lambda x: f'a {a}')
    assert str(lstr) == 'a a'
