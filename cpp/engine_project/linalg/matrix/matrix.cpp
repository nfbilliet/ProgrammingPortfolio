#include <iostream>
#include <vector>

using namespace std;

template <typename T>
using Matrix = vector<vector<T> >;

template <typename T>
bool assertDim(Matrix<T> &mat_1, Matrix<T> &mat_2){     // Pass by reference to reduce overhead of copying
    // Initialize empty vectors to store the dimensions of the matrices 
    vector<int> mat_1_dim;
    vector<int> mat_2_dim;

}


int main(){
    Matrix<int> test_matrix_1 = {{1, 2, 3},
                                 {4, 5, 6},
                                 {7, 8, 9}};
    Matrix<int> test_matrix_2 = {{1, 2, 3},
                                 {4, 5, 6},
                                 {7, 8, 9}};
    for (int row_idx=0; row_idx<3;row_idx++){
        cout << test_matrix_1[row_idx].size() << " ";
    }            

    for (int row_idx=0; row_idx<3;row_idx++){
        for (int col_idx=0; col_idx<3; col_idx++){
            cout << test_matrix_1[row_idx][col_idx] << " ";
        }
        cout << "\n";
    }
}

/*
Matrix mat_add(Matrix mat_1, Matrix mat_2){
        T matSum[R][C];
        for (int row_idx=0; row_idx<R; row_idx++){
            for (int col_idx=0; col_idx<C; col_idx++){
                matSum[row_idx][col_idx] = mat_1[row_idx][col_idx] + mat_2[row_idx][col_idx];
            }
        }
        return matSum;
}
*/



/*
int main(){
    int test_array_1[3][3] = {{1, 2, 3},
                               {4, 5, 6},
                               {7, 8, 9}};
    int test_array_2[3][3] = {{1, 2, 3},
                               {4, 5, 6},
                               {7, 8, 9}};
    int test_sum_dummy[3][3];

    int test_sum_expected[3][3] = {{2, 4, 6},
                                    {8, 10, 12},
                                    {14, 16, 18}};

    for (int row_idx=0; row_idx<3; row_idx++){
        for (int col_idx=0; col_idx<3; col_idx++){
            test_sum_dummy[row_idx][col_idx] = test_array_1[row_idx][col_idx]+test_array_2[row_idx][col_idx];
        }
    };

    for (int row_idx=0; row_idx<3; row_idx++){
        for (int col_idx=0; col_idx<3; col_idx++){
            cout << test_sum_dummy[row_idx][col_idx] << " ";
        }
        cout << "\n";
    };
    int test_sum_dummy_2; 
    mat_add(test_array_1, test_array_2);
    
}
*/
