#!/usr/bin/python3
import sys

from isa import *

labels = {}
start_address = -1


def split_q(string, splitter=" "):
    result = []
    in_quotes = False
    current_word = ""
    for char in string:
        if char == splitter and not in_quotes:
            if current_word:
                result.append(current_word)
                current_word = ""
        elif char == '"':
            in_quotes = not in_quotes
            current_word += char
        else:
            current_word += char
    if current_word:
        result.append(current_word)
    return result


def is_label_string(arr):
    return (
        len(arr) >= 2
        and is_code_label(arr[0])
        and (is_op_string(arr[1:]) or is_nop_string(arr[1:]))
        or is_const_string(arr[1:])
    )


def is_labeless_string(arr):
    return len(arr) <= 2 and (is_op_string(arr) or is_nop_string(arr))


def is_direct_addr(addr):
    return is_address(addr) or (addr in labels.keys())


def is_indirect_addr(addr):
    return (
        addr[0] == "("
        and addr[-1] == ")"
        and (is_address(addr[1 : len(addr) - 1]) or addr[1 : len(addr) - 1] in labels.keys())
    )


def is_op_string(arr):
    return len(arr) == 2 and is_op_command(arr[0]) and (is_direct_addr(arr[1]) or is_indirect_addr(arr[1]))


def is_nop_string(arr):
    return len(arr) == 1 and is_nop_command(arr[0])


def not_empty(arr):
    return [s for s in arr if s != ""]


def is_cstr(arr):
    if arr:
        first_string = arr[0]
        last_string = arr[-1]
        return first_string.startswith('"') and last_string.endswith('"')
    return False


def is_const_string(arr):
    return (
        len(arr) >= 2
        and is_const_label(arr[0])
        and ((is_number(arr[1]) or arr[1] in labels.keys()) or is_cstr(arr[1:]))
    )


def is_address_string(arr):
    return len(arr) == 2 and is_address_label(arr[0]) and is_address(arr[1])


def make_op_string(arr, index):
    is_indirect = False
    if is_indirect_addr(arr[1]):
        arr[1] = arr[1][1 : len(arr[1]) - 1]
        is_indirect = True
    if arr[1] in labels.keys():
        return [{"index": index, "opcode": arr[0], "operand": int(labels[arr[1]]), "value": 0, "address": is_indirect}]
    else:
        return [{"index": index, "opcode": arr[0], "operand": int(arr[1]), "value": 0, "address": is_indirect}]


def make_nop_string(arr, index):
    return [{"index": index, "opcode": arr[0], "value": 0}]


def make_const_string(arr, index):
    if is_cstr(arr[1:]):
        str_arr = "".join(arr[1:]).split('"')[1]  # Получаем строку между кавычками
        lines = []
        for i, char in enumerate(str_arr):
            lines.append({"index": index + i, "value": char, "opcode": "nop"})
        lines.append({"index": index + len(str_arr), "value": 0, "opcode": "nop"})  
        return lines

    if arr[1] in labels.keys():
        return [{"index": index, "value": int(labels[arr[1]]), "opcode": "nop"}]
    else:
        return [{"index": index, "value": int(arr[1]), "opcode": "nop"}]


def source2json(arr, index):
    if is_label_string(arr):
        if is_op_string(arr[1:]):
            return make_op_string(arr[1:], index)
        elif is_const_string(arr[1:]):
            return make_const_string(arr[1:], index)
        else:
            return make_nop_string(arr[1:], index)
    elif is_labeless_string(arr):
        if is_op_string(arr):
            return make_op_string(arr, index)
        elif is_nop_string(arr):
            return make_nop_string(arr, index)
    elif is_const_string(arr):
        return make_const_string(arr, index)
    else:
        return {}


def check_labels(arr, index):
    global start_address
    lbl = arr[0]
    if is_code_label(lbl):
        lbl = lbl[: len(lbl) - 1]
        assert lbl not in labels.keys(), "Labels must be uniq " + str(lbl) + " " + str(labels.keys())
        if lbl == start_label:
            start_address = index
        labels[lbl] = index
        if is_const_string(arr[1:]) and is_cstr(arr[2:]):
            return index + len(arr[2]) - arr[2].count('"') + 1
        else:
            return index + 1
    else:
        if is_const_string(arr) and is_cstr(arr[1:]):
            return index + len(arr[1]) - arr[1].count('"') + 1
        else:
            return index + 1

def translate_stage_1(text):
    pc = 0
    sz = len(text)
    source_code = []
    for i in range(sz):
        if not text[i]:
            continue
        text[i] = split_q(text[i], ";")[0]
        line=text[i]
        source_code.append(line)
        code_str=split_q(line)
        if is_address_string(code_str):
            pc = int(code_str[1])
            continue
        pc = check_labels(code_str, pc)

    return source_code

def translate_stage_2(source_code):
    pc = 0
    translated_code = []
    for line in source_code:
        code_str = split_q(line)
        if is_address_string(code_str):
            pc = int(code_str[1])
            continue
        translated = source2json(code_str, pc)
        assert not translated == {}, ("Incorrect source code line " + str(pc) + ': "' + str(line)) + '"'
        for tr_str in translated:
            translated_code.append(tr_str)
            pc = int(tr_str["index"])
        pc += 1
    return translated_code

def source2json(arr, index):
    if is_label_string(arr):
        if is_op_string(arr[1:]):
            return make_op_string(arr[1:], index)
        elif is_const_string(arr[1:]):
            return make_const_string(arr[1:], index)
        else:
            return make_nop_string(arr[1:], index)
    elif is_labeless_string(arr):
        if is_op_string(arr):
            return make_op_string(arr, index)
        elif is_nop_string(arr):
            return make_nop_string(arr, index)
    elif is_const_string(arr):
        return make_const_string(arr, index)
    else:
        return {}

def translate(text):
    source_code = translate_stage_1(text)
    translated_code = translate_stage_2(source_code)
    assert start_label in labels.keys()
    is_ended = False
    for instr in translated_code:
        if "opcode" in instr.keys() and instr["opcode"] == "hlt":
            is_ended = True
    assert is_ended, "program must have hlt command"
    return translated_code

def main(code_source, code_target):
    with open(code_source, encoding="utf-8") as f:
        code_source = f.read().split("\n")
    code = translate(code_source)
    write_code(code_target, start_address, code)
    global labels
    labels = {}
    print("source LoC:", len(code_source), "code instr:", len(code))


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Wrong arguments: translator.py <input_file> <target_file>"
    _, source, target = sys.argv
    main(source, target)
