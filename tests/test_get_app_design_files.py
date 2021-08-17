from magediff import get_app_design_files


def test_get_app_design_files(prepared_filesystem):
    design = get_app_design_files('/project', ['xml', 'phtml'])

    assert design == [
        '/app/design/frontend/namespace/Magento_Foo/layout/foo.xml',
        '/app/design/frontend/namespace/Magento_Foo/templates/foo.phtml',
        '/app/design/frontend/namespace/Magento_Bar/layout/bar.xml',
        '/app/design/frontend/namespace/Magento_Bar/templates/bar.phtml',
    ]