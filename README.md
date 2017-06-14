Some small tests for dealing with Bazel

# workspacegen.py

Reads yaml files that contain minimal information about code releases in git repositories and generates WORKSPACE files with proper rules in place.
This makes it less verbose than writing these rules by hand and it also can automatically create missing sha256 hashes for example.

Written in Python 3.6+, f-strings are awesome!

Run it:
````
python ./tools/internal/workspacegen/workspacegen.py packages
````

# buildfilegen.py

Generates a BUILD file for each yml file, to make sure that all targets defined in there are actually built.

Run it:
````
python ./tools/internal/buildfilegen/buildfilegen.py packages
````


Snappy was chosen since it is relatively self contained, has relatively few commits, yet is still horrible to build (thanks to autotools!).

The Vagrantfile installs Bazel and the necessary tools to build the generated snappy.WORKSPACE.

# Tips and Tricks

git clone a repo and check with git show-ref --tags which commits have which tag to get a quick overview of releases.



All of the content here is subject to change, this is more of a public backup.
The lack of a license is intentional to discourage people from building upon this.

Until this is actually developed a bit further, commits are expected to be more of http://whatthecommit.com/ quality.