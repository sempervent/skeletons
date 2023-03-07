"""Test the skeletons init."""
import pytest

from skeletons.strings import split_line, FString, LString


def test_split_line():
    """Test that the split_line function behaves."""
    test_txt = "this line will be split"
    expected_txt = "this line \\n"
    actual_txt = split_line(txt=test_txt, nchar=8, flag="be") 
    print(actual_txt)
    assert actual_txt == expected_txt


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
    lstr = LString('a', exp=lambda x: f'a {x}')
    assert str(lstr) == 'a a'
    lstr = LString(exp=lambda x: f'b: {x}', x='b')
    assert str(lstr) == 'b: b'
    lstr = LString(exp=lambda a: f'c: {a}')
    assert lstr.render('a') == 'c: a'
    assert lstr.render(a='b') == 'c: b'
    with pytest.raises(ValueError):
        lstr = LString('arg1', exp=lambda x: '{x=}', x='c')
    with pytest.raises(ValueError):
        lstr.render('arg1', b='b')
    with pytest.raises(TypeError):
        lstr = LString(exp='str')
    with pytest.raises(ValueError):
        lstr = LString('a', 'b', exp=lambda x: '{x}')
