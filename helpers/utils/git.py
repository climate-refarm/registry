import git
repo = git.Repo(search_parent_directories=True)


def get_head_commit_sha():
  """https://stackoverflow.com/questions/14989858/get-the-current-git-hash-in-a-python-script"""
  sha = repo.head.object.hexsha
  return sha
