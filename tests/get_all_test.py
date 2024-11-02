# import unittest
# import warnings
# import sys

# from src.get_all import *

# warnings.filterwarnings("ignore")


# class Tests(unittest.TestCase):

#     def test_filtered_songs(self):
#         filtered = filtered_songs()
#         print(filtered)
#         self.assertTrue(len(filtered) != 0)

#     def test_get_all_songs(self):
#         songs = get_all_songs()
#         print(songs)
#         self.assertTrue(len(songs) != 0)

#     def test_recommend(self):
#         ts = {"track_name": "Your Love Is My Drug", "genre": "dance pop"}
#         songs = recommend(ts)
#         print(songs)
#         #test = {"track_name": "Living For Love", "genre": "dance pop"}
#         self.assertTrue(len(songs) == 10)


import unittest
import warnings
import sys
import pandas as pd

from src.get_all import *

warnings.filterwarnings("ignore")


class Tests(unittest.TestCase):

    def test_filtered_songs(self):
        filtered = filtered_songs()
        print(filtered)
        self.assertTrue(len(filtered) != 0)

    def test_filtered_songs_columns(self):
        filtered = filtered_songs()
        expected_columns = {"track_name", "artist", "year", "genre"}
        self.assertTrue(set(filtered.columns) == expected_columns)

    def test_get_all_songs(self):
        songs = get_all_songs()
        print(songs)
        self.assertTrue(len(songs) != 0)

    def test_get_all_songs_structure(self):
        songs = get_all_songs()
        self.assertIn("track_name", songs.columns)
        self.assertIn("genre", songs.columns)
        self.assertIn("year", songs.columns)
        self.assertIn("artist", songs.columns)

    def test_recommend(self):
        ts = {"track_name": "Your Love Is My Drug", "genre": "dance pop"}
        songs = recommend(ts)
        print(songs)
        self.assertTrue(len(songs) == 10)

    def test_recommend_genre_matching(self):
        ts = {"track_name": "Your Love Is My Drug", "genre": "dance pop"}
        recommended_songs = recommend(ts)
        all_songs = get_all_songs()
        genre = ts["genre"]
        
        # Check if all recommended songs belong to the same genre. Looking for outliers
        valid_genre = all(
            all_songs[all_songs["track_name"] == song]["genre"].values[0] == genre
            for song in recommended_songs if song in all_songs["track_name"].values
        )
        self.assertTrue(valid_genre)

    def test_recommend_fallback(self):
        ts = {"track_name": "Nonexistent Song", "genre": "unknown genre"}
        recommended_songs = recommend(ts)
        # Check that we get 10 songs even if the genre doesn't exist in the dataset
        self.assertEqual(len(recommended_songs), 10)


if __name__ == "__main__":
    unittest.main()
