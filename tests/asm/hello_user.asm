org 0
int_addr: .word read_symb

org 2
line_end: .word 10      ; end-of-line code
stop_input: .word 0     ; flag
in: .word 2046
out: .word 2047

question: .word "What is your name?"
question_addr: .word question
question_ret: .word enter_name_loop

greeting: .word "Hello, "
greeting_addr: .word greeting
greeting_ret: .word name_print

exclamation: .word "!"
exclamation_addr: .word exclamation
exclamation_ret: .word end

print_addr: .word 0
return_address: .word 0

print_loop: load (print_addr)
      jmz (return_address)
      store (out)
      load print_addr
      inc
      store print_addr
      jmp print_loop


read_symb: di
    load (in)
    cmp line_end
    jmnz save_symb
    load stop_input
    inc
    store stop_input
    jmp returning

save_symb: store (user_name_address)
    load user_name_address
    inc
    store user_name_address

returning: iret

org 100
start: ei

    question_print: load question_addr
    store print_addr
    load question_ret
    store return_address
    jmp print_loop

    enter_name_loop: load stop_input   ; spin-loop cycle
    jmz enter_name_loop

    greeting_print: load greeting_addr
    store print_addr
    load greeting_ret
    store return_address
    jmp print_loop

    name_print: load user_name_start
    store print_addr
    load user_name_ret
    store return_address
    jmp print_loop

    exclamation_print: load exclamation_addr
    store print_addr
    load exclamation_ret
    store return_address
    jmp print_loop

    end: hlt

user_name_ret: .word exclamation_print
user_name_start: .word user_name
user_name_address: .word user_name
user_name: .word 0
