from importlib.util import spec_from_file_location, module_from_spec
from setuptools import setup, find_namespace_packages

spec = spec_from_file_location("version", "src/fuckbot/version.py")
mod = module_from_spec(spec)
spec.loader.exec_module(mod)

setup(
    name = "fuckbot",
    version = mod.VERSION,

    package_dir = {"":"src"},
    packages = ["fuckbot"],

    entry_points = {"console_scripts": ["fuckbot = fuckbot.main:main"]},

    install_requires = ['discord.py', 'feedparser', 'pynacl', 'tabulate', 'youtube-dl'],

    author = mod.AUTHOR,
    author_email = mod.AUTHOR_EMAIL,
    description = mod.DESCRIPTION,
    license = mod.LICENSE_SHORT_ID,
    url = mod.URL
)
