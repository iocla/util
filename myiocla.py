import gdb

# in ~/.gdbinit use this line:
# source ~/curs/iocla/myiocla.py

class TillI(gdb.Command):
    """
Continue until instruction with given opcode.

    tilli OPCODE

Example:

    tilli call
    tilli mul
"""
    def __init__(self):
        super().__init__(
            'tilli',
            gdb.COMMAND_BREAKPOINTS,
            gdb.COMPLETE_NONE,
            False
        )
    def invoke(self, arg, from_tty):
        if arg == '':
            gdb.write('Argument missing.\n')
        else:
            thread = gdb.inferiors()[0].threads()[0]
            while thread.is_valid():
                gdb.execute('si', to_string=True)
                frame = gdb.selected_frame()
                arch = frame.architecture()
                pc = gdb.selected_frame().pc()
                instruction = arch.disassemble(pc)[0]['asm']
                if instruction.startswith(arg + ' '):
                    gdb.write(instruction + '\n')
                    break
TillI()


def run_till_depth0(depth):
        thread = gdb.inferiors()[0].threads()[0]
        while thread.is_valid():
                SILENT=True
                frame = gdb.selected_frame()
                arch = frame.architecture()
                pc = gdb.selected_frame().pc()
                instruction = arch.disassemble(pc)[0]['asm']
                if instruction.startswith("call "):
                    depth = depth + 1
                    # gdb.write(instruction + '\n')
                if instruction.startswith("ret "):
                    depth = depth - 1
                    # gdb.write(instruction + '\n')
                gdb.execute("stepi", to_string=SILENT)
                #gdb.execute('si', to_string=True)
                if depth == 0:
                    break 


class StepOverCall(gdb.Command):
    """
    sover
 Step over function call. Executes 'si' command if instruction is not a call
"""
    def __init__(self):
        super().__init__(
            'sover',
            gdb.COMMAND_BREAKPOINTS,
            gdb.COMPLETE_NONE,
            False
        )
    def invoke(self, arg, from_tty):
        depth = 0
        run_till_depth0(depth)

StepOverCall()



class StepOutOfCall(gdb.Command):
    """
    sout
 Steps out of current function call (counting call and ret instructions). 
"""
    def __init__(self):
        super().__init__(
            'sout',
            gdb.COMMAND_BREAKPOINTS,
            gdb.COMPLETE_NONE,
            False
        )
    def invoke(self, arg, from_tty):
        depth = 1
        run_till_depth0(depth)
             
StepOutOfCall()
