def depend(head, dependencies):
    result = []
    for dep in dependencies:
        if dep is not str:
            dep = ' '.join(dep)
        result.append(f'-{head} {dep}')
    return result


def conflict(head, conflicts):
    result = []
    for conf in conflicts:
        result.append(f'-{head} -{conf}')
    return result


def build_cnf(packages: dict, installed):
    index = {}
    for k, v in enumerate(packages, 1):
        index[v] = str(k)

    clauses = []
    for package_name, package in packages.items():
        i = index[package_name]

        if package.get('depends'):
            clauses += depend(i, (
                index[dep] if isinstance(dep, str)
                else (index[alternative] for alternative in dep)
                for dep in package['depends']))

        if package.get('conflicts'):
            clauses += conflict(i, (index[e] for e in package['conflicts']))
    clauses += [index[e] for e in installed]
    return [f'p cnf {len(packages)} {len(clauses)}'] + \
           [e + ' 0' for e in clauses]


def check_structure_satisfiable(packages, install):
    from subprocess import run
    with open('packages.cnf', 'w') as f:
        f.write("\n".join(build_cnf(packages, install)))
    try:
        run(['minisat/minisat', 'packages.cnf', 'result.txt'])
        print('\n' * 1000)
    except:
        print('\n' * 1000)
        print('Не найден файл "minisat\minisat.exe" или папка minisat')
        return None
    try:
        with open('result.txt') as f:
            data = f.read()
        if not data:
            return None
        data = data.split()
        if data[0] != 'SAT':
            return None
        return data[1:-1]
    except:
        return None


def main():
    packages = dict(
        a=dict(depends=["b", "c", "z"], conflicts=[]),
        b=dict(depends=["d"], conflicts=[]),
        c=dict(depends=[["d", "e"], ["f", "g"]], conflicts=[]),
        d=dict(depends=[], conflicts=["e"]),
        e=dict(depends=[], conflicts=[]),
        f=dict(depends=[], conflicts=[]),
        g=dict(depends=[], conflicts=[]),
        y=dict(depends=["z"], conflicts=[]),
        z=dict(depends=[], conflicts=[]),
    )
    install = ["a", "b"]
    result = check_structure_satisfiable(packages, install)

    if not result:
        if len(install):
            print("Модули не могут быть установлены!")
        else:
            print("Система не может быть собрана!")
    else:
        print("Рабочая конфигурация системы: ", end='')
        download = [int(e) for e in result if e[0] != '-']
        if not download:
            print("не содержит пакетов вовсе :)")
        names = list(packages.keys())
        print(', '.join([names[i - 1] for i in download]))


if __name__ == '__main__':
    main()
