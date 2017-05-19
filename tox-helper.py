import subprocess
import sys
rcode = subprocess.call(["autest", "-Dtest_failing"])
rcode2 = subprocess.call(["autest", "-Dtests"])
sys.exit(0 if rcode == 10 and rcode2 == 0 else 1)
