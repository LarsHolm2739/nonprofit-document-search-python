import unittest

from src.nonprofit_search import Document, find_best


class SearchDecisionTest(unittest.TestCase):
    def test_volunteer_question_selects_volunteer_reminder(self):
        documents = (
            Document("donor_receipt", "Receipt", "gift receipt"),
            Document("volunteer_reminder", "Pantry", "pantry volunteer arrival"),
            Document("campaign_report", "Report", "campaign total"),
        )
        vectors = [[1.0, 0.0], [0.0, 1.0], [1.0, 0.0], [0.0, 0.9]]
        self.assertEqual(find_best("arrival", vectors, documents).kind, "volunteer_reminder")


if __name__ == "__main__":
    unittest.main()

