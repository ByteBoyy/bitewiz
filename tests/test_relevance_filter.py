import unittest

from lib_llm.helpers.relevance_filter import RelevanceFilter


class RelevanceFilterTests(unittest.TestCase):
    def test_food_context_ignores_punctuation(self):
        relevance_filter = RelevanceFilter()

        self.assertTrue(relevance_filter.has_food_context("Can you find pizza?"))
        self.assertTrue(relevance_filter.has_food_context("Show restaurants, please."))

    def test_punctuated_food_request_is_processed(self):
        relevance_filter = RelevanceFilter()

        relevant, dormant = relevance_filter.should_process_speech(
            "What restaurants do you recommend?"
        )

        self.assertTrue(relevant)
        self.assertFalse(dormant)


if __name__ == "__main__":
    unittest.main()
