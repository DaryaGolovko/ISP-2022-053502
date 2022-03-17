import re


class Tasks:
    """Class for tasks from lab1"""
    @staticmethod
    def average_word_num(inp: str) -> int:
        """Counts an average number of words in the text"""
        sentences = re.split(r'[.?!]', inp)
        sum_words = 0
        for i in sentences:
            if sentences != "":
                counter = 1
                for j in i:
                    if j == ' ':
                        counter += 1
                sum_words += counter
        return int(sum_words / len(sentences))

    @staticmethod
    def count_iteration(inp: str) -> dict:
        """Counts word iterations in text and prints it"""
        words: dict = {}
        full_text = re.split(r'[.,?! ]', inp)
        for i in full_text:
            if i != 0 and i != "":
                if not words.get(i):
                    words[i] = 1
                else:
                    words[i] += 1
        return words

    def count_median(self, inp: str):
        """Counts median in the text"""
        words = []
        full_text = re.split(r'[.,?! ]', inp)
        for i in full_text:
            if i != 0 and i != "":
                words.append(i)
        return words[self.average_word_num(inp)]

    @staticmethod
    def top_ngrammas(inp: str, k: int, n: int) -> None:
        """Counts top-k ngrams """
        n_grammas: dict = {}
        words = Tasks.count_iteration(inp)
        for i in words:
            if len(i) < n:
                continue
            if len(i) == n:
                n_grammas[i] = 1 * words[i]
                continue
            if len(i) > n:
                while len(i) >= n:
                    n_grammas.update({i[:n]: n_grammas.get(i[:n], 0) + 1})
                    i = i[1:]

        sorted_dict = {}
        sorted_keys = sorted(n_grammas, key=n_grammas.get)
        for i in sorted_keys:
            sorted_dict[i] = n_grammas[i]
        for i in range(k + 1):
            if i >= len(sorted_dict):
                print("No such element")
                break
            print(sorted_dict.popitem())
