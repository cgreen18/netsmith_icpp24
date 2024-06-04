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

using namespace std;

#define MAX_STR_LEN 300


// Enums for CLAs
enum Objective {
    TEST,
    TOTAL_HOPS,
    POWER
};



void usage(const char* name){
    cout<<endl;
    cout << "Usage:                     ./bin/" << name << "  [options]" << endl;
    cout << "Options:"<<endl;
    cout << "   -if, --in_filename <str>        givens file name for # routers, # ports, router positions, etc." << endl;
    cout << "                                       e.g. './files/prob_defs/dev_20r_4p_25ll.dat'" << endl;
    cout << "   -of, --out_filename <str>       base (do not include extension) for model and solution files" << endl;
    cout << "                                       e.g. 'my_20r_25ll'" << endl;

    cout << endl;
    cout << "   --num_routers <int>             manually set # of routers. Will still read other givens from file" <<endl;
    cout << "   --num_router_rows <int>         manually set # of routers. Will still read other givens from file" <<endl;
    cout << "   --num_ports <int>               manually set # of ports. Will still read other givens from file" <<endl;
    cout << "   --longest_link <int>            manually set longest allowable link distance. Will still read other givens from file" <<endl;
    cout << "   --uni_links                     bool flag to relax link symmetry constraint(s)" << endl;
    // cout << "   --allow_multi_links             bool flag to allow multiple links between routers. ie rmap as int (was binary)" << endl;

    cout << endl;
    cout << "   -o, --objective <str>           metric to optimize for" << endl;
    cout << "                                       options: total_hops, power" <<endl;

    cout << endl;
    cout << "   --use_run_sol                   bool flag to output running best solution(s). IMPORTANT CLA" << endl;
    cout << "   --no_solve                      do not solve, just output the model as .lp" << endl;
    cout << "   --write_model                   bool flag to write model" << endl;
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

    cout << endl;
    cout << "   -h, --help                      display help/usage (this)"<<endl;
    cout << endl;
};



void floyd_warshall(double** r2r_hop_dist,
                    int n_routers)
{
    for (int i=0; i<n_routers;i++){
        for (int j=0; j<n_routers;j++){
            for (int k=0; k<n_routers;k++){
                // shorter path from i
                if( (r2r_hop_dist[j][i] + r2r_hop_dist[i][k]) < r2r_hop_dist[j][k]){
                    r2r_hop_dist[j][k] = r2r_hop_dist[j][i] + r2r_hop_dist[i][k];
                }
            }
        }
    }
}

double calc_avg(double** r2r_hop_dist,
                    int n_routers)
{
    double tot_hops = 0.0;
    double n_counted = 0.0;
    for (int i=0; i<n_routers;i++){
        for (int j=0; j<n_routers;j++){
            if(i==j) continue;
            tot_hops += r2r_hop_dist[i][j];
            n_counted += 1.0;
        }
    }
    return tot_hops / n_counted;
}

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

        GRBVar**** flow_out;

        ofstream* logfile_flows;

        string logfile_name_flows;

        int iter;

        // constuctor
        incumbent_solution_callback(GRBModel* arg_model, 
                                    GRBVar** arg_r_map,
                                    GRBVar**** arg_flow_out,
                                    ofstream* arg_outfile,
                                    string arg_outfile_name,
                                    ofstream* arg_outfile_flows,
                                    string arg_outfile_name_flows,
                                    int arg_n_routers)
        {
            lastiter = lastnode = -GRB_INFINITY;
            
            n_routers = arg_n_routers;

            model = arg_model;

            r_map = arg_r_map;

            logfile = arg_outfile;

            logfile_name = arg_outfile_name;

            flow_out = arg_flow_out;

            logfile_flows = arg_outfile_flows;

            logfile_name_flows = arg_outfile_name_flows;

            iter = 0;
        }

    private:


        void print_to_file()//string s,
                            // GRBModel &model,
                            // int n_routers,
                            // int n_ports,
                            // int longest_link)
        {

            try{
                string s;

                ofstream outfile(logfile_name);


                // write array(s)
                // --------------
                for (int i = 0; i < n_routers; i++) {
                    // cout<<i<<" [ ";
                    for (int j = 0; j < n_routers; j++) {
                        s = "r2r_map_r" + to_string(i) + "_r" + to_string(j);
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


                ofstream outfile_flows(logfile_name_flows);


                // write array(s)
                // --------------


                for(int i=0; i<n_routers; i++){
                    for(int j=0; j<n_routers; j++){
                        if(i==j)continue;
                        for(int k=0; k<n_routers; k++){
                            if(j==k)continue;
                            for(int l=0; l<n_ports; l++){

                                s = "flow_out_r" + to_string(i) + "_r" + to_string(j) +
                                    "_r" + to_string(k) + "_p" + to_string(l);

                                GRBVar var = (*model).getVarByName(s);
                                if(var.get(GRB_DoubleAttr_X) >= 0.5){
                                    outfile_flows <<"r"<<i<<"->r"<<j<<": "<<"r"<<k<<"p"<<l<<" : "<<var.get(GRB_DoubleAttr_X)<<endl;
                                }
                            }
                        }
                        
                    }
                }


                outfile_flows.close();



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

void set_hop_objective(GRBModel &model,
                        GRBVar**** flow_out,
                        int n_nodes,
                        int n_routers,
                        int n_ports)
{
    try{

        // Expressions
        // ------------------------------------------------------------------
        
        GRBLinExpr total_path_length_expr = 0;

        for(int i=0; i<n_nodes; i++){
            for(int j=0; j<n_nodes; j++){
                if(i==j) continue;

                GRBLinExpr this_path_length_expr = 0;
                
                for(int k=0; k<n_routers; k++){
                    for(int l=0; l<n_ports; l++){

                        this_path_length_expr += flow_out[i][j][k][l];
                    }
                }

                total_path_length_expr += this_path_length_expr -1;
            }
        }

        model.setObjective(total_path_length_expr, GRB_MINIMIZE);

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

void set_power_objective(GRBModel &model,
                    GRBVar** tot_traff_in_port,
                    GRBVar** tot_traff_out_port,
                    double** n2r_phys_dist,
                    double** r2r_phys_dist,
                    GRBVar****** flow_traffic_link,
                    GRBVar*** n2p_map,
                    int n_routers,
                    int n_ports)
{
    try{

        // Expressions
        // ------------------------------------------------------------------
        
        GRBLinExpr router_pow_expr = 0;
        GRBLinExpr link_pow_expr = 0;

        // for convenience/quick changes
        GRBLinExpr tot_pow_expr = 0;

        for(int i=0; i<n_routers; i++){
            for(int j=0; j<n_ports; j++){

                // if needed, add power factor
                router_pow_expr += tot_traff_in_port[i][j];

                // if needed, add power factor
                router_pow_expr += tot_traff_out_port[i][j];
            }
        }

        for(int i=0; i<n_routers; i++){
            for(int j=0; j<n_routers; j++){
                
                if(i==j) continue;

                for(int k=0; k<n_routers; k++){
                    for(int l=0; l<n_ports; l++){
                        for(int m=0; m<n_routers; m++){
                            for(int n=0; n<n_ports; n++){

                                // can add weight here
                                link_pow_expr +=
                                    r2r_phys_dist[k][m]*flow_traffic_link[i][j][k][l][m][n];

                                // cout << "obj r"<<k<<" -> r"<<m<<" : dist "<<r2r_phys_dist[k][m]<<endl;

                            }
                        }

                        link_pow_expr += n2p_map[i][k][l];

                    }
                }
            }
        }

        // for now, equal weight? or should there be a factor?
        tot_pow_expr = router_pow_expr + link_pow_expr;

        model.setObjective(tot_pow_expr, GRB_MINIMIZE);

        cout << "Set power objective" << endl;

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

void set_test_objective(GRBModel &model,
                        GRBVar**** p2p_map,
                        int n_routers,
                        int n_ports)
{

    try{

        // Expressions
        // ------------------------------------------------------------------
        
        GRBLinExpr total_p2p_expr = 0;

        for(int i=0; i<n_routers; i++){
            for(int j=0; j<n_ports; j++){
                for(int k=0; k<n_routers; k++){
                    if(i==k)continue;
                    for(int l=0; l<n_ports; l++){

                        total_p2p_expr += p2p_map[i][j][k][l];
                    }
                }
            }
        }

        model.setObjective(total_p2p_expr, GRB_MAXIMIZE);

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


void print_to_console(GRBModel &model,
                        int n_nodes,
                        int n_routers,
                        int n_ports)
{

    string s;
    bool toggle;

    cout << endl;
    cout << "p2p_map ("<<n_routers<<"x"<<n_ports<<"x"<<
            n_routers<<"x"<<n_ports<<")"<<endl;

    for(int i=0; i<n_routers; i++){
        toggle = 0;
        for(int j=0; j<n_ports; j++){
            
            for(int k=0; k<n_routers; k++){
                if(i==k)continue;
                for(int l=0; l<n_ports; l++){

                    s = "p2p_map_r" + to_string(i) + "_p" + to_string(j) +
                        "_r" + to_string(k) + "_p" + to_string(l);

                    GRBVar var = model.getVarByName(s);
                    if(var.get(GRB_DoubleAttr_X) >= 0.5){
                        cout<<"r"<<i<<"p"<<j<<" -> "<<"r"<<k<<"p"<<l<<" : "<<var.get(GRB_DoubleAttr_X)<<endl;
                    }
                    // cout<<"r"<<i<<"p"<<j<<" -> "<<"r"<<k<<"p"<<l<<" : "<<var.get(GRB_DoubleAttr_X)<<endl;
                }
            }
        }
    }
    cout<<endl;

    cout << endl;
    cout << "n2p_map ("<<n_nodes<<"x"<<
            n_routers<<"x"<<n_ports<<")"<<endl;

    for(int i=0; i<n_nodes; i++){
        for(int k=0; k<n_routers; k++){
            for(int l=0; l<n_ports; l++){

                s = "n2p_map_n" + to_string(i)  +
                    "_r" + to_string(k) + "_p" + to_string(l);

                GRBVar var = model.getVarByName(s);
                if(var.get(GRB_DoubleAttr_X) >= 0.5){
                    cout<<"n"<<i<<" -> "<<"r"<<k<<"p"<<l<<" : "<<var.get(GRB_DoubleAttr_X)<<endl;
                }
                // cout<<"n"<<i<<" -> "<<"r"<<k<<"p"<<l<<" : "<<var.get(GRB_DoubleAttr_X)<<endl;
            }
        }

    }
    cout<<endl;

    cout << endl;
    cout << "r2r_map ("<<n_routers<<"x"<<n_routers<<")"<<endl;

        for (int i = 0; i < n_routers; i++) {
        // cout<<i<<" [ ";
        for (int j = 0; j < n_routers; j++) {
            s = "r2r_map_r" + to_string(i) + "_r" + to_string(j);
            GRBVar var = model.getVarByName(s);
            // outfile << r2r_map[i][j].get(GRB_DoubleAttr_X);
            cout << var.get(GRB_DoubleAttr_X);
            if(j!=n_routers-1) cout<<" ";
        }
        if(i!=n_routers-1) cout<<endl;
    }
    cout<<endl;

    cout << endl;

    cout << "flow_out ("<<n_routers<<"x"<<n_routers<<"x"<<
            n_routers<<"x"<<n_ports<<")"<<endl;

    for(int i=0; i<n_routers; i++){
        for(int j=0; j<n_routers; j++){
            if(i==j)continue;
            for(int k=0; k<n_routers; k++){
                if(j==k)continue;
                for(int l=0; l<n_ports; l++){

                    s = "flow_out_r" + to_string(i) + "_r" + to_string(j) +
                        "_r" + to_string(k) + "_p" + to_string(l);

                    GRBVar var = model.getVarByName(s);
                    if(var.get(GRB_DoubleAttr_X) >= 0.5){
                        cout<<"r"<<i<<"->r"<<j<<": "<<"r"<<k<<"p"<<l<<" : "<<var.get(GRB_DoubleAttr_X)<<endl;
                    }
                    // cout<<"r"<<i<<"p"<<j<<" -> "<<"r"<<k<<"p"<<l<<" : "<<var.get(GRB_DoubleAttr_X)<<endl;
                }
            }
        }
    }
    cout<<endl;
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
            s = "r2r_map_r" + to_string(i) + "_r" + to_string(j);
            GRBVar var = model.getVarByName(s);
            // outfile << r2r_map[i][j].get(GRB_DoubleAttr_X);
            outfile << var.get(GRB_DoubleAttr_X);
            if(j!=n_routers-1) outfile<<" ";
        }
        if(i!=n_routers-1) outfile<<endl;
    }
}


void print_flows_to_file(string s,
                    GRBModel &model,
                    int n_routers,
                    int n_ports)
{

    ofstream outfile(s);

    // write array(s)
    // --------------
    for(int i=0; i<n_routers; i++){
        for(int j=0; j<n_routers; j++){
            if(i==j)continue;
            for(int k=0; k<n_routers; k++){
                if(j==k)continue;
                for(int l=0; l<n_ports; l++){

                    s = "flow_out_r" + to_string(i) + "_r" + to_string(j) +
                        "_r" + to_string(k) + "_p" + to_string(l);

                    GRBVar var = model.getVarByName(s);
                    if(var.get(GRB_DoubleAttr_X) >= 0.5){
                        outfile <<"r"<<i<<"->r"<<j<<": "<<"r"<<k<<"p"<<l<<" : "<<var.get(GRB_DoubleAttr_X)<<endl;
                    }
                }
            }
            
        }
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

        // Globals
        // ------------------------------------------------------------------

        // temp var for strings (setting names and such)
        string s;
        const char* myname = "lpbt";

        // Design Givens (i.e. inputs)
        // ------------------------------------------------------------------
        int n_routers = 6;

        // TODO: change if not diretly mapping 1:1 node:router
        int n_nodes = n_routers;
        int n_router_rows = 2;

        // 1 extra for n2p
        int n_ports = 5;

        // imprtant
        // 15ll, 2ll, 25ll => 1.5, 2.0, 2.5
        double longest_link = 2.5;


        // allow worst case:
        //      all (n_routers) X (n_routers) flows through this port
        //      = n_routers*n_routers - n_routers
        int max_port_out_bw = n_routers*n_routers - n_routers;
        int max_port_in_bw = n_routers*n_routers - n_routers;

        // distance stuff
        double* router_x_pos;
        double* router_y_pos;
        double** r2r_phys_dist;
        double** n2r_phys_dist;

        // important
        // TODO: change if not diretly mapping 1:1 node:router
        double basic_node_to_router_dist = 0.1;


        // CLA variable declarations
        // ------------------------------------------------------------------
        // file level params
        char givens_file_name[MAX_STR_LEN];
        strcpy(givens_file_name, "files/prob_defs/dev_12r_25ll.dat");
        bool read_from_file = false;

        char out_file_name[MAX_STR_LEN];
        strcpy(out_file_name, "12r_25ll");
        bool out_name_given = false;

        // formulation params
        bool uni_dir_links = false;
        Objective obj = TOTAL_HOPS;

        // solver params
        bool no_solve = false;
        bool use_nodefiles = false;
        bool use_run_sol = false;
        int heuristic_ratio = -1.0;
        bool set_time_limit = false;
        int time_limit = -1;
        bool set_mip_gap = false;
        int mip_gap = -1;
        double obj_limit = 0.0;
        bool use_concurrent_mip = false;
        bool mem_sensitive = false;
        int mip_focus = -1;
        int presolve_val = -1;
        bool write_model = false;
        bool write_presolved = false;
        bool use_lp_model = false;

        // overrides
        int cla_n_routers = n_routers;
        bool override_num_routers = false;
        int cla_router_rows = n_router_rows;
        bool override_router_rows = false;
        int cla_n_ports = n_ports;
        bool override_ports = false;
        double cla_ll = longest_link;
        bool override_ll = false;


        // CLAs
        // ------------------------------------------------------------------

        for(int i=1; i<argc; i++){

            // file level params
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

            // formulation params
            else if( strcmp(argv[i], "--uni_links") == 0 )
            {
                uni_dir_links = true;
            }

            // objectives
            else if( (strcmp(argv[i], "-o") == 0) || 
                (strcmp(argv[i], "--objective") == 0)
                )
            {
                if(strcmp(argv[i+1],"total_hops") == 0){
                    obj = TOTAL_HOPS;
                    i++;
                }
                else if(strcmp(argv[i+1],"power") == 0){
                    obj = POWER;
                    i++;
                }
                else{
                    cout << "Unrecognized objective: "<<argv[i+1]<< endl<<endl;
                    usage(myname);
                    exit(returncode);
                }
            }

            // solver params
            else if(strcmp(argv[i], "--use_run_sol") == 0){
                use_run_sol = true;
            }
            else if( strcmp(argv[i], "--no_solve") == 0 )
            {
                no_solve = true;
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
            else if( strcmp(argv[i], "--obj_limit") == 0 )
            {
                obj_limit = atof(argv[++i]);
            }
            else if( strcmp(argv[i], "--heuristic_ratio") == 0 )
            {
                heuristic_ratio = atof(argv[++i]);
            }
            else if (strcmp(argv[i], "--concurrent_mip") ==0)
            {
                use_concurrent_mip = true;
            }
            else if (strcmp(argv[i], "--mem_sensitive") ==0)
            {
                mem_sensitive = true;
            }
            else if( strcmp(argv[i], "--mip_focus") == 0 )
            {
                mip_focus = atoi(argv[++i]);
            }

            // overrides
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

        // CLA overrides
        // -------------
        if (override_ports) n_ports = cla_n_ports;
        if (override_num_routers) n_routers = cla_n_routers;
        if (override_ll) longest_link = cla_ll;
        if (override_router_rows) n_router_rows = cla_router_rows;

        // TODO: remove if not doing 1:1 node:router ratio
        n_nodes = n_routers;

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

        n2r_phys_dist = (double**)malloc(sizeof(double*)*n_nodes);

        // calculate distances (so that it does not need to be calculated on the fly, during optimization)
        // also, initialize the 2D dist arrays
        // this is euclidean distance
        for(int i = 0; i<n_nodes;i++){
            n2r_phys_dist[i] = (double*)malloc(sizeof(double)*n_routers);
            // r2r_phys_dist.add(IloNumArray(env,n_routers));
            for(int j = 0; j<n_routers;j++){
                if(i == j){
                    n2r_phys_dist[i][j] = 0.0;
                    continue;
                }

                // TODO change this?
                double  dist = 0.1;
                n2r_phys_dist[i][j] = dist;
            }
        }


        // Quick Print of Givens
        // ------------------------------------------------------------------
        cout<<endl;
        cout<<"CLA/default/file values:"<<endl;
        cout<<"------------------------"<<endl;
        cout<<"n_routers="<<n_routers<<", n_ports="<<n_ports<<\
                ", longest_link="<<longest_link<<\
                ", n_router_rows="<<n_router_rows<<endl;


        #ifdef DEBUG

        cout<<"r2r physical distances:"<<endl;
        cout<<"-----------------------"<<endl;
        for (int i = 0; i < n_routers; i++) {
            cout<< i<<": [ ";
            for (int j = 0; j < n_routers; j++) {
                cout << r2r_phys_dist[i][j]<<", ";
            }
            cout << " ]"<<endl;
        }
        cout<<endl;

        cout<<"n2r physical distances:"<<endl;
        cout<<"-----------------------"<<endl;
        for (int i = 0; i < n_nodes; i++) {
            cout<< i<<": [ ";
            for (int j = 0; j < n_routers; j++) {
                cout << n2r_phys_dist[i][j]<<", ";
            }
            cout << " ]"<<endl;
        }
        cout<<endl;

        #endif


        // append obj
        string model_obj_str;
        switch(obj){
            case TOTAL_HOPS:
                model_obj_str = "_tothops";
                break;
            case POWER:
                model_obj_str = "_power";
                break;
            default:
                printf("Objective nto recognized\n");
                model_obj_str = "_unk";
                break;
        }

        string base_file_name;
        string out_model_format;
        out_model_format = ".mps";
        if(use_lp_model) out_model_format = ".lp";

        base_file_name = "lpbt_r" + to_string(n_routers) + "_p" + to_string(n_ports) + "_ll" + to_string(int(10.0*longest_link)) + string(model_obj_str);
        if(uni_dir_links) base_file_name = string(base_file_name) + "_asym";
        // CLA override
        if(out_name_given) base_file_name =  string(out_file_name);


        // ==================================================================
        // | Gurobi Model and Variables
        // ==================================================================
        
        // Model
        // ------------------------------------------------------------------

        GRBModel model = GRBModel(*env);

        #ifdef DEBUG
            cout<<"Token Server: "<<model.get(GRB_StringParam_TokenServer)<<endl;
        #endif

        model.set(GRB_StringAttr_ModelName, "lpbt");

        // Independent Variable Declarations
        // ------------------------------------------------------------------

        GRBVar*** n2p_map = NULL;
        GRBVar**** p2p_map = NULL;
        GRBVar**** flow_out = NULL;
        GRBVar**** flow_in = NULL;

        // n2p_map (n_nodes x n_routers x n_ports)
        // i.e. (node i) X (router j, port k)
        n2p_map = new GRBVar**[n_nodes];
        for(int i=0; i<n_nodes; i++){

            n2p_map[i] = new GRBVar*[n_routers];

            for(int j=0; j<n_routers; j++){
                n2p_map[i][j] = new GRBVar[n_ports];

                for(int k=0; k<n_ports; k++){

                    // naming important
                    // when extracing solution later, uses getVarByName
                    s = "n2p_map_n" + to_string(i) + "_r" + to_string(j) +
                        "_p" + to_string(k);

                    n2p_map[i][j][k] = model.addVar(0,1,0,GRB_BINARY, s);
                }
            }
        }

        // p2p_map (n_routers x n_ports x n_routers x n_ports)
        // i.e. (router i, port j) X (router k, port l)
        p2p_map = new GRBVar***[n_routers];
        for(int i=0; i<n_routers; i++){
            p2p_map[i] = new GRBVar**[n_ports];

            for(int j=0; j<n_ports; j++){
                p2p_map[i][j] = new GRBVar*[n_routers];

                for(int k=0; k<n_routers; k++){
                    p2p_map[i][j][k] = new GRBVar[n_ports];

                    for(int l=0; l<n_ports; l++){

                        // naming important
                        // when extracing solution later, uses getVarByName
                        s = "p2p_map_r" + to_string(i) + "_p" + to_string(j) +
                            "_r" + to_string(k) + "_p" + to_string(l);

                        p2p_map[i][j][k][l] = model.addVar(0,1,0,GRB_BINARY, s);
                    }
                }
            }
        }

        // flow out/in (n_routers x n_routers x n_routers x n_ports)
        // i.e. (router i) X (router j) X (router k, port l)
        flow_out = new GRBVar***[n_nodes];
        flow_in = new GRBVar***[n_nodes];
        for(int i=0; i<n_nodes; i++){
            flow_out[i] = new GRBVar**[n_nodes];
            flow_in[i] = new GRBVar**[n_nodes];

            for(int j=0; j<n_nodes; j++){
                flow_out[i][j] = new GRBVar*[n_routers];
                flow_in[i][j] = new GRBVar*[n_routers];

                for(int k=0; k<n_routers; k++){
                    flow_out[i][j][k] = new GRBVar[n_ports];
                    flow_in[i][j][k] = new GRBVar[n_ports];

                    for(int l=0; l<n_ports; l++){

                        // naming important
                        // when extracing solution later, uses getVarByName
                        s = "flow_out_r" + to_string(i) + "_r" + to_string(j) +
                            "_r" + to_string(k) + "_p" + to_string(l);

                        flow_out[i][j][k][l] = model.addVar(0,1,0,GRB_BINARY, s);

                        // naming important
                        // when extracing solution later, uses getVarByName
                        s = "flow_in_r" + to_string(i) + "_r" + to_string(j) +
                            "_r" + to_string(k) + "_p" + to_string(l);

                        flow_in[i][j][k][l] = model.addVar(0,1,0,GRB_BINARY, s);
                    }
                }
            }
        }



        // Dependent Variable Declarations
        // ------------------------------------------------------------------

        GRBVar** r2r_map = NULL;
        GRBVar** tot_traff_out_port = NULL;
        GRBVar** tot_traff_in_port = NULL;
        GRBVar****** flow_traffic_link = NULL;

        // added to output an r2r map
        // r2r_map (n_routers x n_routers)
        // i.e. (router i) X (router k)
        // later, defined by constraints,
        // r2r_map[i][j] = 1 if sum(p2p_map[i][a][j][b] for a, b 0, ...n_ports)
        //   ie if any port connected
        r2r_map = new GRBVar*[n_routers];

        for(int i=0; i<n_routers; i++){
            r2r_map[i] = new GRBVar[n_routers];

            for(int j=0; j<n_routers; j++){

                // naming important
                // when extracing solution later, uses getVarByName
                s = "r2r_map_r" + to_string(i) + "_r" + to_string(j);

                r2r_map[i][j] = model.addVar(0,n_ports,0,GRB_INTEGER, s);
            }
        }


        // tot_traff_out/in_port (n_routers x n_ports)
        // looking at router i, port j, what is total flows going through
        //      within range [0, n_routers*n_routers - n_routers ]
        tot_traff_out_port = new GRBVar*[n_routers];
        tot_traff_in_port = new GRBVar*[n_routers];

        double max_val = n_routers*n_routers - n_routers;

        for(int i=0; i<n_routers; i++){
            tot_traff_out_port[i] = new GRBVar[n_ports];
            tot_traff_in_port[i] = new GRBVar[n_ports];

            for(int j=0; j<n_ports; j++){

                // naming important
                // when extracing solution later, uses getVarByName
                s = "tot_traff_out_port_r" + to_string(i) + "_p" + to_string(j);

                tot_traff_out_port[i][j] = model.addVar(0,max_val,0,GRB_CONTINUOUS, s);

                // naming important
                // when extracing solution later, uses getVarByName
                s = "tot_traff_in_port_r" + to_string(i) + "_p" + to_string(j);

                tot_traff_in_port[i][j] = model.addVar(0,max_val,0,GRB_CONTINUOUS, s);
            }
        }

        // flow_traffic_link (n_routers x n_routers x n_routers x n_ports x n_routers x n_ports)
        // binary variable
        //  1 if flow i->j and link between router k, port l and router m, port n
        flow_traffic_link = new GRBVar*****[n_routers];

        for(int i=0; i<n_nodes; i++){
            flow_traffic_link[i] = new GRBVar****[n_routers];

            for(int j=0; j<n_nodes; j++){
                flow_traffic_link[i][j] = new GRBVar***[n_routers];

                for(int k=0; k<n_routers; k++){
                    flow_traffic_link[i][j][k] = new GRBVar**[n_ports];

                    for(int l=0; l<n_ports; l++){
                        flow_traffic_link[i][j][k][l] = new GRBVar*[n_routers];

                        for(int m=0; m<n_routers; m++){
                            flow_traffic_link[i][j][k][l][m] = new GRBVar[n_ports];

                            for(int n=0; n<n_ports; n++){
                                s = "flow_traffic_link_n" + to_string(i) + "_n" + to_string(j) +
                                        "_r" + to_string(k) + "_p" + to_string(l) + 
                                        "_r" + to_string(m) + "_p" + to_string(n);
                                flow_traffic_link[i][j][k][l][m][n] = model.addVar(0,1,0,GRB_BINARY, s);
                            }
                        }
                    }
                }
            }
        }


        // ==================================================================
        // | Constraints: ...
        // ==================================================================

        // Variable Constraints (ie defining dependent variables)
        //
        // 1/2) total traffic out/in a port
        // 2) flow of traffic on link
        // ------------------------------------------------------------------

        // TODO

        // 1/2) tot_traff_out/in_port
        for(int k=0; k<n_routers; k++){

            // for every port
            for(int l=0; l<n_ports; l++){
                GRBLinExpr out_expr = 0;
                GRBLinExpr in_expr = 0;

                // sum all flows through
                for(int i=0; i<n_nodes; i++){
                    for(int j=0; j<n_nodes; j++){

                        if(i==j) continue;

                        // add constant if desired

                        out_expr += flow_out[i][j][k][l];
                        in_expr += flow_in[i][j][k][l];

                    }
                }

                model.addConstr(tot_traff_out_port[k][l] == out_expr);
                model.addConstr(tot_traff_in_port[k][l] == in_expr);
            }
        }

        // 3) flow of traffic on link
        // linearized into two equations

        for(int i=0; i<n_nodes; i++){
            for(int j=0; j<n_nodes; j++){
                
                if(i==j) continue;

                for(int k=0; k<n_routers; k++){
                    for(int l=0; l<n_ports; l++){
                        for(int m=0; m<n_routers; m++){
                            for(int n=0; n<n_ports; n++){

                                model.addConstr(2*flow_traffic_link[i][j][k][l][m][n] <= flow_out[i][j][k][l] + p2p_map[k][l][m][n]);
                                model.addConstr(1 + flow_traffic_link[i][j][k][l][m][n] >= flow_out[i][j][k][l] + p2p_map[k][l][m][n]);

                            }
                        }
                    }
                }
            }
        }


        // Other Contstraints
        // ------------------------------------------------------------------


        // port to port mapping
        for(int i=0; i<n_routers; i++){
            for(int j=0; j<n_ports; j++){
                GRBLinExpr total_conns = 0;


                for(int k=0; k<n_routers; k++){

                    if(i==k) continue;

                    for(int l=0; l<n_ports; l++){
                        total_conns += p2p_map[k][l][i][j];
                    }
                }

                for(int m=0; m<n_nodes; m++){
                    total_conns += n2p_map[m][i][j];
                }

                model.addConstr(total_conns <= 1);
            }
        }

        // port symmetry
        for(int i=0; i<n_routers; i++){
            for(int j=0; j<n_ports; j++){
                for(int k=0; k<n_routers; k++){

                    if(i==k) continue;

                    for(int l=0; l<n_ports; l++){
                        model.addConstr(p2p_map[i][j][k][l] == p2p_map[k][l][i][j]);
                    }
                }
            }
        }

        // node to port
        for(int i=0; i<n_nodes; i++){
            GRBLinExpr this_nodes_conn = 0;
            for(int k=0; k<n_routers; k++){
                for(int l=0; l<n_ports; l++){
                    this_nodes_conn += n2p_map[i][k][l];
                }
            }

            model.addConstr(this_nodes_conn == 1);
        }



        // Traffic Routing Constraints (ie making graph connected)
        //
        // 1) ...
        // 2) another node to router (n/a)
        // 3) traffic entering/exiting port should not enter/exit any other
        //      port of same router
        // 4) traffic in => equal traffic out and vice-versa
        // ------------------------------------------------------------------

        // 1) node mapped to port of a router =>
        //      all traffic...
        for(int i=0; i<n_nodes; i++){
            for(int j=0; j<n_nodes; j++){
                
                if(i==j) continue;

                for(int k=0; k<n_routers; k++){
                    

                    for(int l=0; l<n_ports; l++){

                        model.addConstr(flow_in[i][j][k][l] >= n2p_map[i][k][l]);
                        model.addConstr(flow_out[i][j][k][l] >= n2p_map[j][k][l]);

                    }

                }
            }
        }

        // 2) if a node is mapped to a port of a router no traffic from any other...
        for(int i=0; i<n_nodes; i++){
            for(int j=0; j<n_nodes; j++){
                
                if(i==j) continue;
                for(int m=0; m<n_nodes; m++){
                    if(i==m) continue;
                    if(j==m) continue;

                    for(int k=0; k<n_routers; k++){
                        for(int l=0; l<n_ports; l++){

                            model.addConstr(flow_in[i][j][k][l] + n2p_map[m][k][l] <= 1);
                            model.addConstr(flow_out[i][j][k][l] + n2p_map[m][k][l] <= 1);

                        }
                    }
                }
            }
        }        

        // 3) if traffic enters a port of the router it should not enter...
        for(int i=0; i<n_routers; i++){
            for(int j=0; j<n_routers; j++){
                
                if(i==j) continue;

                for(int k=0; k<n_routers; k++){
                    GRBLinExpr all_in_flows = 0;
                    GRBLinExpr all_out_flows = 0;

                    for(int l=0; l<n_ports; l++){
                        all_in_flows += flow_in[i][j][k][l];
                        all_out_flows += flow_out[i][j][k][l];
                    }

                    model.addConstr(all_in_flows <= 1);
                    model.addConstr(all_out_flows <= 1);
                }
            }
        }

        // 4) if traffic neters a port i thas to leave from exactly one 
        for(int i=0; i<n_routers; i++){
            for(int j=0; j<n_routers; j++){
                
                if(i==j) continue;

                for(int k=0; k<n_routers; k++){
                    for(int l=0; l<n_ports; l++){

                        GRBLinExpr all_out_flows = 0;
                        GRBLinExpr all_in_flows = 0;

                        for(int m=0; m<n_ports; m++){

                            if(l==m) continue;

                            all_out_flows += flow_out[i][j][k][m];
                            all_in_flows += flow_in[i][j][k][m];
                        }
                        model.addConstr(all_out_flows >= flow_in[i][j][k][l]);
                        model.addConstr(all_in_flows >= flow_out[i][j][k][l]);
                    }
                }
            }
        }

        // 5)
        for(int i=0; i<n_routers; i++){
            for(int j=0; j<n_routers; j++){

                if(i==j) continue;

                for(int k=0; k<n_routers; k++){
                    for(int l=0; l<n_ports; l++){
                        for(int m=0; m<n_routers; m++){

                            if(k==m) continue;

                            for(int n=0; n<n_ports; n++){

                                model.addConstr(p2p_map[k][l][m][n] + flow_in[i][j][k][l] - flow_out[i][j][m][n] <= 1);
                                model.addConstr(p2p_map[k][l][m][n] - flow_in[i][j][k][l] + flow_out[i][j][m][n] <= 1);

                            }
                        }
                    }
                }
            }
        }

        // 6)
        for(int i=0; i<n_routers; i++){
            for(int j=0; j<n_routers; j++){

                if(i==j) continue;

                for(int k=0; k<n_routers; k++){
                    for(int l=0; l<n_ports; l++){
                        for(int m=0; m<n_routers; m++){

                            if(k==m) continue;

                            for(int n=0; n<n_ports; n++){

                                model.addConstr(p2p_map[k][l][m][n] + flow_in[i][j][k][l] + flow_in[i][j][m][n] <= 2);
                                model.addConstr(p2p_map[k][l][m][n] + flow_out[i][j][k][l] + flow_out[i][j][m][n] <= 2);

                            }
                        }
                    }
                }
            }
        }

        // 7)
        for(int i=0; i<n_nodes; i++){
            for(int j=0; j<n_nodes; j++){

                if(i==j) continue;

                for(int k=0; k<n_routers; k++){
                    for(int l=0; l<n_ports; l++){

                        GRBLinExpr all_conns = 0;
                        for(int m=0; m<n_routers; m++){

                            if(k==m) continue;

                            for(int n=0; n<n_ports; n++){

                                all_conns += p2p_map[k][l][m][n];
                            }
                        }

                        model.addConstr(n2p_map[j][k][l] + all_conns >= flow_in[j][i][k][l]);
                        model.addConstr(n2p_map[i][k][l] + all_conns >= flow_out[j][i][k][l]);
                    }
                }
            }
        }

        // 8) latency constraint
        int max_hops = n_routers - 1;
        for(int i=0; i<n_routers; i++){
            for(int j=0; j<n_routers; j++){

                if(i==j) continue;

                GRBLinExpr n_hops = 0;

                for(int k=0; k<n_routers; k++){
                    for(int l=0; l<n_ports; l++){
                        
                        n_hops += flow_out[i][j][k][l];
                        
                    }
                }

                model.addConstr(n_hops <= max_hops);
            }
        }



        // NetSmith Specific Constraint(s)
        // ------------------------------------------------------------------

        // limit the longest length
        // ------------------------

        for(int i=0; i<n_routers; i++){
            for(int j=0; j<n_ports; j++){
                for(int k=0; k<n_routers; k++){
                    for(int l=0; l<n_ports; l++){

                        // if too long a link
                        //   not too long if less than or equal to max
                        //   (ie inclusive max)
                        if (r2r_phys_dist[i][k] > longest_link ){
                            model.addConstr(p2p_map[i][j][k][l] == 0);
                        }

                    }
                }
            }
        }

        // simple mapping
        // --------------

        for(int i=0; i<n_nodes; i++){

            model.addConstr(n2p_map[i][i][0] == 1);

        }

        // define r2r map
        for(int i=0; i<n_routers; i++){
            for(int k=0; k<n_routers; k++){
                if(i==k) continue;

                GRBLinExpr n_conns = 0;
                for(int j=0; j<n_ports; j++){

                    for(int l=0; l<n_ports; l++){

                        n_conns += p2p_map[i][j][k][l];
                    }
                }

                model.addConstr(r2r_map[i][k] == n_conns);
            }
        }

        // ==================================================================
        // | Model : Write Model to File
        // ==================================================================

        s = "files/models/lpbt/" + string(base_file_name) + string(out_model_format);
        if(write_model){
            model.write(s);
            cout << "Wrote model to " << s << endl;
        }

        // ==================================================================
        // | Objective(s) : ...
        // ==================================================================


        // Set Objective
        // ------------------------------------------------------------------
        switch(obj){
            case TEST:
                cout << "Set obj: test" << endl;
                set_test_objective(model, p2p_map, n_routers, n_ports);
                break;
            case TOTAL_HOPS:
                cout << "Set obj: total hops" << endl;
                set_hop_objective(model, flow_out, n_nodes, n_routers, n_ports);
                break;
            case POWER:
                cout << "Set obj: power" << endl;
                set_power_objective(model,
                                    tot_traff_in_port, tot_traff_out_port,
                                    n2r_phys_dist, r2r_phys_dist,
                                    flow_traffic_link,
                                    n2p_map,
                                    n_routers, n_ports);
                break;
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
        if (obj_limit != 0.0) model.set(GRB_DoubleParam_BestObjStop, obj_limit);


        // proportion of time spent using heuristics
        // 0.5 => 50%
        // -----------------------------------------
        if(heuristic_ratio != -1.0) model.set(GRB_DoubleParam_Heuristics, heuristic_ratio);

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
        string cb_outfile_name;
        ofstream cb_outfile;
        string cb_outfile_name_flows;
        ofstream cb_outfile_flows;

        if(!out_name_given){
            cb_outfile_name = "files/running_solutions/lpbt_r" + to_string(n_routers) + "_p" + to_string(n_ports) +
                "_ll" + to_string(int(10.0*longest_link)) + ".map";
                cb_outfile_name_flows = "files/running_solutions/lpbt_r" + to_string(n_routers) + "_p" + to_string(n_ports) +
                "_ll" + to_string(int(10.0*longest_link)) + ".flows";
        }
        else{
            cb_outfile_name = "files/running_solutions/" + string(out_file_name) + ".map";
            cb_outfile_name_flows = "files/running_solutions/" + string(out_file_name) + ".flows";
        }
        cb_outfile = ofstream(cb_outfile_name, ios_base::trunc);
        cb_outfile_flows = ofstream(cb_outfile_name_flows, ios_base::trunc);

        incumbent_solution_callback isc = incumbent_solution_callback(&model, r2r_map, flow_out , &cb_outfile, cb_outfile_name,&cb_outfile_flows, cb_outfile_name_flows, n_routers);
        if(use_run_sol){

            cout << "Setting callback"<<endl;
            model.setCallback(&isc);
        }

        // TODO

        // Solve
        // ------------------------------------------------------------------

        if (no_solve){
            cout<<"no_solve parameter passed. Exiting early"<<endl;
            return 0;
        }

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

        print_to_console(model, n_nodes, n_routers, n_ports);

        cout << "completed to console"<< endl;

        s = "files/optimal_solutions/" + string(base_file_name) + ".map";
        print_map_to_file(s, model, n_routers);

        s = "files/optimal_solutions/" + string(base_file_name) + ".flows";
        print_flows_to_file(s, model, n_routers, n_ports);

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
