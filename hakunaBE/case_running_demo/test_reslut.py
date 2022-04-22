
import xml.etree.ElementTree as ET

report = "./xml_result.xml"


tree = ET.parse(report)

# 根节点
root = tree.getroot()

# 标签名
print('root_tag: ', root.tag)

# testsuite = root.get('testsuite')
# print("testsuite: ", root)

print('testsuite: ', root[0].tag, root[0].attrib['name'])

testsuite = root[0]

# testsuite = root.find('testsuite')
# print("testsuite: ", testsuite)

# for suite in root.findall('testsuite'):

# result = {}
name = testsuite.get('name')
tests_count = testsuite.get('tests')
failures = testsuite.get('failures')
errors = testsuite.get('errors')
skipped = testsuite.get('skipped')

print('result: ', name, tests_count, failures, errors, skipped)