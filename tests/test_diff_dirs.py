from magediff import diff_dirs


def test_diff_dirs(prepared_filesystem):
    diffs = diff_dirs(
        [
            '/vendor/magento/module-foo/view/frontend/layout/',
            '/vendor/magento/module-foo/view/frontend/templates/',
            '/vendor/magento/module-bar/view/frontend/layout/',
            '/vendor/magento/module-bar/view/frontend/templates/',
        ],
        '/project',
        '/compare'
    )

    assert len(diffs) == 2
    assert diffs == [
        {'project': '/project/vendor/magento/module-foo/view/frontend/templates/',
         'compare': '/compare/vendor/magento/module-foo/view/frontend/templates/',
         'path': '/vendor/magento/module-foo/view/frontend/templates/', 'files': ['foo.phtml']},
        {'project': '/project/vendor/magento/module-bar/view/frontend/templates/',
         'compare': '/compare/vendor/magento/module-bar/view/frontend/templates/',
         'path': '/vendor/magento/module-bar/view/frontend/templates/', 'files': ['bar.phtml']}]
