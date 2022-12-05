"""
Inspired by code from MIT classes (6.101 and 6.190)
"""
from typing import Callable

import numpy as np


##############
# EXCEPTIONS #
##############


class ProcessorError(Exception):
    """
    A general exception raised by the RISC-V processor.
    """
    pass


#############
# PROCESSOR #
#############


class Processor:
    """
    Emulates a (simplified) RISC-V processor, with registers and program code.
    """
    NUM_REGISTERS = 8

    def __init__(self):
        """
        Initializes the processor.
        """
        self.registers = [np.int32(0)] * self.NUM_REGISTERS
        self.functions = []
    
    def dump(self) -> None:
        """
        Dumps the processor's data.
        """
        print("Registers:", self.registers)
        # print("Functions:")
        # for i, body in enumerate(self.functions):
        #     print(f"func_{i}()")
        #     print('\n'.join(", ".join(str(x) for x in e) for e in body))
        #     print()


##############
# OPERATIONS #
##############


def operation_li(args: list, proc: Processor):
    """Load immediate instruction."""
    rd, im = args
    proc.registers[rd] = np.int32(im)


def operation_j(args: list, proc: Processor):
    """Jump instruction."""
    label = args[0]
    evaluate_body(proc.functions[label], proc)


def operation_assign_register(func: Callable):
    """
    Creates an operation with the format args[0] = func(register values in args[1:]).

    :param func: A function that returns a single value.
    :return: A function representing the operation.
    """
    def operation(args: list, proc: Processor):
        proc.registers[args[0]] = func(*[proc.registers[arg] for arg in args[1:]])
    return operation


def operation_branch(func: Callable):
    """
    Creates a branch operation, with the format:
    if func(register values in args[:-1]) then call function args[-1] (and come back). Otherwise, do nothing.

    :param func: A boolean function that takes an arbitrary number of arguments.
    :return: A function representing the operation.
    """
    def operation(args: list, proc: Processor):
        if func(*[proc.registers[arg] for arg in args[:-1]]):
            evaluate_body(proc.functions[args[-1]], proc)
    return operation


# Operation constants
OPERATIONS = {
    "li": operation_li,
    "j": operation_j,
    "beq": operation_branch(lambda a, b: a == b),
    "bne": operation_branch(lambda a, b: a != b),
    "bgt": operation_branch(lambda a, b: a > b),
    "blt": operation_branch(lambda a, b: a < b),
    "mv": operation_assign_register(lambda x: x),
    "not": operation_assign_register(lambda x: ~x),
    "add": operation_assign_register(lambda a, b: a + b),
    "sub": operation_assign_register(lambda a, b: a - b),
    "xor": operation_assign_register(lambda a, b: a ^ b),
    "or": operation_assign_register(lambda a, b: a | b),
    "and": operation_assign_register(lambda a, b: a & b),
    "sll": operation_assign_register(lambda a, b: a << b),
    "sra": operation_assign_register(lambda a, b: a >> b),
}
OPNAME_TO_OPCODE = {name: i for i, name in enumerate(OPERATIONS)}
OPCODE_TO_OPERATION = list(OPERATIONS.values())


def evaluate(e: list, proc: Processor, debug=False):
    """
    Evaluates the given expression on the given processor.

    :param e: The expression.
    :param proc: The processor.
    :param debug: Whether to print debug information.
    :return: The result.
    """
    try:
        opcode, args = e[0], e[1:]
        if debug:
            print(f"{list(OPERATIONS.keys())[opcode]}\t {', '.join(str(a) for a in args)}")
        operation = OPCODE_TO_OPERATION[opcode]
        operation(args, proc)
        proc.dump()
    except Exception as e:
        raise ProcessorError(str(e))


def evaluate_body(body: list, proc: Processor):
    """
    Evaluates the given body on the processor.

    :param body: The body.
    :param proc: The processor.
    """
    for e in body:
        evaluate(e, proc)


######################
# TOKENIZER & PARSER #
######################


def convert_literal(x, label_to_index):
    """
    Converts the given literal into an integer.

    :param x: The literal.
    :param label_to_index: A dictionary mapping labels to indices.
    :return: The converted value.
    """
    if x in label_to_index:
        return label_to_index[x]
    elif x.startswith("r"):
        return int(x[1:])
    else:
        return int(x)


def parse(tokens: list) -> list:
    """
    Converts the given tokens into a nested list of functions.

    :param tokens: The tokens.
    :return: A nested list of functions.
    """
    label_to_index = {}
    for token in tokens:
        if token[0].endswith(":"):
            # Label
            label = token[0][:-1]
            label_to_index[label] = len(label_to_index)
    functions = [[] for _ in range(len(label_to_index))]
    body = None
    for token in tokens:
        if token[0].endswith(":"):
            # Label
            label = token[0][:-1]
            body = functions[label_to_index[label]]
            token = token[1:]
            if len(token) == 0:
                continue
        # Instruction
        opcode = OPNAME_TO_OPCODE[token[0]]
        args = [convert_literal(x, label_to_index) for x in token[1:]]
        body.append([opcode] + args)
    return functions


def tokenize(program: str) -> list:
    """
    Converts the given program into a nested list of tokens, one per line.

    :param program: The program.
    :return: A nested list of tokens.

    >>> tokenize("add r2, r0, r1 \\n mv r3, r2  // Move r3 to r2")
    [['add', 'r2', 'r0', 'r1'], ['mv', 'r3', 'r2']]
    """
    tokens = []
    for line in program.splitlines():
        # Replace commas with spaces
        line = line.replace(",", " ")
        curr_tokens = line.strip().split()
        try:
            comment_index = curr_tokens.index("//")
            curr_tokens = curr_tokens[:comment_index]
        except ValueError:
            pass
        if len(curr_tokens) == 0:
            continue
        tokens.append(curr_tokens)
    return tokens


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


def main():
    proc = Processor()
    tokens = tokenize(basic_control_flow)
    print("Tokens:")
    print(tokens)
    functions = parse(tokens)
    print("Functions:")
    print(functions)
    proc.functions = functions
    proc.registers[0] = np.int32(88)
    evaluate_body(proc.functions[0], proc)
    proc.dump()


if __name__ == "__main__":
    main()
