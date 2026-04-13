from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.

    Algorithm Recipe
    ----------------
    Categorical matches (exact string equality):
        genre match  → +2.0
        mood match   → +1.0

    Numerical proximity (each worth up to the stated max):
        energy       → up to +1.5  (1.5 * (1 - |user - song|))
        valence      → up to +0.5  (0.5 * (1 - |user - song|))
        danceability → up to +0.5  (0.5 * (1 - |user - song|))
        acousticness → up to +0.5  (0.5 * (1 - |user - song|))

    Bonus:
        likes_acoustic + song acousticness > 0.7 → +0.5

    Maximum possible score: 6.5
    """
    score: float = 0.0
    reasons: List[str] = []

    # --- categorical: genre ---
    if user_prefs.get("genre", "").lower() == song["genre"].lower():
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    # --- categorical: mood ---
    if user_prefs.get("mood", "").lower() == song["mood"].lower():
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    # --- numerical: energy ---
    energy_pts = 1.5 * (1.0 - abs(user_prefs["energy"] - song["energy"]))
    score += energy_pts
    reasons.append(f"energy proximity (+{energy_pts:.2f})")

    # --- numerical: valence ---
    valence_pts = 0.5 * (1.0 - abs(user_prefs["valence"] - song["valence"]))
    score += valence_pts
    reasons.append(f"valence proximity (+{valence_pts:.2f})")

    # --- numerical: danceability ---
    dance_pts = 0.5 * (1.0 - abs(user_prefs["danceability"] - song["danceability"]))
    score += dance_pts
    reasons.append(f"danceability proximity (+{dance_pts:.2f})")

    # --- numerical: acousticness ---
    acoustic_pts = 0.5 * (1.0 - abs(user_prefs["acousticness"] - song["acousticness"]))
    score += acoustic_pts
    reasons.append(f"acousticness proximity (+{acoustic_pts:.2f})")

    # --- bonus: acousticness preference ---
    if user_prefs.get("likes_acoustic") and song["acousticness"] > 0.7:
        score += 0.5
        reasons.append("acoustic bonus (+0.50)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Why sorted() instead of .sort()
    --------------------------------
    list.sort()  → mutates the original list in place, returns None.
                   The caller's `songs` list would be permanently reordered —
                   a hidden side-effect that makes functions harder to reason about.

    sorted()     → takes any iterable, returns a *new* sorted list, leaving
                   the original untouched.  The Pythonic choice for functions
                   that shouldn't modify their inputs.
    """
    # Score every song and collect (song, score, explanation) triples
    scored = [
        (song, *score_song(user_prefs, song))   # unpacks (score, reasons) inline
        for song in songs
    ]

    # Sort by score descending; sorted() leaves the original `songs` list intact
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    # Join the reasons list into a single readable explanation string
    top_k = [
        (song, score, ", ".join(reasons))
        for song, score, reasons in ranked[:k]
    ]

    return top_k
