import sys
import os
os.system('') 
register_count = 7
print(f"Available Registers: {register_count}")
registers = [0]*register_count
memory = {}
line_number = 0
labels = {}

class bcolors:
    EXEC = '\033[37m'
    FAIL = '\033[31m'
    ENDC = '\033[0m'

def printc(text):
    print(bcolors.EXEC + text + bcolors.ENDC)

def printe(text):
    print(bcolors.FAIL + text + bcolors.ENDC)

with open(sys.argv[1]) as f:
    program_lines = f.read().splitlines()

def get_register_or_value(text):
    if text[0] == "R":
        try:
            return registers[int(text[1:])-1]
        except:
            printe("Could not read Register")
    else:
        return int(text)
def get_bool_register_or_value(text):
    return get_register_or_value(text) == 1
    
def get_line_value(text):
    if text in labels:
        return labels[text]
    return get_register_or_value(text)

def update_line_number(l):
    global line_number
    line_number = l - 1
    if l < 0:
        printe(f"Cannot jump to {l} as it is negative")
        exit(1)
    #printc(f"Set program line number to {l}")
    
def set_memory(k,v):
    memory[get_register_or_value(k)] = get_register_or_value(v)
    #printc(f"Set memory address {k} to {memory[get_register_or_value(k)]}")
    
def load_memory(k, reg):
    set_reg(reg, memory[get_register_or_value(k)])
    
def print_regs():
    for i in range(register_count):
        print(f"R{i+1:<2} : {registers[i]}")
    return None
def print_mem():
    print(memory)
    return None
def set_reg(reg, val):
    if reg[0] != "R":
        printe(f"Failed: Invalid register name '{reg}'")
    reg_i = int(reg[1:])-1
    if reg_i < 0 or reg_i >= register_count:
        printe(f"Failed: Register index is out of bounds: 1 <= {reg_i+1} <= {register_count}'")
    registers[reg_i] = val
    #printc(f"Setting register {reg} to {val}")
    
def bool_to_num(x):
    return 1 if x else 0
def cjump(x,y):
    if registers[0] == get_register_or_value(y):
        update_line_number(get_line_value(x))
def print_val(x):
    print(x)
def get_input():
    set_reg("R1", int(input("Enter a number: ")))

ops = {
    "MUL": lambda x,y: get_register_or_value(x) * get_register_or_value(y),
    "TIMES": lambda x,y: get_register_or_value(x) * get_register_or_value(y),
    "MINUS": lambda x,y: get_register_or_value(x) - get_register_or_value(y),
    "ADD": lambda x,y: get_register_or_value(x) + get_register_or_value(y),
    "DIV": lambda x,y: get_register_or_value(x) // get_register_or_value(y),
    "MOD": lambda x,y: get_register_or_value(x) % get_register_or_value(y),
    "AND": lambda x,y: bool_to_num(get_bool_register_or_value(x) and get_bool_register_or_value(y)),
    "OR": lambda x,y: bool_to_num(get_bool_register_or_value(x) or get_bool_register_or_value(y)),
    "XOR": lambda x,y: bool_to_num(get_bool_register_or_value(x) ^ get_bool_register_or_value(y)),
    "NEG": lambda x,y: bool_to_num(not get_bool_register_or_value(x)),
    "EQ": lambda x,y: bool_to_num(get_register_or_value(x) == get_register_or_value(y)),
    "GE": lambda x,y: bool_to_num(get_register_or_value(x) >= get_register_or_value(y)),
    "LE": lambda x,y: bool_to_num(get_register_or_value(x) <= get_register_or_value(y)),
    "GT": lambda x,y: bool_to_num(get_register_or_value(x) > get_register_or_value(y)),
    "LT": lambda x,y: bool_to_num(get_register_or_value(x) < get_register_or_value(y)),
    "MOV": lambda x,y: set_reg(y,get_register_or_value(x)),
    "JUMP": lambda x,y: update_line_number(get_line_value(x)),
    "CMP": lambda x,y: 1 if get_register_or_value(x) > get_register_or_value(y) else  -1 if get_register_or_value(x) < get_register_or_value(y) else 0,
    "CJUMP": cjump,
    "STORE": set_memory,
    "LOAD": lambda x,y: load_memory(x, y),
    "PREG": lambda x,y: print_regs(),
    "PMEM": lambda x,y: print_mem(),
    "INP": lambda x,y: get_input(),
    "PRINT": lambda x,y: print_val(get_register_or_value(x))
}

for current_line_number, current_line in enumerate(program_lines):
    if current_line.startswith("LABEL"):
        labels[current_line.strip().split(" ")[-1]] = current_line_number
    
  
while line_number < len(program_lines):
    
    current_line = program_lines[line_number]
    current_line = current_line.split("#")[0].strip()
    current_line_number = line_number
    line_number += 1
    
    if current_line.strip() == "":
        continue
    
    if current_line.startswith("LABEL"):
        labels[current_line.strip().split(" ")[-1]] = current_line_number
        continue
    
    parts = current_line.split(" ")
    if len(parts) < 3:
        printe(f"Too few arguments on line {current_line_number+1}")
        exit(1)
    if len(parts) > 3:
        printe(f"Too many arguments on line {current_line_number+1}")
        exit(1)
        
    op = parts[0]
    if op not in ops:
        printe(f"Unknown opcode {op} on line {current_line_number+1}")
    #printc(f"Executing '{current_line}'...")
    ret = ops[op](parts[1], parts[2])
    if ret is not None:
        set_reg("R1", ret)
    #print()
printc("DONE")
    
    