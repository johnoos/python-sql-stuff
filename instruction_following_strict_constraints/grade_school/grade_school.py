class School:
    def __init__(self):
        self.roster_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
        self.added_all_grades = []

    def add_student(self, name, grade):
        complete_list = []
        for t in range(7):
            complete_list += self.roster_dict[t+1]
        if name in complete_list:
            self.added_all_grades.append(False)
            return False
        else: 
            self.roster_dict[grade].append(name)
            self.added_all_grades.append(True)
            return True 

    def roster(self):
        returned_list = []
        for g in range(7):
            if self.roster_dict[g+1] != []:
                returned_list.extend(sorted(self.roster_dict[g+1]))
        return returned_list    
            
    def grade(self, grade_number):
        return sorted(self.roster_dict[grade_number])

    def added(self):
        return self.added_all_grades
     