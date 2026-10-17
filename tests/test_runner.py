import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('example_app', ROOT/'dockerproj/src/main.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class FlaskSmokeTests(unittest.TestCase):
    def test_json_contract(self):
        response = module.app.test_client().get('/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertEqual(response.json['data']['numbers'], [1, 2, 3, 4, 5])

    def test_error_route_reports_error(self):
        self.assertEqual(module.app.test_client().get('/error').status_code, 500)

class LauncherTests(unittest.TestCase):
    def test_missing_entrypoint_fails_before_python(self):
        result = subprocess.run(['sh', str(ROOT/'dockerproj/scripts/run.sh')], env=dict(os.environ, PYTHON_ENTRYPOINT='does-not-exist.py'), text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('entry point not found', result.stderr)

    def test_exit_status_is_forwarded_from_any_working_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory)/'example task.py'
            script.write_text('raise SystemExit(23)')
            result = subprocess.run(['sh', str(ROOT/'dockerproj/scripts/run.sh')], cwd=directory, env=dict(os.environ, PYTHON_ENTRYPOINT=str(script)), capture_output=True)
            self.assertEqual(result.returncode, 23)
