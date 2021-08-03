"""Setup package."""

import os
import re
import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext as _build_ext

# Packages to include in the distribution
packages = find_packages(include=['meme_generator', 'meme_generator.*'])

# Additional data required to install this package
package_data = {}

# Files with that are data out of the package
# data_files=[('my_data', ['data/data_file'])],

# List of dependencies minimally needed by this project to run
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()
    install_requires = [x for x in install_requires if not x.startswith('--')]


# Trove classifiers
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Topic :: Software Development :: Tools',
    'License :: Non OSI Approved :: Copyright',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy'
]

# Keywords to help users find this package on PyPi
keywords = ''

here = os.path.abspath(os.path.dirname(__file__))
meta = {}
readme = ''

# Read version and README files
with open(os.path.join(here, 'meme_generator', '_meta.py'), 'r') as f:
    exec(f.read(), meta)
with open(os.path.join(here, 'README.md'), 'r') as f:
    readme = f.read()

# Cython and build step configuration


def _should_cythonize():
    """Return True if bdist_wheel and '--cythonize' arguments are found."""
    found = all(x in sys.argv for x in ['bdist_wheel', '--cythonize'])
    if found:
        sys.argv.remove('--cythonize')

    return found


should_cythonize = _should_cythonize()


def _try_cythonize(*args, **kwargs):
    """If cython is available, cythonize with the provided parameters."""
    from Cython.Build import cythonize

    return cythonize(*args, **kwargs)


def _packages_to_cythonize(package_names):
    """Convert a list of package names to glob patterns.

    This packages are those returned by setuptools.find_packages().
    """
    return [package.replace('.', '/') + '/*.py' for package in package_names]

# Custom commands/scripts


class build_ext(_build_ext):
    """Custom building of package.

    Custom build_ext command that:

    1. Setups appropriate cython configuration
    2. Fixes compiled builds by adding missing __init__.py files
    """

    init_filename_regex = "^__init__(\\..+)?\\.so$"
    files_to_remove_regex = "^.*\\.(py|c)$"
    files_to_strip_regex = "^.*\\.so$"

    def run(self):
        """Execute building of package.

        This will be called when the bdist_ext step executes.
        """
        # Setup cython compilation options
        if should_cythonize:
            import Cython.Compiler.Options
            Cython.Compiler.Options.docstrings = False
            Cython.Compiler.Options.embed_pos_in_docstring = False
            Cython.Compiler.Options.emit_code_comments = False

        _build_ext.run(self)

        # Traverse the build files to:
        #
        # 1. Remove source files so they are not included on the distribution
        # (only compiled code)
        # 2. Strips compiled files
        # 3. Create empty __init__.py files to make python recognize the
        # packages
        #
        if should_cythonize:
            target_folders = [x[0] for x in os.walk(self.build_lib)][1:]
            for target_folder in target_folders:
                for filename in os.listdir(target_folder):
                    target_file = os.path.join(target_folder, filename)
                    # remove source files
                    if re.match(self.files_to_remove_regex, filename):
                        print('removing %s' % target_file)
                        os.remove(target_file)
                    # strip compiled files
                    if re.match(self.files_to_strip_regex, filename):
                        print('stripping %s' % target_file)
                        # NOTE: this only works on unix-type systems
                        subprocess.call(["strip", target_file])

                # add empty __init__.py's
                if self._folder_is_package(target_folder):
                    target_file = os.path.join(target_folder, '__init__.py')
                    print('creating %s' % target_file)
                    open(target_file, 'a').close()

    def _folder_is_package(self, target_folder):
        """Determine if a folder is a Python package.

        To determine so, look for __init__.py files.
        """
        return any([filename for filename in os.listdir(target_folder)
                    if re.match(self.init_filename_regex, filename)])


setup(
    name=meta['__title__'],
    version=meta['__version__'],
    description=meta['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    url=meta['__url__'],
    author=meta['__author__'],
    author_email=meta['__email__'],
    license=meta['__license__'],
    classifiers=classifiers,
    keywords=keywords,
    platforms=['any'],
    packages=packages,
    install_requires=install_requires,
    package_data=package_data,
    include_package_data=True,
    ext_modules=_try_cythonize(
        _packages_to_cythonize(packages)) if should_cythonize else None,
    python_requires=(">=3, !=3.0.*, !=3.1.*, !=3.2.*, "
                     "!=3.3.*, !=3.4.*, !=3.5.*, <4"),
    cmdclass={
        'build_ext': build_ext
    }
)