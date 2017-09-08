import option as o

class Poll:
    def __init__(self, question):
        self.question = question
        self.optionList = []

    def set_options(self, optionList):
        idx = 0
        for option in optionList:
            self.optionList.append(o.Option([option, str(idx)]))
            idx += 1

    def add_vote(self, option, vote):
        option.add_vote(vote)

    def has_started(self):
        return bool(len(self.optionList))

    def winning_option(self):
    	#TODO: mention ties / add tie-breakers
    	highest = 0
    	winner = self.optionList[0]
    	for option in self.optionList:
    		if option.totalBits > highest:
    			winner = option
    			highest = option.totalBits
    	return winner

        