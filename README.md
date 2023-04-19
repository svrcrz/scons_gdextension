## scons_gdextension

**scons_gdextension** is a simple python script that provides a builder class for creating and deploying [GDExtensions](https://docs.godotengine.org/en/stable/tutorials/scripting/gdextension/what_is_gdextension.html) for the **Godot Engine** using the **SCons** build system.
This script contains a `GDExtension` class that takes care of building shared libraries and creating .gdextension files.

The purpose of this script began as a side-project of mine attempting to learn about both GDExtension and SCons/python, so it is far from perfect. It is intended to speed up the process of setting up and modifying your SConstruct file for Godot projects. 


### TODOs
- Linux and MacOs support
- Adding pre- and post- actions to gdextension builds
- ...


### Usage
First we pull the `SCons.Environment` object from [godot-cpp](https://github.com/godotengine/godot-cpp):
```python
env = SConscript('godot-cpp/SConstruct')
```

To build our GDExtension, we simply:
```python
gde_example: GDExtension = GDExtension(env)\        # Create our GDExtension object
    .set_name('gde_example')\                       # Set its name
    .add_cpppath('path/to/include/')\               # Add to its include path
    .set_sources('path/to/src/*.cpp')\              # Set its sources
    .set_bin_path('path/to/bin/')\                  # Set the path where our shared library (.dll, .so) will be compiled
    .set_entry_symbol('gde_example_library_init')\  # Set the entry symbol needed for our .gdextension file
    .set_deployment_path('path/to/deploy/')\        # Set the path to deploy our .gdextension file
    .build()                                        # Queue it to build
```

In the case that you have two extensions, A and B, and B depends on A, you can link it this way:
```python
gde_a: GDExtension = GDExtension(env)\
    .set_name('gde_a')\
    .add_cpppath('path/to/include/')\
    .set_sources('path/to/src/*.cpp')\
    .set_bin_path('path/to/bin/')\
    .set_entry_symbol('gde_a_library_init')\
    .set_deployment_path('path/to/deploy/')\
    .build()

gde_b: GDExtension = GDExtension(env)\
    .set_name('gde_b')\
    .add_cpppath('path/to/include/')\
    .add_cpppath(gde_a.env['CPPPATH'][1])\        # Add gde_a include path
    .add_libpath(gde_a.bin_path)\                 # Add gde_a bin_path to lib_path (to find .lib)
    .add_libs(gde_a.lib_name)\                    # Add gde_a lib_name to libs
    .set_sources('path/to/src/*.cpp')\
    .set_bin_path('path/to/bin/')\
    .set_entry_symbol('gde_b_library_init')\
    .set_deployment_path('path/to/deploy/')\
    .build(gde_a)                                 # Add gde_a GDExtension to mark it as dependency
```
**Attention!** You may get unresolved external symbol errors if you do not add `GDE_EXPORT` to the methods you are using between extensions.
