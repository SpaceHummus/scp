# import os

# print (os.popen(cmd).read())

import subprocess

cmd ="git describe --tags"

p = subprocess.Popen(cmd.split(),
                     stdout=subprocess.PIPE)
preprocessed, _ = p.communicate()

print(preprocessed.strip())