#PARA QUE ESSA BIBLIOTECA FUNCIONE, TEMOS QUE SABER O TIPO DA INSTRUÇÃO, OPCODE E FUNCT( SE FOR TIPO R)


INSTRUCOES = {
# INSTRUCOES DO TIPO R
"add":  {"tipo": "R", "opcode": 0, "function": 32},
"sub":  {"tipo": "R", "opcode": 0, "function": 34},
"addu": {"tipo": "R", "opcode": 0, "function": 33},
"subu": {"tipo": "R", "opcode": 0, "function": 35},
"and":  {"tipo": "R", "opcode": 0, "function": 36},
"or":   {"tipo": "R", "opcode": 0, "function": 37},
"slt":  {"tipo": "R", "opcode": 0, "function": 42},

# SHIFTS -> DESLOCADORES DE BITS
"sll": {"tipo": "R", "opcode": 0, "funct": 0},
"srl": {"tipo": "R", "opcode": 0, "funct": 2},

# ESPECIAIS
"jr":   {"tipo": "R", "opcode": 0, "function": 8},
"mfhi": {"tipo": "R", "opcode": 0, "function": 16},
"mflo": {"tipo": "R", "opcode": 0, "function": 18},
"mult": {"tipo": "R", "opcode": 0, "function": 24},
"multu":{"tipo": "R", "opcode": 0, "function": 25},
"div":  {"tipo": "R", "opcode": 0, "function": 26},

# INSTRUCOES DO TIPO I
"addi":  {"tipo": "I", "opcode": 8},
"addiu": {"tipo": "I", "opcode": 9},
"andi":  {"tipo": "I", "opcode": 12},
"ori":   {"tipo": "I", "opcode": 13},
"slti":  {"tipo": "I", "opcode": 10},
"beq":   {"tipo": "I", "opcode": 4},
"bne":   {"tipo": "I", "opcode": 5},
"lw":    {"tipo": "I", "opcode": 35},
"sw":    {"tipo": "I", "opcode": 43},
"lui":   {"tipo": "I", "opcode": 15},

# INSTRUCOES DO TIPO J -> JUMPERS 
"j":   {"tipo": "J", "opcode": 2},
"jal": {"tipo": "J", "opcode": 3},
}
