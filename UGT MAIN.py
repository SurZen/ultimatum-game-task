#!/usr/bin/env python
"""
Rebuilt Ultimatum Game runner with updated flow.

Top-of-file duplicates cleaned.
"""
from __future__ import annotations
import argparse
import csv
import io
import json
from pathlib import Path
from datetime import datetime
import random

try:
    from psychopy import visual, core, event, gui
except Exception:  # pragma: no cover
    from utils.psychopy_stub import visual, core, event, gui
    print("[run_ugt.py] PsychoPy not found — using headless stub for testing")

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "configs" / "config_default.json"
VERSIONS_PATH = ROOT / "configs" / "versions.json"
DATA_DIR = ROOT / "data" / "raw"


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_deck(deck_path: Path) -> list[dict]:
    """Load CSV, parse leading metadata comments (# key: value), return list of rows.
    Inject `partner_name` from metadata if missing in rows.
    """
    with open(deck_path, "r", encoding="utf-8-sig", newline="") as f:
        raw = f.read().splitlines()

    meta: dict[str, str] = {}
    data_lines: list[str] = []
    for line in raw:
        if line.strip().startswith("#"):
            content = line.strip().lstrip("#").strip()
            if ":" in content:
                k, v = content.split(":", 1)
                meta[k.strip().lower()] = v.strip()
            continue
        if line.strip() == "":
            continue
        data_lines.append(line)

    reader = csv.DictReader(io.StringIO("\n".join(data_lines)))
    rows = []
    for row in reader:
        # normalize numeric fields
        for k in ("version", "trial", "stake", "offer_you", "offer_them"):
            if k in row and row[k] != "":
                try:
                    row[k] = int(float(row[k]))
                except Exception:
                    pass
        if ("partner_name" not in row or row.get("partner_name", "") == "") and "partner_name" in meta:
            row["partner_name"] = meta["partner_name"]
        rows.append(row)
    return rows


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--version", type=int, choices=[1,2,3,4,5], help="Deck version 1–5")
    p.add_argument("--sub", type=str, default="", help="Subject ID (e.g., 0007) — stored as P_ID")
    p.add_argument("--ses", type=str, default="01", help="Session (default 01)")
    p.add_argument("--fullscreen", action="store_true", help="Force fullscreen (overrides config)")
    return p.parse_args()


def prompt_if_missing(args: argparse.Namespace) -> dict:
    # Present and store participant ID under `P_ID` (replace previous `sub` label)
    info = {
        "P_ID": args.sub or "",
        "ses": args.ses or "01",
        "version": args.version if args.version is not None else 1,
    }
    if args.version is None or args.sub == "":
        dlg = gui.DlgFromDict(dictionary=info, title="Ultimatum Game – Setup", order=["P_ID", "ses", "version"])
        if not dlg.OK:
            core.quit()
    return info


def wait_or_quit(seconds: float, quit_key: str) -> None:
    timer = core.Clock()
    while timer.getTime() < seconds:
        if quit_key in event.getKeys():
            core.quit()
        core.wait(0.01)


def draw_text(win: visual.Window, txt: visual.TextStim, message: str) -> None:
    # Ensure text is drawn centered by resetting position each time
    txt.text = message
    try:
        txt.pos = (0, 0)
    except Exception:
        pass
    txt.draw()
    win.flip()


def show_loading_screen(win: visual.Window, txt: visual.TextStim, message: str, duration: float, quit_key: str) -> None:
    """Show a mock loading screen with animated dots for `duration` seconds.
    Checks `quit_key` while waiting.
    """
    timer = core.Clock()
    interval = 0.5
    while timer.getTime() < duration:
        if quit_key in event.getKeys():
            core.quit()
        elapsed = timer.getTime()
        dots = "." * int((elapsed // interval) % 4)
        txt.text = f"{message}{dots}"
        try:
            txt.pos = (0, 0)
        except Exception:
            pass
        txt.draw()
        win.flip()
        core.wait(0.1)


def find_avatar(partner: str) -> Path | None:
    """Search several candidate directories for an avatar matching partner (case-insensitive).
    Candidate names: <Partner>P.png, partnerP.jpg, etc.
    """
    candidate_dirs = [ROOT / "AVA_pics", ROOT.parent / "AVA_pics", Path.cwd() / "AVA_pics"]
    for d in candidate_dirs:
        try:
            if not d.exists():
                continue
            # exact
            p_exact = d / f"{partner}P.png"
            if p_exact.exists():
                return p_exact
            # try other suffixes and case-insensitive
            for f in d.iterdir():
                if not f.is_file():
                    continue
                if f.suffix.lower() not in (".png", ".jpg", ".jpeg"):
                    continue
                stem = f.stem.lower()
                target = (partner + "p").lower()
                if stem == target or stem.startswith(partner.lower()):
                    return f
        except Exception:
            continue
    return None


def main():
    args = parse_args()
    config = load_json(CONFIG_PATH)
    versions = load_json(VERSIONS_PATH)
    info = prompt_if_missing(args)

    fullscreen = bool(args.fullscreen) or bool(config.get("fullscreen", True))

    version_key = str(int(info["version"]))
    deck_rel = versions.get(version_key)
    if not deck_rel:
        raise RuntimeError(f"No deck mapping for version {version_key} in {VERSIONS_PATH}")
    deck_path = (ROOT / deck_rel).resolve()
    trials = load_deck(deck_path)

    # Assign a random loading duration (seconds) for each deck version 1..5
    deck_loading_durations: dict[int, float] = {}
    for v in range(1, 6):
        deck_loading_durations[v] = round(random.uniform(30.0, 90.0), 2)
    try:
        print(f"[DEBUG] deck_loading_durations={deck_loading_durations}")
    except Exception:
        pass

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_name = f"sub-{info['P_ID']}_ses-{info['ses']}_task-ugtKT_v{version_key}_{timestamp}.csv"
    out_path = DATA_DIR / out_name

    win = visual.Window(size=[1920,1080], fullscr=fullscreen, color=config.get("screen_color", [0,0,0]), units="height")
    txt = visual.TextStim(win, text="", height=float(config.get("text_height", 0.06)), color=config.get("text_color", [1,1,1]), wrapWidth=1.4)

    # Keys: enforce A/R
    accept_key = str(config.get("accept_key", "a")).lower()
    reject_key = str(config.get("reject_key", "r")).lower()
    quit_key = str(config.get("quit_key", "escape")).lower()

    # Durations
    proposer_dur = float(config.get("proposer_dur", 1.2))
    offer_dur = float(config.get("offer_dur", 1.8))
    decision_max = float(config.get("decision_max", 4.0))
    feedback_dur = float(config.get("feedback_dur", 1.0))
    iti_min = float(config.get("iti_min", 2.0))
    iti_max = float(config.get("iti_max", 5.0))

    practice_count = int(config.get("practice_trials", 2))

    # Instructions (updated)
    instr = (
        "ULTIMATUM GAME\n\n"
        "On each round, a partner proposes how to split $10 between you.\n"
        "You can ACCEPT or REJECT.\n\n"
        f"ACCEPT ({accept_key.upper()}): you get the proposed amount.\n"
        f"REJECT ({reject_key.upper()}): neither gets anything.\n\n"
        "IMPORTANT: If you fail to respond within the allowed time, the PARTNER receives the entire $10 for that round.\n\n"
        f"Press {accept_key.upper()} to Accept or {reject_key.upper()} to Reject.\n"
        f"(Press {quit_key.upper()} anytime to quit.)"
    )

    draw_text(win, txt, instr)
    event.clearEvents()
    event.waitKeys(keyList=[accept_key, reject_key, quit_key])
    if quit_key in event.getKeys([quit_key]):
        core.quit()

    # Data writer
    fieldnames = [
        "P_ID","ses","deck_version","deck_file","timestamp",
        "trial","stake","partner_name","offer_you","offer_them","fairness","deck_avatar",
        "response","accepted","rt","payoff",
        "proposer_onset","offer_onset","decision_onset","feedback_onset"
    ]

    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        global_clock = core.Clock()
        total_payoff = 0

        partner_shown_for_deck = False

        for row in trials:
            event.clearEvents()
            # ensure deck_avatar defined each trial
            deck_avatar = ""

            partner = row.get("partner_name", "Partner")
            trial_no = row.get("trial", "")
            try:
                trial_idx = int(trial_no)
            except Exception:
                trial_idx = None

            # Determine if we should show partner identity now: only once after practice
            show_partner = False
            if trial_idx is not None and (not partner_shown_for_deck) and trial_idx > practice_count:
                show_partner = True
                partner_shown_for_deck = True

            if show_partner:
                proposer_onset = global_clock.getTime()
                avatar_file = find_avatar(partner)
                # If this partner/avatar is Alix, show a mock "other player joining" loading screen
                try:
                    name_lower = (avatar_file.name if avatar_file is not None else partner).lower()
                except Exception:
                    name_lower = str(partner).lower()
                # Show loading screen for Alex (and tolerate typo 'alix')
                try:
                    if any(k in name_lower for k in ("alex", "alix", "morgan")):
                        try:
                            deck_version_num = int(row.get("version", int(version_key)))
                        except Exception:
                            deck_version_num = int(version_key)
                        duration = deck_loading_durations.get(deck_version_num, 90.0)
                        show_loading_screen(win, txt, "Other player joining session\nPlease wait", duration, quit_key)
                except Exception:
                    # If anything goes wrong with the loading helper, continue silently
                    pass
                # debug log for when partner identity is shown
                try:
                    print(f"[DEBUG] show_partner=True partner={partner} trial={trial_idx} avatar_file={avatar_file}")
                except Exception:
                    pass
                if avatar_file:
                    deck_avatar = avatar_file.name
                    try:
                        avatar_size = float(config.get("avatar_size", 0.4))
                        avatar_pos = tuple(config.get("avatar_pos", [0, 0.15]))
                        name_pos = tuple(config.get("name_pos", [0, -0.3]))
                        avatar = visual.ImageStim(win, image=str(avatar_file), size=avatar_size, pos=avatar_pos)
                        # Draw partner name with a dedicated TextStim so we don't mutate the
                        # shared `txt` object (which is used elsewhere and should remain centered).
                        name_txt = visual.TextStim(
                            win,
                            text=str(partner),
                            height=float(config.get("text_height", 0.06)),
                            color=config.get("text_color", [1, 1, 1]),
                            wrapWidth=getattr(txt, "wrapWidth", 1.4),
                            pos=name_pos,
                        )
                        avatar.draw()
                        name_txt.draw()
                        win.flip()
                    except Exception:
                        draw_text(win, txt, f"Partner: {partner}")
                else:
                    draw_text(win, txt, f"Partner: {partner}")
                wait_or_quit(proposer_dur, quit_key)
            else:
                proposer_onset = None

            # Offer display (no partner name)
            offer_onset = global_clock.getTime()
            offer_you = row.get("offer_you", "")
            offer_them = row.get("offer_them", "")
            offer_text = f"Partner gets ${offer_them}, you get ${offer_you}"
            draw_text(win, txt, offer_text)
            wait_or_quit(offer_dur, quit_key)

            # Decision prompt
            decision_onset = global_clock.getTime()
            prompt = f"Accept or Reject?\n\n[{accept_key.upper()}] Accept    [{reject_key.upper()}] Reject"
            draw_text(win, txt, prompt)
            resp_clock = core.Clock()
            keys = event.waitKeys(maxWait=decision_max, keyList=[accept_key, reject_key, quit_key], timeStamped=resp_clock)

            response = "timeout"
            rt = ""
            accepted = 0
            payoff = 0

            if keys:
                key, key_rt = keys[0]
                if key == quit_key:
                    win.close()
                    core.quit()
                response = key
                rt = round(float(key_rt), 4)
                accepted = 1 if key == accept_key else 0
                if accepted == 1:
                    try:
                        payoff = int(row.get("offer_you", 0))
                    except Exception:
                        payoff = 0
                else:
                    # rejected -> both get $0
                    payoff = 0
            else:
                # timeout -> partner gets full $10, participant gets $0
                response = "timeout"
                rt = ""
                accepted = 0
                payoff = 0

            total_payoff += payoff

            # Feedback
            feedback_onset = global_clock.getTime()
            if response == "timeout":
                fb = "No response.\n\nPartner receives $10 for this round. You get $0."
            elif accepted == 1:
                fb = f"Accepted.\n\nYou get ${row.get('offer_you')}"
            else:
                fb = "Rejected.\n\nYou both get $0."
            draw_text(win, txt, fb)
            wait_or_quit(feedback_dur, quit_key)

            # ITI
            iti = random.uniform(iti_min, iti_max)
            draw_text(win, txt, "+")
            wait_or_quit(iti, quit_key)

            writer.writerow({
                "P_ID": info.get("P_ID", ""),
                "ses": info.get("ses", "01"),
                "deck_version": row.get("version", int(version_key)),
                "deck_file": deck_path.name,
                "timestamp": timestamp,
                "trial": row.get("trial", ""),
                "stake": row.get("stake", config.get("stake", 10)),
                "partner_name": partner,
                "offer_you": row.get("offer_you", ""),
                "offer_them": row.get("offer_them", ""),
                "fairness": row.get("fairness", ""),
                "deck_avatar": deck_avatar,
                "response": response,
                "accepted": accepted,
                "rt": rt,
                "payoff": payoff,
                "proposer_onset": round(proposer_onset, 4) if proposer_onset is not None else "",
                "offer_onset": round(offer_onset, 4),
                "decision_onset": round(decision_onset, 4),
                "feedback_onset": round(feedback_onset, 4),
        })

        # End
        draw_text(win, txt, f"Done.\n\nTotal earned this task: ${total_payoff}\n\nPress any key to exit.")
        event.waitKeys()

    win.close()
    core.quit()


if __name__ == "__main__":
    main()
