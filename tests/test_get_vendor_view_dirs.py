from magediff import get_vendor_view_dirs


def test_get_vendor_view_dirs(prepare_filesystem):
    dirs = get_vendor_view_dirs('/project')

    assert (dirs == ['/vendor/magento/module-foo/view/',
                     '/vendor/magento/module-foo/view/frontend',
                     '/vendor/magento/module-foo/view/frontend/layout',
                     '/vendor/magento/module-foo/view/frontend/templates',
                     '/vendor/magento/module-bar/view/',
                     '/vendor/magento/module-bar/view/frontend',
                     '/vendor/magento/module-bar/view/frontend/layout',
                     '/vendor/magento/module-bar/view/frontend/templates']
            )
