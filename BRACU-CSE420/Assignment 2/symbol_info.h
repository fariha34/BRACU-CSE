#ifndef SYMBOL_INFO_H
#define SYMBOL_INFO_H
#include<bits/stdc++.h>
using namespace std;

class symbol_info
{
private:
    string name;
    string type;

    // Write necessary attributes to store what type of symbol it is (variable/array/function)
    // Write necessary attributes to store the type/return type of the symbol (int/float/void/...)
    // Write necessary attributes to store the parameters of a function
    // Write necessary attributes to store the array size if the symbol is an array
    string kind;
    string data_type;
    int array_size;
    vector<string> param_names;
    vector<string> param_types;
    

public:
    symbol_info(string name, string type)
    {
        this->name = name;
        this->type = type;
        this->kind="";
        this->data_type="";
        this->array_size=0;
    }
    string get_name()
    {
        return name;
    }
    string get_type()
    {
        return type;
    }
    void set_name(string name)
    {
        this->name = name;
    }
    void set_type(string type)
    {
        this->type = type;
    }
    // Write necessary functions to set and get the attributes
     void set_as_variable(string dtype)
    {
        kind="variable";
        data_type=dtype;
    }
     void set_as_array(string dtype,int size)
    {
        kind="array";
        data_type=dtype;
        array_size= size;
    }
     void set_as_function(string return_type)
    {
        kind="function";
        data_type=return_type;
    }
    
    string get_kind()
    {
        return kind;
    }
    bool is_variable()
    {
        return kind=="variable";
    }
    bool is_array()
    {
        return kind=="array";
    }
    bool is_function()
    {
        return kind=="function";
    }
    string get_data_type()
    {
        return data_type;
    }
    string get_return_type()
    {
        return data_type;
    }
    void set_data_type(string dtype)
    {
        data_type=dtype;
    }

    int get_array_size()
    {
        return array_size;
    }
    void set_array_size(int size)
    {
        array_size= size;
    }
    void add_parameter(string ptype, string pname)
    {
        param_names.push_back(pname);
        param_types.push_back(ptype);

    }
    string get_param_name(int i)
    {
        return param_names[i];
    }
        string get_param_type(int i)
    {
        return param_types[i];
    }
    int get_param_count()
    {
        return (int)param_types.size();
    }
    void print_details(ofstream& outlog)
    {
        outlog << "< " << name << " : " <<type <<" >\n";
        if (is_function())
        {
            outlog<<"Function Definition\nReturn Type: "<< data_type
                  <<"\nNo. of Parameters: "<< param_types.size()
                  <<"\nParameter Details: ";
            for (size_t i=0; i<param_types.size();i++)
            {
                if (i)outlog<< ", ";
                outlog <<param_types[i];
                if (!param_names[i].empty())
                 outlog << " " <<param_names[i];
            }
            outlog << "\n";
        }
        else if (is_array())
        {
            outlog <<"Array" <<endl;
            outlog <<"Type:" <<data_type<< endl;
            outlog <<"Size:" <<array_size<<endl<<endl;
        }
        else
        {
            outlog <<"Variable" <<endl;
            outlog <<"Type:" <<data_type<<endl<<endl;
        }
    }
    ~symbol_info()
    {
        // Write necessary code to deallocate memory, if necessary
    }
};
#endif