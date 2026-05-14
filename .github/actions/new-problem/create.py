import json
import os
import re
import subprocess

os.chdir(os.environ.get('GITHUB_WORKSPACE'))

prob_names = os.environ.get('PROBLEMNAME', '').split()


for name in prob_names :
    with open('.problems.json', 'r', encoding='utf8') as f:
        problems = json.load(f)

    with open('Makefile', 'r', encoding='utf8') as f:
        makefile = f.read()

    with open('README.md', 'r', encoding='utf8') as f:
        readme = f.read()

    with open('_config.yml', 'r', encoding='utf8') as f:
        jekyll_config = f.read()

    label = name
    path = '{}'.format(label)
    if not os.path.exists(path):
        subprocess.run(['tps', 'init', path, '-T', 'tps-task-templates', '-t', 'default'])

        with open('{}/problem.json'.format(path), 'r', encoding='utf8') as f:
            data = json.load(f)
        data['name'] = label
        data['code'] = label
        with open('{}/problem.json'.format(path), 'w', encoding='utf8') as f:
            f.write(json.dumps(data, indent='\t', ensure_ascii=False))
            f.write('\n')

        subprocess.run(['git', 'add', path])

        problems.append(label)

        makefile = makefile.replace('# NEWPROBLEM', 'import-{0}:\n\tcmsImportTask ./{0}/ -u $(if $(s), , --no-statement)\n\n# NEWPROBLEM'.format(path))


        jekyll_config = jekyll_config.replace('# NEWPROBLEM', '  - {0}/scripts/\n  - {0}/tests/\n# NEWPROBLEM'.format(label))
    else:
        print('{} is exists'.format(path))

with open('.problems.json', 'w', encoding='utf8') as f:
    json.dump(problems, f)

with open('Makefile', 'w', encoding='utf8') as f:
    f.write(makefile)

with open('README.md', 'w', encoding='utf8') as f:
    f.write(readme)

with open('_config.yml', 'w', encoding='utf8') as f:
    f.write(jekyll_config)
