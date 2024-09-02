import sys
sys.path.append("./lib/python3.5/site-packages/")
import iniparser2

ini_path = "./test.ini"

parser = iniparser2.INI('=')

parser.read_file(ini_path)

print(parser)

# {'common': {'name': 'aaa'}, 'test': {'port': '2', 'ip': '1'}}

