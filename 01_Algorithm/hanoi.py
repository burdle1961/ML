def TowerOfHanoi(n , s_pole, d_pole , i_pole):

    if n == 1:
        print("Move disc 1 from pole",s_pole,"to pole",d_pole)
        return

    TowerOfHanoi(n-1, s_pole, i_pole, d_pole)
    print("Move disc",n,"from pole",s_pole,"to pole",d_pole)
    TowerOfHanoi(n-1, i_pole, d_pole, s_pole)
 
n = 10

TowerOfHanoi(n, 'A', 'C', 'B')

# A, C, B are the name of poles
# A : start pole, B : Intermediate pole, C : Destination pole
