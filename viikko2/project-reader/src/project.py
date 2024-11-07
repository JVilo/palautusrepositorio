import textwrap

class Project:
    def __init__(self, name, authors, description, dependencies, dev_dependencies, license):
        self.name = name
        self.description = description
        self.authors: list[str] = authors
        self.dependencies = dependencies
        self.dev_dependencies = dev_dependencies
        self.license = license

    def _stringify_dependencies(self, dependencies):
        return ", ".join(dependencies) if len(dependencies) > 0 else "-"

    def __str__(self):
        # diu = '{:>15}'.format()

        def _list_to_indented_strings(in_list: list[str]):
            return f"{'\n'.join([f'- {x}' for x in in_list])}"
 
        
        fields = [
            f"Name: {self.name}",
            f"Description: {self.description or '-'}",
            f"License: {self.license}",
            f"\nAuthors:",
            _list_to_indented_strings(self.authors),
            f"\nDependencies: ",
            _list_to_indented_strings(self.dependencies),
            f"\nDevelopment dependencies:",
            _list_to_indented_strings(self.dev_dependencies),
        ]

        return '\n'.join(fields)
