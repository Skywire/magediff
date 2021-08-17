import pytest
from pyfakefs.fake_filesystem import FakeFilesystem


@pytest.fixture
def prepare_filesystem(fs: FakeFilesystem):
    files = [
        '/project/vendor/magento/module-foo/view/frontend/layout/foo.xml',
        '/project/vendor/magento/module-foo/view/frontend/layout/bar.xml',
        '/project/vendor/magento/module-foo/view/frontend/templates/foo.phtml',
        '/project/vendor/magento/module-foo/view/frontend/templates/bar.phtml',
        '/project/vendor/magento/module-bar/view/frontend/layout/foo.xml',
        '/project/vendor/magento/module-bar/view/frontend/layout/bar.xml',
        '/project/vendor/magento/module-bar/view/frontend/templates/foo.phtml',
        '/project/vendor/magento/module-bar/view/frontend/templates/bar.phtml',

        '/compare/vendor/magento/module-foo/view/frontend/layout/foo.xml',
        '/compare/vendor/magento/module-foo/view/frontend/layout/bar.xml',
        '/compare/vendor/magento/module-foo/view/frontend/templates/foo.phtml',
        '/compare/vendor/magento/module-foo/view/frontend/templates/bar.phtml',
        '/compare/vendor/magento/module-bar/view/frontend/layout/foo.xml',
        '/compare/vendor/magento/module-bar/view/frontend/layout/bar.xml',
        '/compare/vendor/magento/module-bar/view/frontend/templates/foo.phtml',
        '/compare/vendor/magento/module-bar/view/frontend/templates/bar.phtml',
    ]

    changed = [
        '/compare/vendor/magento/module-foo/view/frontend/templates/foo.phtml',
        '/compare/vendor/magento/module-bar/view/frontend/templates/bar.phtml',
    ]

    for file in files:
        contents = 'Lorem Ipsum'
        if file in changed:
            contents = 'Lorem Ipsum dolor sit amet'
        fs.create_file(file, contents=contents)
