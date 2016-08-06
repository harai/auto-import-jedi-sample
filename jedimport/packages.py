import multiprocessing
import pkgutil
from concurrent.futures import ThreadPoolExecutor
from pprint import PrettyPrinter

from jedimport import util

# from pudb import set_trace

pp = PrettyPrinter(indent=3)


def shallow_scan_by_list(pkgs):
  return sum((shallow_scan(pkg) for pkg in pkgs), [])


def shallow_scan(pkg):
  fs = None if pkg.fs_path is None else [pkg.fs_path]
  return list(
      Package(
          finder.path if pkg.fs_base is None else pkg.fs_base, name.split('.'))
      for finder, name, is_pkg in pkgutil.iter_modules(fs, pkg.prefix)
      if is_pkg)


def make_fs_path(base, path):
  if base is None:
    return None
  if len(path) == 0:
    return base
  return '{}/{}'.format(base, '/'.join(path))


class Package:

  def __init__(self, fs_base, pkg_path):
    self._fs_base = fs_base
    self._pkg_path = pkg_path
    fs_path = make_fs_path(fs_base, pkg_path)
    if fs_path is None:
      self._modules = []
    else:
      self._modules = list(
          name for _, name, _ in pkgutil.iter_modules([fs_path]))

  @property
  def fs_base(self):
    return self._fs_base

  @property
  def fs_path(self):
    return make_fs_path(self._fs_base, self._pkg_path)

  @property
  def pkg_path(self):
    return self._pkg_path

  @property
  def modules(self):
    return self._modules

  def full_modules(self):
    return list((self._pkg_path + [n]) for n in self._modules)

  @property
  def prefix(self):
    if len(self._pkg_path) == 0:
      return ''
    return '.'.join(self._pkg_path) + '.'

  def pack(self):
    return {
        'fs_base': self._fs_base,
        'pkg_path': self._pkg_path,
        'modules': self._modules
    }

  @classmethod
  def root_package(cls):
    return cls(None, [])


def deep_scan():

  def submit_pkgs(executor, pkgs, mp_ctx):
    return list(
        executor.submit(util.isolated(shallow_scan_by_list, ps, mp_ctx))
        for ps in util.chunks(pkgs, 50))

  def yield_pkgs(executor, fs, mp_ctx):
    next_fs = []

    for f in fs:
      new_pkgs = f.result()
      next_fs += submit_pkgs(executor, new_pkgs, mp_ctx)
      for new_pkg in new_pkgs:
        yield new_pkg
    if len(next_fs) != 0:
      yield from yield_pkgs(executor, next_fs, mp_ctx)

  def _do():
    mp_ctx = multiprocessing.get_context('spawn')
    with ThreadPoolExecutor(max_workers=4) as executor:
      yield from yield_pkgs(
          executor, submit_pkgs(executor, [Package.root_package()], mp_ctx),
          mp_ctx)

  yield from _do()
