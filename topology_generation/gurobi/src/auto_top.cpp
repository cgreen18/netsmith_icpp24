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
#include <iostream>
#include <cstdlib>
#include <math.h>
#include <vector>
#include <algorithm> // combo stuff
#include <numeric> // iota
using namespace std;

#define MAX_STR_LEN 300


class incumbent_solution_callback: public GRBCallback
{
    public:
        double lastiter;
        double lastnode;


        // format of output
        int n_routers;
        int n_ports;
        double longest_link;

        GRBModel* model;

        GRBVar** r_map;

        ofstream* logfile;

        string logfile_name;

        int iter;

        // constuctor
        incumbent_solution_callback(GRBModel* arg_model, 
                                    GRBVar** arg_r_map,
                                    ofstream* arg_outfile,
                                    string arg_outfile_name,
                                    int arg_n_routers
                                    )
        {
            lastiter = lastnode = -GRB_INFINITY;
            
            n_routers = arg_n_routers;

            model = arg_model;

            r_map = arg_r_map;

            logfile = arg_outfile;

            logfile_name = arg_outfile_name;

            iter = 0;
        }

    private:


        void print_to_file()
        {

            try{
                string s;

                ofstream outfile(logfile_name);

                // logfile->open(logfile_name);

                // write scalars
                // -------------
                // *logfile << n_routers << endl<<n_ports<<endl<<longest_link<<endl;
                // outfile << n_routers << endl<<n_ports<<endl<<longest_link<<endl;

                // write array(s)
                // --------------
                for (int i = 0; i < n_routers; i++) {
                    // cout<<i<<" [ ";
                    for (int j = 0; j < n_routers; j++) {
                        s = "map_r" + to_string(i) + "_r" + to_string(j);
                        GRBVar var = (*model).getVarByName(s);
                        // *logfile << r_map[i][j].get(GRB_DoubleAttr_X);
                        // *logfile << var.get(GRB_DoubleAttr_X);

                        // *logfile << getSolution(var);
                        outfile << getSolution(var);
                        if(j!=n_routers-1) outfile<<" ";
                        // *logfile<<" ";
                    }
                    outfile<<endl;
                    // *logfile<<endl;
                }

                outfile.close();

                iter ++;
                // logfile->close();
                
            }
            catch (GRBException e) {
                cout << "Error number: " << e.getErrorCode() << endl;
                cout << e.getMessage() << endl;
            }
            catch(...){
                cout << "Error during incumbent solution callback." << endl;
            }
            
        }

        void callback(){
            try{

                if(false){//where==GRB_CB_MIP){
                    double nodecnt = getDoubleInfo(GRB_CB_MIP_NODCNT);
                    double objbst = getDoubleInfo(GRB_CB_MIP_OBJBST);
                    double objbnd = getDoubleInfo(GRB_CB_MIP_OBJBND);
                    int solcnt = getIntInfo(GRB_CB_MIP_SOLCNT);

                    if (nodecnt - lastnode >= 100) {
                        lastnode = nodecnt;
                        int actnodes = (int) getDoubleInfo(GRB_CB_MIP_NODLFT);
                        int itcnt = (int) getDoubleInfo(GRB_CB_MIP_ITRCNT);
                        int cutcnt = getIntInfo(GRB_CB_MIP_CUTCNT);
                        cout << "MIP callback " <<
                            "nodecnt=" << nodecnt << " and lastnode=" << lastnode<< " " << actnodes << " " << itcnt
                            << " " << objbst << " " << objbnd << " "
                            << solcnt << " " << cutcnt << endl;
                    }
                    if (fabs(objbst - objbnd) < 0.1 * (1.0 + fabs(objbst))) {
                        cout << "Stop early - 10% gap achieved" << endl;
                        abort();
                    }
                    if (nodecnt >= 10000 && solcnt) {
                        cout << "Stop early - 10000 nodes explored" << endl;
                        abort();
                    }
                }
                if(where==GRB_CB_MIPSOL){
                    cout << "New best solution found"<<endl;
                    cout << "Printing out to file: "<<logfile_name<<endl;

                    print_to_file();

                }

            }
            catch (GRBException e) {
                cout << "Error number: " << e.getErrorCode() << endl;
                cout << e.getMessage() << endl;
            }
            catch(...){
                cout << "Error during incumbent solution callback." << endl;
            }
        }
};

void usage(const char* name){
    cout<<endl;
    cout << "Usage:                     ./bin/" << name << "  [options]" << endl;
    cout << "Options:"<<endl;
    cout << "   -if, --in_filename <str>        givens file name for # routers, # ports, router positions, etc." << endl;
    cout << "                                       e.g. './files/prob_defs/dev_20r_4p_25ll.dat'" << endl;
    cout << "   -of, --out_filename <str>       base (do not include extension) for model and solution files" << endl;
    cout << "                                       e.g. 'my_20r_25ll'" << endl;
    cout << "   --use_run_sol                   bool flag to output running best solution(s). IMPORTANT CLA" << endl;
    cout << "   --start_hint_file <str>         rmap hints to seed solution value" << endl;
    cout << "                                       e.g. './files/prev_topos/kite_small.map'" << endl;
    cout << "   --hard_sets_file <str>          rmap forced/constrained positive values. all '1' in file will be constrained as connected. '0' ignored" << endl;
    cout << "                                       e.g. './files/prev_topos/cmesh.map'" << endl;

    cout << endl;
    cout << "   --num_routers <int>             manually set # of routers. Will still read other givens from file" <<endl;
    cout << "   --num_router_rows <int>         manually set # of routers. Will still read other givens from file" <<endl;
    cout << "   --num_ports <int>               manually set # of ports. Will still read other givens from file" <<endl;
    cout << "   --longest_link <int>            manually set longest allowable link distance. Will still read other givens from file. 15ll => small, 2ll => medium, 25ll => large" <<endl;
    cout << "   --unlim_link_length             bool flag to ignore link length constraint(s)" << endl;
    cout << "   --sym_links                     bool flag to force link symmetry constraint(s)" << endl;
    cout << "   --allow_multi_links             bool flag to allow multiple links between routers. ie rmap as int (was binary)" << endl;

    cout << endl;
    cout << "   -o, --objective <str>           metric to optimize for" << endl;
    cout << "                                       options: total_hops, avg_hops, shuffle_hops, bi_bw, sc_bw" <<endl;
    cout << "   --memcoh_ratio <dbl>            ratio of memory to coherence traffic. 1.0 => all memory. 0.0 => all coherence. 0.5 => balanced"<< endl;
    cout << "   --link_length_coeffs            bool flag to weight each link's objective value based on its link length" << endl;
    cout << "   --use_noci_weighting            bool flag to weight objective with noci concentration factors"<< endl;
    
    cout << endl;
    cout << "   --max_diam <int>                ..." << endl;
    cout << "   --max_avg_hops <dbl>            ..." << endl;
    cout << "   --min_bi_bw <int>               minimum allowable bisection bandwidth" << endl;
    cout << "   --min_vert_bw <int>             ..." << endl;
    cout << "   --min_horiz_bw <int>            ..." << endl;
    cout << "   --min_sc_bw <dbl>               ..." << endl;

    cout << endl;
    cout << "   --no_solve                      do not solve, just output the model as .lp" << endl;
    cout << "   --model_type <str>              which formulation: with or without one_hop." << endl;
    cout << "                                       options: w_hop, no_hop" <<endl;
    cout << "   --simple_model                  bool flag to write all general and SOS constraints as simple linear (for exporting to open source solvers)" << endl;
    cout << "   --write_presolved               bool flag to presolve and write model" << endl;
    cout << "   --use_lp_model                  bool flag to use .lp format when writing model" << endl;

    cout << "   --use_nodefiles                 bool flag to use (disk) nodefiles when node memory reaches (hardcoded) bound" << endl;
    cout << "   --time_limit <int>              time limit in MINUTES at which time to stop and output solution(s)" << endl;
    cout << "   --mip_gap <int>                 limit to MIP gap (best vs. bound) in PERCENT at which time to stop and output solution(s)" << endl;
    cout << "   --heuristic_ratio <dbl>         ratio of heuristics to optimality. something like that." << endl;
    cout << "   --obj_limit <dbl>               objective value at which to stop optimization and print result" << endl;
    cout << "   --concurrent_mip                bool flag to use concurrent mip" << endl;
    cout << "   --mem_sensitive                 bool flag if computer has low memory (<64GB)" << endl;
    cout << "   --mip_focus <int>               mip focus" << endl;
    cout << "   --max_sc_size <int>             limit sparsest cut set sizes to lesser than and equal to this size" << endl;
    cout << "   --use_vlo_sc                    bool to limit sparsest cut constr to only valid links (reduces model size)" << endl;

    cout << endl;
    cout << "   -h, --help                      display help/usage (this)"<<endl;
    cout << endl;
};

// Enums for CLAs
enum Objective {
    AVG_HOPS,
    TOTAL_HOPS,
    SHUFFLE_HOPS,
    BI_BW,
    SC_BW
};

enum ModelType {
    NO_HOP,
    W_HOP
};

// for weighting noi creation based on noci weighting
void set_weighted_objective(GRBModel &model,
                    Objective obj,
                    GRBVar** r2r_dist,
                    int n_routers,
                    GRBVar bi_bw,
                    GRBVar sc_bw,
                    vector< vector< int > > noci_weights )
{

    string s;

    try{
        // Expressions
        // ------------------------------------------------------------------

        GRBLinExpr total_hops_expr = 0;
        GRBLinExpr avg_hops_expr = 0.0;

        GRBLinExpr bi_bw_expr = bi_bw;
        GRBLinExpr sc_bw_expr = sc_bw;

        GRBLinExpr n_links = 0;

        int n_paths = n_routers*n_routers - n_routers;

        for(int i=0; i<n_routers; i++){
            for(int j=0; j<n_routers; j++){
                if(i==j)continue;

                total_hops_expr += noci_weights[i][j]*r2r_dist[i][j];
            }
        }

        avg_hops_expr = total_hops_expr  / (double) n_paths; /// n_counted;


        // Set Objective
        // ------------------------------------------------------------------
        switch(obj){
            case TOTAL_HOPS:
                cout << "Set total hops obj" << endl;
                model.setObjective(total_hops_expr, GRB_MINIMIZE);
                break;
            case AVG_HOPS:
                cout << "Set avg hops obj" << endl;
                model.setObjective(avg_hops_expr, GRB_MINIMIZE);
                break;
            case BI_BW:
                cout << "Set bi bw obj" << endl;
                model.setObjective(bi_bw_expr, GRB_MAXIMIZE);
                break;
            case SC_BW:
                cout << "Set sc bw obj" << endl;
                model.setObjective(sc_bw_expr, GRB_MAXIMIZE);
                break;
            default:
                printf("Objective not recognized\n");
                break;
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

// use this
// except for shuffle (traffic pattern)
void set_objective(GRBModel &model,
                    Objective obj,
                    GRBVar** r2r_dist,
                    int n_routers,
                    GRBVar bi_bw,
                    GRBVar sc_bw)
{

    string s;

    try{
        // Expressions
        // ------------------------------------------------------------------

        GRBLinExpr total_hops_expr = 0;
        GRBLinExpr avg_hops_expr = 0.0;

        GRBLinExpr bi_bw_expr = bi_bw;
        GRBLinExpr sc_bw_expr = sc_bw;

        double n_paths = n_routers*n_routers - n_routers;
        double ll_coeff;

        for(int i=0; i<n_routers; i++){

            for(int j=0; j<n_routers; j++){
                if(i==j)continue;
    
                total_hops_expr += r2r_dist[i][j];
            }
        }

        avg_hops_expr = total_hops_expr  / n_paths;

        // Set Objective
        // ------------------------------------------------------------------
        switch(obj){
            case TOTAL_HOPS:
                cout << "Set total hops obj" << endl;
                model.setObjective(total_hops_expr, GRB_MINIMIZE);
                break;
            case AVG_HOPS:
                cout << "Set avg hops obj" << endl;
                model.setObjective(avg_hops_expr, GRB_MINIMIZE);
                break;
            case BI_BW:
                cout << "Set bi bw obj" << endl;
                model.setObjective(bi_bw_expr, GRB_MAXIMIZE);
                break;
            case SC_BW:
                cout << "Set sc bw obj" << endl;
                model.setObjective(sc_bw_expr, GRB_MAXIMIZE);
                break;
            default:
                printf("Objective nto recognized\n");
                break;
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


// use this
void set_objective_shuffle(GRBModel &model,
                    Objective obj,
                    GRBVar** r2r_dist,
                    int n_routers)
{

    string s;

    try{

        // Expressions
        // ------------------------------------------------------------------

        GRBLinExpr shuffle_hops_expr = 0;

        for(int i=0; i<n_routers; i++){
            int j;
            // pattern from gem5's garnet_synthetic
            if (i < n_routers/2)
                j = i*2;
            else
                j = (i*2 - n_routers + 1);

            shuffle_hops_expr += r2r_dist[i][j];


        }

        // Set Objective
        // ------------------------------------------------------------------
        
        cout << "Set shuffle hops obj" << endl;
        model.setObjective(shuffle_hops_expr, GRB_MINIMIZE);
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


// doesnt work for bi bw nor sc bw
// because not using memcoh anyway
void set_objective_memcoh(GRBModel &model,
                    Objective obj,
                    GRBVar** r2r_dist,
                    int n_routers,
                    int n_router_rows,
                    double mem_coherence_traffic_ratio)
{

    int* ext_routers;
    int* int_routers;

    string s;

    try{
        // list of edge routers
        // 2 externals per row
        int n_exts = n_router_rows*2;
        ext_routers = (int *)malloc(n_exts*sizeof(int));
        // all internal but 2 per row
        int n_ints = n_routers - n_exts;
        int_routers = (int *)malloc(n_ints*sizeof(int));

        int per_row = n_routers / n_router_rows;

        int index = 0;

        // 0 and per_row-1, per_row and 2*per_row - 1
        for(int i = 0; i<n_routers; i+=per_row){
            ext_routers[index++] = i;
            ext_routers[index++] = i + per_row - 1;
        }
        // 0 and per_row-1, per_row and 2*per_row - 1
        index = 0;
        for(int i = 0; i<n_routers; i++){
            if(i%per_row == 0 || i%per_row==per_row-1) continue;

            int_routers[index++] = i;
        }

        #ifdef DEBUG
            cout << "Externals and internals" << endl;
            for(int i=0; i<n_exts; i++){
                cout << ext_routers[i] << " ";      
            }
            cout << endl;
            for(int j=0; j<n_ints; j++){
                cout << int_routers[j] << " ";       
            }
            cout << endl;
        #endif



        // Expressions
        // ------------------------------------------------------------------

        GRBLinExpr total_hops_expr = 0;
        GRBLinExpr avg_hops_expr = 0.0;

        // int n_paths = n_routers*n_routers - n_routers;
        double n_counted = 0;


        // mem traf ext->any or any->ext
        // coh traf any->any


        #ifdef DEBUG
            cout << "memcoh=";
            cout << mem_coherence_traffic_ratio <<endl;
        #endif

        // mem
        double weight = 1.0;
        for(int i=0; i<n_exts; i++){
            int src = ext_routers[i];
            for(int dest=0; dest<n_routers; dest++){
                if (src==dest) continue;
                s = "dist_r" + to_string(src) + "_r" + to_string(dest);
                // cout << s << endl;
                // GRBVar var = model.getVarByName(s);
                // total_hops_expr += mem_coherence_traffic_ratio*var;
                weight = 1.0;//4.0;
                total_hops_expr += weight*mem_coherence_traffic_ratio*r2r_dist[src][dest];
                n_counted += weight;

                // and reverse
                total_hops_expr += weight*mem_coherence_traffic_ratio*r2r_dist[dest][src];
                n_counted += weight;
            }
        }


        // coherence
        for(int src=0; src<n_routers; src++){
            for(int dest=0; dest<n_routers; dest++){

                if (src==dest) continue;

                s = "dist_r" + to_string(src) + "_r" + to_string(dest);
                
                // GRBVar var = model.getVarByName(s);
                // total_hops_expr += (1.0-mem_coherence_traffic_ratio)*var;
                weight = 1.0;//8.0;
                total_hops_expr += weight*(1.0-mem_coherence_traffic_ratio)*r2r_dist[src][dest];
                n_counted += weight;

                total_hops_expr += weight*(1.0-mem_coherence_traffic_ratio)*r2r_dist[dest][src];
                n_counted += weight;

                #ifdef DEBUG
                    cout << s;
                    cout<<"weight*(1.0-mem_coherence_traffic_ratio)="<<weight*(1.0-mem_coherence_traffic_ratio)<<endl;
                #endif
            }
        }


        avg_hops_expr = total_hops_expr / n_counted;

        // Set Objective
        // ------------------------------------------------------------------
        switch(obj){
            case TOTAL_HOPS:
                cout << "Set obj" << endl;
                model.setObjective(total_hops_expr, GRB_MINIMIZE);
                break;
            case AVG_HOPS:
                model.setObjective(avg_hops_expr, GRB_MINIMIZE);
                break;
                break;
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

    free(ext_routers);
    free(int_routers);
}

void reflex_constr(GRBModel &model,
                        GRBVar** r2r_map,
                        GRBVar** r2r_dist,
                        GRBVar** r2r_one_hop,
                        int n_routers)
{
    string s;

    for(int i = 0; i < n_routers; i++){
        s = "reflex_rmap_r" + to_string(i);

        model.addConstr(r2r_map[i][i],GRB_EQUAL, 0, s);

        s = "reflex_rdist_r" + to_string(i);
        model.addConstr(r2r_dist[i][i],GRB_EQUAL, 0.0, s);

        s = "reflex_onehop_r" + to_string(i);
        model.addConstr(r2r_one_hop[i][i],GRB_EQUAL, 0.0, s);
    }
}

void sym_constr(GRBModel &model,
                        GRBVar** r2r_map,
                        GRBVar** r2r_dist,
                        GRBVar** r2r_one_hop,
                        int n_routers)
{
    string s;

    for(int i = 0; i < n_routers; i++){
        for(int j = 0; j < n_routers; j++){
            if(i==j) continue;
            s = "sym_rmap_r" + to_string(i) + "_r" + to_string(j);

            model.addConstr(r2r_map[i][j],GRB_EQUAL, r2r_map[j][i], s);
            
            s = "sym_rdist_r" + to_string(i) + "_r" + to_string(j);
            model.addConstr(r2r_dist[i][j],GRB_EQUAL, r2r_dist[j][i], s);

            s = "sym_onehop_r" + to_string(i) + "_r" + to_string(j);
            model.addConstr(r2r_one_hop[i][j],GRB_EQUAL, r2r_one_hop[j][i], s);
        }
    }
}


void radix_constr_taken_ports(GRBModel &model,
                    GRBVar** r2r_map,
                    int* taken_ports,
                    int n_routers,
                    int n_ports)
{
    string s;
    for(int i = 0; i < n_routers; i++){
        GRBLinExpr out_links = 0;
        GRBLinExpr in_links = 0;

        for(int j = 0; j < n_routers; j++){
            if(i==j) continue;

            out_links += r2r_map[i][j];

            in_links += r2r_map[j][i];
        }

        // assume symmetric for now. add burden of taken ports
        out_links += taken_ports[i];
        in_links += taken_ports[i];

        s = "radix_out_r" + to_string(i);
        model.addConstr(out_links,GRB_LESS_EQUAL, n_ports, s);
        s = "radix_in_r" + to_string(i);
        model.addConstr(in_links,GRB_LESS_EQUAL, n_ports, s);
    }
}

void radix_constr(GRBModel &model,
                    GRBVar** r2r_map,
                    int n_routers,
                    int n_ports)
{
    string s;
    for(int i = 0; i < n_routers; i++){
        GRBLinExpr out_links = 0;
        GRBLinExpr in_links = 0;

        for(int j = 0; j < n_routers; j++){
            if(i==j) continue;

            out_links += r2r_map[i][j];

            in_links += r2r_map[j][i];
        }
        s = "radix_out_r" + to_string(i);
        model.addConstr(out_links,GRB_LESS_EQUAL, n_ports, s);
        s = "radix_in_r" + to_string(i);
        model.addConstr(in_links,GRB_LESS_EQUAL, n_ports, s);
    }
}

void avg_hops_constraint(GRBModel &model,
                        GRBVar** r2r_dist,
                        int n_routers,
                        double max_avg_hops)
{
    string s;

    GRBLinExpr total_hops;

    double n_counted = 0.0;

    for(int i = 0; i < n_routers; i++){

        // every other router except self
        for(int j = 0; j < n_routers; j++){
            if(i==j) continue;

            

            total_hops += r2r_dist[i][j];

            n_counted += 1.0;
        }
    }

    GRBLinExpr avg_hops = total_hops / n_counted;

    s = "avg_hops_constr";
    model.addConstr(avg_hops, GRB_LESS_EQUAL, max_avg_hops, s);
}

void tri_ineq_nohop_constr(GRBModel &model,
                            GRBVar** r2r_map,
                            GRBVar** r2r_dist,
                            int n_routers,
                            double max_dist)
{
    string s;
    for(int i = 0; i < n_routers; i++){

        // every other router except self
        for(int j = 0; j < n_routers; j++){
            if(i==j) continue;
        
            s = "min_dist_r" + to_string(i) + "_r" + to_string(j);
            model.addConstr(r2r_dist[i][j],GRB_GREATER_EQUAL, 1.0, s);

            s = "map2dist_pos_r" + to_string(i) + "_r" + to_string(j);
            model.addGenConstrIndicator(r2r_map[i][j],1,r2r_dist[i][j],GRB_EQUAL,1,s);//GRB_INFINITY);
            
            // helpful hint
            s = "map2dist_neg_r" + to_string(i) + "_r" + to_string(j);
            model.addGenConstrIndicator(r2r_map[i][j],0,r2r_dist[i][j],GRB_GREATER_EQUAL,2.0,s);

            GRBVar* k_route = model.addVars(n_routers);
            for(int k = 0; k<n_routers; k++){

                #ifdef DEBUG
                    cout<<"Triangle ineqaulity considering i"<<i<<"->k"<<k<<"->j"<<j<<endl;
                #endif
                if(j==k){
                    s = "k_route_r" + to_string(i) + "_r" + to_string(j) +"_k" + to_string(k);
                    // model.addConstr(k_route[k] == max_dist,s);
                    model.addConstr(k_route[k] == max_dist,s);
                    continue; 
                }
                // if(i==k || j==k){
                if(i==k){
                    // continue;
                    s = "k_route_r" + to_string(i) + "_r" + to_string(j) +"_k" + to_string(k);
                    // model.addConstr(k_route[k] == max_dist,s);
                    // model.addConstr(k_route[k] == (1.0-r2r_map[i][j])*max_dist + 1,s);

                    // binvar, bin_match, expr, sense, rhs_dbl, name
                    model.addGenConstrIndicator(r2r_map[i][j], 0, k_route[k], GRB_EQUAL, max_dist, s);
                    model.addGenConstrIndicator(r2r_map[i][j], 1, k_route[k], GRB_EQUAL, 1, s);

                    continue;
                }

                s = "k_route_i" + to_string(i) + "_k" + to_string(k) + "_j" + to_string(j);
                k_route[k].set(GRB_StringAttr_VarName,s);

                GRBLinExpr expr = 0;

                expr += r2r_dist[i][k];
                expr += r2r_dist[k][j];

                s = "k_route_r" + to_string(i) + "_r" + to_string(j) +"_k" + to_string(k);
                // k_route[k] = r2r_dist[i][k] + r2r_dist[k][j]
                model.addConstr(expr == k_route[k], s);
            }

            s = "min_constr_r" + to_string(i) + "_r" + to_string(j);
            // r2r_dist[i][j] = min(k_route[k] forall k)
            model.addGenConstrMin(r2r_dist[i][j],k_route,n_routers,GRB_INFINITY,s);
        }
        
    }
}

void tri_ineq_whop_constr(GRBModel &model,
                            GRBVar** r2r_map,
                            GRBVar** r2r_dist,
                            GRBVar** r2r_one_hop,
                            int n_routers,
                            double max_dist)
{
    string s;
    for(int i = 0; i < n_routers; i++){

        // every other router except self
        for(int j = 0; j < n_routers; j++){
        // for(int j = i+1; j < n_routers; j++){
            if(i==j) continue;
        
            s = "map2onehop_pos_r" + to_string(i) + "_r" + to_string(j);
            model.addGenConstrIndicator(r2r_map[i][j],1,r2r_one_hop[i][j],GRB_EQUAL,1.0,s);//GRB_INFINITY);
            s = "map2onehop_neg_r" + to_string(i) + "_r" + to_string(j);
            model.addGenConstrIndicator(r2r_map[i][j],0,r2r_one_hop[i][j],GRB_EQUAL,max_dist,s);

            // hints. maybe remove?
            s = "map2hop_pos_r" + to_string(i) + "_r" + to_string(j);
            model.addGenConstrIndicator(r2r_map[i][j],1,r2r_dist[i][j],GRB_EQUAL,1.0,s);//GRB_INFINITY);
            // hints. maybe remove?
            s = "map2hop_neg_r" + to_string(i) + "_r" + to_string(j);
            model.addGenConstrIndicator(r2r_map[i][j],0,r2r_dist[i][j],GRB_GREATER_EQUAL,2.0,s);


            GRBVar* k_route = model.addVars(n_routers);
            for(int k = 0; k<n_routers; k++){

                #ifdef DEBUG
                    cout<<"Triangle ineqaulity considering i"<<i<<"->k"<<k<<"->j"<<j<<endl;
                #endif

                // (i=k)->j
                if(i==k){
                    s = "k_route_r" + to_string(i) + "_r" + to_string(j) +"_k" + to_string(k);
                    model.addConstr(k_route[k] == max_dist,s);
                    continue;
                }

                s = "k_route_i" + to_string(i) + "_k" + to_string(k) + "_j" + to_string(j);
                k_route[k].set(GRB_StringAttr_VarName,s);

                GRBLinExpr expr = 0;

                // i -1hop-> k -dist-> j
                expr += r2r_one_hop[i][k];
                expr += r2r_dist[k][j];

                s = "k_route_r" + to_string(i) + "_r" + to_string(j) +"_k" + to_string(k);
                // k_route[k] = r2r_dist[i][k] + r2r_dist[k][j]
                model.addConstr(expr == k_route[k], s);
            }

            s = "min_constr_r" + to_string(i) + "_r" + to_string(j);
            // r2r_dist[i][j] = min(k_route[k] forall k)
            model.addGenConstrMin(r2r_dist[i][j],k_route,n_routers,GRB_INFINITY,s);
        }
        
    }
}

void tri_ineq_whop_greaterequal_constr(GRBModel &model,
                            GRBVar** r2r_map,
                            GRBVar** r2r_dist,
                            GRBVar** r2r_one_hop,
                            int n_routers,
                            double max_dist)
{
    string s;

    for(int i = 0; i < n_routers; i++){

        // every other router except self
        for(int j = 0; j < n_routers; j++){
            if(i==j) continue;

            s = "map2onehop_r" + to_string(i) + "_r" + to_string(j);
            GRBLinExpr map2onehop_expr = 0.0;

            map2onehop_expr += 1;
            map2onehop_expr += max_dist;
            map2onehop_expr += -1*max_dist*r2r_map[i][j];
            model.addConstr(map2onehop_expr,GRB_EQUAL,r2r_one_hop[i][j],s);  
        }
    }


    for(int i = 0; i < n_routers; i++){
        // every other router except self
        for(int j = 0; j < n_routers; j++){
            if(i==j) continue;
        

            // GRBVar* k_route = model.addVars(n_routers);
            for(int k = 0; k<n_routers; k++){

                #ifdef DEBUG
                    cout<<"Triangle ineqaulity considering i"<<i<<"->k"<<k<<"->j"<<j<<endl;
                #endif

                // (i=k)->j
                if(i==k){
                    // s = "k_route_r" + to_string(i) + "_r" + to_string(j) +"_k" + to_string(k);
                    // model.addConstr(k_route[k] == max_dist,s);
                    continue;
                }

                // s = "k_route_i" + to_string(i) + "_k" + to_string(k) + "_j" + to_string(j);
                // k_route[k].set(GRB_StringAttr_VarName,s);

                GRBLinExpr expr = 0;

                // i -1hop-> k -dist-> j
                expr += r2r_one_hop[i][k];
                expr += r2r_dist[k][j];

                s = "k_route_r" + to_string(i) + "_r" + to_string(j) +"_k" + to_string(k);
                // k_route[k] = r2r_dist[i][k] + r2r_dist[k][j]
                // model.addConstr(expr == k_route[k], s);
                model.addConstr(expr, GRB_LESS_EQUAL, r2r_dist[i][j],s);
            }

            // s = "min_constr_r" + to_string(i) + "_r" + to_string(j);
            // // r2r_dist[i][j] = min(k_route[k] forall k)
            // model.addGenConstrMin(r2r_dist[i][j],k_route,n_routers,GRB_INFINITY,s);
        }
        
    }
}

void tri_ineq_whop_simple_constr(GRBModel &model,
                            GRBVar** r2r_map,
                            GRBVar** r2r_dist,
                            GRBVar** r2r_one_hop,
                            bool sos_allowed,
                            int n_routers,
                            double max_dist)
{
    string s;

    // for big M type constraints
    double eM = 2*max_dist;
    double epsilon = 0.001;

    for(int i = 0; i < n_routers; i++){

        // every other router except self
        for(int j = 0; j < n_routers; j++){
            if(i==j) continue;

            s = "map2onehop_r" + to_string(i) + "_r" + to_string(j);
            GRBLinExpr map2onehop_expr = 0.0;

            map2onehop_expr += 1;
            map2onehop_expr += max_dist;
            map2onehop_expr += -1*max_dist*r2r_map[i][j];
            model.addConstr(map2onehop_expr,GRB_EQUAL,r2r_one_hop[i][j],s);  
        }
    }

    for(int i = 0; i < n_routers; i++){

        // every other router except self
        for(int j = 0; j < n_routers; j++){
            if(i==j) continue;

            // k_route[k] = r2r_one_hop[i][k] + r2r_dist[k][j]
            GRBVar* k_route = model.addVars(n_routers);
            for(int k = 0; k<n_routers; k++){

                #ifdef DEBUG
                    cout<<"Triangle inequality considering i"<<i<<"->k"<<k<<"->j"<<j<<endl;
                #endif

                // (i=k)->j
                if(i==k){
                    s = "k_route_r" + to_string(i) + "_r" + to_string(j) +"_k" + to_string(k);
                    model.addConstr(k_route[k] == max_dist,s);
                    continue;
                }

                s = "k_route_i" + to_string(i) + "_k" + to_string(k) + "_j" + to_string(j);
                k_route[k].set(GRB_StringAttr_VarName,s);

                GRBLinExpr expr = 0;

                // i -1hop-> k -dist-> j
                expr += r2r_one_hop[i][k];
                expr += r2r_dist[k][j];

                s = "k_route_r" + to_string(i) + "_r" + to_string(j) +"_k" + to_string(k);
                // k_route[k] = r2r_dist[i][k] + r2r_dist[k][j]
                model.addConstr(expr == k_route[k], s);

            }


            // define min here
            GRBVar* s_for_min = model.addVars(n_routers + 1);
            GRBVar* z_for_min = model.addVars(n_routers + 1, GRB_BINARY);


            for(int k = 0; k<n_routers + 1; k++){
                model.addConstr(s_for_min[k], GRB_GREATER_EQUAL, 0.0);
            }

            s = "min_kroute_zatmost_r" + to_string(i) + "_r" + to_string(j);
            GRBLinExpr min_kroute_zatmost_expr = 0.0;
            for(int k = 0; k<n_routers + 1; k++){
                min_kroute_zatmost_expr += z_for_min[k];
            }
            // exclusivity of k routes
            // model.addConstr(min_kroute_zatmost_expr, GRB_EQUAL, 1, s);
            model.addConstr(min_kroute_zatmost_expr, GRB_GREATER_EQUAL, 1, s);

            // result (r2r_dist[i][j]) is one of k_routes
            for(int k = 0; k<n_routers; k++){
                s = "min_kroute_res_r" + to_string(i) + "_r" + to_string(j) + "_r" + to_string(k);
                GRBLinExpr min_kroute_res_expr = 0.0;

                min_kroute_res_expr += k_route[k];
                min_kroute_res_expr += -1*s_for_min[k];
                model.addConstr(min_kroute_res_expr,GRB_EQUAL,r2r_dist[i][j],s);  
            }

            // or result (r2r_dist[i][j]) is max_dist (const)
            s = "min_kroute_res_r" + to_string(i) + "_r" + to_string(j) + "_r" + to_string(n_routers);
            GRBLinExpr min_kroute_res_expr = 0.0;

            min_kroute_res_expr += eM;
            min_kroute_res_expr += -1*s_for_min[n_routers];
            model.addConstr(min_kroute_res_expr,GRB_EQUAL,r2r_dist[i][j],s);


            // SOS1  between 2 vars, s_i and z_i , for each k + 1
            if (sos_allowed){
                for(int k = 0; k<n_routers + 1; k++){
                    GRBVar sos_vars_set[]  = {s_for_min[k], z_for_min[k]};
                    double sos_weights[] = {1, 1};
                    model.addSOS( sos_vars_set , sos_weights, 2, GRB_SOS_TYPE1);
                    // cout << "Added SOS" << endl;
                }
            }
            else{
                for(int k = 0; k<n_routers + 1; k++){
                    // si >= eps*(1-zi)
                    GRBLinExpr lowbound_expr = 0.0;
                    lowbound_expr += 1;
                    lowbound_expr -= z_for_min[k];
                    lowbound_expr *= epsilon;
                    model.addConstr(lowbound_expr, GRB_LESS_EQUAL, s_for_min[k]);

                    // si <= M(1-zi)
                    GRBLinExpr highbound_expr = 0.0;
                    highbound_expr += 1;
                    highbound_expr -= z_for_min[k];
                    highbound_expr *= eM;
                    model.addConstr(highbound_expr, GRB_GREATER_EQUAL, s_for_min[k]);

                    // cout << "Added SOS alternative" << endl;
                }
            }
        }
        
    }
}

void tri_ineq_whop_forexport_constr(GRBModel &model,
                            GRBVar** r2r_map,
                            GRBVar** r2r_dist,
                            GRBVar** r2r_one_hop,
                            int n_routers,
                            double max_dist)
{
    string s;

    // for big M type constraints
    double eM = 10*max_dist;
    double epsilon = 0.0001;
    
    // pass as CLA later?
    bool sos_allowed = false;
    // bool sos_allowed = true;


    for(int i = 0; i < n_routers; i++){

        // every other router except self
        for(int j = 0; j < n_routers; j++){
            if(i==j) continue;

            s = "map2onehop_r" + to_string(i) + "_r" + to_string(j);
            GRBLinExpr map2onehop_expr = 0.0;

            map2onehop_expr += 1;
            map2onehop_expr += max_dist;
            map2onehop_expr += -1*max_dist*r2r_map[i][j];
            model.addConstr(map2onehop_expr,GRB_EQUAL,r2r_one_hop[i][j],s);  
        }
    }

    for(int i = 0; i < n_routers; i++){

        // every other router except self
        for(int j = 0; j < n_routers; j++){
            if(i==j) continue;

            // k_route[k] = r2r_one_hop[i][k] + r2r_dist[k][j]
            GRBVar* k_route = model.addVars(n_routers);
            for(int k = 0; k<n_routers; k++){

                #ifdef DEBUG
                    cout<<"Triangle inequality considering i"<<i<<"->k"<<k<<"->j"<<j<<endl;
                #endif

                // (i=k)->j
                if(i==k){
                    s = "k_route_r" + to_string(i) + "_r" + to_string(j) +"_k" + to_string(k);
                    model.addConstr(k_route[k] == max_dist,s);
                    continue;
                }

                s = "k_route_i" + to_string(i) + "_k" + to_string(k) + "_j" + to_string(j);
                k_route[k].set(GRB_StringAttr_VarName,s);

                GRBLinExpr expr = 0;

                // i -1hop-> k -dist-> j
                expr += r2r_one_hop[i][k];
                expr += r2r_dist[k][j];

                s = "k_route_r" + to_string(i) + "_r" + to_string(j) +"_k" + to_string(k);
                // k_route[k] = r2r_dist[i][k] + r2r_dist[k][j]
                model.addConstr(expr == k_route[k], s);

            }


            // define min here
            GRBVar* s_for_min = model.addVars(n_routers + 1);
            GRBVar* z_for_min = model.addVars(n_routers + 1, GRB_BINARY);


            for(int k = 0; k<n_routers + 1; k++){
                model.addConstr(s_for_min[k], GRB_GREATER_EQUAL, 0.0);
            }

            s = "min_kroute_zatmost_r" + to_string(i) + "_r" + to_string(j);
            GRBLinExpr min_kroute_zatmost_expr = 0.0;
            for(int k = 0; k<n_routers + 1; k++){
                min_kroute_zatmost_expr += z_for_min[k];
            }
            // exclusivity of k routes
            model.addConstr(min_kroute_zatmost_expr, GRB_EQUAL, 1, s);

            // result (r2r_dist[i][j]) is one of k_routes
            for(int k = 0; k<n_routers; k++){
                s = "min_kroute_res_r" + to_string(i) + "_r" + to_string(j) + "_r" + to_string(k);
                GRBLinExpr min_kroute_res_expr = 0.0;

                min_kroute_res_expr += k_route[k];
                min_kroute_res_expr += -1*s_for_min[k];
                model.addConstr(min_kroute_res_expr,GRB_EQUAL,r2r_dist[i][j],s);  
            }

            // or result (r2r_dist[i][j]) is max_dist (const)
            s = "min_kroute_res_r" + to_string(i) + "_r" + to_string(j) + "_r" + to_string(n_routers);
            GRBLinExpr min_kroute_res_expr = 0.0;

            min_kroute_res_expr += eM;
            min_kroute_res_expr += -1*s_for_min[n_routers];
            model.addConstr(min_kroute_res_expr,GRB_EQUAL,r2r_dist[i][j],s);


            // SOS1  between 2 vars, s_i and z_i , for each k + 1
            if (sos_allowed){
                for(int k = 0; k<n_routers + 1; k++){
                    GRBVar sos_vars_set[]  = {s_for_min[k], z_for_min[k]};
                    double sos_weights[] = {1, 1};
                    model.addSOS( sos_vars_set , sos_weights, 2, GRB_SOS_TYPE1);
                    // cout << "Added SOS" << endl;
                }
            }
            else{
                for(int k = 0; k<n_routers + 1; k++){
                    // si >= eps*(1-zi)
                    GRBLinExpr lowbound_expr = 0.0;
                    lowbound_expr += 1;
                    lowbound_expr -= z_for_min[k];
                    lowbound_expr *= epsilon;
                    model.addConstr(lowbound_expr, GRB_LESS_EQUAL, s_for_min[k]);

                    // si <= M(1-zi)
                    GRBLinExpr highbound_expr = 0.0;
                    highbound_expr += 1;
                    highbound_expr -= z_for_min[k];
                    highbound_expr *= eM;
                    model.addConstr(highbound_expr, GRB_GREATER_EQUAL, s_for_min[k]);

                    // cout << "Added SOS alternative" << endl;
                }
            }
            
            // GRBVar* w_for_min = model.addVars(n_routers + 1, GRB_BINARY);
            // for(int k = 0; k<n_routers + 1; k++){
            //     GRBQuadExpr w_s_i_expr = 0.0;
            //     w_s_i_expr += w_for_min[k] * s_for_min[k];
            //     model.addQConstr(w_s_i_expr, GRB_EQUAL, s_for_min[k]);

            //     GRBLinExpr w_z_i_expr = 0.0;
            //     w_z_i_expr += w_for_min[k];
            //     w_z_i_expr += z_for_min[k];
            //     model.addConstr(w_z_i_expr , GRB_EQUAL, 0.0  );
            // }


        }
        
    }
}

void diameter_constr(GRBModel &model,
                    GRBVar** r2r_dist,
                    int n_routers, 
                    int max_diam)
{
    string s;
    for(int i=0; i<n_routers; i++){
        for(int j=0; j<n_routers;j++){
            s = "diam_r" + to_string(i) + "_r" + to_string(j);
            model.addConstr(r2r_dist[i][j], GRB_LESS_EQUAL, max_diam, s);
        }
    }
}

// for bi_bw
struct c_unique {
    int current;
    c_unique() {current=0;}
    int operator()() {return ++current;}
} UniqueNumber;

void printfunction ( int i) {
  cout << i << ' ';
}

// constrains in_group to have at least min_bw
// this is weighted
void bw_given_combo_constr(GRBModel &model,
                                GRBVar** r2r_map,
                                int n_routers,
                                vector<int> in_group,
                                vector<int> out_group,
                                double min_weighted_bw,
                                int constr_num)
{
    string s;

    #ifdef DEBUG
        cout << "inputs:" <<endl;
        for_each(in_group.begin(), in_group.end(), printfunction);
        cout<< " | ";
        for_each(out_group.begin(), out_group.end(), printfunction);
        cout<< endl;
    #endif

    GRBLinExpr num_crossings = 0;
    for(auto in_it = in_group.begin(); in_it != in_group.end(); in_it++){
        for(auto out_it = out_group.begin(); out_it!=out_group.end(); out_it++){
            int in_r = (*in_it);
            int out_r = (*out_it);

            num_crossings += r2r_map[in_r][out_r];

            #ifdef DEBUG
                cout << "Considering "<<in_r<<"->"<<out_r<<endl;
            #endif
        }
    }

    #ifdef DEBUG
        cout << endl;
        cout << "Adding bi bw constraint #" << constr_num<<endl;
        for_each(in_group.begin(), in_group.end(), printfunction);
        cout << endl;
    #endif
    // assert this bi bw is greater than minimum

    // remark, num_crossings is # of unidirectional links
    // min_bw needs to be specified in unidirectional links
    // therefore, num_crossings >= min_bw
    s = "bw_r" + to_string(constr_num);

    // if bi_bw specified in bilinks
    // int min_uni_bi_bw = min_bw * 2;

    float in_size = (float)(in_group.size());
    float out_size = (float)n_routers - in_size;

    GRBLinExpr weighted_crossings = num_crossings / (in_size*out_size);

    model.addConstr(weighted_crossings,GRB_GREATER_EQUAL, min_weighted_bw, s);
}

// constrains in_group to have at least min_bw
void unweighted_bw_given_combo_constr(GRBModel &model,
                                GRBVar** r2r_map,
                                int n_routers,
                                vector<int> in_group,
                                vector<int> out_group,
                                int min_bw,
                                int constr_num)
{
    string s;

    #ifdef DEBUG
        cout << "inputs:" <<endl;
        for_each(in_group.begin(), in_group.end(), printfunction);
        cout<< " | ";
        for_each(out_group.begin(), out_group.end(), printfunction);
        cout<< endl;
    #endif

    GRBLinExpr num_crossings = 0;
    for(auto in_it = in_group.begin(); in_it != in_group.end(); in_it++){
        for(auto out_it = out_group.begin(); out_it!=out_group.end(); out_it++){
            int in_r = (*in_it);
            int out_r = (*out_it);

            num_crossings += r2r_map[in_r][out_r];

            #ifdef DEBUG
                cout << "Considering "<<in_r<<"->"<<out_r<<endl;
            #endif
        }
    }

    #ifdef DEBUG
        cout << endl;
        cout << "Adding unweighted bi bw constraint #" << constr_num<<endl;
        for_each(in_group.begin(), in_group.end(), printfunction);
        cout << endl;
    #endif
    // assert this bi bw is greater than minimum

    // remark, num_crossings is # of unidirectional links
    // min_bw needs to be specified in unidirectional links
    // therefore, num_crossings >= min_bw
    s = "bw_r" + to_string(constr_num);

    // if bi_bw specified in bilinks
    // int min_uni_bi_bw = min_bw * 2;
    model.addConstr(num_crossings,GRB_GREATER_EQUAL, min_bw, s);
}

// constrains r2r_map to have at least min_bw
void sc_bw_constr(GRBModel &model,
                    GRBVar** r2r_map,
                    int n_routers,
                    double min_bw)
{

    // alg. for all combos nCk from s.o. post:
    //  https://stackoverflow.com/questions/12991758/creating-all-possible-k-combinations-of-n-items-in-c

    int num_constrs = 0;

    // for all sets of all sizes [1,n_routers)

    for(int k=1; k<n_routers; k++){

        std::string bitmask(k,1); // K leading 1s
        bitmask.resize(n_routers, 0); //N-K trailing 0s

        // std::cout<< "Combos of size " << k << std::endl;

        do {

            // 1) create this combo
            vector<int> this_combo;

            // std::cout<< "This combo: ";

            for(int i=0; i<n_routers; ++i){ //[0,N-1] ints
                if(bitmask[i]){
                    // std::cout << " " << i;
                    this_combo.push_back(i);
                }
            }
            // std::cout << std::endl;

            // 2) create other combo
            vector<int> other_combo;

            // std::cout<< "Other combo: ";

            for(int i=0; i<n_routers; i++){
                // not in this_combo
                if(find(this_combo.begin(), this_combo.end(), i) == this_combo.end()){
                    other_combo.push_back(i);
                    // std::cout << " " << i;
                }
            }
            // std::cout << std::endl;

            // 3) apply constraint to these combos
            bw_given_combo_constr(model, r2r_map, n_routers, this_combo, other_combo,min_bw,num_constrs);

        }while (std::prev_permutation(bitmask.begin() , bitmask.end() ));
    }

}


// constrains sc_bw to have at least min_bw
void sc_bw_constr_2(GRBModel &model,
                    GRBVar sc_bw,
                    double min_bw)
{
    model.addConstr(sc_bw >= min_bw);
}

// constrains sc_bw to have at least min_bw
void bi_bw_constr_2(GRBModel &model,
                    GRBVar bi_bw,
                    double min_bw)
{
    model.addConstr(bi_bw >= min_bw);
}

// constrains r2r_map to have at least min_bw
void bi_bw_constr(GRBModel &model,
                    GRBVar** r2r_map,
                    int n_routers,
                    double min_bw)
{

    int n=n_routers - 1;
    int r=n/2 + 1;

    int num_constrs = 0;

    vector<int> myints(r);
    vector<int>::iterator first = myints.begin(), last = myints.end();

    generate(first, last, UniqueNumber);

    // for_each(first, last, myfunction);
    // cout << endl;

    // for first 
    vector<int>::iterator it_1 = first;

    vector<int> this_combo_1;

    for(;it_1 != last; it_1++){
        // cout<< (*it_1) << "my ";
        this_combo_1.push_back((*it_1));
    }

    vector<int> other_combo_1;

    for(int i=0; i<n_routers; i++){
        // not in this_combo
        if(find(this_combo_1.begin(), this_combo_1.end(), i) == this_combo_1.end()){
            other_combo_1.push_back(i);
        }
    }

    unweighted_bw_given_combo_constr(model, r2r_map, n_routers, this_combo_1, other_combo_1, min_bw, num_constrs++);

    while((*first) != n-r+1){
        vector<int>::iterator mt = last;

        while (*(--mt) == n-(last-mt)+1);
        (*mt)++;
        while (++mt != last) *mt = *(mt-1)+1;

        vector<int>::iterator it = first;

        vector<int> this_combo;

        for(;it != last; it++){
            this_combo.push_back((*it));
        }

        vector<int> other_combo;

        for(int i=0; i<n_routers; i++){
            // not in this_combo
            if(find(this_combo.begin(), this_combo.end(), i) == this_combo.end()){
                other_combo.push_back(i);
            }
        }

        unweighted_bw_given_combo_constr(model, r2r_map, n_routers, this_combo, other_combo, min_bw, num_constrs++);
    }
}

float calc_cross_weight(vector<int> in_group,
                        vector<int> out_group,
                        vector<vector<int> > noci_weights)
{

    int cross_weight_int = 0;
    for(auto in_it = in_group.begin(); in_it != in_group.end(); in_it++){
        for(auto out_it = out_group.begin(); out_it!=out_group.end(); out_it++){
            int in_r = (*in_it);
            int out_r = (*out_it);

            cross_weight_int += noci_weights[in_r][out_r];

            #ifdef DEBUG
                cout << "Considering "<<in_r<<"->"<<out_r<<" for cross weight"<<endl;
            #endif
        }
    }

    float cross_weight = (float) cross_weight_int;

    return cross_weight;

}


// confusing naming. this defines bi_bw OR sc_bw var
// note, this does bw weighted by size of in and out group
// ie bw = n_links / (in_size * out_size)
void constr_weighted_bw_given_combo(GRBModel &model,
                                GRBVar** r2r_map,
                                int n_routers,
                                vector<int> in_group,
                                vector<int> out_group,
                                GRBVar bw,
                                int constr_num,
                                vector<vector<int> > noci_weights)
{
    string s;

    #ifdef DEBUG
        cout << "inputs:" <<endl;
        for_each(in_group.begin(), in_group.end(), printfunction);
        cout<< " | ";
        for_each(out_group.begin(), out_group.end(), printfunction);
        cout<< endl;
    #endif

    GRBLinExpr num_crossings = 0;
    for(auto in_it = in_group.begin(); in_it != in_group.end(); in_it++){
        for(auto out_it = out_group.begin(); out_it!=out_group.end(); out_it++){
            int in_r = (*in_it);
            int out_r = (*out_it);

            num_crossings += r2r_map[in_r][out_r];

            #ifdef DEBUG
                cout << "Considering "<<in_r<<"->"<<out_r<<endl;
            #endif
        }
    }

    float in_size = (float)(in_group.size());
    float out_size = (float)n_routers - in_size;

    float cross_weight = calc_cross_weight(in_group, out_group, noci_weights);

    GRBLinExpr weighted_crossings = num_crossings / cross_weight;
    // weighted_crossings *= 100;

    #ifdef DEBUG
        cout << endl;
        cout << "Adding weighted sc/bi bw constraint #" << constr_num<<endl;
        for_each(in_group.begin(), in_group.end(), printfunction);
        cout << endl;
        cout<< "    when cross_weight = "<<cross_weight<<endl;
    #endif
    // assert this bi bw is less than this bw and all others
    s = "bw_expr" + to_string(constr_num);
    model.addConstr(bw,GRB_LESS_EQUAL, weighted_crossings, s);
}


// confusing naming. this defines bi_bw OR sc_bw var
// note, this does bw weighted by size of in and out group
// ie bw = n_links / (in_size * out_size)
void constr_bw_given_combo(GRBModel &model,
                                GRBVar** r2r_map,
                                int n_routers,
                                vector<int> in_group,
                                vector<int> out_group,
                                GRBVar bw,
                                int constr_num)
{
    string s;

    #ifdef DEBUG
        cout << "inputs:" <<endl;
        for_each(in_group.begin(), in_group.end(), printfunction);
        cout<< " | ";
        for_each(out_group.begin(), out_group.end(), printfunction);
        cout<< endl;
    #endif

    GRBLinExpr num_crossings = 0;
    for(auto in_it = in_group.begin(); in_it != in_group.end(); in_it++){
        for(auto out_it = out_group.begin(); out_it!=out_group.end(); out_it++){
            int in_r = (*in_it);
            int out_r = (*out_it);

            num_crossings += r2r_map[in_r][out_r];

            #ifdef DEBUG
                cout << "Considering "<<in_r<<"->"<<out_r<<endl;
            #endif
        }
    }

    float in_size = (float)(in_group.size());
    float out_size = (float)n_routers - in_size;

    GRBLinExpr weighted_crossings = num_crossings / (in_size*out_size);
    // weighted_crossings *= 100;

    #ifdef DEBUG
        cout << endl;
        cout << "Adding bi bw constraint #" << constr_num<<endl;
        for_each(in_group.begin(), in_group.end(), printfunction);
        cout << endl;
    #endif
    // assert this bi bw is less than this bw and all others
    s = "bw_var_constr" + to_string(constr_num);
    model.addConstr(bw,GRB_LESS_EQUAL, weighted_crossings, s);
}


bool is_valid_link(int a, int b, double** pds, double ll){
    if ( pds[a][b] > ll) return false;

    return true;
}

// confusing naming. this defines bi_bw OR sc_bw var
// note, this does bw weighted by size of in and out group
// ie bw = n_links / (in_size * out_size)
void constr_bw_given_combo_vlo(GRBModel &model,
                                GRBVar** r2r_map,
                                int n_routers,
                                vector<int> in_group,
                                vector<int> out_group,
                                GRBVar bw,
                                int constr_num,
                                double** r2r_phys_dist,
                                double longest_link)
{
    string s;

    #ifdef DEBUG
        cout << "inputs:" <<endl;
        for_each(in_group.begin(), in_group.end(), printfunction);
        cout<< " | ";
        for_each(out_group.begin(), out_group.end(), printfunction);
        cout<< endl;
    #endif

    GRBLinExpr num_crossings = 0;
    for(auto in_it = in_group.begin(); in_it != in_group.end(); in_it++){
        for(auto out_it = out_group.begin(); out_it!=out_group.end(); out_it++){
            int in_r = (*in_it);
            int out_r = (*out_it);

            bool is_valid_link = true;

            if (r2r_phys_dist[in_r][out_r] > longest_link) is_valid_link = false;

            if(!is_valid_link){
                // cout<<"Skipping link too long "<<in_r<<" -> "<<out_r<<endl;

                // char tmp = cin.get();

                continue;
            }

            num_crossings += r2r_map[in_r][out_r];

            #ifdef DEBUG
                cout << "Considering "<<in_r<<"->"<<out_r<<endl;
            #endif
        }
    }

    float in_size = (float)(in_group.size());
    float out_size = (float)n_routers - in_size;

    GRBLinExpr weighted_crossings = num_crossings / (in_size*out_size);
    // weighted_crossings *= 100;

    #ifdef DEBUG
        cout << endl;
        cout << "Adding bi bw constraint #" << constr_num<<endl;
        for_each(in_group.begin(), in_group.end(), printfunction);
        cout << endl;
    #endif
    // assert this bi bw is less than this bw and all others
    s = "bw_var_constr" + to_string(constr_num);
    model.addConstr(bw,GRB_LESS_EQUAL, weighted_crossings, s);
}

// confusing naming. this defines bi_bw var
void constr_bi_bw(GRBModel &model,
                    GRBVar** r2r_map,
                    int n_routers,
                    GRBVar bi_bw)
{

    int n=n_routers - 1;
    int r=n/2 + 1;

    int num_constrs = 0;

    vector<int> myints(r);
    vector<int>::iterator first = myints.begin(), last = myints.end();

    generate(first, last, UniqueNumber);

    // for_each(first, last, printfunction);
    // cout << endl;

    // for first 
    vector<int>::iterator it_1 = first;

    vector<int> this_combo_1;

    for(;it_1 != last; it_1++){
        // cout<< (*it_1) << "my ";
        this_combo_1.push_back((*it_1));
    }

    vector<int> other_combo_1;

    for(int i=0; i<n_routers; i++){
        // not in this_combo
        if(find(this_combo_1.begin(), this_combo_1.end(), i) == this_combo_1.end()){
            other_combo_1.push_back(i);
        }
    }

    constr_bw_given_combo(model, r2r_map, n_routers, this_combo_1, other_combo_1, bi_bw, num_constrs++);

    while((*first) != n-r+1){
        vector<int>::iterator mt = last;

        while (*(--mt) == n-(last-mt)+1);
        (*mt)++;
        while (++mt != last) *mt = *(mt-1)+1;

        vector<int>::iterator it = first;

        vector<int> this_combo;

        for(;it != last; it++){
            this_combo.push_back((*it));
        }

        vector<int> other_combo;

        for(int i=0; i<n_routers; i++){
            // not in this_combo
            if(find(this_combo.begin(), this_combo.end(), i) == this_combo.end()){
                other_combo.push_back(i);
            }
        }

        constr_bw_given_combo(model, r2r_map, n_routers, this_combo, other_combo, bi_bw, num_constrs++);
    }

}

// confusing naming. this defines bi_bw var
void constr_bi_bw_2(GRBModel &model,
                    GRBVar** r2r_map,
                    int n_routers,
                    GRBVar bi_bw)
{

    int n=n_routers - 1;
    int k=n/2 + 1;

    int num_constrs = 0;

    cout << "sc for set size: "<< k << endl;

    std::string bitmask(k,1); // K leading 1s
    bitmask.resize(n_routers, 0); //N-K trailing 0s

    // std::cout<< "Combos of size " << k << std::endl;

    do {

        // 1) create this combo
        vector<int> this_combo;

        // std::cout<< "This combo: ";

        for(int i=0; i<n_routers; ++i){ //[0,N-1] ints
            if(bitmask[i]){
                // std::cout << " " << i;
                this_combo.push_back(i);
            }
        }
        // std::cout << std::endl;

        // 2) create other combo
        vector<int> other_combo;

        // std::cout<< "Other combo: ";

        for(int i=0; i<n_routers; i++){
            // not in this_combo
            if(find(this_combo.begin(), this_combo.end(), i) == this_combo.end()){
                other_combo.push_back(i);
                // std::cout << " " << i;
            }
        }
        // std::cout << std::endl;

        // 3) apply constraint to these combos
        constr_bw_given_combo(model, r2r_map, n_routers, this_combo, other_combo, bi_bw, num_constrs++);

    }while (std::prev_permutation(bitmask.begin() , bitmask.end() ));

}

// confusing naming. this defines sc_bw var
void constr_weighted_sc_bw(GRBModel &model,
                    GRBVar** r2r_map,
                    int n_routers,
                    GRBVar sc_bw,
                    vector< vector< int > > noci_weights)
{

    // alg. for all combos nCk from s.o. post:
    //  https://stackoverflow.com/questions/12991758/creating-all-possible-k-combinations-of-n-items-in-c

    int num_constrs = 0;

    // for all sets of all sizes [2,n_routers)
    for(int k=2; k<n_routers; k++){

        cout << "sc for set size: "<< k << endl;

        std::string bitmask(k,1); // K leading 1s
        bitmask.resize(n_routers, 0); //N-K trailing 0s

        // std::cout<< "Combos of size " << k << std::endl;

        do {

            // 1) create this combo
            vector<int> this_combo;

            // std::cout<< "This combo: ";

            for(int i=0; i<n_routers; ++i){ //[0,N-1] ints
                if(bitmask[i]){
                    // std::cout << " " << i;
                    this_combo.push_back(i);
                }
            }
            // std::cout << std::endl;

            // 2) create other combo
            vector<int> other_combo;

            // std::cout<< "Other combo: ";

            for(int i=0; i<n_routers; i++){
                // not in this_combo
                if(find(this_combo.begin(), this_combo.end(), i) == this_combo.end()){
                    other_combo.push_back(i);
                    // std::cout << " " << i;
                }
            }
            // std::cout << std::endl;

            // 3) apply constraint to these combos
            constr_weighted_bw_given_combo(model, r2r_map, n_routers, this_combo, other_combo, sc_bw, num_constrs++, noci_weights);

        }while (std::prev_permutation(bitmask.begin() , bitmask.end() ));
    }


}



// confusing naming. this defines sc_bw var
void constr_sc_bw_vlo(GRBModel &model,
                    GRBVar** r2r_map,
                    int n_routers,
                    GRBVar sc_bw,
                    double** r2r_phys_dist,
                    double longest_link)
{

    // alg. for all combos nCk from s.o. post:
    //  https://stackoverflow.com/questions/12991758/creating-all-possible-k-combinations-of-n-items-in-c

    int num_constrs = 0;

    // FLAG: vlo (use this)
    // heuristic 
    int max_size = n_routers / 2;

    // for all sets of all sizes [2,n_routers/2]
    for(int k=2; k <= max_size; k++){

        cout << "sc for set size: "<< k << endl;

        std::string bitmask(k,1); // K leading 1s
        bitmask.resize(n_routers, 0); //N-K trailing 0s

        // std::cout<< "Combos of size " << k << std::endl;

        do {

            // 1) create this combo
            vector<int> this_combo;

            // std::cout<< "This combo: ";

            for(int i=0; i<n_routers; ++i){ //[0,N-1] ints
                if(bitmask[i]){
                    // std::cout << " " << i;
                    this_combo.push_back(i);
                }
            }
            // std::cout << std::endl;

            // 2) create other combo
            vector<int> other_combo;

            // std::cout<< "Other combo: ";

            for(int i=0; i<n_routers; i++){
                // not in this_combo
                if(find(this_combo.begin(), this_combo.end(), i) == this_combo.end()){
                    other_combo.push_back(i);
                    // std::cout << " " << i;
                }
            }
            // std::cout << std::endl;

            // 3) apply constraint to these combos
            constr_bw_given_combo_vlo(model, r2r_map, n_routers, this_combo, other_combo, sc_bw, num_constrs++, r2r_phys_dist, longest_link);

        }while (std::prev_permutation(bitmask.begin() , bitmask.end() ));
    }


}


// confusing naming. this defines sc_bw var
void constr_sc_bw_vlo(GRBModel &model,
                    GRBVar** r2r_map,
                    int n_routers,
                    GRBVar sc_bw,
                    double** r2r_phys_dist,
                    double longest_link,
                    int max_sc_size)
{

    // alg. for all combos nCk from s.o. post:
    //  https://stackoverflow.com/questions/12991758/creating-all-possible-k-combinations-of-n-items-in-c

    int num_constrs = 0;

    // FLAG: vlo & vso (use this)
    // heuristic 
    int max_size = max_sc_size;
    int min_size = 1;

    // for all sets of all sizes [2,n_routers/2]
    for(int k=min_size; k <= max_size; k++){

        int n_valid = 0;
        int n_sets = 0;

        cout << "sc for set size: "<< k << endl;

        std::string bitmask(k,1); // K leading 1s
        bitmask.resize(n_routers, 0); //N-K trailing 0s

        // std::cout<< "Combos of size " << k << std::endl;

        do {

            // 1) create this combo
            vector<int> this_combo;

            n_sets++;

            // std::cout<< "This combo: ";

            for(int i=0; i<n_routers; ++i){ //[0,N-1] ints
                if(bitmask[i]){
                    // std::cout << " " << i;
                    this_combo.push_back(i);
                }
            }
            // std::cout << std::endl;

            // 2) create other combo
            vector<int> other_combo;

            // std::cout<< "Other combo: ";

            for(int i=0; i<n_routers; i++){
                // not in this_combo
                if(find(this_combo.begin(), this_combo.end(), i) == this_combo.end()){
                    other_combo.push_back(i);
                    // std::cout << " " << i;
                }
            }
            // std::cout << std::endl;

            // 2.5) determine if valid set

            bool is_valid_set = true;

            // (not tight but lower bound)
            // valid if for all routers in set,
            //      there exists at least one other router also in set
            //      s.t. there can be a valid link
            //          i.e. phys_dist <= ll
            for(auto in_it = this_combo.begin(); in_it != this_combo.end(); in_it++){
                int in_r = (*in_it);

                bool is_valid_elem = false;

                for(auto other_it = this_combo.begin(); other_it!=this_combo.end(); other_it++){
                    
                    int other_r = (*other_it);

                    if (in_r == other_r) continue;

                    // close distance
                    if (r2r_phys_dist[in_r][other_r] <= longest_link) is_valid_elem = true;


                }

                if (!is_valid_elem) is_valid_set = false;
            }


            // is valid

            //

            // 3) apply constraint to these combos
            if (is_valid_set){
                constr_bw_given_combo_vlo(model, r2r_map, n_routers, this_combo, other_combo, sc_bw, num_constrs++, r2r_phys_dist, longest_link);
                n_valid++;
            }

        }while (std::prev_permutation(bitmask.begin() , bitmask.end() ));

        cout << "# valid / total sets = " << n_valid << " / " << n_sets << endl;
    }


}

// confusing naming. this defines sc_bw var
void constr_sc_bw(GRBModel &model,
                    GRBVar** r2r_map,
                    int n_routers,
                    GRBVar sc_bw)
{

    // alg. for all combos nCk from s.o. post:
    //  https://stackoverflow.com/questions/12991758/creating-all-possible-k-combinations-of-n-items-in-c

    int num_constrs = 0;

    // for all sets of all sizes [1,n_routers)
    for(int k=1; k<n_routers; k++){

        cout << "sc for set size: "<< k << endl;

        std::string bitmask(k,1); // K leading 1s
        bitmask.resize(n_routers, 0); //N-K trailing 0s

        // std::cout<< "Combos of size " << k << std::endl;

        do {

            // 1) create this combo
            vector<int> this_combo;

            // std::cout<< "This combo: ";

            for(int i=0; i<n_routers; ++i){ //[0,N-1] ints
                if(bitmask[i]){
                    // std::cout << " " << i;
                    this_combo.push_back(i);
                }
            }
            // std::cout << std::endl;

            // 2) create other combo
            vector<int> other_combo;

            // std::cout<< "Other combo: ";

            for(int i=0; i<n_routers; i++){
                // not in this_combo
                if(find(this_combo.begin(), this_combo.end(), i) == this_combo.end()){
                    other_combo.push_back(i);
                    // std::cout << " " << i;
                }
            }
            // std::cout << std::endl;

            // 3) apply constraint to these combos
            constr_bw_given_combo(model, r2r_map, n_routers, this_combo, other_combo, sc_bw, num_constrs++);

        }while (std::prev_permutation(bitmask.begin() , bitmask.end() ));
    }


}

void longest_link_constr(GRBModel &model,
                    GRBVar** r2r_map,
                    int n_routers,
                    double** r2r_phys_dist, 
                    double longest_link)
{
    string s;
    for(int i=0; i<n_routers; i++){
        for(int j=0; j<n_routers;j++){
            if(r2r_phys_dist[i][j] > longest_link){
                s = "longdist_r" + to_string(i) + "_r" + to_string(j);
                model.addConstr(r2r_map[i][j], GRB_EQUAL, 0.0,s);
            }
        }
    }
}

void print_map_to_file(string s,
                    GRBModel &model,
                    int n_routers)
{

    ofstream outfile(s);


    // write array(s)
    // --------------
    for (int i = 0; i < n_routers; i++) {
        // cout<<i<<" [ ";
        for (int j = 0; j < n_routers; j++) {
            s = "map_r" + to_string(i) + "_r" + to_string(j);
            GRBVar var = model.getVarByName(s);
            // outfile << r2r_map[i][j].get(GRB_DoubleAttr_X);
            outfile << var.get(GRB_DoubleAttr_X);
            if(j!=n_routers-1) outfile<<" ";
        }
        if(i!=n_routers-1) outfile<<endl;
    }
}

void print_to_file(string s,
                    GRBModel &model,
                    int n_routers,
                    int n_ports,
                    int longest_link)
{

    ofstream outfile(s);

    // write scalars
    // -------------
    outfile << n_routers << endl<<n_ports<<endl<<longest_link<<endl;

    // write array(s)
    // --------------
    for (int i = 0; i < n_routers; i++) {
        // cout<<i<<" [ ";
        for (int j = 0; j < n_routers; j++) {
            s = "map_r" + to_string(i) + "_r" + to_string(j);
            GRBVar var = model.getVarByName(s);
            // outfile << r2r_map[i][j].get(GRB_DoubleAttr_X);
            outfile << var.get(GRB_DoubleAttr_X);
            if(j!=n_routers-1) outfile<<" ";
        }
        if(i!=n_routers-1) outfile<<endl;
    }
}

// print_to_console(model, r2r_phys_dist, router_x_pos, router_y_pos, n_routers);
void print_to_console(GRBModel &model,
                    ModelType model_type,
                    double** r2r_phys_dist,
                    double* router_x_pos,
                    double* router_y_pos,
                    int n_routers)
{

    string s;

    // r2r_map
    // -------
    cout<<endl;
    cout<<"r2r_map ("<<n_routers<<"x"<<n_routers<<")"<<endl;
    bool toggle;
    for(int i = 0; i< n_routers;i++){
        toggle = 0;
        for(int j = 0; j< n_routers;j++){
            s = "map_r" + to_string(i) + "_r" + to_string(j);
            GRBVar var = model.getVarByName(s);
            // if(r2r_map[i][j].get(GRB_DoubleAttr_X) >= 0.5){
            if(var.get(GRB_DoubleAttr_X) >= 0.5){
                if(toggle == 0) cout<<"r"<<i;
                else cout<<"  ";
                toggle = 1;

                cout<<"->"<<"r"<<j<<endl;
            }
        }
    }
    cout<<endl;

    cout << endl;
    cout<<"r2r_map ("<<n_routers<<"x"<<n_routers<<")"<<endl;
    for (int i = 0; i < n_routers; i++) {
        cout<<i<<" [ ";
        for (int j = 0; j < n_routers; j++) {
            s = "map_r" + to_string(i) + "_r" + to_string(j);
            GRBVar var = model.getVarByName(s);
            // cout << r2r_map[i][j].get(GRB_DoubleAttr_X)<<", ";
            cout << var.get(GRB_DoubleAttr_X)<<", ";
        }
        cout << " ]"<<endl;
    }

    // r2r_dist (hop)
    // --------------
    cout << endl;
    cout<<"r2r_dist ("<<n_routers<<"x"<<n_routers<<")"<<endl;
    for (int i = 0; i < n_routers; i++) {
        cout<<i<<" [ ";
        for (int j = 0; j < n_routers; j++) {
            s = "dist_r" + to_string(i) + "_r" + to_string(j);
            GRBVar var = model.getVarByName(s);
            // cout << r2r_dist[i][j].get(GRB_DoubleAttr_X)<<", ";
            cout << var.get(GRB_DoubleAttr_X)<<", ";
        }
        cout << " ]"<<endl;
    }

    // // r2r_one_hop (hop)
    // // --------------
    // if(model_type == W_HOP){
    //     cout << endl;
    //     cout<<"r2r_one_hop ("<<n_routers<<"x"<<n_routers<<")"<<endl;
    //     for (int i = 0; i < n_routers; i++) {
    //         cout<<i<<" [ ";
    //         for (int j = 0; j < n_routers; j++) {
    //             s = "onehop_r" + to_string(i) + "_r" + to_string(j);
    //             GRBVar var = model.getVarByName(s);
    //             // cout << r2r_dist[i][j].get(GRB_DoubleAttr_X)<<", ";
    //             cout << var.get(GRB_DoubleAttr_X)<<", ";
    //         }
    //         cout << " ]"<<endl;
    //     }
    // }

    // // k route
    // // --------------
    // if(model_type == W_HOP){
    //     cout << endl;
    //     cout<<"k route ("<<n_routers<<"x"<<n_routers<<")"<<"x"<<n_routers<<")"<<endl;
    //     for (int i = 0; i < n_routers; i++) {
            
    //         for (int j = 0; j < n_routers; j++) {
    //             if(i==j) continue;
    //             cout<<i<<" -> " << j<<" [ ";
    //             for(int k=0; k<n_routers; k++){
    //                 if(k==i){
    //                     cout << "-, ";
    //                     continue;
    //                 }

    //                 s = "k_route_i" + to_string(i) + "_k" + to_string(k) + "_j" + to_string(j);
    //                 GRBVar var = model.getVarByName(s);
    //                 // cout << r2r_dist[i][j].get(GRB_DoubleAttr_X)<<", ";
    //                 cout << var.get(GRB_DoubleAttr_X)<<", ";
    //             }
    //             cout << " ]"<<endl;
    //         }
            
    //     }
    // }


    // // temporaries
    // // --------------
    // if(model_type == W_HOP){
    //     cout << endl;
    //     cout<<"temps"<<endl;
    //     int i = 0;
    //     bool below = true;
    //     int n_skipped = 0;
    //     while(true){
    //         s = "C" + to_string(i) ;

    //         try{
    //             GRBVar var = model.getVarByName(s);
    //             // cout << r2r_dist[i][j].get(GRB_DoubleAttr_X)<<", ";
    //             cout << "i " << i << " " << var.get(GRB_DoubleAttr_X)<<endl;

    //             i += 1;
    //             below = false;
    //             n_skipped = 0;
    //             continue;
    //         }
    //         catch (...) {
    //             if(n_skipped > 10 && !below) return;
    //             n_skipped += 1;
    //         }

    //         i += 1;


    //     }
    // }

    // cout << endl;
    // cout<<"r2r_one_hop ("<<n_routers<<"x"<<n_routers<<")"<<endl;
    // for (int i = 0; i < n_routers; i++) {
    //     cout<<i<<" [ ";
    //     for (int j = 0; j < n_routers; j++) {
    //         cout << r2r_one_hop[i][j].get(GRB_DoubleAttr_X)<<", ";
    //     }
    //     cout << " ]"<<endl;
    // }

    // r2r_phys_dist (phys)
    // --------------------
    cout << endl;
    cout<<"r2r_phys_dist ("<<n_routers<<"x"<<n_routers<<")"<<endl;
    for (int i = 0; i < n_routers; i++) {
        cout<<i<<" [ ";
        for (int j = 0; j < n_routers; j++) {
            cout << r2r_phys_dist[i][j]<<", ";
        }
        cout << " ]"<<endl;
    }

    // router_x/y_pos
    // --------------
    cout << endl;
    cout<<"router positions (2x"<<n_routers<<")"<<endl;
    cout<<"   (x, y)"<<endl;
    for (int i = 0; i < n_routers; i++) {
        // for (j = 0; j < n_routers; j++) {
        cout << i<<": ("<< router_x_pos[i]<<", "<<router_y_pos[i]<<")"<<endl;
        // }
        // cout << " ]"<<endl;
    }
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

        // useful
        string s;
        const char* myname = "auto_top";

        // Design Givens
        // ------------------------------------------------------------------

        // defaults
        // configs

        // router technology stuff
        int n_routers = 12;
        int n_ports = 4;
        double longest_link = 2.0;
        bool ignore_ll = false;

        int min_bi_bw = 0;  // default val. 0=> no concern for biseciont bw
        double min_sc_bw = 0.0;  // default val. 0=> no concern for biseciont bw
        bool has_min_sc_bw = false; // reduce # constraints
        bool has_min_bi_bw = false; // reduce # constraints
        int max_diam = 8; // default val. most likely won't change the system much
        bool has_max_diam = false;
        int min_horiz_bw = 0;
        bool has_horiz_bw = false;
        int min_vert_bw = 0;
        bool has_vert_bw = false;
        double max_avg_hops = 10.0;
        bool has_max_avg_hops = false;
        bool allowing_multi_links = false;

        bool use_sym_links = false;
        bool use_linklength_coeffs = false;

        // distance stuff
        double* router_x_pos;
        double* router_y_pos;
        double** r2r_phys_dist;
        int n_router_rows = 3;

        // link length coefficients
        double** linklength_coeffs;

        // objective stuff
        Objective obj = AVG_HOPS;
        double mem_coherence_traffic_ratio = 0.5;
        bool use_memcoh = false;

        // model type stuff
        ModelType model_type = W_HOP;
        bool simple_model = false;
        bool sos_allowed = false;

        // solver params
        bool set_time_limit = false;
        int time_limit = 1; //in minutes
        bool set_mip_gap = false;
        int mip_gap = 2; // in percent
        bool set_heuristic_ratio = false;
        double heuristic_ratio = 0.5; // ratio (e.g. 0.5=50%)
        bool set_obj_limit = false;
        double obj_limit = 0.0;
        bool use_run_sol = false;
        bool use_concurrent_mip = false;
        bool mem_sensitive = false;
        int mip_focus = -1;
        int presolve_val = -1;
        int max_sc_size = -1;
        bool use_vlo_sc = false;

        bool use_start_hint = false;
        int** start_map;
        char start_map_name[MAX_STR_LEN];

        bool use_hard_sets = false;
        int** hard_sets;
        char hard_sets_name[MAX_STR_LEN];

        bool use_taken_ports = false;
        int* taken_ports;
        char taken_ports_name[MAX_STR_LEN];

        // file names
        char givens_file_name[MAX_STR_LEN];
        strcpy(givens_file_name, "files/prob_defs/dev_12r_4p_25ll.dat");

        bool read_from_file = true;

        // for cla overrides of values
        int cla_n_routers = 20;
        bool override_num_routers = false;
        int cla_n_ports = 4;
        bool override_ports = false;
        int cla_ll = 15;
        bool override_ll = false;
        int cla_router_rows = 4;
        bool override_router_rows = false;
        bool use_noci_weighting = false;

        char out_file_name[MAX_STR_LEN];
        strcpy(out_file_name, "12r_25ll");
        bool out_name_given = false;

        // just output model to file
        bool no_solve = false;
        bool use_nodefiles = false;
        bool write_model = false;
        bool write_presolved = false;
        bool use_lp_model = false;

        // Parse CLAs
        // ------------------------------------------------------------------
        for(int i=1; i<argc; i++){
            // in/out and physical/tech params
            // ------------------------------------------------------------------
            if( (strcmp(argv[i], "-if") == 0) ||
                (strcmp(argv[i], "--in_filename") == 0)
                )
            {
                strcpy(givens_file_name, argv[i+1]);
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
            else if(strcmp(argv[i], "--start_hint_file") == 0){
                use_start_hint = true;
                strcpy(start_map_name, argv[i+1]);
                i++;
            }
            else if(strcmp(argv[i], "--hard_sets_file") == 0){
                use_hard_sets = true;
                strcpy(hard_sets_name, argv[i+1]);
                i++;
            }
            // else if(strcmp(argv[i], "--taken_ports_file") == 0){
            //     use_taken_ports = true;
            //     strcpy(taken_ports_name, argv[i+1]);
            //     i++;
            // }
            else if( strcmp(argv[i], "--num_routers") == 0 )
            {
                cla_n_routers = atoi(argv[++i]);
                // read_from_file = false;
                override_num_routers = true;
            }
            else if (strcmp(argv[i], "--num_router_rows") == 0){
                cla_router_rows = atoi(argv[++i]);
                // read_from_file = false;
                override_router_rows = true;
            }
            else if( strcmp(argv[i], "--num_ports") == 0 )
            {
                cla_n_ports = atoi(argv[++i]);
                // read_from_file = false;
                override_ports = true;
            }
            else if( strcmp(argv[i], "--longest_link") == 0 )
            {
                cla_ll = stod(argv[++i]);
                // read_from_file = false;
                override_ll = true;
            }
            else if( strcmp(argv[i], "--unlim_link_length") == 0 )
            {
                ignore_ll = true;
            }
            else if( strcmp(argv[i], "--sym_links") == 0 )
            {
                use_sym_links = true;
            }
            else if(strcmp(argv[i],"--allow_multi_links") == 0){
                allowing_multi_links = true;
            }
            // formulation
            // ------------------------------------------------------------------
            else if( (strcmp(argv[i], "-o") == 0) || 
                (strcmp(argv[i], "--objective") == 0)
                )
            {
                if(strcmp(argv[i+1],"total_hops") == 0){
                    obj = TOTAL_HOPS;
                    i++;
                }
                else if(strcmp(argv[i+1],"avg_hops") == 0){
                    obj = AVG_HOPS;
                    i++;
                }
                else if(strcmp(argv[i+1],"shuffle_hops") == 0){
                    obj = SHUFFLE_HOPS;
                    i++;
                }
                else if(strcmp(argv[i+1],"bi_bw") == 0){
                    obj = BI_BW;
                    i++;
                }
                else if(strcmp(argv[i+1],"sc_bw") == 0){
                    obj = SC_BW;
                    i++;
                }
                else{
                    cout << "Unrecognized objective: "<<argv[i+1]<< endl<<endl;
                    usage(argv[0]);
                    exit(returncode);
                }
            }
            else if( strcmp(argv[i], "--memcoh_ratio") == 0 )
            {
                mem_coherence_traffic_ratio = stod(argv[++i]);
                use_memcoh = true;
            }
            else if(strcmp(argv[i], "--link_length_coeffs") == 0){
                use_linklength_coeffs = true;
            }
            else if(strcmp(argv[i],"--use_noci_weighting") == 0){
                use_noci_weighting = true;
            }

            // min/max allowances
            // ------------------------------------------------------------------
            else if( strcmp(argv[i], "--max_diam") == 0 )
            {
                max_diam = stod(argv[++i]);
                has_max_diam = true;
            }
            else if( strcmp(argv[i], "--max_avg_hops") == 0 )
            {
                max_avg_hops = stod(argv[++i]);
                has_max_avg_hops = true;
            }
            else if( strcmp(argv[i], "--min_bi_bw") == 0 )
            {
                min_bi_bw = stod(argv[++i]);
                has_min_bi_bw = true;
            }
            else if( strcmp(argv[i], "--min_vert_bw") == 0 )
            {
                min_vert_bw = stod(argv[++i]);
                has_vert_bw = true;
            }
            else if( strcmp(argv[i], "--min_horiz_bw") == 0 )
            {
                min_horiz_bw = stod(argv[++i]);
                has_horiz_bw = true;
            }
            else if( strcmp(argv[i], "--min_sc_bw") == 0 )
            {
                min_sc_bw = atof(argv[++i]);
                has_min_sc_bw = true;
            }
            // model solve parameters
            // ------------------------------------------------------------------
            else if( strcmp(argv[i], "--no_solve") == 0 )
            {
                no_solve = true;
            }
            else if( strcmp(argv[i], "--model_type") == 0 )
            {
                if(strcmp(argv[i+1],"w_hop") == 0){
                    model_type = W_HOP;
                    i++;
                }
                else if(strcmp(argv[i+1],"no_hop") == 0){
                    model_type = NO_HOP;
                    i++;
                }
                else{
                    cout << "Unrecognized model type: "<<argv[i+1]<< endl<<endl;
                    usage(argv[0]);
                    exit(returncode);
                }
            }
            else if( strcmp(argv[i], "--simple_model") == 0 )
            {
                simple_model = true;
            }
            else if( strcmp(argv[i], "--sos_allowed") == 0 )
            {
                sos_allowed = true;
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
            else if (strcmp(argv[i], "--use_nodefiles") ==0)
            {
                use_nodefiles = true;
            }
            else if( strcmp(argv[i], "--time_limit") == 0 )
            {
                set_time_limit = true;
                time_limit = atoi(argv[++i]);
            }
            else if( strcmp(argv[i], "--mip_gap") == 0 )
            {
                set_mip_gap = true;
                mip_gap = atoi(argv[++i]);
            }
            else if( strcmp(argv[i], "--heuristic_ratio") == 0 )
            {
                set_heuristic_ratio = true;
                heuristic_ratio = atof(argv[++i]);
            }
            else if( strcmp(argv[i], "--obj_limit") == 0 )
            {
                set_obj_limit = true;
                obj_limit = atof(argv[++i]);
            }
            else if(strcmp(argv[i], "--use_run_sol") == 0){
                use_run_sol = true;
            }
            else if(strcmp(argv[i], "--concurrent_mip") == 0){
                use_concurrent_mip = true;
            }
            else if(strcmp(argv[i], "--mem_sensitive") == 0){
                mem_sensitive = true;
            }
            else if (strcmp(argv[i], "--mip_focus") == 0){
                mip_focus = atoi(argv[++i]);
            }
            else if (strcmp(argv[i], "--presolve_val") == 0){
                presolve_val = atoi(argv[++i]);
            }
            else if (strcmp(argv[i], "--max_sc_size") == 0){
                max_sc_size = atoi(argv[++i]);
            }
            else if (strcmp(argv[i], "--use_vlo_sc") == 0){
                use_vlo_sc = true;
            }
            // cla meta
            // ------------------------------------------------------------------
            else if( (strcmp(argv[i], "-h") == 0) ||
                (strcmp(argv[i], "--help") == 0)
                )
            {
                usage(myname);
                exit(returncode);
            }
            else{
                cout << "Unrecognized argument: "<<argv[i]<< endl<<endl;
                usage(myname);
                exit(returncode);
            }
        }

        // Read from File or Not
        // ------------------------------------------------------------------
        if(read_from_file){
            cout<<"Reading inputs from: " << givens_file_name << endl<<endl;

            ifstream givens_file;
            givens_file.open(givens_file_name);

            if(!givens_file){
                cerr << endl << "ERROR: Could not open file = " << givens_file_name << endl;
                // usage(argv[0]);
                return -1;
            }
            // read i
            // n stream
            givens_file>>n_routers>>n_ports>>longest_link>>n_router_rows;

            router_x_pos = (double*)malloc(sizeof(double)*n_routers);
            router_y_pos = (double*)malloc(sizeof(double)*n_routers);

            // double d;
            for(int i=0; i<n_routers; i++){
                givens_file>>router_x_pos[i];
            }
            for(int i=0; i<n_routers; i++){
                givens_file>>*(router_y_pos + i);
            }

            givens_file.close();
        }
        // not read from file
        else{

            router_x_pos = (double*)malloc(sizeof(double)*n_routers);
            router_y_pos = (double*)malloc(sizeof(double)*n_routers);

            // arbitrary
            int per_row = n_routers / n_router_rows;
            for(int item=0; item<n_routers; item++){
                router_x_pos[item] = (double)(item % per_row);
                router_y_pos[item] = (double)(item / per_row);
            }

        }

        // overrides
        if (override_ports) n_ports = cla_n_ports;
        if (override_num_routers) n_routers = cla_n_routers;
        if (override_ll) longest_link = cla_ll;
        if (override_router_rows) n_router_rows = cla_router_rows;

        // Quick Print of Givens
        // ------------------------------------------------------------------
        cout<<"CLA/default/file values: n_routers="<<n_routers<<", n_ports="<<\
                n_ports<<", longest_link="<<longest_link<<endl<<\
                "memcoh="<<mem_coherence_traffic_ratio<<\
                ", n_router_rows="<<n_router_rows<<", min_bi_bw="<<min_bi_bw<<\
                ", horiz_bi_bw="<<min_horiz_bw<<", vert_bi_bw"<<min_vert_bw<<\
                ", min_sc_bw="<<min_sc_bw<<", max_diam="<<max_diam<<endl;

        cout<<"router positions (2x"<<n_routers<<")"<<endl;
        cout<<"   (x, y)"<<endl;
        for (int i = 0; i < n_routers; i++) {
            // for (j = 0; j < n_routers; j++) {
            cout << i<<": ("<< router_x_pos[i]<<", "<<router_y_pos[i]<<")"<<endl;
            // }
            // cout << " ]"<<endl;
        }

        // Hint init
        // ------------------------------------------------------------------

        if(use_start_hint){
            cout<<"Reading start hint map from: " << start_map_name << endl<<endl;

            ifstream start_map_file;
            start_map_file.open(start_map_name);

            if(!start_map_file){
                cerr << endl << "ERROR: Could not open file = " << start_map_name << endl;
                // usage(argv[0]);
                return -1;
            }

            start_map = (int**)malloc(sizeof(int*)*n_routers);

            // double d;
            for(int i=0; i<n_routers; i++){
                start_map[i] = (int*)malloc(sizeof(int)*n_routers);
                for(int j=0; j<n_routers; j++){
                    start_map_file >> start_map[i][j];
                }
            }

            start_map_file.close();

            cout << "start map"<<endl;
            for (int i = 0; i < n_routers; i++) {
                cout<< i<<": [ ";
                for (int j = 0; j < n_routers; j++) {
                    cout << start_map[i][j]<<", ";
                }
                cout << " ]"<<endl;
            }

        }
        else{
            cout << "Not using start map" << endl;
        }

        // Hard sets init
        // ------------------------------------------------------------------

        if(use_hard_sets){
            cout<<"Reading hard sets map from: " << hard_sets_name << endl<<endl;

            ifstream hard_sets_file;
            hard_sets_file.open(hard_sets_name);

            if(!hard_sets_file){
                cerr << endl << "ERROR: Could not open file = " << hard_sets_name << endl;
                // usage(argv[0]);
                return -1;
            }

            hard_sets = (int**)malloc(sizeof(int*)*n_routers);

            // double d;
            for(int i=0; i<n_routers; i++){
                hard_sets[i] = (int*)malloc(sizeof(int)*n_routers);
                for(int j=0; j<n_routers; j++){
                    hard_sets_file >> hard_sets[i][j];
                }
            }

            hard_sets_file.close();

            cout << "hard sets map"<<endl;
            for (int i = 0; i < n_routers; i++) {
                cout<< i<<": [ ";
                for (int j = 0; j < n_routers; j++) {
                    cout << hard_sets[i][j]<<", ";
                }
                cout << " ]"<<endl;
            }

        }
        else{
            cout << "Not using hard sets" << endl;
        }

        // Hard sets init
        // ------------------------------------------------------------------

        if(use_taken_ports){
            cout<<"Reading taken ports from: " << taken_ports_name << endl<<endl;

            ifstream taken_ports_file;
            taken_ports_file.open(taken_ports_name);

            if(!taken_ports_file){
                cerr << endl << "ERROR: Could not open file = " << taken_ports_name << endl;
                // usage(argv[0]);
                return -1;
            }

            taken_ports = (int*)malloc(sizeof(int)*n_routers);

            for(int i=0; i<n_routers; i++){
                taken_ports_file >> taken_ports[i];
            }

            taken_ports_file.close();

            cout << "taken_ports"<<endl;
            for (int i = 0; i < n_routers; i++) {
                cout<< i<<": [ ";
                cout << taken_ports[i]<<", ";
                cout << " ]"<<endl;
            }

        }
        else{
            cout << "Not using taken ports" << endl;
        }

        // Constant Calculations
        // ------------------------------------------------------------------

        // router-to-router physical distances
        // -----------------------------------
        
        r2r_phys_dist = (double**)malloc(sizeof(double*)*n_routers);

        // calculate distances (so that it does not need to be calculated on the fly, during optimization)
        // also, initialize the 2D dist arrays
        // this is euclidean distance
        for(int i = 0; i<n_routers;i++){
            r2r_phys_dist[i] = (double*)malloc(sizeof(double)*n_routers);
            // r2r_phys_dist.add(IloNumArray(env,n_routers));
            for(int j = 0; j<n_routers;j++){
                if(i == j){
                    r2r_phys_dist[i][j] = 0.0;
                    continue;
                }

                double  dist;
                dist = (router_x_pos[i]-router_x_pos[j])*(router_x_pos[i]-router_x_pos[j]);
                dist += (router_y_pos[i]-router_y_pos[j])*(router_y_pos[i]-router_y_pos[j]);
                dist = sqrt(dist);
                r2r_phys_dist[i][j] = dist;
            }
        }

        cout << "r2r physical distances"<<endl;
        for (int i = 0; i < n_routers; i++) {
            cout<< i<<": [ ";
            for (int j = 0; j < n_routers; j++) {
                cout << r2r_phys_dist[i][j]<<", ";
            }
            cout << " ]"<<endl;
        }

        // hardcoded for 64 noc + 20 noi (misaligned) config
        vector< vector< int > > noci_weights   {{4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4},
                                                {8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8},
                                                {8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8},
                                                {8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8},
                                                {4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4},
                                                {4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4},
                                                {8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8},
                                                {8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8},
                                                {8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8},
                                                {4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4},
                                                {4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4},
                                                {8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8},
                                                {8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8},
                                                {8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8},
                                                {4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4},
                                                {4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4},
                                                {8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8},
                                                {8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8},
                                                {8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8, 8, 0, 0, 0, 8},
                                                {4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4, 4, 8, 8, 8, 4}};

        int max_noci_weight = 8;

        // link length distance co-efficients
        // ----------------------------------

        linklength_coeffs =  (double**)malloc(sizeof(double*)*n_routers);

        // base distance is that (1,1)
        // so 0 to the diagonal to it
        int n_cols = n_routers / n_router_rows;
        int r_above_zero = n_cols;
        double base_dist = r2r_phys_dist[0][r_above_zero+1];


        cout<<"base dist = "<<base_dist<<endl;
        cout<<"n_cols = "<<n_cols<<endl;

        for(int i=0; i<n_routers; i++){
            linklength_coeffs[i] = (double*)malloc(sizeof(double)*n_routers);

            for(int j = 0; j<n_routers;j++){
                if(i == j){
                    linklength_coeffs[i][j] = 0.0;
                    continue;
                }

                // get phys dist between i and j
                double dist = r2r_phys_dist[i][j];
                linklength_coeffs[i][j] = int( ceil(dist / base_dist));
            }

        }

        cout << "link length distance coefficients"<<endl;
        for (int i = 0; i < n_routers; i++) {
            cout<< i<<": [ ";
            for (int j = 0; j < n_routers; j++) {
                cout << linklength_coeffs[i][j]<<", ";
            }
            cout << " ]"<<endl;
        }


        // setup names
        string out_model_format;
        out_model_format = ".mps";
        if(use_lp_model) out_model_format = ".lp";

        double ll_for_str = longest_link;

        if(ll_for_str == 2.0) ll_for_str = ll_for_str/10.0;


        // append obj
        string model_obj_str;
        switch(obj){
            case TOTAL_HOPS:
                model_obj_str = "_tothops";
                break;
            case AVG_HOPS:
                model_obj_str = "_avghops";
                break;
            case BI_BW:
                model_obj_str = "_bibw";
                break;
            case SC_BW:
                model_obj_str = "_scbw";
                break;
            default:
                printf("Objective nto recognized\n");
                model_obj_str = "_unk";
                break;
        }

        string base_file_name;
        base_file_name = "autotop_r" + to_string(n_routers) + "_p" + to_string(n_ports) + "_ll" + to_string(int(10.0*ll_for_str)) + string(model_obj_str);
        if(use_sym_links) base_file_name = string(base_file_name) + "_sym";
        // CLA override
        if(out_name_given) base_file_name =  string(out_file_name);

        // ==================================================================
        // | Gurobi Model and Variables
        // ==================================================================
        //

        // Model Instantiation
        // ------------------------------------------------------------------

        GRBModel model = GRBModel(*env);

        #ifdef DEBUG
            cout<<"Token Server: "<<model.get(GRB_StringParam_TokenServer)<<endl;
        #endif

        model.set(GRB_StringAttr_ModelName, myname);


        // Variables
        // ------------------------------------------------------------------

        GRBVar** r2r_map = NULL;
        GRBVar** r2r_dist = NULL;
        GRBVar** r2r_one_hop = NULL;
        double theoretical_max = (double)(n_routers * n_ports);
        s = "bi_bw";
        GRBVar bi_bw = model.addVar(0,theoretical_max, 0.0, GRB_CONTINUOUS,s);
        s = "sc_bw";
        GRBVar sc_bw = model.addVar(0,theoretical_max, 0.0, GRB_CONTINUOUS,s);

        r2r_map = new GRBVar*[n_routers];
        r2r_dist = new GRBVar*[n_routers];
        r2r_one_hop = new GRBVar*[n_routers];

        // arbitrary large max dist
        // seems better than infinity
        double max_dist =  sqrt( ((double)n_routers)*((double)n_routers));

        for(int i=0;i<n_routers; i++){
            r2r_map[i] = new GRBVar[n_routers];
            r2r_dist[i] = new GRBVar[n_routers];
            r2r_one_hop[i] = new GRBVar[n_routers];

            for(int j=0;j<n_routers;j++){
            // for(j=i+1;j<n_routers;j++){
                s = "map_r" + to_string(i) + "_r" + to_string(j);
                // range = [0,1] cost_func_coeff=0.0

                // if only single-link conns then max_val is 1.0
                //   else, if allowing multi-link conns then max_val is radix
                //   also, changes variable type...

                if (allowing_multi_links){
                    r2r_map[i][j] = model.addVar(0.0, n_ports, 0.0, GRB_INTEGER, s);
                }
                else{
                    r2r_map[i][j] = model.addVar(0.0, 1.0, 0.0, GRB_BINARY, s);
                }

                s = "dist_r" + to_string(i) + "_r" + to_string(j);
                // range = [0,max_dist] cost_func_coeff=0.0
                r2r_dist[i][j] = model.addVar(0, max_dist, 0.0, GRB_INTEGER, s);

                s = "onehop_r" + to_string(i) + "_r" + to_string(j);
                // range = [0,inf] cost_func_coeff=0.0
                r2r_one_hop[i][j] = model.addVar(0.0,GRB_INFINITY, 0.0,GRB_INTEGER, s);
            }
        }

        // ==================================================================
        // | Constraints: Variable, Port, Mapping, Traffic, and Latency
        // ==================================================================

        // Variable Constraints
        // ------------------------------------------------------------------

        // Reflexivity and Symmetry Constraints
        // ------------------------------------------------------------------
        reflex_constr(model, r2r_map, r2r_dist, r2r_one_hop, n_routers);

        // if bi directional links then symmetry
        if(use_sym_links)
        sym_constr(model, r2r_map, r2r_dist, r2r_one_hop, n_routers);


        // Radix Constraint
        // ------------------------------------------------------------------

        if(!use_taken_ports){
            radix_constr(model, r2r_map, n_routers, n_ports);
        }
        else{
            radix_constr_taken_ports(model, r2r_map, taken_ports, n_routers, n_ports);
        }

        // Triangle Inequality
        // ------------------------------------------------------------------
        if(model_type == NO_HOP){
            tri_ineq_nohop_constr(model, r2r_map, r2r_dist, n_routers, max_dist);
        }
        else if(model_type == W_HOP && simple_model){
            tri_ineq_whop_simple_constr(model, r2r_map, r2r_dist, r2r_one_hop, sos_allowed, n_routers, max_dist);
        }
        else if(model_type == W_HOP){
            tri_ineq_whop_constr(model, r2r_map, r2r_dist, r2r_one_hop, n_routers, max_dist);
        }
        else{
            cout << "Error in choosing which formulation."<<endl;
            exit(returncode);
        }

        // Max Link Length
        // ------------------------------------------------------------------
        if(!ignore_ll){
            longest_link_constr(model, r2r_map, n_routers, r2r_phys_dist, longest_link);
        }

        // Bisection Bandwidth (user provided bi bw constrains r2r map)
        // ------------------------------------------------------------------
        if(has_min_bi_bw)
        bi_bw_constr_2(model, bi_bw, min_bi_bw);

        // Bisection Bandwidth (user provided sc bw constrains r2r map)
        // ------------------------------------------------------------------
        if(has_min_sc_bw) sc_bw_constr_2(model, sc_bw, min_sc_bw);
        // sc_bw_constr(model, r2r_map, n_routers, min_sc_bw);

        // Diameter
        // ------------------------------------------------------------------
        if(has_max_diam)
        diameter_constr(model, r2r_dist, n_routers, max_diam);

        // Avg Hops
        // ------------------------------------------------------------------
        if(has_max_avg_hops)
        avg_hops_constraint(model, r2r_dist, n_routers, max_avg_hops);

        // Bisection Bandwidth (constraints to define bi_bw var)
        //                      (only applies if objective is bi_bw or min bi_bw)
        // ------------------------------------------------------------------
        if(obj == BI_BW || has_min_bi_bw)
        constr_bi_bw_2(model, r2r_map, n_routers, bi_bw);

        // Sparsest Cut Bandwidth (constraints to define sc_bw var)
        //                      (only applies if objective is sc_bw or min sc_bw)
        // ------------------------------------------------------------------
        if(obj == SC_BW || has_min_sc_bw){
            if(use_noci_weighting) constr_weighted_sc_bw(model, r2r_map, n_routers, sc_bw, noci_weights);
            // valid links only and limit size
            else if (use_vlo_sc && max_sc_size != -1) constr_sc_bw_vlo(model, r2r_map, n_routers, sc_bw, r2r_phys_dist, longest_link, max_sc_size);
            // valid links only
            else if (use_vlo_sc) constr_sc_bw_vlo(model, r2r_map, n_routers, sc_bw, r2r_phys_dist, longest_link);

            // basic
            else constr_sc_bw(model, r2r_map, n_routers, sc_bw);
        }

        // ==================================================================
        // | Hints
        // ==================================================================

        // R map
        // ------------------------------------------------------------------
        if(use_start_hint){
            for(int i=0; i<n_routers; i++){
                for(int j=0; j<n_routers; j++){
                    r2r_map[i][j].set(GRB_DoubleAttr_Start, start_map[i][j]);
                    // cout << "Set hint r_map["<<i<<"][" << j <<"] = " << start_map[i][j] << endl;
                }
            }
        }

        // ==================================================================
        // | Hardcoded connections
        // ==================================================================

        // R map links
        // ------------------------------------------------------------------
        if(use_hard_sets){
            for(int i=0; i<n_routers; i++){
                for(int j=0; j<n_routers; j++){
                    if( hard_sets[i][j] > 0){
                        model.addConstr(r2r_map[i][j] == hard_sets[i][j]);
                        // cout << "Set hard set r_map["<<i<<"][" << j <<"] = " << hard_sets[i][j] << endl;
                    }
                    
                }
            }
        }

        // ==================================================================
        // | Objective(s) : Total/average hops
        // ==================================================================

        if (use_noci_weighting){
            set_weighted_objective(model, obj, r2r_dist, n_routers, bi_bw, sc_bw, noci_weights);
            cout << "Set noci weighted r2r objective" <<endl;
        }
        else if(use_memcoh){
            set_objective_memcoh(model, obj, r2r_dist, n_routers, n_router_rows, mem_coherence_traffic_ratio);
            cout << "Set memcoh r2r objective" <<endl;
        }
        else if(obj == SHUFFLE_HOPS){
            set_objective_shuffle(model, obj, r2r_dist, n_routers);
            cout << "Set shuffle r2r objective" <<endl;
        }
        else{
            set_objective(model, obj, r2r_dist, n_routers, bi_bw, sc_bw);
            cout << "Set simple r2r objective" <<endl;
        }
        
        // ==================================================================
        // | Model : Write Model to File
        // ==================================================================

        string model_descriptors;
        if(simple_model && !sos_allowed) model_descriptors = "_simple";
        else if(simple_model && sos_allowed) model_descriptors = "_simple_wsos";



        s = "files/models/auto_top/" + string(base_file_name) + string(model_descriptors) + string(out_model_format);
        if(write_model){
            model.write(s);
            cout << "Wrote model to " << s << endl;
        }


        // Presolve
        // ------------------------------------------------------------------



        if(write_presolved)
        {
            GRBModel presolved_model = model.presolve();

            s = "files/models/auto_top/" + string(base_file_name) + string(model_descriptors) + "_presolved" + string(out_model_format);

            presolved_model.write(s);
            cout << "Wrote presolved model to " << s<< endl;
        }




        // ==================================================================
        // | Solver : Set Model Paramaters and Solve
        // ==================================================================

        if(no_solve)
        {
            cout << "Exiting before solve as requested" << endl;
            return -1;
        }

        // Parameters
        // ------------------------------------------------------------------

        // time_limit in minutes
        // ---------------------
        if(set_time_limit) model.set(GRB_DoubleParam_TimeLimit, time_limit*60);

        // mip gap in percent
        // ------------------
        if (set_mip_gap) model.set(GRB_DoubleParam_MIPGap, mip_gap);

        // objective objective
        // -------------------
        if (set_obj_limit) model.set(GRB_DoubleParam_BestObjStop, obj_limit);


        // proportion of time spent using heuristics
        // 0.5 => 50%
        // -----------------------------------------
        if(set_heuristic_ratio) model.set(GRB_DoubleParam_Heuristics, heuristic_ratio);

        // for out of memory of bibw
        // 0.5 recommended by Gurobi
        // they recommend this value
        // with gurobi 10.0 it seems the param is GB now??
        if (use_nodefiles || mem_sensitive){
            model.set(GRB_DoubleParam_NodefileStart, 0.5);

            model.set(GRB_StringParam_NodefileDir, "./gurobi/nodefiles");
        }

        if(use_concurrent_mip && !mem_sensitive) model.set(GRB_IntParam_ConcurrentMIP, 16);

        // bool mem_sensitive = false;
        if(mem_sensitive) model.set(GRB_IntParam_Threads, 1);

        // set max threads for mem limits

        // TODO: DistributedMIPJobs

        // TODO: MIPFocus
        // If you are more interested in finding
        // feasible solutions quickly, you can select MIPFocus=1. If you believe the solver is having no trouble
        // finding good quality solutions, and wish to focus more attention on proving optimality, select
        // MIPFocus=2. If the best objective bound is moving very slowly (or not at all), you may want to
        // try MIPFocus=3 to focus on the bound.
        if (mip_focus != -1) model.set(GRB_IntParam_MIPFocus, mip_focus); 

        // TODO: make cla
        // model.set(GRB_IntParam_PrePasses, 50); 

        if (presolve_val != -1) model.set(GRB_IntParam_Presolve, presolve_val);

        // Callbacks!
        // ----------

        // Running solution (on every new valid solution)

        string cb_outfile_name = "files/running_solutions/" + string(base_file_name) + ".map";

        ofstream cb_outfile = ofstream(cb_outfile_name, ios_base::trunc);

        incumbent_solution_callback isc = incumbent_solution_callback(&model, r2r_map, &cb_outfile, cb_outfile_name, n_routers);
        // incumbent_solution_callback isc;
        if(use_run_sol){
            cout << "Setting running solution callback for file "<< cb_outfile_name <<endl;
            model.setCallback(&isc);
        }

        // Solve
        // ------------------------------------------------------------------

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

        // Print Result to Console
        // ------------------------------------------------------------------

        double objval = model.get(GRB_DoubleAttr_ObjVal);

        print_to_console(model, model_type, r2r_phys_dist, router_x_pos, router_y_pos, n_routers);


        // printUpperTriVarSolution(&r2r_map,n_routers,n_routers);

        // Print Result to File
        // ------------------------------------------------------------------

        s = "files/optimal_solutions/" + string(base_file_name) + ".map";

        print_map_to_file(s, model, n_routers);

        cout<< "Wrote solution to " << s << endl;

        // Return Code for Python Launcher
        // ------------------------------------------------------------------

        returncode = objval;

    } //end try

    catch(GRBException e){
        cout << "Error code = " << e.getErrorCode() << endl;
        cout << e.getMessage() << endl;
    }
    catch (...) {
        cout << "Exception during optimization" << endl;
    }

    // // Frees
    // // ------------------------------------------------------------------
    // free(router_x_pos);
    // free(router_y_pos);
    // for(int i=0;i<n_routers;i++){
    //     free(r2r_phys_dist[i]);
    // }

    return returncode;
} //end main
