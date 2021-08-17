from click.testing import CliRunner
from magediff import run

def test_run(prepared_filesystem):
    runner = CliRunner()
    result = runner.invoke(run, ['--project-path=/project', '/compare'])
    assert result.exit_code == 0
    assert '/app/design/frontend/namespace/default/Magento_Foo/templates/foo.phtml' in result.output
    assert '/app/design/frontend/namespace/default/Magento_Bar/templates/bar.phtml' in result.output
