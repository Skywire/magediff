from magediff import merge_dir_lists


def test_merge_dir_lists():

    project = [
        '/vendor/foo/dir1/',
        '/vendor/foo/dir2/',
        '/vendor/bar/dir1/',
        '/vendor/bar/dir2/',
    ]

    compare = [
        '/vendor/foo/dir1/',
        '/vendor/baz/dir1/',
        '/vendor/bar/dir1/',
        '/vendor/baz/dir1/',
    ]

    merged = sorted(merge_dir_lists(project, compare))
    assert merged == [
        '/vendor/bar/dir1/',
        '/vendor/foo/dir1/',
    ]