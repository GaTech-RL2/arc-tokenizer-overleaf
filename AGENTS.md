# Local paper workflow

Run `bash scripts/build_paper.sh` to regenerate the plots and compile this
multi-file LaTeX project. It uses the task-local `.venv`, not the bundled
runtime, which lacked Matplotlib on 2026-10-05. Install `requirements-plots.txt`
into `.venv` if that environment is missing. The build also checks for
unresolved citations, references, and LaTeX group warnings.

The four-task values in `data/task_results.csv` are explicitly authorized
placeholders. Keep that status visible in both the figure and paper caption
until real evaluation data are supplied. Do not infer performance conclusions,
confidence intervals, or trial counts from these numbers.

The single-task/multi-task table uses `data/task_training_results.csv` and
`scripts/generate_task_training_table.py`. Preserve both training scopes for
all four tasks, with Baseline and ARC under BC and co-training (32 scores).
The generated LaTeX table under `sections/generated/` is rebuilt from the CSV;
edit the CSV rather than hand-editing scores in the table. Keep placeholder
status explicit until measured data are supplied.

The simulation design in `data/simulation_results.csv` is user-specified:
Pusher and Grabber, BC and co-training, Baseline and ARC, and in-domain and
generalization cases. Preserve every one of the 16 combinations. The plot
generator rejects missing or duplicate cells. Simulation numbers remain
authorized placeholders and must stay visibly labeled until measured data
are supplied. Simulator details and generalization split definitions are
pending; do not invent them.

The paper is split into one file per section under `sections/`
(`abstract`, `introduction`, `related_work`, `method`, `experiments`,
`conclusion`, `statements`, `appendix`), each pulled in by `\input` from
`iclr2027_conference.tex`; keep new sections in their own file. The
single-task/multi-task table belongs in `method.tex`; the real-world and
simulation figures belong in `experiments.tex`. Red `\todo{...}` notes mark
unwritten text and must all be removed before submission. Floats are held
inside their section by `placeins`; keep that shared guard rather than
patching individual page breaks. `\notationheading` remains defined for any
notation table reintroduced later.

Use a bounded listing to resolve rendered page filenames before visual QA.
Poppler zero-pads page numbers when a PDF reaches 10 pages (for example,
`page-01.png`), so do not assume a `page-1.png` suffix.

Read the exact current lines before applying patch hunks to this instruction
file. A 2026-10-06 multi-file patch was rejected because its context assumed
a different line break; no partial edits were applied.

Keep file discovery scoped to this checkout or exact referenced artifact
directories. The figure sources are `scripts/plot_task_results.py`,
`scripts/plot_simulation_results.py`, and their CSVs under `data/`.
Plot typography and runtime checks are shared in `scripts/plot_style.py`;
build products are in `figures/` and `output/pdf/`.
