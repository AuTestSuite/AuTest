from __future__ import absolute_import, division, print_function
import subprocess
import sys

print("Testing Failing tests ----------------------")
rcode = subprocess.call(["autest", "-Dtests/failing"])
print("Testing Passing tests ----------------------")
rcode2 = subprocess.call(["autest", "-Dtests/passing"])
print("Testing autest-site loading ----------------------")
rcode3 = subprocess.call(["autest", "-Dtests/site-tests", "--autest-site", "tests/autest-site", "tests/autest-site2"])

sys.exit(0 if rcode == 10 and rcode2 == 0 and rcode3 == 0 else 1)
