// g++ -o libpyc.so -shared -fPIC pyctest.cpp
// g++ -o libpyc.so -shared -fPIC -std=c++11 pyctest.cpp
#include <iostream>
#include <memory.h>
using namespace std;
#define CCALL extern "C"
#define SIZE_ID 20
typedef struct KeyValue
{
    KeyValue()
    {
      memset(achKey, 0, sizeof(achKey));
      memset(achValue, 0, sizeof(achValue));
      nLen = 0;
    }
    char achKey[1024];
    char achValue[1024];
    int  nLen;
}TKeyValue;
typedef struct PycPointer
{
    PycPointer()
    { 
      number = 0;
      id = nullptr;

    }
    char* id;
    int number;
}TcPointer;

CCALL int add(int &a, int b)
{
    cout<<"add: \n input args:" << a << "+" <<b << " = " << a + b << endl;
    return a + b;
}
CCALL float sub(float *num1, float num2)
{
    cout << "sub:\n input args:" << *num1 << "-" << num2 << " = ";
    float sub_res = *num1 - num2;
    cout << sub_res << endl;
    return sub_res;
}
CCALL TKeyValue GetKeyValue(TKeyValue kv)
{
    char testkey[100] = "TEST_KEY";
    char testval[100] = "TEST_VALUE";
    memcpy(kv.achKey, testkey, sizeof(testkey));
    memcpy(kv.achValue, testval, sizeof(testval));
    kv.nLen = 99;
    return kv;
}
CCALL int GetCPointer(TcPointer* cpointer)
{
    const char* pszSrc = "Hello pyc";
    cpointer->id = (char*)malloc( sizeof(char) * ( SIZE_ID + 1 ) );
    cpointer->number = 8;
    memset( cpointer->id, 0, SIZE_ID + 1);
    strcpy( cpointer->id, pszSrc );
    cout << "cpointer:" << (cpointer->id) <<","<< cpointer->number << endl;
    return 0;
}
CCALL char* GetCPointer1(TcPointer* cpointer, int size)
{
    const char* pszSrc = "python c++ dll.";
    cpointer->id = (char*)malloc( sizeof(char) * ( size + 1 ) );
    cpointer->number = 8;
    memset( cpointer->id, 0, size + 1);
    strcpy( cpointer->id, pszSrc );
    cout << "cpointer1:" << (cpointer->id) <<","<< cpointer->number << endl;
    char* pres = (char*)malloc( sizeof(char) * ( size + 1 ) );
    strcpy( pres, cpointer->id);
    
    return pres;
}