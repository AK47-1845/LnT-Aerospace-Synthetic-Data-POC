# Changelog

All notable changes to the Physical AI Atlas are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [v0.2.0] — 2026-09-09

### Added
- **End-to-end canonical demo** (`03-build/end-to-end/run_atlas_demo.py`): Full pipeline — VLA reasoning → Flow Matching policy → CBF safety filter → MuJoCo simulation → telemetry reporting
- **CBF latency benchmark** (`04-validate/benchmarks/benchmark_cbf_latency.py`): Reproducible QP solve-time measurement with p50/p95/p99 reporting
- **5-tier repository structure**: Learn → Architect → Build → Validate → Industrialize
- `requirements.txt` for one-command environment setup
- `CHANGELOG.md` (this file)
- `01-learn/research-index.md`: Curated paper index (moved from README for cleaner navigation)
- `01-learn/fundamentals.md`: Pearl's Causal Ladder, failure modes, world model taxonomy
- `02-architect/safety-architecture.md`: Dedicated safety architecture discussion with honest qualification
- `04-validate/README.md`: Validation methodology and benchmark reproduction instructions
- `05-industrialize/plc-integration.md`: PLC/fieldbus deployment guide

### Changed
- **Calibrated claims throughout**: "Open Standard" → "Open Engineering Reference", "ISO 13849 PL-d Compliance" → "targeting ISO 13849 / IEC 61508 safety architecture patterns", "Guaranteed collision bounds" → "physics-enforced collision constraints", "1,000 Hz Hard Real-Time" → "designed for 1 kHz safety-loop operation"
- Qualified safety architecture language with explicit disclaimer about formal certification
- Fixed quick-start `cd physical-ai` → `cd physical-ai-atlas`
- README rewritten with 5-tier navigation table and "What This Is / What This Is Not" section
- Moved research paper index from README to `01-learn/research-index.md`

### Removed
- ISO 13849 compliance badge from README title (replaced with safety architecture pattern reference)
- "Living Standard" badge (replaced with "Active Development")
- Self-referential "100% PASS" from README (kept in validator documentation only)

## [v0.1.0] — 2026-09-08

### Added
- Initial release of The Physical AI Atlas
- System architecture with multi-rate pipeline (sensing → reasoning → execution → safety → actuation)
- Pearl's Causal Ladder framework for Physical AI
- 5 standalone starter kits (Diffusion Policy, Flow Matching, CBF, VLA, PLC Bridge)
- 8-stage practitioner roadmap across 4 personas
- Hardware lab guide ($250 DIY to $100k+ enterprise)
- Mathematical architecture blueprints (SE(3), Flow Matching, CBF QPs, DLS)
- Master 25-slide executive presentation with programmatic generator and self-QA validator
- Interactive dark glassmorphic web portal (GitHub Pages ready)
- Executive strategic briefing document
