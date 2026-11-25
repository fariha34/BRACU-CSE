
#ifndef SCOPE_TABLE_H
#define SCOPE_TABLE_H
#include "symbol_info.h"

class scope_table
{
private:
    int bucket_count;
    int unique_id;
    scope_table *parent_scope = NULL;
    vector<list<symbol_info *>> table;

    int hash_function(string name)
    {
        // write your hash function here
        unsigned long sum=0;
        for (size_t i=0; i< name.size(); i++)
           sum += (unsigned char) name[i];
        return (int)(sum % bucket_count);
    }

public:
    scope_table();
    scope_table(int bucket_count, int unique_id, scope_table *parent_scope);
    scope_table *get_parent_scope();
    int get_unique_id();
    symbol_info *lookup_in_scope(symbol_info* symbol);
    bool insert_in_scope(symbol_info* symbol);
    bool delete_from_scope(symbol_info* symbol);
    void print_scope_table(ofstream& outlog);
    ~scope_table();

    // you can add more methods if you need
};

// complete the methods of scope_table class
scope_table::scope_table()
{
    this->bucket_count=10;
    this->unique_id=0;
    this->parent_scope=NULL;
    table.resize(bucket_count);
}
scope_table::scope_table(int bucket_count, int unique_id, scope_table *parent_scope)
{
    this->bucket_count=bucket_count;
    this->unique_id=unique_id;
    this->parent_scope=parent_scope;
    table.resize(bucket_count);
}
scope_table*scope_table::get_parent_scope()
{
    return parent_scope;
}

int scope_table::get_unique_id()
{
    return unique_id;
}
symbol_info*scope_table::lookup_in_scope(symbol_info* symbol)
{
    int idx=hash_function(symbol->get_name());
    for (symbol_info*s : table[idx])
       if (s->get_name()==symbol->get_name())
         return s;
    return NULL;
}
bool scope_table::insert_in_scope(symbol_info* symbol)
{
    if (lookup_in_scope(symbol)!=NULL)
       return false;
    table [hash_function(symbol->get_name())].push_back(symbol);
    return true;

}
bool scope_table::delete_from_scope(symbol_info* symbol)
{
    int idx= hash_function(symbol->get_name());
    for (list<symbol_info*>::iterator it= table[idx].begin();
          it !=table[idx].end();++it)
    {
        if ((*it)->get_name()==symbol->get_name())
        {
            symbol_info*stored=*it;
            table[idx].erase(it);
            delete stored;
            return true;
        }
    }
    return false;
}

void scope_table::print_scope_table(ofstream& outlog)
{
    outlog << "ScopeTable # "+ to_string(unique_id) << endl;

    //iterate through the current scope table and print the symbols and all relevant information
     for (int i=0; i< bucket_count;i++)
     {
        if (table[i].empty())
            continue;
        outlog <<i<< " --> " << endl;
        for (symbol_info*s : table[i])
            s->print_details(outlog);
     }
     outlog <<endl;
}

scope_table::~scope_table()
{
    for (int i=0; i<bucket_count;i++)
       for (symbol_info*s :table[i])
            delete s;
}
#endif