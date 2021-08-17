import glob
import subprocess
import typing
from filecmp import dircmp
from os import getcwd
from os.path import splitext, isdir

import click


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


@click.command()
@click.argument('compare_path', type=click.Path(exists=True))
@click.option('-x', '--extensions', multiple=True, default=['phtml', 'html'],
              help="Extensions to check, default -x phtml -x html")
@click.option('-p', '--project-path', type=click.Path(exists=True))
@click.option('-m', '--merge', help="Perform a 3 way merge", default=False, is_flag=True)
@click.option('-dt', '--diff-theme', help="Diff the theme file to the vendor file (current version)", default=False,
              is_flag=True)
@click.option('-dv', '--diff-vendor', help="Diff the current project and compare project vendor files", default=False,
              is_flag=True)
@click.option('-i', '--interactive', help="Interactive mode, choose action per file", default=False,
              is_flag=True)
def run(compare_path, extensions, project_path=None, merge=False, diff_theme=False, diff_vendor=False,
        interactive=False):
    if project_path is None:
        project_path = getcwd()

    source_dirs = get_vendor_view_dirs(project_path)
    compare_dirs = get_vendor_view_dirs(compare_path)
    common_dirs = merge_dir_lists(source_dirs, compare_dirs)

    diff = diff_dirs(common_dirs, project_path, compare_path)
    vendor_changed = diff_to_file_list(diff)

    design_files = get_app_design_files(project_path, extensions)

    fmt = click.HelpFormatter(width=9999)
    fmt.write_heading("Files to review")
    for line in find_changed_design_files(design_files, vendor_changed):
        if interactive:
            process_file_action(line, project_path, compare_path)
        else:
            if merge:
                run_three_way_merge(line, project_path, compare_path)
            if diff_theme:
                run_theme_diff(line, project_path)
            if diff_vendor:
                run_vendor_diff(line, project_path, compare_path)

        fmt.write_text(line[0])

    click.echo(fmt.getvalue())


def get_app_design_files(project_path, extensions):
    """Get all view files under app/design"""
    search_path = "{}/app/design/**".format(project_path)

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
        result.extend([diff['path'].rstrip('/') + '/' + f for f in diff['files']])

    return result


def find_changed_design_files(design_files, vendor_changed):
    """Get list of all app/design overrides where the vendor file has changed between versions"""
    result = []
    for file in design_files:
        to_vendor = design_path_to_vendor_path(file)
        if to_vendor in vendor_changed:
            result.append((file, to_vendor))

    return result


def design_path_to_vendor_path(path):
    """Convert app/design override path to vendor view path"""
    parts = path.split('/')
    if 'Magento_' in parts[6]:
        parts[6] = parts[6].replace('Magento_', 'module-').lower() + '/view/' + parts[3]
        parts[3] = None

        return '/vendor/magento/' + '/'.join(parts[6:])

    return path


def run_three_way_merge(line, project_path, compare_path):
    """Three way merge between the app/design files, the current version vendor file, and the compare version vendor
    file """
    local = project_path + line[0]
    remote = project_path + line[1]
    base = compare_path + line[1]

    process = subprocess.Popen("bcompare {} {} {}".format(local, remote, base), shell=True, stdout=subprocess.PIPE)
    process.wait()


def run_theme_diff(line, project_path):
    """Diff between the app/design and current version vendor files"""
    local = project_path + line[0]
    remote = project_path + line[1]

    process = subprocess.Popen("bcompare {} {}".format(local, remote), shell=True, stdout=subprocess.PIPE)
    process.wait()


def run_vendor_diff(line, project_path, compare_path):
    """Diff between the current version and compare version vendor files"""
    local = project_path + line[1]
    remote = compare_path + line[1]

    process = subprocess.Popen("bcompare {} {}".format(local, remote), shell=True, stdout=subprocess.PIPE)
    process.wait()


def process_file_action(line, project_path, compare_path):
    action = click.prompt("{}".format(line[0]), type=CustomChoice(['(m)erge', '(d)iff', '(v)endor diff', '(i)gnore']),
                          show_choices=True)

    if action == 'merge':
        run_three_way_merge(line, project_path, compare_path)
    if action == 'diff':
        run_theme_diff(line, project_path)
    if action == 'vendor diff':
        run_vendor_diff(line, project_path, compare_path)


class CustomChoice(click.Choice):
    def convert(
            self, value: typing.Any, param: typing.Optional["Parameter"], ctx: typing.Optional["Context"]
    ) -> typing.Any:
        # Match through normalization and case sensitivity
        # first do token_normalize_func, then lowercase
        # preserve original `value` to produce an accurate message in
        # `self.fail`
        normed_value = value
        normed_choices = {choice: choice for choice in self.choices}

        # check for single character response
        if len(normed_value) == 1:
            for choice in normed_choices:
                if choice[1:2] == normed_value:
                    return choice.replace('(', '').replace(')', '')

        return super().convert(value, param, ctx)


if __name__ == '__main__':
    run()
