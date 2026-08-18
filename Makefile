.PHONY: phase0 audit qc features fallback figures phase1b_features phase1b_axes phase1b_external phase1b phase2a phase2b test

phase0: audit test

audit:
	python3 src/data/audit_metadata.py

qc: audit
	python3 src/qc/expression_qc.py

features: qc
	python3 src/features/build_feature_scores.py

fallback: features
	python3 src/clustering/phase1_biological_fallback.py

figures: fallback
	python3 src/plotting/make_phase1_figures.py

test:
	python3 -m pytest tests

phase1: figures test
	@echo "Fallback Phase 1 completed. Preferred GSVA/MOFA2 workflow remains pending if R dependencies are available."

phase1b_features:
	environment/phase1b_venv/bin/python src/features/build_phase1b_features.py

phase1b_axes: phase1b_features
	environment/phase1b_venv/bin/python src/integration/phase1b_molecular_axes.py

phase1b_external:
	environment/phase1b_venv/bin/python src/data/audit_external_geo_phase1b.py
	environment/phase1b_venv/bin/python src/integration/phase1b_external_support.py
	environment/phase1b_venv/bin/python src/integration/phase1b_external_replication.py

phase1b: phase1b_axes phase1b_external test
	@echo "Phase 1B molecular-axis rescue completed."

phase2a:
	environment/phase1b_venv/bin/python src/integration/phase2a_strict_axis_freeze.py
	environment/phase1b_venv/bin/python -m pytest tests
	@echo "Phase 2A axis mechanism prioritization completed."

phase2b:
	environment/phase1b_venv/bin/python src/integration/phase2b_gse228421_single_cell_localization.py
	environment/phase1b_venv/bin/python -m pytest tests
	@echo "Phase 2B GSE228421 donor-level single-cell localization completed."
