# Python container runner

An experimental Docker launcher with a small Flask example. It supports an explicit Python entry point and dependency installation from Poetry metadata or a requirements file. It is not an untrusted-code sandbox or an LLM evaluation framework.

## Run the included example

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r dockerproj/requirements.txt
python -m unittest discover -s tests -v
PYTHON_ENTRYPOINT=src/main.py sh dockerproj/scripts/run.sh
```

The example serves `/`, `/json`, `/html` and `/error` on port 8000. Stop it with Ctrl-C. The Flask development server is for local demonstration.

With Docker:

```bash
docker build -t python-container-runner dockerproj
docker run --rm -p 8000:8000 python-container-runner
```

`PYTHON_ENTRYPOINT` is relative to the application directory and defaults to `src/main.py`. A missing entry point fails immediately. The runner does not install packages at application startup. Exit status and termination signals are passed through with `exec`.

## Dependency workflow

The included example uses pinned `requirements.txt`. For a different Poetry application, replace the example requirements with its project files and commit `poetry.lock` before building. `scripts/install.sh` chooses requirements first, otherwise requires an existing Poetry lockfile; it does not silently resolve a new lock during a build.

## Automation and benchmarking roadmap

Implemented: explicit entry-point selection, fail-fast dependency setup, launcher tests and Flask smoke tests.

Planned: container smoke checks, resource/time limits for trusted tasks, structured run artifacts and measured startup overhead. A future evaluation workflow would need task isolation, scheduling, scoring and reporting beyond this launcher.
