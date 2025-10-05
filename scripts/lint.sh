#!/bin/bash
# Linting script

set -e

echo "Running Ruff linter..."
ruff check apps config metatasks_lib

echo "✓ Linting passed"
