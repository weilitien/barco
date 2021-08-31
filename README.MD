Barco Warranty WebUI Test & API Test
=======

## Installation
1. Clone this
2. Setup one virtualenv for your env based on python 3 and activate it
  $ virtualenv -p python3 .barco-env
  $ . .barco-env/bin/activate
3. run setup.py to install all required dependencies.
  (.barco-env)$ python setup.py develop

## Execution
1. To execute all testcases under tests/:
  pytest tests/
2. To execute testcases under tests:
  pytest tests/test_web_ui.py
3. To execute testcases in single test class:
  pytest [path of testcase file]::[test class name]
4. To execute single testcases in a test class:
  pytest [path of testcase file]::[test class name]::[testccase name]
5. Check the report file in ./reports