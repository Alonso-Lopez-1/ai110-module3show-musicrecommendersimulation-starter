"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    user_prefs = {
    "genre":        "pop",
    "mood":         "happy",
    "energy":       0.80,
    "tempo_bpm":    120,
    "valence":      0.80,
    "danceability": 0.75,
    "acousticness": 0.20,
    "likes_acoustic": False
    }

    # Primary profile: chill/lofi listener
    # user_prefs = {
    #     "genre":        "lofi",
    #     "mood":         "chill",
    #     "energy":       0.40,
    #     "tempo_bpm":    80,
    #     "valence":      0.60,
    #     "danceability": 0.60,
    #     "acousticness": 0.80,
    #     "likes_acoustic": True
    # }

    # Alternate profile: hype/workout listener
    # user_prefs = {
    #     "genre":        "edm",
    #     "mood":         "energetic",
    #     "energy":       0.95,
    #     "tempo_bpm":    138,
    #     "valence":      0.75,
    #     "danceability": 0.92,
    #     "acousticness": 0.05,
    #     "likes_acoustic": False
    # }

    # Alternate profile: melancholic/late-night listener
    # user_prefs = {
    #     "genre":        "blues",
    #     "mood":         "sad",
    #     "energy":       0.32,
    #     "tempo_bpm":    78,
    #     "valence":      0.30,
    #     "danceability": 0.45,
    #     "acousticness": 0.88,
    #     "likes_acoustic": True
    # }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print(f"  TOP {len(recommendations)} RECOMMENDATIONS")
    print("=" * 50)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  —  {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"    Score: {score:.2f} / 8.50")
        print(f"    Why:   {explanation}")
        print("-" * 50)


if __name__ == "__main__":
    main()
