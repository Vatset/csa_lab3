first: .word "What is your name?\n"
first_addr: .word 0
second: .word "Hello, "
second_addr: .word 0
third: .word "!"
third_addr: .word 0
result_addr: .word 0
buffer: .word 0
result: .word ""
in: .word 2046
out: .word 2047

int: load in
    cmp 0
    jmz write_second
    store (buffer)
    load buffer
    inc
    store buffer
    iret
start: load (first)
     store first_addr
     load (second)
     store second_addr
     load (third)
     store third_addr
     load (result)
     store result_addr
     store buffer
write_first: load (first_addr)
        cmp 0
        jmz wait
        store (out)
        load first_addr
        inc
        store first_addr
        jmp write_first
wait: jmp wait
write_second: load (second_addr)
        cmp 0
        jmz write_result
        store (out)
        load second_addr
        inc
        store second_addr
        jmp write_second
write_result: load (result_addr)
        cmp 0
        jmz write_third
        store (out)
        load result_addr
        inc
        store result_addr
        jmp write_result
write_third: load (third_addr)
        cmp 0
        jmz end
        store (out)
        load third_addr
        inc
        store third_addr
        jmp write_third
end: hlt
