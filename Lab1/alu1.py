from myhdl import block, always_comb, instances

#tag: ff15f3e8d1d9357da1414ff35032c8c5e0ba9813

@block
def ALU1bit(a, b, carryin, binvert, operation, result, carryout):

    """ 1-bit ALU

    result and carryout are output

    all other signals are input

    operation, the select signal to 4-input Mux, has two bits.
    We can compare operation directly integers, for example, 
        if operation == 0:

    """

    # internal signals
    notb = Signal(bool(0))
    mux1_out, and_out, or_out, adder_sum = (Signal(bool(0)), 
                            Signal(bool(0)), Signal(bool(0)), Signal(bool(0)))

    # we can read/set these signals (input, output, and internal) in submodules

    # the 'always_comb' decorator indicates a combinational circuit 
    # funciton name is not important. we could name it 'a_circuit' 
    # MyHDL analyzes code and adds Signals (of MyHDL Signal type) that appear
    # on the right hand side of any statements to a sentitivity list. 
    # In this example, if b's value changed, this function com_not is called
    # and notb will get a new value, which will trigger other submodules.
    @always_comb
    def comb_not():
        # We may use 'and', 'or', 'not' operators on single-bit values
        # for example, notb.next = not b
        # However, we will use bitwise operators in this course. 
        # Use "& 1" to keep the LSB only. 
        # We only need to do "& 1" once in the end.
        notb.next = (~ b) & 1

    # the 2-1 MUX that generates mux1_out
    @always_comb
    def comb_mux_2_1():
        # Use if-elif. 
        # Remember to use mux1_out.next = ...
        # TODO
        if binvert: 
            mux1_out.next = notb
        else:
            mux1_out.next = b

    # the AND gate
    @always_comb
    def comb_and():
        # TODO
        and_out.next = (a & mux1_out) & 1

    # the OR gate
    @always_comb
    def comb_or():
        # TODO
        or_out.next = (a | mux1_out) & 1

    # adder.
    @always_comb
    def comb_adder():
        # Generate adder_sum and carryout
        # The lecture slides have the logic expressions.
        # TODO
        adder_sum.next = (a ^ mux1_out ^ carryin) & 1
        carryout.next = (a & mux1_out | a & carryin | mux1_out & carryin) & 1

    # 4-1 mux to generate result
    @always_comb
    def comb_mux_4_1():
        # Use if-elif-else. Remember to do "result.next = ..."
        # TODO
        if operation == 0:
            result.next = and_out
        elif operation == 1:
            result.next = or_out
        elif operation == 2:
            result.next = adder_sum
        else:
            result.next = 0

    # return all the functions/submodules 
    # we could list them explicitly, like
    #     return comb_not, comb_and, ...
    return instances()

if __name__ == "__main__":
    from myhdl import intbv, delay, instance, Signal, StopSimulation, bin
    import argparse

    # testbench itself is a block
    @block
    def test_comb(args):

        # create signals
        result = Signal(bool(0))
        carryout = Signal(bool(0))

        a, b, carryin, binvert = [Signal(bool(0)) for i in range(4)]

        # operation has two bits
        operation = Signal(intbv(0)[2:])

        # instantiating a block
        alu1 = ALU1bit(a, b, carryin, binvert, operation, result, carryout)

        @instance
        def stimulus():
            print("op a b cin bneg | cout res")
            for op in args.op:
                assert 0 <= op <= 3
                for i in range(16):
                    # use MyHDL intbv to split bits, instead of shift and AND
                    bi = intbv(i)
                    a.next, b.next, carryin.next, binvert.next = \
                        bi[0], bi[1], bi[2], bi[3]
                    operation.next = op
                    yield delay(10)
                    print("{} {} {} {}   {}    | {}    {}".format(
                        bin(op, 2), 
                        int(a), int(b), int(carryin), int(binvert), 
                        int(carryout), int(result)))

            # stop simulation
            raise StopSimulation()

        return alu1, stimulus

    parser = argparse.ArgumentParser(description='Testing 1-bit ALU')
    parser.add_argument('op', type=int, nargs='*', 
            default=[0, 1, 2], help='operation')
    parser.add_argument('--trace', action='store_true', help='generate trace')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')

    args = parser.parse_args()
    if args.verbose:
        print(args)

    tb = test_comb(args)
    tb.config_sim(trace=args.trace)
    tb.run_sim()
