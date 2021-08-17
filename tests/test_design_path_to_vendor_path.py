from magediff import design_path_to_vendor_path


def test_design_path_to_vendor_path():
    assert design_path_to_vendor_path('/app/design/frontend/namespace/default/Magento_Foo/layout/foo.xml') == '/vendor/magento/module-foo/view/frontend/layout/foo.xml'
    assert design_path_to_vendor_path('/app/design/frontend/namespace/default/Magento_Foo/templates/foo.phtml') == '/vendor/magento/module-foo/view/frontend/templates/foo.phtml'
