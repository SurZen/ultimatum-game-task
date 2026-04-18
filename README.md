# UGT_PsychoPy (Koenigs & Tranel-style Ultimatum Game)

This project includes:
- `run_ugt.py`: a single PsychoPy script that can run any of 5 fixed decks
- `decks/`: five fixed-order Koenigs & Tranel-style decks (22 trials each)
- `configs/`: optional config files for easy edits
- `data/raw/`: output data will be saved here

## Quick start (Windows 11)
1. Install PsychoPy (Standalone is fine).
2. Put this folder anywhere (Desktop is fine).
3. Run from PsychoPy Runner:
   - Open `run_ugt.py` and click Run
   - Choose `version` 1–5 when prompted (or pass `--version`)

## Running with a specific version (command line)
If you're running from a terminal in this folder:
```bash
python run_ugt.py --version 3 --sub 0007 --ses 01
```

## Keys (default)
- Accept: `a`
- Reject: `r`
- Quit anytime: `escape`

Edit `configs/config_default.json` to change timings/keys.

## Deck format and metadata
Deck CSVs support simple deck-level metadata via leading comment lines. Add lines starting with `#` and a `key: value` pair. The loader will parse these and inject values into each trial row when needed.

Required behavior:
- Add a deck-level partner name using: `# partner_name: Alex`
- You can remove the per-row `partner_name` column; `run_ugt.py` will inject the deck-level `partner_name` into each trial.

Example deck header with metadata:
```
# partner_name: Alex
version,trial,stake,offer_you,offer_them,fairness,offer_text
1,1,10,3,7,unfair,"Partner gets $7, you get $3"
```
