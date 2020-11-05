from xml.etree import ElementTree
from urllib.request import urlopen
import io
import zipfile


#Загрузка
def get_link(package_name, simple_index ='https://pypi.org/simple/%s/'):
    with urlopen(simple_index % package_name) as f:
        tree = ElementTree.parse(f)
    list = [a.attrib['href'] for a in tree.iter('a') if a.text.endswith(".whl")]
    if list:
        return list[-1] #возвращает ссылку для скачивания
    else:
        return


def load(url):
    with urlopen(url) as f:
        data = f.read()
    return data


#Установка связей
def get_deps(package_name):
    link = get_link(package_name)
    if not link:
        return
    file = load(link)
    iof = io.BytesIO(file)
    zf = zipfile.ZipFile(iof)
    metadata = [x for x in zf.namelist() if "METADATA" in x]
    with zf.open(metadata[0]) as f:
        meta = f.read().decode("utf-8")
    dep = []
    for i in meta.split("\n"):
        i = i.replace(";", " ").split()
        if not i:
            break
        if i[0] == "Requires-Dist:" and "extra" not in i:
            dep.append(i[1])
    if dep:
        deps[package_name] = dep
    for i in range(len(dep)):
        get_deps(dep[i])
    return dep


#Создание графа
def graph(deps):
    graph = 'digraph G { \n'
    for i in deps.keys():
        for j in range(len(deps[i])):
            graph += '\t"' + i + '"->"' + deps[i][j] + '";\n'
    graph += "}"
    print(graph)


deps = {}


def main():
    package_name = (input("Введите название пакета: ")).lower()
    get_deps(package_name)
    graph(deps)



if __name__ == '__main__':
    main()
