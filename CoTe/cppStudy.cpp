#include<iostream>
#include<list>
 
using namespace std;
 
//100과 200사이이면 true 
bool predicate(int num){
    return num>=10 && num<=20;
}
int main(void){
    list<int> lt;
    
    lt.push_back(10);
    lt.push_back(23);
    lt.push_back(44);
    lt.push_back(20);
    lt.push_back(1);

    cout << "lt is:";
    list<int>::iterator iter;
    for(iter=lt.begin(); iter!=lt.end(); iter++){
        cout << *iter << " ";
    }
    
    cout << endl << endl;
    cout << lt.front();
    
    
    // for(iter=lt.begin();i!=)
    return 0;    
}


