# Release checklist

## 1. Validate develop

```bash
source .venv/bin/activate

git checkout develop
git pull origin develop

pytest -q
python scripts/fix_github_math_macros.py --check

rm -rf dist build *.egg-info
python -m pip install build twine
python -m build
python -m twine check "dist/*"
```

## 2. TestPyPI dry validation

Run the `TestPyPI` GitHub Actions workflow manually with:

```text
publish = false
```

This only builds and validates the distributions.

## 3. Configure TestPyPI Trusted Publisher

Create a TestPyPI account if needed.

Configure a pending Trusted Publisher using:

```text
Project name: relationalstats
Owner: HubertRonald
Repository: relationalstats
Workflow file: test-pypi.yml
Environment: testpypi
```

## 4. Publish to TestPyPI

Run the `TestPyPI` workflow manually with:

```text
publish = true
```

## 5. Test installation from TestPyPI

```bash
python3.10 -m venv /tmp/relationalstats-testpypi
source /tmp/relationalstats-testpypi/bin/activate

python -m pip install --upgrade pip
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ relationalstats==0.1.0a1

python - <<'PY'
import relationalstats
print(relationalstats.__version__)
PY
```

## 6. Create release branch

```bash
source .venv/bin/activate

git checkout develop
git pull origin develop
git checkout -b release/v0.1.0a1
git push -u origin release/v0.1.0a1
```

Open a PR:

```text
release/v0.1.0a1 -> main
```

## 7. Configure PyPI Trusted Publisher

Configure a pending Trusted Publisher using:

```text
Project name: relationalstats
Owner: HubertRonald
Repository: relationalstats
Workflow file: release.yml
Environment: pypi
```

Require manual approval for the `pypi` environment.

## 8. Merge release branch to main

After checks pass, merge the release PR into `main`.

## 9. Tag release from main

```bash
source .venv/bin/activate

git checkout main
git pull origin main

pytest -q

git tag v0.1.0a1
git push origin v0.1.0a1
```

The tag should trigger the `Release` workflow and publish to PyPI.
