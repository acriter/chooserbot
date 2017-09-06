class Option:
    def __init__(self, validNames):
        self.votes = []
        self.totalBits = 0
        self.validNames = validNames
        self.name = validNames[0]
        
    def add_vote(self, vote):
        self.votes.append(vote)
        self.totalBits += vote.bitAmount
            
    def bits_for_user(self, userId):
        bits = 0
        for vote in self.votes:
            if vote.userId == userId:
                bits += vote.bitAmount
        return bits