from trace import *
from NGramPattern import *
from save_load_pickle import *
from trainers.ModelSelectionTrainer import *


class PatternAnalysis(object):
    variation_list = ['1111', '1110', '1100', '1011', '1010', '1000', '0011', '0010']
    traces = {}

    @staticmethod
    def generate_traces():
        for variation in PatternAnalysis.variation_list:
            PatternAnalysis.traces[variation] = {}
            for i in range(1, 11):
                t = Trace()
                t.variation = variation
                t.session = i
                predicate_dict = t.get_predicate()
                if predicate_dict:
                    PatternAnalysis.traces[variation][i] = predicate_dict

    @staticmethod
    def extract_all_patterns(sprite_name):
        predicate_list = []
        for variation in PatternAnalysis.variation_list:
            for i in range(1, 11):
                predicate_dict = PatternAnalysis.traces[variation].get(i, None)
                if predicate_dict:
                    predicate_list.extend(predicate_dict[sprite_name])
        all_pattern_set = NGramPattern.extract_all_from_trace(predicate_list)
        return all_pattern_set


class ClassificationTarget(object):
    target_name_dict = {1: "Paddle Moves with Key", 2: "Ball Bounces on Paddle", 3: "Ball Bounces on Touching Edges"}

    def get_x_y(self):
        PatternAnalysis.generate_traces()
        all_patterns = {'Paddle': PatternAnalysis.extract_all_patterns("Paddle"),
                        'Ball': PatternAnalysis.extract_all_patterns("Ball")}

        save_obj(all_patterns['Paddle'], "paddle_patterns", "data/pong", "result")
        save_obj(all_patterns['Ball'], "ball_patterns", "data/pong", "result")

        for target in [1, 2, 3]:
            y_pred_accu = np.array([])
            y_test_accu = np.array([])
            for fold in range(8):
                x_train, x_test = [], []
                y_train, y_test = [], []
                for v, variation in enumerate(PatternAnalysis.variation_list):
                    for i in range(1, 11):
                        predicate_dict = PatternAnalysis.traces[variation].get(i, None)
                        if not predicate_dict:
                            continue
                        sprite_name = ['Paddle', 'Ball'][target != 1]
                        predicate_list = predicate_dict[sprite_name]
                        current_patterns = NGramPattern.extract_all_from_trace(predicate_list)
                        save_obj(current_patterns, f"{sprite_name}_{target}_patterns", 'data/pong', f'patterns/{variation}/{i}')
                        cur_x = list(map(lambda x: int(x in current_patterns), all_patterns[sprite_name]))
                        if fold != v:
                            x_train.append(cur_x)
                            y_train.append(int(variation[target - 1]))
                        elif fold == v:
                            x_test.append(cur_x)
                            y_test.append(int(variation[target - 1]))

                x_train, x_test = np.array(x_train), np.array(x_test)
                y_train, y_test = np.array(y_train), np.array(y_test)
                y_pred = bernoulli_nb.get_y_pred(x_train, x_test, y_train)
                y_pred_accu = np.append(y_pred_accu, y_pred)
                y_test_accu = np.append(y_test_accu, y_test)
            performance = bernoulli_nb.get_matrix(y_test_accu, y_pred_accu)
            performance_df = pd.Series(performance)
            save_obj(performance_df, f"{target}_performance_df", 'data/pong', 'result')






    def display_data_df(self):
        paddle_patterns = load_obj("paddle_patterns", "data/pong", "result")
        ball_patterns = load_obj("ball_patterns", "data/pong", "result")
        all_patterns = {'Paddle': paddle_patterns,
                        'Ball': ball_patterns}

        for target in [1, 2, 3]:
            x = load_obj(f"{target}_x", "data/pong", "result")
            y = load_obj(f"{target}_y", "data/pong", "result")
            sprite_name = ['Paddle', 'Ball'][target != 1]
            patterns = all_patterns[sprite_name]
            df = pd.DataFrame(columns=patterns)
            for i in range(len(x)):
                new_row = {}
                for j, colname in enumerate(patterns):
                    new_row[colname] = x[i][j]
                df.loc[len(df)] = new_row

            df['y'] = y
            print("df: ", df)
            data_index = []
            for variation in PatternAnalysis.variation_list:
                for i in range(1, 11):
                    if i in PatternAnalysis.traces[variation]:
                        data_index.append(f"{variation}-{i}")
            print(len(data_index))
            print(len(df))
            df['data_index'] = data_index
            save_obj(df, f"{target}_df", "data/pong", "result")






ClassificationTarget().get_x_y()
ClassificationTarget().display_data_df()
