"""Tests for apply_pipeline in mip.utils.tranformers"""

from mip.utils.transforms import apply_pipeline



def test_apply_pipeline_composes_three_functions_in_order():

    add =  lambda x : x+1 
    multiply = lambda x: x*4
    power = lambda x : x**2


    pipeline = [add , multiply , power]

    assert apply_pipeline(0 , *pipeline) == 16


def test_apply_pipeline_with_no_functions_returns_value_unchanged() :

    assert apply_pipeline(4 , *[]) == 4

