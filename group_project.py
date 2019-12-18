'''
@ author: Shahzeb Afroze

'''

import pulp

# Decison variables
# cohorts - only one index (cohort i) 
BC = {} # BBA binary
IC = {} # IBBA binary 
BCZ = {} # size of BBA cohort
ICZ = {} # size of IBBA cohort

# sections assigned or not
# 3 indexes (cohort i course c section j)
BSF = {} # binary 
BSW = {} # binary
ISF = {} # binary 
ISW = {} # binary

# If a course is taken by a cohort in the fall or winter
# 2 indexes (course c cohort i) 
BCF= {} # binary
BCW= {} # binary
ICF= {} # binary
ICW= {} # binary


# If a course is taken by a cohort during a particular time - 5 indexes 
# (cohort-i, section-j, 30 min increment-q, course-c, day-d)
BTF = {} # binary 
BTW = {} # binary
ITF = {} # binary
ITW = {} # binary

# Deviational Decision Variables for soft constraints (all positive) - 1 index
BOV = {} # dissatisfaction for BBA cohort i 
IOV = {} # dissatisfaction for IBBA cohort i 

# cohort i day d - 2 index
BFLD  = {} # BBA Fall number of Long Days
BWLD  = {} # BBA Winter number of Long Days
IFLD  = {} # IBBA Fall number of Long Days
IWLD  = {} # IBBA Winter number of Long Days

# cohort i on day d - 2 index
BFNS  = {} # BBA Fall number of No Sleep 
BWNS  = {} # BBA Winter number of No Sleep 
IFNS  = {} # IBBA Fall number of No Sleep 
IWNS  = {} # IBBA Winter number of No Sleep 

# cohort i on day d for increment q
BFB2B = {} # BBA Fall Back to Back
BWB2B = {} # BBA Winter Back to Back
IFB2B = {} # IBBA Fall Back to Back
IWB2B = {} # IBBA Winter Back to Back



B2B = {} # of Back to Back classes for cohort i on day d for increment q - 3 index
OB2B = {} # total back to back classes for cohort i - 1 index
PQ = {} # of non-high-quality professors for cohort i - 1 index

# Deviational variables between cohorts
DevOV_plus = {} # positive deviation for overall cohort
DevOV_negative = {} # negative deviation for overall cohort
DevLD_positive = {} # positive long day deviation
DevLD_negative = {} # negative long day deviation
DevNS_positive_ = {} # positive no sleep deivation
DevNS_negative = {}  # negative no sleep deviation
DevB2B_positive = {} # positive deviation between each cohort’s back to back class value
DevB2B_negative = {} # negative deviation between each cohort’s back to back class value
DevPQ_positive = {} # positive deviation between each cohort’s degree of professor quality
DevPQ_negative = {} # negative deviation between each cohort’s degree of professor quality}

'''
Non-Decision Variables:
Djc = {day d for section j in course c}
Sjc = {start time for section j in course c}
Ejc = {end time for section j in course c}
Ljc = {size in terms of 30-min increments of section j in course c} (3 hours = 6 increments)
Cjc = {max number of people in each section j for course c}
Pjc = {if professor for section j in course c won a TEA award} 
'''

# Create a new optimization milp to minimize deviation
milp = pulp.LpProblem("Scheduling", pulp.LpMinimize)

# Coefficients for the deviational variables
dev = [1, 1, 1, 2] # one variation, other could be that we keep 2 multiple for others leaving one option open


# fit the dictionaries

COHORT_NUMBER = 14 # MAX - insights
COURSE_NUMBER  = 5 # NEED TO BE CHANGED 
SECTIONS_OF_EACH_COURSE = 3 # NEED TO BE CHANGED
INCREMENT = 10 # NEED TO BE CHANGED

package = [BC, IC, BCZ, ICZ]
program = ['BBA', 'BBA', 'IBBA', 'IBBA']


# number of BBA cohorts i
for i in range(COHORT_NUMBER):
    BC[i] = pulp.LpVariable(f"BBA Cohort {i}", lowBound = 0, cat = "Integer")

# number of IBBA cohorts i 
for i in range(COHORT_NUMBER):
    IC[i] = pulp.LpVariable(f"IBBA Cohort {i}", lowBound = 0, cat = "Integer")
    
# number students in IBBA cohorts i 
for i in range(COHORT_NUMBER):
    BCZ[i] = pulp.LpVariable(f"IBBA Cohort {i}", lowBound = 0, cat = "Integer")

# number students in BBA cohorts i 
for i in range(COHORT_NUMBER):
    ICZ[i] = pulp.LpVariable(f"IBBA Cohort {i}", lowBound = 0, cat = "Integer")


    

# ---- NOTE: later will get converted to getting value from dictionary of courses

# ------------------------ SECTION ASSIGNMENT -------------------------------- #

#  sections assigned or not for each section j from course c for Fall cohort BBA
for i in range(COHORT_NUMBER):
    for c in range(COURSE_NUMBER):
        for j in range(SECTIONS_OF_EACH_COURSE):        
            BSF[i,j,c] = pulp.LpVariable(f"BBA Fall Cohort {i} section {j} course {c}", cat = "Binary")
        
        
#  sections assigned or not for each section j from course c for Winter cohort BBA
for i in range(COHORT_NUMBER):
    for c in range(COURSE_NUMBER):
        for j in range(SECTIONS_OF_EACH_COURSE):        
            BSW[i,j,c] = pulp.LpVariable(f"BBA Winter Cohort {i} section {j} course {c}", cat = "Binary")

#  sections assigned or not for each section j from course c for Fall cohort IBBA
for i in range(COHORT_NUMBER):
    for c in range(COURSE_NUMBER):
        for j in range(SECTIONS_OF_EACH_COURSE):        
            ISF[i,j,c] = pulp.LpVariable(f"IBBA Fall Cohort {i} section {j} course {c}", cat = "Binary")
        

#  sections assigned or not for each section j from course c for Winter cohort IBBA
for i in range(COHORT_NUMBER):
    for c in range(COURSE_NUMBER):
        for j in range(SECTIONS_OF_EACH_COURSE):        
            ISW[i,j,c] = pulp.LpVariable(f"IBBA Winter Cohort {i} section {j} course {c}", cat = "Binary")
                

# ------------------------ COURSE ASSIGNMENT -------------------------------- #

# If a course is taken by a cohort in the fall by BBA (course c cohort i)
for i in range(COHORT_NUMBER):
    for c in range(COURSE_NUMBER):
        BCF[i,c] = pulp.LpVariable(f"BBA Fall Cohort {i} course {c}", cat = "Binary")
 
# If a course is taken by a cohort in the Winter by BBA (course c cohort i)
for i in range(COHORT_NUMBER):
    for c in range(COURSE_NUMBER):
        BCW[i,c] = pulp.LpVariable(f"BBA Winter Cohort {i} course {c}", cat = "Binary")
 
# If a course is taken by a cohort in the fall by IBBA (course c cohort i)
for i in range(COHORT_NUMBER):
    for c in range(COURSE_NUMBER):
        ICF[i,c] = pulp.LpVariable(f"IBBA Fall Cohort {i} course {c}", cat = "Binary")
 
# If a course is taken by a cohort in the Winter by IBBA (course c cohort i)
for i in range(COHORT_NUMBER):
    for c in range(COURSE_NUMBER):
        ICW[i,c] = pulp.LpVariable(f"IBBA Winter Cohort {i} course {c}", cat = "Binary")
 

# --------------------------------- TIME AND SECTIONS --------------------------------- # 

# BBA taking class at particular times - FALL
for i in range(COHORT_NUMBER):
    for d in range(DAYS):
        for c in range(COURSE_NUMBER):
            for j in range(SECTIONS_OF_EACH_COURSE):  
                for q in range(INCREMENT):
                    BTF[i,j,c,d,q] = pulp.LpVariable(f"BBA Fall Cohort {i} section {j} course {c} on day {d} with {q} increments of 30 minuites", cat = "Binary")
        

# BBA taking class at particular times - WINTER
for i in range(COHORT_NUMBER):
    for d in range(DAYS):
        for c in range(COURSE_NUMBER):
            for j in range(SECTIONS_OF_EACH_COURSE):  
                for q in range(INCREMENT):
                    BTW[i,j,c,d,q] = pulp.LpVariable(f"BBA Winter Cohort {i} section {j} course {c} on day {d} with {q} increments of 30 minuites", cat = "Binary")
        



# IBBA taking class at particular times - FALL
for i in range(COHORT_NUMBER):
    for d in range(DAYS):
        for c in range(COURSE_NUMBER):
            for j in range(SECTIONS_OF_EACH_COURSE):  
                for q in range(INCREMENT):
                    ITF[i,j,c,d,q] = pulp.LpVariable(f"IBBA Fall Cohort {i} section {j} course {c} on day {d} with {q} increments of 30 minuites", cat = "Binary")
        


# BBA taking class at particular times - WINTER
for i in range(COHORT_NUMBER):
    for d in range(DAYS):
        for c in range(COURSE_NUMBER):
            for j in range(SECTIONS_OF_EACH_COURSE):  
                for q in range(INCREMENT):
                    ITW[i,j,c,d,q] = pulp.LpVariable(f"IBBA Winter Cohort {i} section {j} course {c} on day {d} with {q} increments of 30 minuites", cat = "Binary")
        


# --------------------------------- DEVIATIONAL VARIABLES --------------------------------- # 

# cohort i day d - 2 index
BFLD  = {} # BBA Fall number of Long Days
BWLD  = {} # BBA Winter number of Long Days
IFLD  = {} # IBBA Fall number of Long Days
IWLD  = {} # IBBA Winter number of Long Days

# cohort i on day d - 2 index
BFNS  = {} # BBA Fall number of No Sleep 
BWNS  = {} # BBA Winter number of No Sleep 
IFNS  = {} # IBBA Fall number of No Sleep 
IWNS  = {} # IBBA Winter number of No Sleep 

# cohort i on day d for increment q
BFB2B = {} # BBA Fall Back to Back
BWB2B = {} # BBA Winter Back to Back
IFB2B = {} # IBBA Fall Back to Back
IWB2B = {} # IBBA Winter Back to Back



# BBA cohort satisfaction
for i in range(COHORT_NUMBER):
    BOV[i] = pulp.LpVariable(f"BBA Cohort {i} Overall Dissatisfaction", cat = "Continuous")

# IBBA cohort satisfaction
for i in range(COHORT_NUMBER):
    IOV[i] = pulp.LpVariable(f"IBBA  Cohort {i} Overall Dissatisfaction", cat = "Continuous")



# cohort i day d - 2 index
BFLD  = {} # BBA Fall number of Long Days
BWLD  = {} # BBA Winter number of Long Days
IFLD  = {} # IBBA Fall number of Long Days
IWLD  = {} # IBBA Winter number of Long Days



# BBA Cohort Number of Long days
for i in range(COHORT_NUMBER):
    BFLD[i] = pulp.LpVariable(f"BBA Fall Cohort {i} total number of long days", cat = "Integer")

# IBBA Cohort Number of Long days
for i in range(COHORT_NUMBER):
    LD[i] = pulp.LpVariable(f"BBA Winter Cohort {i} total number of long days", cat = "Integer")


# BBA Cohort Number of No Sleep days
for i in range(COHORT_NUMBER):
    NS[i] = pulp.LpVariable(f"BBA Winter Cohort {i} total number of long days", cat = "Integer")

# IBBA Cohort Number of No Sleep days
for i in range(COHORT_NUMBER):
    NS[i] = pulp.LpVariable(f"IBBA Winter Cohort {i} total number of long days", cat = "Integer")



# BBA Back to Back 
for i in range(COHORT_NUMBER):
    for d in range(DAYS):
        for q in range(INCREMENT):
            B2B[i,d,q] = pulp.LpVariable(f"BBA Winter Cohort {i} total number of long days", cat = "Integer")

# IBBA Back to Back 
for i in range(COHORT_NUMBER):
    for d in range(DAYS):
        for q in range(INCREMENT):
            B2B[i,d,q] = pulp.LpVariable(f"IBBA Winter Cohort {i} total number of long days", cat = "Integer")


# Deviational Decision Variables for soft constraints (all positive)
BOV = {} # dissatisfaction for BBAcohort i - 1 index
IOV = {} # dissatisfaction for IBBA cohort i - 1 index


# Deviational variables between cohorts
DevOV_plus = {} # positive deviation for overall cohort
DevOV_negative = {} # negative deviation for overall cohort
DevLD_positive = {} # positive long day deviation
DevLD_negative = {} # negative long day deviation
DevNS_positive_ = {} # positive no sleep deivation
DevNS_negative = {}  # negative no sleep deviation
DevB2B_positive = {} # positive deviation between each cohort’s back to back class value
DevB2B_negative = {} # negative deviation between each cohort’s back to back class value
DevPQ_positive = {} # positive deviation between each cohort’s degree of professor quality
DevPQ_negative = {} # negative deviation between each cohort’s degree of professor quality}



  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    