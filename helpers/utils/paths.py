import os


def top_folder(rel='') -> str:
  """Returns the path to the top of `registry`."""
  return os.path.join(os.path.abspath(os.path.join(os.path.realpath(__file__), "../../../")), rel)


def ledger_folder(rel='') -> str:
  """Returns a path relative to the `ledger` folder."""
  return os.path.join(top_folder('ledger'), rel)


def projects_folder(rel='') -> str:
  """Returns a path relative to the `projects` folder."""
  return os.path.join(top_folder('projects'), rel)
