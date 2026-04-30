def test_import_package():
    import pyside6_widgets
    assert pyside6_widgets is not None


def test_public_imports():
    from pyside6_widgets import NumericLineEdit
    assert NumericLineEdit is not None