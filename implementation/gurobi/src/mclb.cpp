/*
Copyright (c) 2024 Purdue University
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met: redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer;
redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution;
neither the name of the copyright holders nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Authors: Conor Green
*/

#undef _GLIBCXX_USE_CXX11_ABI
#define _GLIBCXX_USE_CXX11_ABI 0

#include "gurobi_c++.h"
#include <string.h>
#include <fstream>
#include <cstdlib>
#include <math.h>
// #include <cassert>
#include <vector>
#include <list>
#include <sstream>
#include <algorithm>

using namespace std;

#define MAX_STR_LEN 300

// Enums for CLAs
enum Objective {
    TEST,
    MIN_CLOAD,
    MAX_MIN_CLOAD
};



bool
is_exterior(int node, int per_row, bool is_noci){

    // for noci, the 64 noc are not considered exterior
    if(is_noci && node >= 20){
        return false;
    }

    // lefts
    if (node % per_row == 0){
        return true;
    }
    // rights
    else if (node % per_row == per_row - 1)
    {
        return true;
    }
    return false;
}


void set_maxmincload_objective(GRBModel &model,
                        GRBVar maxcload,
                        GRBVar maxmemcload,
                        bool mem_traf_priority)
{
    try{

        // Expressions
        // ------------------------------------------------------------------
        


        if (mem_traf_priority){
            // primary
            model.setObjectiveN(maxmemcload, 0, 3);

            // secondary
            model.setObjectiveN(maxcload, 1, 2);

        }
        else{
            GRBLinExpr maxcload_expr = maxcload;

            model.setObjective(maxcload_expr, GRB_MINIMIZE);


        }

    }// end try

    catch(GRBException e){
        cout << "Obj err"<<endl;
        cout << "Error code = " << e.getErrorCode() << endl;
        cout << e.getMessage() << endl;
    }
    catch (...) {
        cout << "Exception during optimization" << endl;
    }

}


void set_maxmincload_objective_memcoh_priority(GRBModel &model,
                        GRBVar maxcohcload,
                        GRBVar maxmemcload)
{
    try{

        // Expressions
        // ------------------------------------------------------------------

        GRBLinExpr max_coh_cload_expr = maxcohcload;
        GRBLinExpr max_mem_cload_expr = maxmemcload;

        // model.setObjective(max_coh_cload_expr, GRB_MINIMIZE);

        // primary
        model.setObjectiveN(max_mem_cload_expr, 0, 1);

        // secondary
        model.setObjectiveN(max_coh_cload_expr, 1, 0);


    }// end try

    catch(GRBException e){
        cout << "Obj err"<<endl;
        cout << "Error code = " << e.getErrorCode() << endl;
        cout << e.getMessage() << endl;
    }
    catch (...) {
        cout << "Exception during optimization" << endl;
    }

}


void set_maxmincload_objective_cohmem_priority(GRBModel &model,
                        GRBVar maxcohcload,
                        GRBVar maxmemcload)
{
    try{

        // Expressions
        // ------------------------------------------------------------------

        GRBLinExpr max_coh_cload_expr = maxcohcload;
        GRBLinExpr max_mem_cload_expr = maxmemcload;

        model.setObjective(max_coh_cload_expr, GRB_MINIMIZE);

        // primary
        model.setObjectiveN(max_coh_cload_expr, 0, 1);

        // secondary
        model.setObjectiveN(max_mem_cload_expr, 1, 0);


    }// end try

    catch(GRBException e){
        cout << "Obj err"<<endl;
        cout << "Error code = " << e.getErrorCode() << endl;
        cout << e.getMessage() << endl;
    }
    catch (...) {
        cout << "Exception during optimization" << endl;
    }

}


void set_maxmincload_objective_cohmemplus_priority(GRBModel &model,
                        GRBVar maxcohcload,
                        GRBVar maxcload)
{
    try{

        // Expressions
        // ------------------------------------------------------------------

        GRBLinExpr max_coh_cload_expr = maxcohcload;
        GRBLinExpr max_cload_expr = maxcload;

        model.setObjective(max_coh_cload_expr, GRB_MINIMIZE);

        // primary
        model.setObjectiveN(max_coh_cload_expr, 0, 1);

        // secondary
        model.setObjectiveN(max_cload_expr, 1, 0);


    }// end try

    catch(GRBException e){
        cout << "Obj err"<<endl;
        cout << "Error code = " << e.getErrorCode() << endl;
        cout << e.getMessage() << endl;
    }
    catch (...) {
        cout << "Exception during optimization" << endl;
    }

}

void print_to_file(GRBModel &model,
                    string outfile_name,
                    int n_routers)
{

    try{
        string s;

        ofstream outfile(outfile_name);

        GRBVar var;

        // logfile->open(logfile_name);

        // write scalars
        // -------------
        // *logfile << n_routers << endl<<n_ports<<endl<<longest_link<<endl;
        // outfile << n_routers << endl<<n_ports<<endl<<longest_link<<endl;



        cout << "Writing to " <<outfile_name <<endl;

        for(int src=0; src<n_routers; src++){
            for(int d=0; d<n_routers; d++){
                
                // if(mem_only && !is_exterior(d, per_row)){
                //     continue;
                // }
                
                int cur = src;

                int iters = 0;

                vector < int > bad_dests;

                vector < int > path;
                path.push_back(cur);
                while(cur != d){
                    // cout << "cur="<<cur<<". dest="<<d<<endl;
                    for(int i=0; i<n_routers; i++){

                        if (find(bad_dests.begin(), bad_dests.end(),i) != bad_dests.end())continue;

                        s = "flow_load_n" + to_string(src) + "_n" + to_string(d) +
                            "_r" + to_string(cur) + "_r" + to_string(i);
                        GRBVar var = model.getVarByName(s);
                        if(var.get(GRB_DoubleAttr_X) != 0.0){
                            cur = i;
                            break;
                        }
                    }
                    path.push_back(cur);

                    iters +=1;
                    if (iters >= 20){
                        bad_dests.push_back(cur);
                        cur = src;
                        iters = 0;
                    }


                }

                // print it
                outfile<<"[";
                int path_len = path.size();
                for(int i=0;i<path_len;i++){
                    outfile << path.at(i);
                    if(i!=path_len-1){
                        outfile<< ", ";
                    } 
                }

                outfile << "]" << endl;
            }
        }



        outfile.close();

        
    }
    catch (GRBException e) {
        cout << "Error number: " << e.getErrorCode() << endl;
        cout << e.getMessage() << endl;
    }
    catch(...){
        cout << "Error during incumbent solution callback." << endl;
    }
}


void print_to_console(GRBModel &model,
                        int** topo_map,
                        int n_routers)
{

    string s;
    bool toggle;

    cout << endl;

    GRBVar tmp = model.getVarByName("max_cload");
    cout << "max cload = "<< tmp.get(GRB_DoubleAttr_X)  <<endl;

    tmp = model.getVarByName("max_mem_cload");
    cout << "max mem cload = "<< tmp.get(GRB_DoubleAttr_X)  <<endl;

    tmp = model.getVarByName("max_coh_cload");
    cout << "max coh cload = "<< tmp.get(GRB_DoubleAttr_X)  <<endl;

    cout << endl;
    cout << "flow_load ("<<n_routers<<"x"<<n_routers<<"x"<<
            n_routers<<"x"<<n_routers<<")"<<endl;

    for(int i=0; i<n_routers; i++){
        toggle = 0;
        for(int j=0; j<n_routers; j++){
            
            for(int k=0; k<n_routers; k++){
                // if(i==k)continue;
                for(int l=0; l<n_routers; l++){

                    s = "flow_load_n" + to_string(i) + "_n" + to_string(j) +
                        "_r" + to_string(k) + "_r" + to_string(l);

                    GRBVar var = model.getVarByName(s);
                    if(var.get(GRB_DoubleAttr_X) != 0.0){
                        cout<<"flow n"<<i<<"->n"<<j<<" : "<<"r"<<k<<"r"<<l<<" : "<<var.get(GRB_DoubleAttr_X)<<endl;
                    }

                }
            }
        }
    }
    cout<<endl;

    cout << endl;
    cout << "cload ("<<n_routers<<"x"<<n_routers<<")"<<endl;

    for(int i=0; i<n_routers; i++){
        toggle = 0;
        for(int j=0; j<n_routers; j++){
            
            // if(i==j)continue;

            s = "cload_r" + to_string(i) + "_r" + to_string(j);

            GRBVar var = model.getVarByName(s);
            if(var.get(GRB_DoubleAttr_X) != 0.0){
                cout<<"cload r"<<i<<"->r"<<j<<" : "<<" : "<<var.get(GRB_DoubleAttr_X)<<endl;
            }
        }
    }
    cout<<endl;

    cout << "mem cload ("<<n_routers<<"x"<<n_routers<<")"<<endl;

    for(int i=0; i<n_routers; i++){
        toggle = 0;
        for(int j=0; j<n_routers; j++){
            
            // if(i==j)continue;

            s = "mem_cload_r" + to_string(i) + "_r" + to_string(j);

            GRBVar var = model.getVarByName(s);
            if(var.get(GRB_DoubleAttr_X) != 0.0){
                cout<<"mem cload r"<<i<<"->r"<<j<<" : "<<" : "<<var.get(GRB_DoubleAttr_X)<<endl;
            }
        }
    }
    cout<<endl;

    cout << "Reconstructing paths..." <<endl;


    // max noi diam is mesh at 15. both src and dest nodes are one hop from noi
    int theoretical_max_path_len = 2 + 15;

    for(int src=0; src<n_routers; src++){
        for(int d=0; d<n_routers; d++){
            
            // if(mem_only && !is_exterior(d, per_row)){
            //     continue;
            // }
            
            int cur = src;

            int iters = 0;

            vector < int > bad_dests;

            vector < int > path;
            path.push_back(cur);
            while(cur != d){
                // cout << "cur="<<cur<<". dest="<<d<<endl;
                for(int i=0; i<n_routers; i++){

                    // if (find(bad_dests.begin(), bad_dests.end(),i) != bad_dests.end())continue;

                    s = "flow_load_n" + to_string(src) + "_n" + to_string(d) +
                        "_r" + to_string(cur) + "_r" + to_string(i);
                    GRBVar var = model.getVarByName(s);
                    if(var.get(GRB_DoubleAttr_X) != 0.0){
                        cur = i;
                        break;
                    }
                }
                path.push_back(cur);

                iters +=1;
                if (iters >= theoretical_max_path_len){
                    bad_dests.push_back(cur);
                    cur = src;
                    iters = 0;
                }


            }

            // print it
            cout<<"[";
            int path_len = path.size();
            for(int i=0;i<path_len;i++){
                cout << path.at(i);
                if(i!=path_len-1){
                    cout<< ", ";
                } 
            }

            cout << "]" << endl;
        }
    }

    // cout << endl;
    // cout << "residual_capacities ("<<n_routers<<"x"<<n_routers<<")"<<endl;

    // for(int i=0; i<n_routers; i++){
    //     toggle = 0;
    //     for(int j=0; j<n_routers; j++){
            
    //         if(i==j)continue;

    //         s = "residual_capacities_r" + to_string(i) + "_r" + to_string(j);

    //         GRBVar var = model.getVarByName(s);
    //         if(topo_map[i][j] >= 0.5){
    //             cout<<"residual_capacities r"<<i<<"->r"<<j<<" : "<<var.get(GRB_DoubleAttr_X)<<endl;
    //         }
    //     }
    // }
    // cout<<endl;

    cout << endl;
}


// noci weighting tuff
bool is_noc(int node){
    int n_noi = 20;

    if (node >= n_noi) return true;
    return false;
}

bool is_valid_sender(int node, int per_row, bool is_noci){
    // cout << "is node " << node << " a valid sender? ";

    bool valid = false;

    if (is_noc(node)) valid = true;
    if (is_exterior(node, per_row, is_noci)) valid = true;
    
    // cout << valid << endl;
    return valid;

}

// count all noc->noc and noc->mem only
bool is_useful_single_counted_path(int src, int dest, int per_row, bool is_noci){

    bool valid = true;

    // cout << "is src " << src << " -> dest " << dest << " a valid path? ";

    // src

    // if src not noc
    if (!is_noc(src)) return false;//valid = false;

    // dest

    else if (is_noc(dest)) return true;//valid = true;

    // if dest interior
    else if(!is_exterior(dest, per_row, is_noci)) return false; //valid = false;

    // cout << valid << endl;

    return true;//valid;

}

// count all noc->noc, noc->mem, mem->noc
bool is_useful_double_counted_path(int src, int dest, int per_row, bool is_noci){

    bool valid = true;

    // cout << "is src " << src << " -> dest " << dest << " a valid path? ";

    // src


    if(is_noc(src)){
        // noc->noc
        if(is_noc(dest)) return true;
        // noc-> mem
        if(is_exterior(dest,per_row, is_noci)) return true;
    }
    else if(is_exterior(src, per_row, is_noci)){
        if(is_noc(dest)) return true;
    }


    return false;//valid;

}

int main(int argc, char *argv[])
{
    GRBEnv* env = 0;

    int returncode = -1;

    try{
        // must be done early
        env = new GRBEnv();//true);
        env->set(GRB_StringParam_TokenServer, "mooring.ecn.purdue.edu");

        // ==================================================================
        // | File Reading, Model, and Givens
        // ==================================================================

        // Globals
        // ------------------------------------------------------------------

        // temp var for strings (setting names and such)
        string s;

        // Design Givens (i.e. inputs)
        // ------------------------------------------------------------------
        int n_routers = 20;
        int per_row = 5;
        bool is_noci = false;

        // for inputting topology map file
        int** topo_map;



        using path_t = vector < int >;
        using pathlist_t = list < path_t >;

        // matrix (flattened to 1d vector) of list of vectors
        // vector< list< vector< int > > > path_list_matrix;
        vector< pathlist_t > path_list_matrix;


        // CLA variable declarations
        // ------------------------------------------------------------------
        // file level params
        char topo_file_name[MAX_STR_LEN];
        strcpy(topo_file_name, "files/paper_solutions/minitopo/test.map");
        char pathlist_file_name[MAX_STR_LEN];
        strcpy(pathlist_file_name, "files/route_allpathslists4/test.rallpaths");
        bool read_from_file = true;

        char out_file_name[MAX_STR_LEN];
        strcpy(out_file_name, "tempname");
        bool out_name_given = false;

        // formulation params
        Objective obj = MAX_MIN_CLOAD;

        bool mem_traf_priority = false;
        bool noci_weighting = false;
        bool valid_senders_only = false;
        bool useful_paths_only = false;
        bool doubley_useful_paths_only = false;
        bool nocnoc_traffic_only = false;
        bool cohmem_prioritized = false;
        bool mem_over_coh = false;
        bool cohmemplus_prioritized = false;
        bool doubley_memory = false;


        // solver params
        bool no_solve = false;
        bool use_nodefiles = false;
        bool use_run_sol = false;
        bool set_heuristic_ratio = false;
        int heuristic_ratio = 0.5;
        bool set_time_limit = false;
        int time_limit = -1;
        bool set_mip_gap = false;
        int mip_gap = -1;
        bool set_obj_limit = false;
        double obj_limit = 0.0;
        bool write_model = false;
        bool write_presolved = false;
        bool use_lp_model = false;



        // CLAs
        // ------------------------------------------------------------------

        for(int i=1; i<argc; i++){

            // file level params
            if( (strcmp(argv[i], "-t") == 0) ||
                (strcmp(argv[i], "--topo_name") == 0)
                )
            {
                strcpy(topo_file_name, argv[i+1]);
                read_from_file = true;
                i++;
            }
            else if( (strcmp(argv[i], "-pl") == 0) ||
                (strcmp(argv[i], "--pathlist_name") == 0)
                )
            {
                strcpy(pathlist_file_name, argv[i+1]);
                read_from_file = true;
                i++;
            }
            else if( (strcmp(argv[i], "-of") == 0) ||
                (strcmp(argv[i], "--out_filename") == 0)
                )
            {
                strcpy(out_file_name, argv[i+1]);
                out_name_given = true;
                i++;
            }


            // objectives
            else if( (strcmp(argv[i], "-o") == 0) || 
                (strcmp(argv[i], "--objective") == 0)
                )
            {
                if(strcmp(argv[i+1],"max_min_cload") == 0){
                    obj = MAX_MIN_CLOAD;
                    i++;
                }
                else{
                    cout << "Unrecognized objective: "<<argv[i+1]<< endl<<endl;
                    // usage(argv[0]);
                    exit(returncode);
                }
            }

            // params
            else if ( strcmp(argv[i], "--is_noci") == 0 )
            {
                is_noci = true;
            }
            else if ( strcmp(argv[i], "--mem_traf") == 0 )
            {
                mem_traf_priority = true;
            }
            else if ( strcmp(argv[i], "--noci_weighting") == 0 )
            {
                noci_weighting = true;
            }
            else if ( strcmp(argv[i], "--valid_senders") == 0 )
            {
                valid_senders_only = true;
            }
            else if ( strcmp(argv[i], "--useful_paths") == 0 )
            {
                useful_paths_only = true;
                is_noci = true;
            }
            else if ( strcmp(argv[i], "--doubley_useful_paths") == 0 )
            {
                doubley_useful_paths_only = true;
                is_noci = true;
            }
            else if ( strcmp(argv[i], "--doubley_memory") == 0 )
            {
                doubley_memory = true;
                is_noci = true;
            }
            else if ( strcmp(argv[i], "--nocnoc_only") == 0 )
            {
                nocnoc_traffic_only = true;
                is_noci = true;
            }
            else if ( strcmp(argv[i], "--cohmem_prioritized") == 0 )
            {
                cohmem_prioritized = true;
                is_noci = true;
            }
            else if ( strcmp(argv[i], "--mem_over_coh") == 0 )
            {
                mem_over_coh = true;
                is_noci = true;
            }
            else if ( strcmp(argv[i], "--cohmemplus_prioritized") == 0 )
            {
                cohmemplus_prioritized = true;
                is_noci = true;
            }

            // solver params
            else if( strcmp(argv[i], "--no_solve") == 0 )
            {
                no_solve = true;
            }
            else if (strcmp(argv[i], "--no_nodefile") ==0)
            {
                use_nodefiles = false;
            }
            else if(strcmp(argv[i], "--use_run_sol") == 0){
                use_run_sol = true;
            }
            else if( strcmp(argv[i], "--heuristic_ratio") == 0 )
            {
                set_heuristic_ratio = true;
                heuristic_ratio = atof(argv[i+1]);
                i++;
            }
            else if( strcmp(argv[i], "--time_limit") == 0 )
            {
                set_time_limit = true;
                time_limit = atoi(argv[i+1]);
                i++;
            }
            else if( strcmp(argv[i], "--mip_gap") == 0 )
            {
                set_mip_gap = true;
                mip_gap = atoi(argv[i+1]);
                i++;
            }
            else if( strcmp(argv[i], "--obj_limit") == 0 )
            {
                set_obj_limit = true;
                obj_limit = atof(argv[++i]);
            }
            else if( strcmp(argv[i], "--write_model") == 0 )
            {
                write_model = true;
            }
            else if( strcmp(argv[i], "--write_presolved") == 0 )
            {
                write_presolved = true;
            }
            else if( strcmp(argv[i], "--use_lp_model") == 0 )
            {
                use_lp_model = true;
            }

            // overrides
            else if( strcmp(argv[i], "--num_routers") == 0 )
            {
                n_routers = atoi(argv[i+1]);
                i++;

            }
            // overrides
            else if( strcmp(argv[i], "--per_row") == 0 )
            {
                per_row = atoi(argv[++i]);

            }
            // default for now
            else{
                cout << "Unrecognized argument: "<<argv[i]<< endl<<endl;
                cout << "TODO: usage print" << endl;
                // usage(argv[0]);
                exit(returncode);
            }
        }

        // Read from File or Not
        // ------------------------------------------------------------------


        // // init 2d vector...?
        // for (int i=0; i<n_routers*n_routers;i++){
        //    path_list_matrix.push_back();
        // }
        if(read_from_file){

            // added June
            cout<<"Reading topology from: " << topo_file_name << endl<<endl;

            ifstream topo_file;
            topo_file.open(topo_file_name);

            if(!topo_file){
                cerr << endl << "ERROR: Could not open file = " << topo_file_name << endl;
                // usage(argv[0]);
                return -1;
            }
            // read i
            // n stream



            topo_map = (int**)malloc(sizeof(int*)*n_routers);

            // int
            for(int i=0; i<n_routers; i++){

                topo_map[i] = (int*)malloc(sizeof(int)*n_routers);

                for(int j=0; j<n_routers; j++){
                    topo_file>>topo_map[i][j];
                }
            }

            // --------------------------------------------------------
            // added June
            cout<<"Reading path list from: " << pathlist_file_name << endl<<endl;

            ifstream pathlist_file;
            pathlist_file.open(pathlist_file_name);

            if(!pathlist_file){
                cerr << endl << "ERROR: Could not open file = " << pathlist_file_name << endl;
                // usage(argv[0]);
                return -1;
            }
            // read i
            // n stream

            string line;
            string delim = " ";
            pathlist_t paths;
            int last_dest = 0;
            while(getline(pathlist_file, line)){

                int src = -1;
                int dest = -1;
                int val = -1;

                string token;
                size_t pos = 0;

                path_t path;


                istringstream iss(line);
                // cout << "read " << line << endl;
                while((pos = line.find(delim)) != string::npos){
                    token = line.substr(0,pos);
                    // cout<< token << " ";
                    
                    if (src == -1){
                        src = stoi(token);
                    }

                    val = stoi(token);

                    path.push_back(val);                    


                    line.erase(0,pos + delim.length());
                }
                // cout << line;
                dest = stoi(line);
                path.push_back(dest);
                if (src == -1){
                    src = dest;
                }
                // cout << endl;

                // cout << "flow " << src << "->" << dest << " over path (len " << path.size() <<") ";
                // for (auto val : path){
                //     cout << val << " ";
                // }
                // cout << endl;

                // still working on path list
                if (dest == last_dest){
                    // cout << "adding to same pathlist"<<endl;
                    paths.push_back(path);
                }
                // on new path list. save old one and begin new
                else{
                    // cout << "clearing old pathlist and adding to new pathlist"<<endl;
                    path_list_matrix.push_back(paths);
                    paths.clear();
                    paths.push_back(path);
                }

                last_dest = dest;
            }

            //final path
            path_list_matrix.push_back(paths);

        }
        // not read from file
        // mesh?
        else{

            topo_map = (int**)malloc(sizeof(int*)*n_routers);

            // int
            for(int i=0; i<n_routers; i++){

                topo_map[i] = (int*)malloc(sizeof(int)*n_routers);

                for(int j=0; j<n_routers; j++){
                    if ( j - i == 1 || i - j == 1){
                        topo_map[i][j] = 1;
                    }
                    else if ( i % 5 == j % 5 ){
                        topo_map[i][j] = 1;
                    }
                    else{
                        topo_map[i][j] = 0;
                    }
                    
                }
            }

        }


        // only noc->noc uses of noi routing
        // noci weighting
        vector< vector< int > > noci_weights {{0, 6, 8, 8, 4, 3, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4},
                                                {6, 0, 14, 16, 8, 8, 14, 16, 16, 8, 8, 16, 16, 16, 8, 8, 16, 16, 16, 8},
                                                {8, 14, 0, 14, 8, 8, 16, 14, 16, 8, 8, 16, 16, 16, 8, 8, 16, 16, 16, 8},
                                                {8, 16, 14, 0, 6, 8, 16, 16, 14, 8, 8, 16, 16, 16, 8, 8, 16, 16, 16, 8},
                                                {4, 8, 8, 6, 0, 4, 8, 8, 8, 3, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4},
                                                {3, 8, 8, 8, 4, 0, 6, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4},
                                                {8, 14, 16, 16, 8, 6, 0, 14, 16, 8, 8, 16, 16, 16, 8, 8, 16, 16, 16, 8},
                                                {8, 16, 14, 16, 8, 8, 14, 0, 14, 8, 8, 16, 16, 16, 8, 8, 16, 16, 16, 8},
                                                {8, 16, 16, 14, 8, 8, 16, 14, 0, 6, 8, 16, 16, 16, 8, 8, 16, 16, 16, 8},
                                                {4, 8, 8, 8, 3, 4, 8, 8, 6, 0, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4},
                                                {4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 0, 6, 8, 8, 4, 3, 8, 8, 8, 4},
                                                {8, 16, 16, 16, 8, 8, 16, 16, 16, 8, 6, 0, 14, 16, 8, 8, 14, 16, 16, 8},
                                                {8, 16, 16, 16, 8, 8, 16, 16, 16, 8, 8, 14, 0, 14, 8, 8, 16, 14, 16, 8},
                                                {8, 16, 16, 16, 8, 8, 16, 16, 16, 8, 8, 16, 14, 0, 6, 8, 16, 16, 14, 8},
                                                {4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 6, 0, 4, 8, 8, 8, 3},
                                                {4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 3, 8, 8, 8, 4, 0, 6, 8, 8, 4},
                                                {8, 16, 16, 16, 8, 8, 16, 16, 16, 8, 8, 14, 16, 16, 8, 6, 0, 14, 16, 8},
                                                {8, 16, 16, 16, 8, 8, 16, 16, 16, 8, 8, 16, 14, 16, 8, 8, 14, 0, 14, 8},
                                                {8, 16, 16, 16, 8, 8, 16, 16, 16, 8, 8, 16, 16, 14, 8, 8, 16, 14, 0, 6},
                                                {4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 3, 4, 8, 8, 6, 0}};
        int max_noci_weight = 16;


        // setup names
        string out_model_format;
        out_model_format = ".mps";
        if(use_lp_model) out_model_format = ".lp";



        string base_file_name;
        base_file_name = "autotop_r" + to_string(n_routers);
        // CLA override
        if(out_name_given) base_file_name =  string(out_file_name);


        // Quick Print of Givens
        // ------------------------------------------------------------------
        cout<<endl;
        cout<<"CLA/default/file values:"<<endl;
        cout<<"------------------------"<<endl;
        cout<<"n_routers="<<n_routers<<endl;

        cout<<"topology map:"<<endl;
        cout<<"-------------"<<endl;
        for (int i = 0; i < n_routers; i++) {
            cout<< i<<": [ ";
            for (int j = 0; j < n_routers; j++) {
                cout << topo_map[i][j]<<", ";
            }
            cout << " ]"<<endl;
        }
        cout<<endl;

        // print test path_list_matrix
        for (auto path_list : path_list_matrix){
            cout << "next path list"<<endl;
            int i = 0;
            for (auto path : path_list){
                cout << "   path " << i;
                i++;
                cout << " : ";
                for(auto n : path){
                    cout<< n << " ";
                }
                cout<<endl;
            }
        }

        // Constant Calculations
        // ---------------------

        // all flows pass over link?
        int theoretical_max = n_routers * n_routers;
        if (noci_weighting){
            theoretical_max *= max_noci_weight;
        }


        // ==================================================================
        // | Gurobi Model and Variables
        // ==================================================================
        
        // Model
        // ------------------------------------------------------------------

        GRBModel model = GRBModel(*env);

        #ifdef DEBUG
            cout<<"Token Server: "<<model.get(GRB_StringParam_TokenServer)<<endl;
        #endif

        model.set(GRB_StringAttr_ModelName, "mclb");

        cout<<"set name"<<endl;

        // Independent Variable Declarations
        // ------------------------------------------------------------------


        GRBVar**** flow_load = NULL;

        flow_load = new GRBVar***[n_routers];
        for(int i=0; i<n_routers; i++){


            flow_load[i] = new GRBVar**[n_routers];

            for(int j=0; j<n_routers; j++){
               
                flow_load[i][j] = new GRBVar*[n_routers];
            
                for(int u=0; u<n_routers; u++){

                    flow_load[i][j][u] = new GRBVar[n_routers];

                    for(int v=0; v<n_routers; v++){

                        // naming important
                        // when extracing solution later, uses getVarByName
                        s = "flow_load_n" + to_string(i) + "_n" + to_string(j) + "_r" + to_string(u) + "_r" + to_string(v);

                        flow_load[i][j][u][v] = model.addVar(0,1,0,GRB_BINARY, s);

                    }
                }

            }
        }


        // Dependent Variable Declarations
        // ------------------------------------------------------------------

        s = "max_cload";
        GRBVar max_cload = model.addVar(0, theoretical_max, 0,GRB_INTEGER, s);
        s = "max_coh_cload";
        GRBVar max_coh_cload = model.addVar(0, theoretical_max, 0,GRB_INTEGER, s);
        s = "max_mem_cload";
        GRBVar max_mem_cload = model.addVar(0, theoretical_max, 0,GRB_INTEGER, s);

        GRBVar** cload = new GRBVar*[n_routers];
        GRBVar** coh_cload = new GRBVar*[n_routers];
        GRBVar** mem_cload = new GRBVar*[n_routers];

        for(int i=0; i<n_routers; i++){

            cload[i] = new GRBVar[n_routers];
            coh_cload[i] = new GRBVar[n_routers];
            mem_cload[i] = new GRBVar[n_routers];

            for(int j=0; j<n_routers; j++){
               

                // naming important
                // when extracing solution later, uses getVarByName
                s = "cload_r" + to_string(i) + "_r" + to_string(j);

                cload[i][j] = model.addVar(0,theoretical_max,0,GRB_INTEGER, s);

                s = "coh_cload_r" + to_string(i) + "_r" + to_string(j);

                coh_cload[i][j] = model.addVar(0,theoretical_max,0,GRB_INTEGER, s);
                                
                s = "mem_cload_r" + to_string(i) + "_r" + to_string(j);

                mem_cload[i][j] = model.addVar(0,theoretical_max,0,GRB_INTEGER, s);
            }
        }

        cout << "init cload vars" << endl;

        // ==================================================================
        // | Constraints: ...
        // ==================================================================

        // Variable Constraints (ie defining dependent variables)
        // ------------------------------------------------------------------


        // link (i,j)
        for(int i=0; i<n_routers; i++){
            for(int j=0; j<n_routers; j++){

                GRBLinExpr load_sum = 0;
                GRBLinExpr mem_load_sum = 0;

                for(int u=0; u<n_routers; u++){
                    for(int v=0; v<n_routers; v++){

                        if (!noci_weighting){
                            load_sum += flow_load[u][v][i][j];
                        }
                        else{
                            load_sum += noci_weights[u][v]*flow_load[u][v][i][j];
                        }
                        
                        
                        if(is_exterior(v,per_row, is_noci)){
                            mem_load_sum += flow_load[u][v][i][j];
                        }

                    }
                }

                model.addConstr(cload[i][j] == load_sum);
                model.addConstr(mem_cload[i][j] == mem_load_sum);
                
            }
        }


        // Path Selection
        // ------------------------------------------------------------------


        for(int i=0; i<n_routers*n_routers;i++){
            int src = i / n_routers;
            int dest = i % n_routers;

            // if(mem_traf_only && !is_exterior(dest, per_row))
            // {
            //     continue;
            // }

            pathlist_t plist = path_list_matrix[i];

            GRBLinExpr satisfied = 0;
            // GRBQuadExpr satisfied = 0;


            for(auto path : plist){
                // GRBLinExpr path_used = 1;

                // GRBQuadExpr path_used = 1;

                GRBVar path_used = model.addVar(0,1,0,GRB_BINARY);
                // GRBVar path_weight = model.addVar(0,1,0,GRB_CONTINUOUS);

                int path_len = path.size();

                GRBVar* links_used = new GRBVar[path_len - 1];

                for(int n=0; n<path_len-1; n++){
                    int a = path.at(n);
                    int b = path.at(n+1);

                    // path_used *= flow_load[src][dest][a][b];

                    links_used[n] = model.addVar(0,1,0,GRB_BINARY);
                    model.addConstr(links_used[n] == flow_load[src][dest][a][b]);

                }

                // path_used = (links_used[0] AND links_used[1] AND ... links_used[path_len-2])
                model.addGenConstrAnd(path_used, links_used, path_len-1 );

                // satisfied += path_weight*path_used;
                satisfied += path_used; 

            }

            model.addConstr(satisfied == 1);
            // model.addQConstr(satisfied == 1);

        }


        #ifdef DEBUG
        cout << "Completed constraints" << endl;
        #endif


        // ==================================================================
        // | Objective(s) : ...
        // ==================================================================


        // Set Objective
        // ------------------------------------------------------------------
        switch(obj){
            case MAX_MIN_CLOAD:
                cout << "Set obj: max min flow" << endl;
                if (cohmemplus_prioritized){
                    set_maxmincload_objective_cohmemplus_priority(model, max_coh_cload, max_cload);
                    cout << "Set coh-mem plus prioritized obj" << endl;
                }
                else if(cohmem_prioritized){
                    if (mem_over_coh){
                        set_maxmincload_objective_memcoh_priority(model, max_coh_cload, max_mem_cload);
                        cout << "Set mem-coh (mem over coh) prioritized obj" << endl;
                    }
                    else{
                        set_maxmincload_objective_cohmem_priority(model, max_coh_cload, max_mem_cload);
                        cout << "Set coh-mem prioritized obj" << endl;
                    }
                    
                }
                else{
                    set_maxmincload_objective(model, max_cload, max_mem_cload, mem_traf_priority);
                    cout << "Set general cload obj" << endl;
                }
            default:
                printf("Objective not recognized\n");
                break;
        }


        // ==================================================================
        // | Model : Write Model to File
        // ==================================================================

        // Write out
        // ------------------------------------------------------------------
        s = "files/models/auto_top/" + string(base_file_name) + string(out_model_format);
        if(write_model){
            model.write(s);
            cout << "Wrote model to " << s << endl;
        }

        // Presolve
        // ------------------------------------------------------------------
        if(write_presolved)
        {
            GRBModel presolved_model = model.presolve();

            s = "files/models/auto_top/" + string(base_file_name) + "_presolved" + string(out_model_format);

            presolved_model.write(s);
            cout << "Wrote presolved model to " << s<< endl;
        }

        // ==================================================================
        // | Solver : Set Model Parameters and Solve
        // ==================================================================

        if(no_solve)
        {
            cout << "Exiting before solve as requested" << endl;
            return -1;
        }

        // Model Parameters
        // ------------------------------------------------------------------

        // proportion of time spent using heuristics
        // 0.5 => 50%
        // -----------------------------------------
        if(set_heuristic_ratio) model.set(GRB_DoubleParam_Heuristics, heuristic_ratio);

        // model.set(GRB_IntParam_NonConvex, 2);

        // objective objective
        // -------------------
        if (set_obj_limit) 
        model.set(GRB_DoubleParam_BestObjStop, obj_limit);

        // mip gap in percent
        // ------------------
        if (set_mip_gap)
        model.set(GRB_DoubleParam_MIPGap, mip_gap);

        // time_limit in minutes
        // ---------------------
        if(set_time_limit)
        model.set(GRB_DoubleParam_TimeLimit, time_limit*60);

        // Solve
        // ------------------------------------------------------------------

        if (no_solve){
            cout<<"no_solve parameter passed. Exiting early"<<endl;
            return 0;
        }

        cout << "About to solve..." << endl;

        model.optimize();

        // status checking
        // ---------------
        int status = model.get(GRB_IntAttr_Status);

        if (status == GRB_INF_OR_UNBD ) {
            cout << "The model cannot be solved " <<
                    "because it is infeasible or unbounded" << endl;
            return -2;
        }
        else if (status == GRB_INFEASIBLE) {
            cout << "The model cannot be solved " <<
                    "because it is infeasible" << endl;
            return -2;
        }
        else if (status == GRB_UNBOUNDED) {
            cout << "The model cannot be solved " <<
                    "because it is unbounded" << endl;
            return -2;
        }
        else if(status == GRB_TIME_LIMIT){
            cout << "Model exited due to time limit"<<endl;
        }
        else if(status == GRB_USER_OBJ_LIMIT){
            cout << "Model achieved desired objective value"<<endl;
        }
        else if (status != GRB_OPTIMAL) {
            cout << "Optimization was stopped with status " << status << endl;
            return -3;
        }

        // ==================================================================
        // | Output : Print and Write Files
        // ==================================================================

        // Print
        // ------------------------------------------------------------------

        string outname;

        if(!out_name_given && noci_weighting){
            outname = "./mclb_r" + to_string(n_routers) + "_nociweighted_mclb.paths";
        }
        if(!out_name_given && is_noci){
            outname = "./mclb_r" + to_string(n_routers) + "_noci_mclb.paths";
        }
        else{
            outname = string(out_file_name);
        }

        print_to_file(model,outname, n_routers);

    } //end try (ie important part of script)

    catch(GRBException e){
        cout << "Error code = " << e.getErrorCode() << endl;
        cout << e.getMessage() << endl;
    }
    catch (...) {
        cout << "Exception during optimization" << endl;
    }


    return returncode;
} //end main
