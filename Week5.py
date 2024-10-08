names = {
    "A": ["x", "y"],
    "B": ["x", "v"],
    "C": ["w", "y"],
    "D": ["w"]
}

# Initialize CRT with static name info.
def init_crt(crt):
    for vars in names.values():
        for v in vars:
            if v not in crt:
                crt[v] = (0, "")  # (flag, ref)

def display(crt, hstack):
    print("CRT")
    for var, (flag, ref) in crt.items():
        print(var, flag, ref)
    print("Hidden Stack")
    for var, ref in reversed(hstack):
        print(var, ref)
    print()

def block_enter(block, crt, hstack):
    # Activate block variables in crt
    for i, var in enumerate(names[block]):
        if crt[var][0] == 1:  # If variable is already active
            hstack.append((var, crt[var][1]))  # Push current ref to hstack
        crt[var] = (1, f"{block}{i+1}")  # Activate with new reference
    display(crt, hstack)

def block_exit(block, crt, hstack):
    # Deactivate block variables in crt
    for var in names[block]:
        if hstack and hstack[-1][0] == var:  # If the top of the stack is this variable
            crt[var] = (1, hstack.pop()[1])  # Restore previous state from hstack
        else:
            crt[var] = (0, crt[var][1])  # Deactivate the variable
    display(crt, hstack)

# Call sequence.
crt = dict()
hstack = []
init_crt(crt)
block_enter("A", crt, hstack)  # Enter block A
block_enter("B", crt, hstack)  # Enter block B
block_exit("B", crt, hstack)   # Exit block B
block_enter("C", crt, hstack)  # Enter block C
block_enter("D", crt, hstack)  # Enter block D
block_exit("D", crt, hstack)   # Exit block D
block_exit("C", crt, hstack)   # Exit block C
block_exit("A", crt, hstack)   # Exit block A
display(crt, hstack)           # Final display