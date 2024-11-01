import unittest
from src.songs_queue import Songs_Queue

class TestSongsQueue(unittest.TestCase):

    def setUp(self):
        self.sample_songs = ["Song A", "Song B", "Song C", "Song D", "Song E"]
        self.queue = Songs_Queue(self.sample_songs)

    def test_init(self):
        self.assertEqual(self.queue.queue, self.sample_songs)
        self.assertEqual(self.queue.index, 0)
        self.assertEqual(self.queue.current_index, 0)

    def test_next_song(self):
        # Test normal next song functionality
        for i in range(len(self.sample_songs)):
            self.assertEqual(self.queue.next_song(), self.sample_songs[i])
        
        # Test wrapping around to the beginning
        self.assertEqual(self.queue.next_song(), self.sample_songs[0])

    def test_prev_song(self):
        # Move to the end of the queue
        for _ in range(len(self.sample_songs)):
            self.queue.next_song()
        
        # Test normal previous song functionality
        for i in range(len(self.sample_songs) - 1, -1, -1):
            self.assertEqual(self.queue.prev_song(), self.sample_songs[i])
        
        # Test wrapping around to the end
        self.assertEqual(self.queue.prev_song(), self.sample_songs[-1])

    def test_get_len(self):
        self.assertEqual(self.queue.get_len(), len(self.sample_songs))

    def test_return_queue(self):
        returned_queue, current_index = self.queue.return_queue()
        self.assertEqual(returned_queue, self.sample_songs)
        self.assertEqual(current_index, 0)

        # Test after moving to next song
        self.queue.next_song()
        returned_queue, current_index = self.queue.return_queue()
        self.assertEqual(current_index, 0)  # Because next_song() updates current_index after returning

    def test_shuffle_queue(self):
        original_queue = self.queue.queue.copy()
        self.queue.shuffle_queue()
        self.assertNotEqual(self.queue.queue, original_queue)
        self.assertEqual(set(self.queue.queue), set(original_queue))

    def test_add_to_queue(self):
        new_song = "New Song"
        original_length = self.queue.get_len()
        self.queue.add_to_queue(new_song)
        self.assertEqual(self.queue.get_len(), original_length + 1)
        self.assertEqual(self.queue.queue[-1], new_song)

if __name__ == '__main__':
    unittest.main()
