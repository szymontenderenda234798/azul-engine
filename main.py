from game_engine import GameEngine
from model.random_player import RandomPlayer
from model.mcts_player import MCTSPlayer
from datetime import datetime
import statistics

if __name__ == "__main__":

    def evaluate_performance(n_iter, c_param, num_games=10):
        wins = 0
        total_score = 0

        for _ in range(num_games):
            game_engine = GameEngine(print_enabled=False, visualize=False)
            player1 = MCTSPlayer("MCTS Player", n_iter=n_iter, c_param=c_param)
            player2 = RandomPlayer("Player 2")
            ending_state = game_engine.play_game(player1=player1, player2=player2)
            
            # Assume that the GameEngine provides a method to get the winner and the scores
            winner = game_engine.get_winner(ending_state)
            score1, score2 = game_engine.get_scores(ending_state)

            if winner == player1:
                wins += 1
            total_score += score1  # Assuming score1 is for MCTSPlayer

        average_score = total_score / num_games
        win_rate = wins / num_games

        return win_rate, average_score



    def evaluate_performance_for_iterations(n_iter, num_games=3):
        wins = 0
        scores = []

        for _ in range(num_games):
            game_engine = GameEngine(print_enabled=False, visualize=False)
            player1 = MCTSPlayer("MCTS Player", n_iter=n_iter, c_param=1.4)
            player2 = RandomPlayer("Player 2")
            ending_state = game_engine.play_game(player1=player1, player2=player2)
            
            # Assume that the GameEngine provides a method to get the winner and the scores
            winner = game_engine.get_winner(ending_state)
            score1, score2 = game_engine.get_scores(ending_state)

            if winner == player1:
                wins += 1
            scores.append(score1)  # Assuming score1 is for MCTSPlayer

        average_score = sum(scores) / num_games
        win_rate = wins / num_games
        stdev_score = statistics.stdev(scores)


        return win_rate, average_score, stdev_score
    
    def test_c_values():
        c_values = [0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1]
        best_c_param = None
        best_performance = float('-inf')
        stats = []

        for c in c_values:
            win_rate, average_score = evaluate_performance(n_iter=100, c_param=c, num_games=10)
            performance = win_rate # You can adjust the performance metric as needed
            stats.append((c, win_rate, average_score, performance))
            print(f"c_param: {c}, Win Rate: {win_rate}, Average Score: {average_score}, Performance: {performance}")

            if performance > best_performance:
                best_performance = performance
                best_c_param = c

        print(f"\nThe best c_param is: {best_c_param}\n")

        # Print all stats
        print("All stats:")
        for stat in stats:
            print(f"c_param: {stat[0]}, Win Rate: {stat[1]}, Average Score: {stat[2]}, Performance: {stat[3]}")

    def test_n_iter_values(num_games=3):
        iteration_counts = [10, 100, 1_000, 10_000, 50_000, 100_000, 200_000]
        results = []
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"mcts_performance_results_{timestamp}.txt"

        with open(output_file, 'w') as f:
            for n_iter in iteration_counts:
                win_rate, average_score, stdev_score = evaluate_performance_for_iterations(n_iter=n_iter, num_games=num_games)
                results.append((n_iter, win_rate, average_score, stdev_score))
                result_str = f"n_iter: {n_iter}, Win Rate: {win_rate}, Average Score: {average_score}, Score Std Dev: {stdev_score}"
                print(result_str)
                f.write(result_str + "\n")

            # Print summarized results
            summary_str = "\nSummarized Results:\n"
            print(summary_str)
            f.write(summary_str)

            for result in results:
                result_str = f"n_iter: {result[0]}, Win Rate: {result[1]}, Average Score: {result[2]}, Score Std Dev: {result[3]}"
                print(result_str)
                f.write(result_str + "\n")

    test_n_iter_values(num_games=3)