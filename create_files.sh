#!/bin/bash

#python ./tools/internal/workspacegen/workspacegen.py packages
#python ./tools/internal/buildfilegen/buildfilegen.py packages

python ./tools/internal/buildozerfilegen/buildozerfilegen.py packages
# generate WORKSPACE files
# run bash -c to expand the {} inside the $().
find ./packages -name buildozerfile -exec bash -c './tools/buildozer/buildozer -f {} </dev/null >$(dirname {})/WORKSPACE' \;
find ./packages -name buildozertestfile -exec bash -c './tools/buildozer/buildozer -f {} </dev/null >$(dirname {})/BUILD' \;