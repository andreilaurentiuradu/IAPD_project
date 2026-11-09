#!/usr/bin/env python3
"""Download player-match statistics from FBref and/or Understat.

The output is raw source data saved as CSV. It is intentionally not a modeling
pipeline: feature engineering and the high-offensive-performance label belong
in a later step.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import pandas as pd
import soccerdata as sd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "raw"

# Names accepted by soccerdata differ slightly between providers.
UNDERSTAT_LEAGUES = {
    "ENG-Premier League": "EPL",
    "ESP-La Liga": "La Liga",
    "GER-Bundesliga": "Bundesliga",
    "ITA-Serie A": "Serie A",
    "FRA-Ligue 1": "Ligue 1",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extrage statistici de fotbal la nivel de jucator-meci."
    )
    parser.add_argument(
        "--source",
        choices=("fbref", "understat", "both"),
        default="fbref",
        help="Sursa de date (implicit: fbref).",
    )
    parser.add_argument(
        "--leagues",
        nargs="+",
        default=["ENG-Premier League"],
        help=(
            "Ligi FBref, de ex. 'ENG-Premier League'. Pentru Understat, ligile "
            "FBref de top 5 sunt mapate automat."
        ),
    )
    parser.add_argument(
        "--seasons",
        nargs="+",
        default=["2023-2024", "2024-2025"],
        help="Sezoane în format YYYY-YYYY.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Directorul pentru CSV-uri (implicit: data/raw).",
    )
    return parser.parse_args()


def write_frame(frame: pd.DataFrame, source: str, kind: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = frame.copy()
    if isinstance(result.index, pd.MultiIndex) or result.index.name is not None:
        result = result.reset_index()
    result.insert(0, "data_source", source)
    path = output_dir / f"{source}_{kind}.csv"
    result.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"Salvat {len(result):,} rânduri: {path}")
    return path


def fetch_fbref(leagues: Iterable[str], seasons: Iterable[str], output_dir: Path) -> None:
    reader = sd.FBref(leagues=list(leagues), seasons=list(seasons))
    # Summary includes player match log fields such as minutes, goals, assists,
    # shots, shots on target, and cards where FBref has them.
    frame = reader.read_player_match_stats(stat_type="summary")
    if frame.empty:
        raise RuntimeError("FBref nu a returnat rânduri pentru ligile/sezoanele cerute.")
    write_frame(frame, "fbref", "player_match_stats", output_dir)


def fetch_understat(leagues: Iterable[str], seasons: Iterable[str], output_dir: Path) -> None:
    mapped = [UNDERSTAT_LEAGUES.get(league, league) for league in leagues]
    # Understat indexes a season by its starting year (e.g. 2023 for 2023-2024).
    understat_seasons = [str(season).split("-")[0] for season in seasons]
    reader = sd.Understat(leagues=mapped, seasons=understat_seasons)
    frame = reader.read_player_match_stats()
    if frame.empty:
        raise RuntimeError("Understat nu a returnat rânduri pentru ligile/sezoanele cerute.")
    write_frame(frame, "understat", "player_match_stats", output_dir)


def main() -> None:
    args = parse_args()
    if args.source in ("fbref", "both"):
        fetch_fbref(args.leagues, args.seasons, args.output_dir)
    if args.source in ("understat", "both"):
        fetch_understat(args.leagues, args.seasons, args.output_dir)


if __name__ == "__main__":
    main()
