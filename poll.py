import option as o

class Poll:
    def __init__(self, optionList):
        self.optionList = []
        idx = 0
        for option in optionList:
            self.optionList.append(o.Option([option, str(idx)]))
            idx += 1
    
    def add_vote(self, option, vote):
        option.add_vote(vote)

    def winning_option(self):
    	#TODO: mention ties / add tie-breakers
    	highest = 0
    	winner = self.optionList[0]
    	for option in self.optionList:
    		if option.totalBits > highest:
    			winner = option
    			highest = option.totalBits
    	return winner

        