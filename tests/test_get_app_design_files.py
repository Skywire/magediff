from magediff import get_app_design_files


def test_get_app_design_files(prepared_filesystem):
    design = get_app_design_files('/project', ['xml', 'phtml'])

    assert design == [
        '/app/design/frontend/namespace/default/Magento_Foo/layout/foo.xml',
        '/app/design/frontend/namespace/default/Magento_Foo/templates/foo.phtml',
        '/app/design/frontend/namespace/default/Magento_Bar/layout/bar.xml',
        '/app/design/frontend/namespace/default/Magento_Bar/templates/bar.phtml',
    ]