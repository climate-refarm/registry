import sys
sys.path.extend([".", "..", "../.."])
import helpers.validation.checks as checks


def test_check_all_projects_have_unique_ids():
  checks.check_all_projects_have_unique_ids()


def test_check_all_projects_have_monitoring():
  checks.check_all_projects_have_monitoring()


def test_check_all_projects_have_docs():
  checks.check_all_projects_have_docs()


def test_check_all_projects_have_valid_monitoring():
  checks.check_all_projects_have_valid_monitoring()
