#include <iostream.h>
#include <math.h>
#include <time.h>
#include "complex.C"
#include "util.C"

int main() {
    //Establish a random seed.
    srand(time(NULL));
    
    //Output standard greeting.
    cout << "Welcome to the simulation of Shor’s algorithm." << endl
        << "There are four restrictions for Shor’s algorithm:" << endl
        << "1) The number to be factored must be >= 15." << endl
        << "2) The number to be factored must be odd." << endl
        << "3) The number must not be prime." << endl
        << "4) The number must not be a prime power." << endl
        << endl << "There are efficient classical methods of factoring "
        << "any of the above numbers, or determining that they are prime."
        << endl << endl << "Input the number you wish to factor." << endl
        << flush;

    //n is the number we are going to factor, get n.
    int n;
    cin >> n;
    
    //Test to see if n is factorable by Shor’s algorithm.
    //Exit if the number is even.
    if (n%2 == 0) {
        cout << "Error, the number must be odd!" << endl << flush;
        exit(0);
    }
    
    //Exit if the number is prime.
    if (TestPrime(n)) {
        cout << "Error, the number must not be prime!" << endl << flush;
        exit(0);
    }

    //Prime powers are prime numbers raised to integral powers.
    //Exit if the number is a prime power.
    if (TestPrimePower(n)) {
        cout << "Error, the number must not be a prime power!" << endl << flush;
        exit(0);
    }
    
    //Now we must pick a random integer x, coprime to n. Numbers are
    //coprime when their greatest common denominator is one. One is not
    //a useful number for the algorithm.
    int x = 0;
    x = 1+ (int)((n-1)*(double)rand()/(double)RAND_MAX);
    while (GCD(n,x) != 1 || x == 1) {
        x = 1 + (int)((n-1)*(double)rand()/(double)RAND_MAX);
    }
    cout << "Found x to be " << x << "." << endl << flush;
    //Now we must figure out how big a quantum register we need for our
    //input, n. We must establish a quantum register big enough to hold
    //an equal superposition of all integers 0 through q - 1 where q is
    //the power of two such that n^2 <= q < 2n^2.
    int q;
    q = GetQ(n);
    cout << "Found q to be " << q << "." << endl << flush;

    //Create the register.
    QuReg * reg1 = new QuReg(RegSize(q) - 1);
    cout << "Made register 1 with register size = " << RegSize(q) << endl
        << flush;
    
    //This array will remember what values of q produced for x^q mod n.
    //It is necessary to retain these values for use when we collapse
    //register one after measuring register two. In a real quantum
    //computer these registers would be entangled, and thus this extra
    //bookkeeping would not be needed at all. The laws of quantum
    //mechanics dictate that register one would collapse as well, and
    //into a state consistent with the measured value in resister two.
    int * modex = new int[q];

    //This array holds the probability amplitudes of the collapsed state
    //of register one, after register two has been measured it is used
    //to put register one in a state consistent with that measured in
    //register two.
    Complex *collapse = new Complex[q];

    //This is a temporary value.
    Complex tmp;

    //This is a new array of probability amplitudes for our second
    //quantum register, that populated by the results of x^a mod n.
    Complex *mdx = new Complex[(int)pow(2,RegSize(n))];

    // This is the second register. It needs to be big enough to hold
    // the superposition of numbers ranging from 0 -> n - 1.
    QuReg *reg2 = new QuReg(RegSize(n));
    cout << "Created register 2 of size " << RegSize(n) << endl << flush;

    //This is a temporary value.
    int tmpval;

    //This is a temporary value.
    int value;

    //c is some multiple lambda of q/r, where q is q in this program,
    //and r is the period we are trying to find to factor n. m is the
    //value we measure from register one after the Fourier
    //transformation.
    double c,m;

    //This is used to store the denominator of the fraction p / den where
    //p / den is the best approximation to c with den <= q.
    int den;
    
    //This is used to store the numerator of the fraction p / den where
    //p / den is the best approximation to c with den <= q.
    int p;

    //The integers e, a, and b are used in the end of the program when
    //we attempts to calculate the factors of n given the period it
    //measured.
    //Factor is the factor that we find.
    int e,a,b, factor;

    //Shor’s algorithm can sometimes fail, in which case you do it
    //again. The done variable is set to 0 when the algorithm has
    //failed. Only try a maximum number of tries.
    int done = 0;
    int tries = 0;
    while (!done) {
        if (tries >= 5) {
            cout << "There have been five failures, giving up." << endl << flush;
            exit(0);
        }
        
        //Now populate register one in an even superposition of the
        //integers 0 -> q - 1.
        reg1->SetAverage(q - 1);

        //Now we preform a modular exponentiation on the superposed
        //elements of reg 1. That is, perform x^a mod n, but exploiting
        //quantum parallelism a quantum computer could do this in one
        //step, whereas we must calculate it once for each possible
        //measurable value in register one. We store the result in a new
        //register, reg2, which is entangled with the first register.
        //This means that when one is measured, and collapses into a base
        //state, the other register must collapse into a superposition of
        //states consistent with the measured value in the other.. The
        //size of the result modular exponentiation will be at most n, so
        //the number of bits we will need is therefore less than or equal
        //to log2 of n. At this point we also maintain a array of what
        //each state produced when modularly exponised, this is because
        //these registers would actually be entangled in a real quantum
        //computer, this information is needed when collapsing the first
        //register later.
        
        //This counter variable is used to increase our probability amplitude.
        tmp.Set(1,0);

        //This for loop ranges over q, and puts the value of x^a mod n in
        //modex[a]. It also increases the probability amplitude of the value
        //of mdx[x^a mod n] in our array of complex probabilities.
        for (int i = 0 ; i < q ; i++) {
            //We must use this version of modexp instead of c++ builtins as
            //they overflow when x^i > 2^31.
            tmpval = modexp(x,i,n);
            modex[i] = tmpval;
            mdx[tmpval] = mdx[tmpval] + tmp;
        }

        //Set the state of register two to what we calculated it should be.
        reg2->SetState(mdx);
        
        //Normalise register two, so that the probability of measuring a
        //state is given by summing the squares of its probability
        //amplitude.
        reg2->Norm();

        //Now we measure reg1.
        value = reg2->DecMeasure();

        //Now we must using the information in the array modex collapse
        //the state of register one into a state consistent with the value
        //we measured in register two.
        for (int i = 0 ; i < q ; i++) {
            if (modex[i] == value) {
                collapse[i].Set(1,0);
            } else {
                collapse[i].Set(0,0);
            }
        }

        //Now we set the state of register one to be consistent with what
        //we measured in state two, and normalise the probability
        //amplitudes.
        reg1->SetState(collapse);
        reg1->Norm();

        //Here we do our Fourier transformation.
        cout << "Begin Discrete Fourier Transformation!" << endl << flush;
        DFT(reg1, q);

        //Next we measure register one, due to the Fourier transform the
        //number we measure, m will be some multiple of lambda/r, where
        //lambda is an integer and r is the desired period.
        m = reg1->DecMeasure();

        //If nothing goes wrong from here on out we are done.
        done = 1;
        
        //If we measured zero, we have gained no new information about the
        //period, we must try again.
        if (m == 0) {
            cout << "Measured, 0 this trial a failure!" << endl << flush;
            done = 0;
        }

        //The DecMeasure subroutine will return -1 as an error code, due
        //to rounding errors it will occasionally fail to measure a state.
        if (m == -1) {
            cout << "We failed to measure anything, this trial a failure!" << " Trying again." << endl << flush;
            done = 0;
        }

        //If nothing has gone wrong, try to determine the period of our
        //function, and get factors of n.
        if (done) {
            //Now c =~ lambda / r for some integer lambda. Borrowed with
            //modifications from Berhnard Ohpner.
            c = (double)m / (double)q;
            
            //Calculate the denominator of the best rational approximation
            //to c with den < q. Since c is lambda / r for some integer
            //lambda, this will provide us with our guess for r, our period.
            den = denominator(c, q);

            //Calculate the numerator from the denominator.
            p = (int)floor(den * c + 0.5);

            //Give user information.
            cout << "measured " << m <<", approximation for " << c << " is " << p << " / " << den << endl << flush;

            //The denominator is our period, and an odd period is not
            //useful as a result of Shor’s algorithm. If the denominator
            //times two is still less than q we can use that.
            if (den % 2 == 1 && 2 * den < q ){
                cout << "Odd denominator, expanding by 2\n";
                p = 2 * p;
                den = 2 * den;
            }

            //Initialise helper variables.
            e = a = b = factor = 0;
            
            // Failed if odd denominator.
            if (den % 2 == 1) {
                cout << "Odd period found. This trial failed." << " Trying again." << endl << flush;
                done = 0;
            } else {
                //Calculate candidates for possible common factors with n.
                cout << "possible period is " << den << endl << flush;
                e = modexp(x, den / 2, n);
                a = (e + 1) % n;
                b = (e + n - 1) % n;
                cout << x << "^" << den / 2 << " + 1 mod " << n << " = " << a
                << "," << endl
                << x << "^" << den / 2 << " - 1 mod " << n << " = " << b
                << endl << flush;
                factor = max(GCD(n,a),GCD(n,b));
            }
        }

        //GCD will return a -1 if it tried to calculate the GCD of two
        //numbers where at some point it tries to take the modulus of a
        //number and 0.
        if (factor == -1) {
            cout << "Error, tried to calculate n mod 0 for some n. Trying again." << endl << flush;
            done = 0;
        }

        if ((factor == n || factor == 1) && done == 1) {
            cout << "Found trivial factors 1 and " << n
            << ". Trying again." << endl << flush;
            done = 0;
        }

        //If nothing else has gone wrong, and we got a factor we are
        //finished. Otherwise start over.
        if (factor != 0 && done == 1) {
            cout << n << " = " << factor << " * " << n / factor << endl << flush;
        } else if (done == 1) {
            cout << "Found factor to be 0, error. Trying again." << endl
            << flush;
            done = 0;
        }
        tries++;
    }
    delete reg1;
    delete reg2;
    delete [] modex;
    delete [] collapse;
    delete [] mdx;
    return 1;
}
