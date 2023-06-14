import pytest
import os, shutil
from data import *
from findNreplace import *

normal_files = os.listdir('./inputs/normal')
normal_count = len( [file for file in normal_files if file.startswith('input')] )
complex_files = os.listdir('./inputs/complex')
complex_count = len( [file for file in complex_files if file.startswith('input')] )

print("###################### normal count:", normal_count, "\tcomplex count:", complex_count)

def ex_identical(f, g): # explicit identicality test
    filePos = (f.tell(), g.tell())
    f.seek(0,0); g.seek(0,0)
    toReturn = (f.read()) == (g.read())
    f.seek(filePos[0]); g.seek(filePos[1])
    return toReturn


@pytest.fixture(params= [(f"input{i}.txt", f"output{i}.txt") for i in range(1, normal_count+1)])
def setup_normal(request):
    (input_name, output_name) = request.param
    yield (input_name, output_name)

@pytest.fixture(params= [(f"input{i}.txt", f"output{i}.txt") for i in range(1, complex_count+1)])
def setup_complex(request):
    (input_name, output_name) = request.param
    print("complex count:", complex_count)
    print("SETUPCOMPLEX", request.param)
    yield (input_name, output_name)


def test_normal(setup_normal):
    config = {
        'location': 'absolute',
        'folder': False,
        'debug': True,
        'complex': False,
    }

    (input_name, output_name) = setup_normal;
    shutil.copy(f"./inputs/normal/{input_name}", ".")
    findNreplace(input_name, config)

    with open(f"output-{input_name}", 'r') as f, open(f"./outputs/normal/{output_name}", 'r') as g:
        assert ex_identical(f, g), f"test failed for normal input {input_name} with normal config"
    os.remove(f"./output-{input_name}")

def test_complex_1(setup_normal):
    config = {
        'location': 'absolute',
        'folder': False,
        'debug': True,
        'complex': True,
    }
    (input_name, output_name) = setup_normal;
    shutil.copy(f"./inputs/normal/{input_name}", ".")
    findNreplace(input_name, config)

    with open(f"output-{input_name}", 'r') as f, open(f"./outputs/normal/{output_name}", 'r') as g:
        assert ex_identical(f, g), f"test failed for normal input {input_name} with complex config"
    os.remove(f"./output-{input_name}")

def test_complex_2(setup_complex):
    config = {
        'location': 'absolute',
        'folder': False,
        'debug': True,
        'complex': True,
    }
    (input_name, output_name) = setup_complex;
    print("INPUT:",input_name, "OUTPUT:", output_name)
    shutil.copy(f"./inputs/complex/{input_name}", ".")
    findNreplace(input_name, config)

    with open(f"output-{input_name}", 'r') as f, open(f"./outputs/complex/{output_name}", 'r') as g:
        assert ex_identical(f, g), f"test failed for complex input {input_name} with complex config"
    os.remove(f"./output-{input_name}")

