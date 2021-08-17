from magediff import find_changed_design_files


def test_find_changed_design_files():
    design = [
        '/app/design/frontend/namespace/default/Magento_Foo/templates/foo.phtml',
        '/app/design/frontend/namespace/default/Magento_Bar/templates/bar.phtml',
        '/app/design/frontend/namespace/default/Magento_Baz/templates/baz.phtml',
    ]
    vendor = [
        '/vendor/magento/module-foo/view/frontend/templates/foo.phtml',
        '/vendor/magento/module-bar/view/frontend/templates/bar.phtml'
    ]

    changed = find_changed_design_files(design, vendor)
    assert changed == [
        ('/app/design/frontend/namespace/default/Magento_Foo/templates/foo.phtml',
         '/vendor/magento/module-foo/view/frontend/templates/foo.phtml'),
        ('/app/design/frontend/namespace/default/Magento_Bar/templates/bar.phtml',
         '/vendor/magento/module-bar/view/frontend/templates/bar.phtml')
    ]
