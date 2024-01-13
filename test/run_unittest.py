import os
import sys
import unittest

sys.path[0:0] = ['.']

def main():
    if not os.path.isdir("test"):
        print("Please run this script from the root of the repository.")
        sys.exit(1)
    else:
        tests = unittest.TestLoader().discover('test', 'test*.py', 'test')
        result = unittest.TextTestRunner(verbosity=2).run(tests)
        sys.exit(not result.wasSuccessful())

if __name__ == '__main__':
    main()
