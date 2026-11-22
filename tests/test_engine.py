import unittest

from atomic_mind.engine import ConversationEngine


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = ConversationEngine({
            "fallback": ["Fallback response."],
            "rules": [
                {"id": "hello", "priority": 10, "keywords": ["hello"],
                 "responses": ["Hello there.", "Hi again."]},
                {"id": "name", "priority": 20, "pattern": r"my name is (.+)",
                 "responses": ["Nice to meet you, {1}."]}
            ]
        })

    def test_keyword_match(self):
        self.assertEqual(self.engine.respond("Hello!").text, "Hello there.")

    def test_pattern_capture(self):
        self.assertEqual(self.engine.respond("My name is Tanvir").text,
                         "Nice to meet you, tanvir.")

    def test_fallback(self):
        result = self.engine.respond("quantum mechanics")
        self.assertEqual(result.text, "Fallback response.")
        self.assertFalse(result.matched)

    def test_response_rotation(self):
        self.engine.respond("hello")
        self.assertEqual(self.engine.respond("hello").text, "Hi again.")


if __name__ == "__main__":
    unittest.main()
