
class IdeaSelector():
    
    def instantiateService(self, language, location):
        pass #instantiate API service and set Language and location 
    
    def get_ideas(self, keyweords, iterations):
        pass # this should return a dictionary of {<original_keyword>: {'keyword': STRING, 'Rank': INT, 'SearchVolume': INT, 'AverageCPC': FLOAT, 'Competition': INT, DUPE: FLOAT}



class IdeasIterator():
    
    def __init__(self, results_per_request = 10,  iterations = 5, language = 'English', localtion = 'UK'):
        self.results_per_request = results_per_request
        self.iterations = iterations
        self.language = language
        self.localtion
        self.output_path = ''
        
    
    def run(self, keywords):
        next_keywords = [keywords]
        for i in self.iterations:
            new_selector = IdeaSelector()
            new_selector.instantiateService(self.language, self.location)
            this_ideas = new_selector.get_ideas(keywords, self.iterations)
            next_keywords = [x['keyword'] for x in this_ideas.values()]
            self.write_in_csv(this_ideas, i)
    
    def write_in_csv(self, res_dic, iteration):
        pass
            
            
            
if __name__ == '__main__':
    
    #arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', "--keyword", help="The keyword you want to start with")
    parser.add_argument('-i', "--iterations", default = 5, help="Number of iteration. If not given it will defaults to 5")
    parser.add_argument("--r", "--results", defaukt = 10, help="Number of results per iteration. If not given it will default to 10")
    parser.add_argument("--ln", "--language", default = 'English', help="Language. If not entered it will default to English")
    parser.add_argument("--lc", "--location", default = 'UK', help="Location. If not entered it will default to UK")
    args = parser.parse_args()
    
    
    
    ideas = IdeasIterator(args.results, args.iterations, args.language, args.localtion)                   
    ideas.run(args.keyword)