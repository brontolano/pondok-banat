#!/bin/bash
echo "=== TSC ==="
npx tsc --noEmit
echo "TSC_EXIT=$?"
echo "=== ESLINT ==="
npm run lint
echo "LINT_EXIT=$?"
echo "=== BUILD ==="
npm run build
echo "BUILD_EXIT=$?"
