class NGramPattern(object):
    # python class and instance attributes: https://www.liaoxuefeng.com/wiki/1016959663602400/1017594591051072

    def __init__(self, tokens):
        self.followers = None
        self.max_followers = None
        self.tokens = tokens
        self.n = 1

    def __repr__(self):
        return str(self.n) + " * " + str(self.tokens)

    def __hash__(self):
        return hash(str(self.tokens))

    def __eq__(self, other):
        return str(self.tokens) == str(other.tokens)

    def support(self):
        return self.followers / self.max_followers

    @staticmethod
    def extract_all_from_trace(predicate_list):
        ngram_pattern_set = set()
        for i, p in enumerate(predicate_list):
            ngram_pattern = NGramPattern(p)
            found = False
            for pattern in ngram_pattern_set:
                if ngram_pattern == pattern:
                    pattern.n += 1
                    found = True
                    break
            if not found:
                ngram_pattern_set.add(ngram_pattern)
        return ngram_pattern_set





