# Python implementation of Naive method
# to print all divisors
  
# method to print the divisors
def printDivisors(n) :
    i = 1
    while i <= n :
        if (n % i==0) :
            print (i,end=" ")
        i = i + 1
          
# Driver method
print ("The divisors of 100 are: ")
printDivisors(738)
  
#This code is contributed by Nikita Tiwari.