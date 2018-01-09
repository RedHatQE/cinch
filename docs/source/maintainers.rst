Maintainers
===========

cinch contains automation to aid in the process of creating releases on GitHub
and PyPI, driven by Travis CI.

Release Procedure
-----------------

As a maintainer, to create a release of cinch, follow this checklist:

* Ensure version has been bumped in **setup.py**, following `Semantic
  Versioning <https://semver.org/>`_ guidelines
* Ensure significant changes are listed in the **CHANGELOG**
* Merge desired changes, including the above checklist items to the **master**
  branch
* The release is based on git tags, and the following steps can be followed to
  tag the release, given that the upstream remote in your git config is named
  **upstream** (adjust git remote and version number as necessary):

``git fetch upstream master``

``git merge upstream/master``

``git tag v0.9.0``

``git push --tags upstream master``

* It will take about fifteen minutes or so for the automation to add the
  release to PyPI, and while you wait, manually copy the release notes from the
  **CHANGELOG** to the GitHub releases page.  This step is something that could
  possibly be automated in the future.
