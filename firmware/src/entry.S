#define MIE_MEIE    0x800

    .section .init, "ax"
    .global _start
_start:
    j _reset_vector

    .global _reset_vector
_reset_vector:
    # Initialize the stack
    la sp, __stack_top
    
    # Set the vector for interrupt handling
    la t0, trap_vector
    csrw mtvec, t0

    # initialize data
    # initialize bss

    ##
    # TODO: Abstract 
    ##

    # Enable external interrupts
    li t0, MIE_MEIE
    csrs mie, t0

    # Invoke program
    call boot

    # Halt
1:  j 1b

trap_vector:
    # Save registers
    addi sp, sp, -16*4
    sw ra,  0*4(sp)
    sw t0,  1*4(sp)
    sw t1,  2*4(sp)
    sw t2,  3*4(sp)
    sw a0,  4*4(sp)
    sw a1,  5*4(sp)
    sw a2,  6*4(sp)
    sw a3,  7*4(sp)
    sw a4,  8*4(sp)
    sw a5,  9*4(sp)
    sw a6, 10*4(sp)
    sw a7, 11*4(sp)
    sw t3, 12*4(sp)
    sw t4, 13*4(sp)
    sw t5, 14*4(sp)
    sw t6, 15*4(sp)

    call isr

    # Load registers
    lw ra,  0*4(sp)
    lw t0,  1*4(sp)
    lw t1,  2*4(sp)
    lw t2,  3*4(sp)
    lw a0,  4*4(sp)
    lw a1,  5*4(sp)
    lw a2,  6*4(sp)
    lw a3,  7*4(sp)
    lw a4,  8*4(sp)
    lw a5,  9*4(sp)
    lw a6, 10*4(sp)
    lw a7, 11*4(sp)
    lw t3, 12*4(sp)
    lw t4, 13*4(sp)
    lw t5, 14*4(sp)
    lw t6, 15*4(sp)
    addi sp, sp, 16*4    

    mret
