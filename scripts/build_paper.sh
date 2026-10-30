#!/usr/bin/env bash
set -euo pipefail
repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"
plot_python=${PLOT_PYTHON:-"$repo_root/.venv/bin/python"}
if [[ ! -x "$plot_python" ]]; then
  printf '%s\n' 'Create .venv and install requirements-plots.txt before building.' >&2
  exit 1
fi
"$plot_python" scripts/plot_task_results.py
"$plot_python" scripts/plot_simulation_results.py
"$plot_python" scripts/generate_task_training_table.py
if [[ -d /Library/TeX/texbin ]]; then
  export PATH="/Library/TeX/texbin:$PATH"
fi
command -v latexmk >/dev/null || { printf '%s\n' 'latexmk is required.' >&2; exit 1; }
mkdir -p output/pdf
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
  -outdir=output/pdf iclr2027_conference.tex > output/pdf/compile.stdout.log 2>&1
if grep -Eq 'occurred inside a group|undefined references|undefined citations|Fatal error' \
    output/pdf/iclr2027_conference.log; then
  printf '%s\n' 'Unresolved LaTeX diagnostics; inspect output/pdf/iclr2027_conference.log.' >&2
  exit 1
fi
printf '%s\n' 'Built output/pdf/iclr2027_conference.pdf'
