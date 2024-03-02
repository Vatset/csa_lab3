org 0
int_addr: .word interrupt
org 2
line_end: .word 10
stop_input: .word 0
in: .word 2046
out: .word 2047

org 10
start: ei
    loop: load stop_input
    jmz loop
    hlt

interrupt: push
    load (in)
    cmp line_end
    jmnz print
    load stop_input
    inc
    store stop_input
    jmp end
    print: store (out)
    end: pop
    iret