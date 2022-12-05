import numpy as np
import pytest
import riscv_sim.main as riscv


basic_control_flow = """

// r0: 80-89 => 90, 90-99 => 100, Other => -1
flatten_grade:
    li r1, -1
    li r2, 79
    bgt r0, r2, grade_b
    li r3, 10
    add r2, r2, r3
    bgt r0, r2, grade_a
    mv r0, r1

grade_a:
    li r1, 100

grade_b:
    li r1, 90

"""


@pytest.fixture
def processor():
    return riscv.Processor()


def test_doctests():
    import doctest
    doctest.testmod()


def test_tokenize():
    assert riscv.tokenize("not r3, r8") == [["not", "r3", "r8"]]
    assert riscv.tokenize("addi r3 ,r8,5") == [["addi", "r3", "r8", "5"]]
    assert riscv.tokenize("// This is a // comment") == []
    assert riscv.tokenize("""
    mv r1, r0
    xor r2, r0, r1
    ret
    """) == [["mv", "r1", "r0"], ["xor", "r2", "r0", "r1"], ["ret"]]
    assert riscv.tokenize(basic_control_flow) == [
        ['flatten_grade:'],
        ['li', 'r1', '-1'],
        ['li', 'r2', '79'],
        ['bgt', 'r0', 'r2', 'grade_b'],
        ['li', 'r3', '10'],
        ['add', 'r2', 'r2', 'r3'],
        ['bgt', 'r0', 'r2', 'grade_a'],
        ['mv', 'r0', 'r1'],
        ['grade_a:'],
        ['li', 'r1', '100'],
        ['grade_b:'],
        ['li', 'r1', '90']
    ]


def test_parse():
    opcodes = riscv.OPNAME_TO_OPCODE
    assert riscv.parse([["a:", "not", "r3", "r8"]]) == [[[opcodes["not"], 3, 8]]]
    assert riscv.parse([["b:", "add", "r3", "r8", "r5"]]) == [[[opcodes["add"], 3, 8, 5]]]
    assert riscv.parse(riscv.tokenize(basic_control_flow)) == [
        [
            [opcodes["li"], 1, -1],
            [opcodes["li"], 2, 79],
            [opcodes["bgt"], 0, 2, 2],
            [opcodes["li"], 3, 10],
            [opcodes["add"], 2, 2, 3],
            [opcodes["bgt"], 0, 2, 1],
            [opcodes["mv"], 0, 1]
        ],
        [[opcodes["li"], 1, 100]],
        [[opcodes["li"], 1, 90]]
    ]


def test_evaluate(processor):
    processor.registers[0] = np.int32(20)
    riscv.evaluate(riscv.parse(riscv.tokenize("hello: li r1, 5"))[0][0], processor)
    assert processor.registers[1] == np.int32(5)
    riscv.evaluate(riscv.parse(riscv.tokenize("main: add r3, r0, r1"))[0][0], processor)
    assert processor.registers[3] == np.int32(25)


def test_evaluate_body(processor):
    processor.functions = riscv.parse(riscv.tokenize(basic_control_flow))

    riscv.evaluate_body(processor.functions[1], processor)
    assert processor.registers[1] == np.int32(100)

    riscv.evaluate_body(processor.functions[2], processor)
    assert processor.registers[1] == np.int32(90)

    processor.registers[0] = np.int32(50)
    riscv.evaluate_body(processor.functions[0], processor)
    assert processor.registers[0] == np.int32(-1)

    processor.registers[0] = np.int32(85)
    riscv.evaluate_body(processor.functions[0], processor)
    assert processor.registers[0] == np.int32(90)

    processor.registers[0] = np.int32(95)
    riscv.evaluate_body(processor.functions[0], processor)
    assert processor.registers[0] == np.int32(100)
