import os
import sys


tests_root = Test.TestRoot
tests_dir = os.path.dirname(tests_root)
autest_site = os.path.join(tests_dir, "autest-site")
autest_site2 = os.path.join(tests_dir, "autest-site2")

t = Test.AddTestRun("List tests with custom YAML format")
t.Processes.Default.Command = (
    f'"{sys.executable}" -m autest list -D "{tests_root}" --autest-site "{autest_site}" "{autest_site2}" --json'
)
t.Processes.Default.ReturnCode = 0
t.Processes.Default.Streams.stdout += Testers.ContainsExpression(
    '"name": "custom-format"',
    "The custom .test.yaml file should be discovered")
t.Processes.Default.Streams.stdout += Testers.ContainsExpression(
    '"description": "Custom YAML test format works"',
    "The custom .test.yaml summary should be reported by autest list")
t.Processes.Default.Streams.stdout += Testers.ExcludesExpression(
    'ignored\\.yaml',
    "Plain .yaml files should not be discovered as tests")
