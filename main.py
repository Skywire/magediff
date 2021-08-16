import glob
from filecmp import dircmp
from os import getcwd
from os.path import splitext, isdir

import click


@click.command()
@click.argument('compare_path', type=click.Path(exists=True))
@click.option('-p','--project-path', type=click.Path(exists=True))
def run(compare_path, project_path=None):

    if project_path is None:
        project_path = getcwd()

    source_dirs = get_vendor_view_dirs(project_path)
    compare_dirs = get_vendor_view_dirs(compare_path)
    common_dirs = merge_dir_lists(source_dirs, compare_dirs)

    diff = diff_dirs(common_dirs, project_path, compare_path)
    vendor_changed = diff_to_file_list(diff)

    design_files = get_app_design_files(project_path)

    fmt = click.HelpFormatter(width=9999)
    fmt.write_heading("Files to review")
    for line in find_changed_design_files(design_files, vendor_changed):
        fmt.write_text(line)

    click.echo(fmt.getvalue())


def get_vendor_view_dirs(path) -> list:
    """Get all view directories under the vendor directory """
    search_path = "{}/vendor/magento/module-*/view/**".format(path)
    paths = glob.glob(search_path, recursive=True)

    return [p.replace(path, '') for p in paths if isdir(p)]


def diff_dirs(common_dirs, project_path, compare_path):
    """Diff directories and return list of dicts containing dir and changed file names"""
    project_dirs = [project_path + p for p in common_dirs]
    compare_dirs = [compare_path + p for p in common_dirs]
    result = []

    to_compare = list(zip(project_dirs, compare_dirs))

    for pair in to_compare:
        diff = dircmp(pair[0], pair[1])
        if (len(diff.diff_files)):
            result.append({
                "project": diff.left,
                "compare": diff.right,
                "path": diff.left.replace(project_path, ''),
                "files": diff.diff_files})

    return result


def merge_dir_lists(source_dirs, compare_dirs):
    """Return list of directories that appear in both lists"""
    return list(set(source_dirs).intersection(compare_dirs))


def get_app_design_files(project_path):
    """Get all view files under app/design"""
    search_path = "{}/app/design/**".format(project_path)
    extensions = ['xml', 'phtml', 'js', 'html']
    paths = glob.glob(search_path, recursive=True)

    return [p.replace(project_path, '') for p in paths if get_extension(p) in extensions]


def get_extension(filename) -> str:
    return splitext(filename)[1][1:]


def diff_to_file_list(vendor_diff):
    """
    Take the result of the diff function and create a single list of files paths, relative to project root
    """

    result = []

    for diff in vendor_diff:
        result.extend([diff['path'] + '/' + f for f in diff['files']])

    return result


def find_changed_design_files(design_files, vendor_changed):
    """Get list of all app/design overrides where the vendor file has changed between versions"""
    result = []
    for file in design_files:
        to_vendor = design_path_to_vendor_path(file)
        if to_vendor in vendor_changed:
            result.append(file)

    return result


def design_path_to_vendor_path(path):
    """Convert app/design override path to vendor view path"""
    parts = path.split('/')
    if 'Magento_' in parts[6]:
        parts[6] = parts[6].replace('Magento_', 'module-').lower() + '/view/' + parts[3]
        parts[3] = None

        return '/vendor/magento/' + '/'.join(parts[6:])

    return path


if __name__ == '__main__':
    run()
