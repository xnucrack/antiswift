document = Document.getCurrentDocument()

SWITCH_REF_OPCODE_PATTERN = [
    'adr',
    'nop',
    'adr',
    'ldrsw',
    'add',
    'br'
]


def satisfies_pattern(address: int):
    segment = document.getSegmentAtAddress(address)
    opcodes = [segment.getInstructionAtAddress(address + a*4).getInstructionString() for a in range(len(SWITCH_REF_OPCODE_PATTERN))]

    print(opcodes)

    return opcodes == SWITCH_REF_OPCODE_PATTERN


def solve_switch_table(address: int):

    assert satisfies_pattern(address)

    segment = document.getSegmentAtAddress(address)
    table_base = int(segment.getInstructionAtAddress(address).getRawArgument(1)[1:], 16)
    switch_base = int(segment.getInstructionAtAddress(address + 8).getRawArgument(1)[1:], 16)

    # read in the switch table...
    case = 0
    while segment.getProcedureAtAddress(table_base) == None:
        loc = switch_base + document.readUInt32LE(table_base)
        segment.markAsProcedure(loc)
        segment.addReference(address, loc)
        segment.setInlineCommentAtAddress(loc, f"case {case} for switch at {hex(address)}")
        print(f"switch case {case} at {hex(loc)}")
        case += 1
        table_base += 4


solve_switch_table(document.setCurrentAddress())
