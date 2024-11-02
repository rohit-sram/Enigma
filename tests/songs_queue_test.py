import unittest
from src.songs_queue import Songs_Queue
from unittest.mock import patch


class TestSongsQueue(unittest.TestCase):

    def setUp(self):
        self.initial_songs = ["Song1", "Song2", "Song3"]
        self.queue = Songs_Queue(self.initial_songs)

    def test_init(self):
        self.assertEqual(self.queue.queue, self.initial_songs)
        self.assertEqual(self.queue.index, 0)
        self.assertEqual(self.queue.current_index, 0)

    def test_next_song(self):
        # Test normal progression
        self.assertEqual(self.queue.next_song(), "Song1")
        self.assertEqual(self.queue.next_song(), "Song2")
        self.assertEqual(self.queue.next_song(), "Song3")

        # Test wrapping around to the beginning
        self.assertEqual(self.queue.next_song(), "Song1")

    def test_prev_song(self):
        # Move to the end of the queue
        self.queue.index = 3

        # Test normal regression
        self.assertEqual(self.queue.prev_song(), "Song3")
        self.assertEqual(self.queue.prev_song(), "Song2")
        self.assertEqual(self.queue.prev_song(), "Song1")

        # Test wrapping around to the end
        self.assertEqual(self.queue.prev_song(), "Song3")

    def test_get_len(self):
        self.assertEqual(self.queue.get_len(), 3)

    def test_return_queue(self):
        returned_queue, current_index = self.queue.return_queue()
        self.assertEqual(returned_queue, self.initial_songs)
        self.assertEqual(current_index, 0)

    @patch("src.songs_queue.shuffle")
    def test_shuffle_queue(self, mock_shuffle):
        self.queue.shuffle_queue()
        mock_shuffle.assert_called_once_with(self.queue.queue)

    def test_add_to_queue(self):
        self.queue.add_to_queue("Song4")
        self.assertEqual(self.queue.queue, ["Song1", "Song2", "Song3", "Song4"])
        self.assertEqual(self.queue.get_len(), 4)

    def test_empty_queue(self):
        empty_queue = Songs_Queue([])
        with self.assertRaises(IndexError):
            empty_queue.next_song()
        with self.assertRaises(IndexError):
            empty_queue.prev_song()


if __name__ == "__main__":
    unittest.main()
