import pytest

def average_rating(rating):
    if len(rating) == 0:
        return None
    return sum(rating) / len(rating)

@pytest.mark.parametrize("input_list, expected_output", [
    ([4, 5, 3], 4.0),    
    ([1, 2], 1.5),       
    ([], None),          
])
def test_average_rating_edge(input_list, expected_output):
    assert average_rating(input_list) == expected_output