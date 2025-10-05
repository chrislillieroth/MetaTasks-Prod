#!/bin/bash
# Code formatter script

set -e

echo "Formatting code with Ruff..."
ruff check --fix apps config metatasks_lib
ruff format apps config metatasks_lib

echo "✓ Code formatted"
