class ExpenseCategorizer:
    def __init__(self):
        # Initial rule-based mapping
        self.rules = {
            'food': ['pizza', 'burger', 'restaurant', 'cafe', 'grocery', 'starbucks', 'mcdonalds', 'dinner', 'lunch'],
            'travel': ['uber', 'lyft', 'taxi', 'bus', 'train', 'flight', 'gas', 'fuel', 'petrol'],
            'bills': ['rent', 'electricity', 'water', 'internet', 'phone', 'subscription', 'netflix', 'spotify'],
            'shopping': ['amazon', 'walmart', 'target', 'clothing', 'shoes', 'electronics', 'mall'],
            'entertainment': ['movie', 'cinema', 'game', 'concert', 'theater']
        }

    def categorize(self, text):
        text = text.lower()
        for category, keywords in self.rules.items():
            if any(keyword in text for keyword in keywords):
                return category.capitalize()
        return "Other"
