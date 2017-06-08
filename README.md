Some small tests for dealing with Bazel

# workspacegen.py

Reads yaml files that contain minimal information about code releases in git repositories and generates WORKSPACE files with proper rules in place.
This makes it less verbose than writing these rules by hand and also automatically creates sha256 hashes for example.

Written in Python 3.6+, f-strings are awesome!

Snappy was chosen since it is relatively self containes, has relatively few commits, yet is still horrible to build (thanks to autotools!).

The Vagrantfile installs Bazel and the necessary tools to build the generated snappy.WORKSPACE.


All of the content here is subject to change, this is more of a public backup.
The lack of a license is intentional to discourage people from building upon this.
