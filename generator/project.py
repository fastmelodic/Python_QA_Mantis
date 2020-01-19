import os
from model.project import Project
import jsonpickle
import random
import string
import getopt
import sys

try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of projects", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

n = 5
f = 'data/projects.json'

for o, a in opts:
    if o == "-n":
        n = int(a)
    elif o == "-f":
        f = a


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " "#*10 + string.punctuation
    return prefix + "".join(random.choice(symbols) for x in range(random.randrange(maxlen)))

status_opt = ['development','release', 'stable', 'obsolete']
view_status_opt = ['private','public']

testdata = [
    Project(name = random_string("test_name", 7), desc= random_string("test_disc", 10), status = random.choice(status_opt), view_status = random.choice(view_status_opt))
    for i in range(n)
]

file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)

with open(file, "w") as f:
    jsonpickle.set_encoder_options("json", indent = 2)
    f.write(jsonpickle.dumps(testdata))
