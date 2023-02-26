#include <iostream>
#include <chrono>

#define Array(a, i)  ((unsigned)(((a) >> (60 - 4 * (i))) & 0xf))

class stopwatch
{
public:
    stopwatch() : start(std::chrono::high_resolution_clock::now()) {}
    ~stopwatch() {
        auto end = std::chrono::high_resolution_clock::now();
        std::cout << "Elapsed time: " << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << " ms" << std::endl;
    }
private:
    std::chrono::high_resolution_clock::time_point start;
};

/*
class Layer
{
public:
    Layer() : s1(0), s2(0), c1(false), c2(false), lut(nullptr) {}
    ~Layer() {}

    int comparator() { lut[Array(s1, 0) | (Array(s2, 0) << 4) | (c1 << 8) | (c2 << 9)]; }
private:
    unsigned int s1:4;
    unsigned int s2:4;
    bool c1;
    bool c2;
    uint64_t* lut;
};

class Function
{
public:

private:
    uint64_t* array;
};
*/

uint64_t* precalcArray(int n)
{
    uint64_t legality[n];
    
    for (int i = 0; i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            if ((i & (1 << j)) != 0)
            {
                legality[i] |= (1 << j);
                legality[i] |= (1 << (j + 4));
            }
        }
    }

    return;
}

uint64_t* precalcArray()
{
    uint64_t array[16][16][16][2][2];

    return;
}

int main(int argc, char** argv)
{
    std::cout << "Precaluating arrays..." << std::endl;
    stopwatch sw;
    precalcArray();
    sw.~stopwatch();
    
    return 0;
}