import pytest

from wiki_game.main import is_valid_suffix

class TestURLS:
    # TODO: Assert not only the first element in the array, but all of them
    def test_bad_urls(self):
        bad_urls = ["https://en.wikipedia.org/wiki/Representation_of_the_Faroes,_Reykjav%C3%ADk#cite_note-1",
                    "https://en.wikipedia.org//wiki/Wikipedia:Stub",
                    "https://en.wikipedia.org//wiki/Wikipedia",
                    "https://en.wikipedia.org/https://en.wikipedia.org/w/index.php?title=Spey_Tower&action=edit"
                    ]
        for url in bad_urls:
            assert not is_valid_suffix(url=url)