import os
import glob
from SCons.Environment import Environment
from SCons.Node import Node

class GDExtension:

    def __init__(self, env: Environment):
        self.env: Environment = env.Clone()
        self.lib: Node = None
        self.name: str = ''
        self.sources: str = ''
        self.bin_name: str = ''
        self.bin_path: str = ''
        self.lib_name: str = ''
        self.entry_symbol: str = ''
        self.deployment_path: str = ''
        self.icon_list: list[str] = []


    def build(self, *args: 'GDExtension') -> 'GDExtension':
        self.bin_name = self._create_file_name(self.env['SHLIBSUFFIX'])
        self.lib_name = self._create_file_name(self.env['LIBSUFFIX'])

        self.lib = self.env.SharedLibrary(f'{self.bin_path}{self.bin_name}', self.sources)
        self.env.Default(self.lib)

        for arg in args:
            self.env.Depends(self.lib, f'{arg.bin_path}{arg.lib_name}')

        self._create_cfg()

        return self


    def _create_file_name(self, extension: str) -> str:
        file_name: str = ''

        if self.env['platform'] == 'macos':
            file_name = f'{self.name}.{self.env["platform"]}.{self.env["target"]}.framework/{self.name}.{self.env["platform"]}.{self.env["target"]}'
        else:
            file_name = f'{self.name}{self.env["suffix"]}{extension}'
        
        return file_name


    def _create_cfg(self):
        local_dir = os.path.dirname(os.path.abspath(__file__))

        cfg_template = os.path.join(local_dir, "gdextension.ini")
        with open(cfg_template, "r") as f:
            contents = f.read()
        
        contents = contents.replace('$entry_symbol', self.entry_symbol)
        contents = contents.replace('$bin_name', self.bin_name)
        contents = contents.replace('$bin_path', self.bin_path)

        if len(self.icon_list) != 0:
            contents += f'\n\n[icons]'
            for icon in self.icon_list:
                contents += f'\n{icon}'

        file_name = f'{self.deployment_path}{self.name}.gdextension'

        if not os.path.exists(self.deployment_path):
            os.makedirs(self.deployment_path)
        
        with open(file_name, 'w') as f:
            f.write(contents)


    def add_cpppath(self, cpppath: str) -> 'GDExtension':
        self.env.Append(CPPPATH=cpppath)
        return self
    

    def add_icon(self, class_name: str, icon_path: str) -> 'GDExtension':
        self.icon_list.append(f'{class_name} = "res://{icon_path}"')
        return self


    def add_libpath(self, libpath: str) -> 'GDExtension':
        self.env.Append(LIBPATH=libpath)
        return self


    def add_libs(self, libs: str) -> 'GDExtension':
        self.env.Append(LIBS=[libs])
        return self


    def set_bin_path(self, bin_path: str) -> 'GDExtension':
        self.bin_path = bin_path
        return self


    def set_deployment_path(self, deployment_path: str) -> 'GDExtension':
        self.deployment_path = deployment_path
        return self


    def set_entry_symbol(self, entry_symbol: str) -> 'GDExtension':
        self.entry_symbol = entry_symbol
        return self


    def set_name(self, name: str) -> 'GDExtension':
        self.name = name
        return self


    def set_sources(self, path: str) -> 'GDExtension':
        self.sources = glob.glob(path)
        return self