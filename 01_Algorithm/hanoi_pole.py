pole = {'A':[], 'B':[], 'C':[]}

def TowerOfHanoi(n , s_pole, d_pole , i_pole):

    if n == 1:
        #print("-Move disc 1 from pole",s_pole,"to pole",d_pole)
        pole[d_pole].append(pole[s_pole].pop())
        print ('A : ', pole['A'], '\t\t','B : ',pole['B'], '\t\t','C : ',pole['C'])
        return

    TowerOfHanoi(n-1, s_pole, i_pole, d_pole)
    
    #print("+Move disc",n,"from pole",s_pole,"to pole",d_pole)
    pole[d_pole].append(pole[s_pole].pop())
    print ('A : ', pole['A'], '\t\t','B : ',pole['B'], '\t\t','C : ',pole['C'])

    TowerOfHanoi(n-1, i_pole, d_pole, s_pole)
 
pole['A'] = [3,2,1]
# pole['A'] = [1,2,3,4,5]

n = len(pole['A'])

# what if n < length of pole['A']?
# n = 3

print ('A : ', pole['A'], '\t\t','B : ',pole['B'], '\t\t','C : ',pole['C'])

TowerOfHanoi(n, 'A', 'C', 'B')
# A, C, B are the name of poles
