
import pytest 
import time

import source.functions as func 


@pytest.fixture(autouse=True)
def setup_function():
    print("B E F O R E - T E S T")
   
@pytest.mark.parametrize("first_num, second_num, expected_sum", [(2, 4, 6), (5, 5, 10), (3, 1, 4)])
def test_add(first_num, second_num, expected_sum):
    assert func.add(first_num, second_num) == expected_sum

@pytest.mark.slow
def test_divide():
    time.sleep(5)
    result = func.divide(8, 4)
    assert result == 2

@pytest.mark.xfail
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        func.divide(10, 0)

@pytest.mark.skip(reason = "Writing test unit for operation on digits")
def test_concat():
    result = func.concat("papa ", "maman")
    assert result == "papa maman"




