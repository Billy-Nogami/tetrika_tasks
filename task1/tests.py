from solution import strict  # Импорт из solution.py

def test_correct_args():
    @strict
    def sum_two(a: int, b: int) -> int:
        return a + b
    
    assert sum_two(1, 2) == 3
    print("Test 1 passed")

def test_wrong_type():
    @strict
    def sum_two(a: int, b: int) -> int:
        return a + b
    
    try:
        sum_two(1, 2.4)
        raise AssertionError("Expected TypeError but no exception was raised")
    except TypeError as e:
        assert "Argument 'b' must be int, not float" in str(e), f"Wrong error message: {e}"
        print("Test 2 passed")

def test_bool_type():
    @strict
    def invert(flag: bool) -> bool:
        return not flag
    
    assert invert(True) is False
    try:
        invert(1)
        raise AssertionError("Expected TypeError for bool")
    except TypeError:
        print("Test 3 passed")

def test_string_type():
    @strict
    def greet(name: str) -> str:
        return f"Hello, {name}!"
    
    assert greet("Alice") == "Hello, Alice!"
    try:
        greet(123)
        raise AssertionError("Expected TypeError for str")
    except TypeError:
        print("Test 4 passed")

def test_keyword_args():
    @strict
    def multiply(a: float, b: float) -> float:
        return a * b
    
    assert multiply(a=2.5, b=2.0) == 5.0
    try:
        multiply(a=2.5, b="2")
        raise AssertionError("Expected TypeError for keyword argument")
    except TypeError as e:
        assert "Argument 'b' must be float, not str" in str(e)
        print("Test 5 passed")

def test_no_annotations():
    @strict
    def no_types(a, b):
        return a + b
    
    assert no_types(3, 4) == 7
    assert no_types("a", "b") == "ab"
    print("Test 6 passed")

def test_mixed_args():
    @strict
    def power(base: float, exponent: int) -> float:
        return base ** exponent
    
    assert power(2.0, 3) == 8.0
    try:
        power(2.0, exponent=3.5)
        raise AssertionError("Expected TypeError for mixed arguments")
    except TypeError:
        print("Test 7 passed")

if __name__ == "__main__":
    test_correct_args()
    test_wrong_type()
    test_bool_type()
    test_string_type()
    test_keyword_args()
    test_no_annotations()
    test_mixed_args()
    print("All tests passed successfully!")