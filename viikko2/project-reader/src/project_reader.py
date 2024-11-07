from urllib import request
from project import Project
import toml


class ProjectReader:
    def __init__(self, url):
        self._url = url

    def get_project(self):
        # tiedoston merkkijonomuotoinen sisältö
        content = request.urlopen(self._url).read().decode("utf-8")
        #print(content)
        content = toml.loads(content,_dict=dict)
        

        test_name = content['tool']['poetry']['name']
        description = content['tool']['poetry']['description']
        dependencies = content['tool']['poetry']['dependencies']
        dependencies = dependencies.keys()
        dev_dependencies = content['tool']['poetry']['group']['dev']['dependencies']
        #print(dev_dependencies)
        dev_dependencies = dev_dependencies.keys()
        authors = content['tool']['poetry']['authors']
        license = content['tool']['poetry']['license']
    
        # deserialisoi TOML-formaatissa oleva merkkijono ja muodosta Project-olio sen tietojen perusteella
        return Project(test_name, authors, description, dependencies, dev_dependencies, license)
