def ode_function(t, y, function_str):
    """
    Định nghĩa một bài toán giá trị ban đầu, ví dụ: y' = f(t, y).

    Args:
        t (float): Biến thời gian.
        y (float): Biến phụ thuộc.
        function_str (str): Biểu thức toán học dưới dạng chuỗi.

    Returns:
        float: Giá trị của f(t, y) đã được đánh giá.
    """
    # Đánh giá biểu thức với giá trị của t và y
    return eval(function_str)

# Nhập biểu thức một lần trước vòng lặp
function_str = input("Nhập hàm f(t, y): ").replace("^", "**")

# Ví dụ với một vòng lặp for
for i in range(3):  # Lặp lại 3 lần
    t = float(input(f"Nhập giá trị t lần {i+1}: "))
    y = float(input(f"Nhập giá trị y lần {i+1}: "))
    
    result = ode_function(t, y, function_str)
    print(f"Kết quả của lần {i+1}: {result}")
