from game_engine import GameEngine

class Test:

    def __init__(self):
        self.game_engine = GameEngine()
        self.factory_count = 6
        self.color_count = 5
        self.pattern_lines = 5

    def test_action_indexing(self):
        all_actions_valid = True
        for factory_index in range(-1, self.factory_count - 1):
            for color_index in range(self.color_count):
                for pattern_line_index in range(self.pattern_lines):
                    original_action = (factory_index, color_index, pattern_line_index)
                    index = self.game_engine.action_to_index(*original_action)
                    resulting_action = self.game_engine.index_to_action(index)
                    transformed_original_action = self.game_engine.transform_action_color(original_action)
                    if transformed_original_action != resulting_action:
                        all_actions_valid = False
                        print(f"Error: original action {original_action} resulted in {resulting_action}")
        if all_actions_valid:
            print("All actions correctly transformed to indices and back.")
        else:
            print("There were errors in transforming actions.")

if __name__ == "__main__":
    test = Test()
    test.test_action_indexing()