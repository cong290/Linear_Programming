# Khai báo thư viện
import pulp

def input_linear_programming_problem():
    print("\n*** NHẬP VÀO BÀI TOÁN QUY HOẠCH TUYẾN TÍNH ***")
    # Nhập vào điều kiện tối ưu
    optimize = input("- Nhập vào min/max: ")
    
    # Yêu cầu nhập số lượng biến và số lượng ràng buộc
    num_variables = int(input("- Nhập số lượng biến: "))
    num_constraints = int(input("- Nhập số lượng ràng buộc: "))
    
    # Nhập các hệ số của hàm mục tiêu
    obj_coeffs = []
    print("------")
    for i in range(num_variables):
        coeff = float(input(f"Nhập hệ số của x{i+1} trong hàm mục tiêu: "))
        obj_coeffs.append(coeff)
        
    # Tạo các ràng buộc và thêm vào list
    constraints = []
    for i in range(num_constraints):
        constraint_coeffs = []
        print("------")
        for j in range(num_variables):
            coeff = float(input(f"Nhập hệ số của x{j+1} trong ràng buộc thứ {i+1}: "))
            constraint_coeffs.append(coeff)
        relation = input(f"Nhập dấu của ràng buộc thứ {i+1} ('<=', '>=', '='): ")
        value = float(input(f"Nhập giá trị của ràng buộc thứ {i+1}: "))
        
        constraints.append((constraint_coeffs, relation, value))

        
    return  optimize, num_variables, num_constraints, obj_coeffs, constraints

def check_coeff_diff0_before(index_j, num_variables, obj_coeffs):
    for i in range(0, index_j):
        if obj_coeffs[i] != 0:
            return True
    return False      

def display_linear_programming_problem(optimize, num_variables, num_constraints, obj_coeffs, constraints):
    print("\n--- BÀI TOÁN QUY HOẠCH TUYẾN TÍNH ---\n")
    # In hàm mục tiêu
    print(f"{optimize} ", end="")
    for j in range(num_variables):
        if j == 0:
            if obj_coeffs[j] == 0:
                continue
            elif obj_coeffs[j] == 1:
                print(f"x{j+1} ", end="")
            elif obj_coeffs[j] == -1:
                print(f"-x{j+1} ", end="")
            else: 
                print(f"{obj_coeffs[j]}*x{j+1} ",end="")
        else: # Không phải phần hệ số đầu tiên
            if obj_coeffs[j] == 0:
                continue
            elif obj_coeffs[j] > 0:
                # Kiểm tra tồn tại biến phía trước có hệ số khác 0
                if check_coeff_diff0_before(j, num_variables, obj_coeffs) == False:
                    if obj_coeffs[j] == 1:
                        print(f"x{j+1} ", end="")
                    else:
                        print(f"{obj_coeffs[j]}*x{j+1} ", end="")
                else:
                    if obj_coeffs[j] == 1:
                        print(f"+ x{j+1} ", end="")
                    else:
                        converted_num = "{}".format(obj_coeffs[j])
                        converted_num = f"+ {converted_num}"
                        print(f"{converted_num}*x{j+1} ", end="")
            else: 
                if obj_coeffs[j] == -1:
                    print(f"- x{j+1} ", end="")
                else: 
                    converted_num = "{}".format(obj_coeffs[j])
                    converted_num = converted_num.replace('-', '- ')
                    print(f"{converted_num}*x{j+1} ", end="")
    print()
    # In ràng buộc
    for i in range(num_constraints):
        constraint_coeffs, relation, value = constraints[i]
        for j in range(num_variables):
            if j == 0:
                if constraint_coeffs[j] == 0:
                    continue
                elif constraint_coeffs[j] == 1:
                    print(f"x{j+1} ", end="")
                elif constraint_coeffs[j] == -1:
                    print(f"-x{j+1} ", end="")
                else: 
                    print(f"{constraint_coeffs[j]}*x{j+1} ", end="")
            else: # Không phải phần hệ số đầu tiên
                if constraint_coeffs[j] == 0:
                    continue
                elif constraint_coeffs[j] > 0:
                    # Kiểm tra tồn tại biến phía trước có hệ số khác 0
                    if check_coeff_diff0_before(j, num_variables, constraint_coeffs) == False:
                        if constraint_coeffs[j] == 1:
                            print(f"x{j+1} ", end="")
                        else:
                            print(f"{constraint_coeffs[j]}*x{j+1} ", end="")
                    else:
                        if constraint_coeffs[j] == 1:
                            print(f"+ x{j+1} ", end="")
                        else:
                            converted_num = "{}".format(constraint_coeffs[j])
                            converted_num = f"+ {converted_num}"
                            print(f"{converted_num}*x{j+1} ", end="")
                else: 
                    if constraint_coeffs[j] == -1:
                        print(f"- x{j+1} ", end="")
                    else: 
                        converted_num = "{}".format(constraint_coeffs[j])
                        converted_num = converted_num.replace('-', '- ')
                        print(f"{converted_num}*x{j+1} ", end="")
        if relation == "<=":
            print(f"<= {value}")
        elif relation == ">=":
            print(f">= {value}")
        elif relation == "=":
            print(f"= {value}")
    print()
        
def solve_linear_programming_problem(optimize, num_variables, num_constraints, obj_coeffs, constraints):
    # Khởi tạo mô hình bài toán quy hoạch tuyến tính 
    if optimize == 'max':
        model = pulp.LpProblem("Linear Programming", pulp.LpMaximize)
    else:
        model = pulp.LpProblem("Linear Programming", pulp.LpMinimize)
    
    # Khai báo các biến 
    variables = [pulp.LpVariable(f"x{i+1}", lowBound=0, cat="Continuous") for i in range(num_variables)]

    # Thêm hàm mục tiêu vào mô hình
    obj_func = pulp.lpSum([obj_coeffs[i] * variables[i] for i in range(num_variables)])
    model += obj_func

    # Thêm các ràng buộc vào mô hình
    for i in range(num_constraints):
        constraint_coeffs, relation, value = constraints[i]
        if relation == '<=':
            model += pulp.lpSum([constraint_coeffs[i] * variables[i] for i in range(num_variables)]) <= value
        elif relation == '>=':
            model += pulp.lpSum([constraint_coeffs[i] * variables[i] for i in range(num_variables)]) >= value
        elif relation == '=':
            model += pulp.lpSum([constraint_coeffs[i] * variables[i] for i in range(num_variables)]) == value
    
    # Giải bài toán
    model.solve()
    
    # Lấy trạng thái của giải quyết bài toán
    status = pulp.LpStatus[model.status]
    
    # Giá trị tối ưu
    optimize_value = model.objective.value()
    
    # Nghiệm tối ưu là list các giá trị của tất cả các biến
    optimize_of_vars = [variable.value() for variable in variables]
    
    # Trả về giá trị tối ưu và nghiệm tối ưu
    return status, optimize_value, optimize_of_vars        
        
if __name__ == "__main__":
    
    optimize, num_variables, num_constraints, obj_coeffs, constraints = input_linear_programming_problem()
    display_linear_programming_problem(optimize, num_variables, num_constraints, obj_coeffs, constraints)

    status, optimize_value, optimize_of_vars = solve_linear_programming_problem(optimize, num_variables, num_constraints, obj_coeffs, constraints)
    # In kết quả
    if status == "Unbounded":
        print("--- Bài toán QHTT thuộc trường hợp không giới nội! ---")
        if optimize == 'max':
            print("--- Giá trị tối ưu: max = infinity\n")
        else:
            print("--- Giá trị tối ưu: min = - infinity\n")
    elif status == "Infeasible":
            print("--- Bài toán QHTT vô nghiệm! ---")
    else:
        print("--- Giá trị tối ưu: ", optimize_value)
        print("--- Nghiệm tối ưu: ",)
        for i in range(0, len(optimize_of_vars)):
            print(f"\tx{i+1} =", optimize_of_vars[i])
