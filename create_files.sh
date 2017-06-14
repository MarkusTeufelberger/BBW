#!/bin/bash

python ./tools/internal/workspacegen/workspacegen.py packages
python ./tools/internal/buildfilegen/buildfilegen.py packages