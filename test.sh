#!/bin/bash

# reproducibility check
pushd ./packages/github.com/google/snappy
bazel build ...
sha256sum bazel-bin/*.tar > hash1
bazel clean
bazel build ...
sha256sum bazel-bin/*.tar > hash2
bazel clean
diff hash1 hash2 > hash.diff
popd

pushd ./packages/sqlite.org/sqlite
bazel build ...
sha256sum bazel-bin/*.tar > hash1
bazel clean
bazel build ...
sha256sum bazel-bin/*.tar > hash2
bazel clean
diff hash1 hash2 > hash.diff
popd
