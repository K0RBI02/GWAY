# Contributing

Thanks for helping improve GWAY.

## Issues

- **Bugs:** use the bug report template and include the add-on version, router model and firmware, and the relevant add-on log lines.
- **Ideas:** use the feature request template and describe what you want to do, not only how.
- **Security problems:** please do not open a public issue, see [SECURITY.md](SECURITY.md).

## Pull requests

- Create a branch for your change and keep each PR focused on one topic.
- Include screenshots for UI changes (desktop and mobile, light and dark if relevant).
- Never commit router passwords, IP addresses of your own network or probe scripts. Files named `test_*.py`, `probe_*.py` and `debug_*.py` are ignored by git for that reason.

## Releases

Versions follow **major.feature.fix**:

| Change | Example |
|---|---|
| New feature | `0.7.0` → `0.8.0` |
| Bug fix | `0.8.0` → `0.8.1` |
| Major rework or breaking change | `0.8.1` → `1.0.0` |

For every release:

1. Raise `version` in `src/config.yaml`. Home Assistant only offers an update when this number changes.
2. Add a section to `src/CHANGELOG.md` that describes the change from the user's point of view.
3. Update `src/DOCS.md` and `README.md` if options or features changed.
4. Tag the commit as `vX.Y.Z`.

Changes outside `src/` (README, CI, templates) do not need a new version.

## Checks

Every push runs the add-on linter, a Python syntax check, `ruff` and a Docker build. To run the Python checks locally:

```sh
pip install ruff
ruff check src
python -m py_compile src/*.py
```
