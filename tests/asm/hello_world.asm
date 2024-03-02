org 2
message: .word "Hello, World!"
pointer: .word message
zero:    .word 0
out_port: .word 2047

org 30
start:   nop
loop:    load (pointer)
         store (out_port)
         jmz end
         load pointer
         inc
         store pointer
         jmp loop
end:     hlt
