

from PhysicsTools.PatAlgos.tools.helpers import cloneProcessingSnippet,massSearchReplaceAnyInputTag
class HambSyst():
    def __init__(self , process , sequence , systlabel) :
        self.a = cloneProcessingSnippet( process , sequence , systlabel )
        massSearchReplaceAnyInputTag( self.a , "slimmedJets" , "slimmedJets" + systlabel )
