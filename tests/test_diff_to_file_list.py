from magediff import diff_to_file_list


def test_diff_to_file_list():
    diff = [
        {'project': '/project/vendor/magento/module-foo/view/frontend/templates/',
         'compare': '/compare/vendor/magento/module-foo/view/frontend/templates/',
         'path': '/vendor/magento/module-foo/view/frontend/templates/', 'files': ['foo.phtml']},
        {'project': '/project/vendor/magento/module-bar/view/frontend/templates/',
         'compare': '/compare/vendor/magento/module-bar/view/frontend/templates/',
         'path': '/vendor/magento/module-bar/view/frontend/templates/', 'files': ['bar.phtml']}]

    files = diff_to_file_list(diff)

    assert files == [
        '/vendor/magento/module-foo/view/frontend/templates/foo.phtml',
        '/vendor/magento/module-bar/view/frontend/templates/bar.phtml',
    ]
