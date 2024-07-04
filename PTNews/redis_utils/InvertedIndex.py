from collections import Counter, defaultdict

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(lambda: defaultdict(list))
    
    def update(self, doc, words):
        try:
            word_positions = find_occurrences(doc, words)
            keys = list(word_positions.keys())
            
            for i in range(len(keys)):
                word1 = keys[i].lower()
                positions1 = word_positions[word1]
                
                for pos1 in positions1:
                    for word2, positions2 in list(word_positions.items())[i+1:]:
                        word2 = word2.lower()
                        
                        if word1 == word2:
                            continue

                        for pos2 in positions2:
                            start1, end1 = pos1[0], pos1[1]
                            start2, end2 = pos2[0], pos2[1]
                            
                            if (start1 <= start2 <= end1) or (start2 <= start1 <= end2):
                                continue
                            else:
                                difference = min(abs(start2 - end1), abs(start1 - end2), abs(end1 - start2), abs(end2 - start1))
                                
                                # Inicializar listas se não existirem
                                if word1 not in self.index:
                                    self.index[word1] = defaultdict(list)
                                if word2 not in self.index[word1]:
                                    self.index[word1][word2] = []

                                if word2 not in self.index:
                                    self.index[word2] = defaultdict(list)
                                if word1 not in self.index[word2]:
                                    self.index[word2][word1] = []

                                self.index[word1][word2].append(difference)
                                self.index[word2][word1].append(-difference)
        
        except Exception as e:
            print(f"Erro ao processar a palavra '{word1}' com '{word2}': {e}")


    def get_top_cooccurrences(self, target_word, window_size=20, top_n=10):
        if window_size == 0:
            window_size = float('inf')

        if target_word in self.index:
            cooccurrences = Counter()
            for co_word, differences in self.index[target_word].items():
                if window_size == float('inf'):
                    count = len(differences)
                else:
                    count = sum(1 for diff in differences if abs(diff) <= window_size)
                cooccurrences[co_word] += count

            # Filter out elements with zero occurrences
            sorted_cooccurrences = [(word, count) for word, count in cooccurrences.items() if count > 0]
            # Sort the cooccurrences by count in descending order
            sorted_cooccurrences.sort(key=lambda x: x[1], reverse=True)
            # Return only the top_n elements
            return sorted_cooccurrences[:top_n]
        else:
            return []

    def get_index(self):
        return self.index

def find_occurrences(text, words):
    dictOfPositions = {}
    text = text.lower()
    
    for word in words:
        word = word.lower()
        start = 0
        positions = []
        while True:
            start = text.find(word, start)
            if start == -1:
                break
            positions.append((start, start + len(word) - 1))  # Save the start and end indices of the word
            start += len(word)  # Move past the word
        
        dictOfPositions[word] = positions
    return dictOfPositions