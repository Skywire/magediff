import pytest
from magediff import get_extension

def test_get_extension():
    assert get_extension('thisisafile.xml') == 'xml'
    assert get_extension('thisisafile.phtml') == 'phtml'
    assert get_extension('thisisafile.js') == 'js'
    assert get_extension('thisisafile.html') == 'html'
