#include <stdio.h>
#include <stdlib.h>

char isBigEndian() {
    short int b = 1;
    char* p = (char*) &b;
    return !(*p);
}

int htons(unsigned short int a) {
    // check system's endianness
    if (isBigEndian()) return a;

    //convert
    char* start = (char*) &a;
    char first = *start;
    char second = *(start+1);
    *start = second;
    *(start+1) = first;

    unsigned short int* aa = (unsigned short int*) start;
    return *aa;
}

int htonl(unsigned long a) {
    // check system's endianness
    if (isBigEndian()) return a;

    //convert
    char* number = (char*) &a;
    char newNumber[4];
    for (char i = 0; i < 4; i++) newNumber[i] = *(number+3-i);

    unsigned long* aa = (unsigned long*) newNumber;
    return *aa;
}

int main() {
    unsigned short int tmp1[1];
    printf("Inserisci un numero tra 0 e %d (unsigned short int): ", (unsigned short) USHRT_MAX);
    scanf("%hd", tmp1);
    unsigned short int a1 = *tmp1;
    a1 = htons(a1);
    printf("Il tuo unsigned short int in formato big endian è %d.\n", a1);

    unsigned long tmp2[1];
    printf("Inserisci un numero tra 0 e %lu (unsigned long): ", (unsigned long) ULONG_MAX);
    scanf("%lu", tmp2);
    unsigned long a2 = *tmp2;
    a2 = htonl(a2);
    printf("Il tuo unsigned long in formato big endian è %lu.\n", a2);
}