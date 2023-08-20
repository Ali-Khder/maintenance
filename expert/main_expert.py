from experta import *


# Define your facts
class Symptom(Fact):
    pass


class Diagnosis(Fact):
    pass


class RobotCrossStreet(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.matched_rules = []

    @Rule(Symptom('cough'))
    def rule1(self):
        self.matched_rules.append('تبديل زيت بالسرعة القصوى')
        self.declare(Diagnosis('common_cold'))

    @Rule(Symptom('fever') & Symptom('rash'))
    def rule2(self):
        self.matched_rules.append('أوقف السيارة واتصل بطوارئ الصيانة لدينا أو أقرب مركز صيانة، لديك خلل في المحرك')
        self.declare(Diagnosis('measles'))

    # @Rule(AS.f1 << Symptom(MATCH.symptom1) & AS.f2 << Symptom(MATCH.symptom2) & NOT(Diagnosis()))
    # def rule3(self, f1, f2, symptom1, symptom2):
    #     self.matched_rules.append('rule3')
    #     self.declare(Diagnosis('unknown'))


