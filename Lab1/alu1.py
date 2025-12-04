from myhdl import block, always_comb, instances, Signal

#tag: ff15f3e8d1d9357da1414ff35032c8c5e0ba9813

@block
def ALU1bit(a, b, carryin, binvert, operation, result, carryout):
    """
    1-bit ALU

    result and carryout are output; all other signals are input.

    operation is a 2-bit select signal for a 4-input MUX.
    """

    # internal signals
    notb = Signal(bool(0))
    mux1_out = Signal(bool(0))
    and_out  = Signal(bool(0))
    or_out   = Signal(bool(0))
    adder_sum = Signal(bool(0))

    # ------------------------------
    # NOT block for b -> notb
    # ------------------------------
    @always_comb
    def comb_not():
        """
        TODO:
            Implement bitwise NOT of b, keeping only the least significant bit.
            Hint:
              - Use bitwise operator (~) instead of 'not'
              - Use '& 1' once to keep only the LSB.
        Example pattern (NOT the final answer):
            notb.next = 0
        """
        notb.next = 0  # TODO: replace with correct expression

    # ------------------------------
    # 2-to-1 MUX: chooses between b and notb -> mux1_out
    # ------------------------------
    @always_comb
    def comb_mux_2_1():
        """
        TODO:
            Implement a 2-to-1 multiplexer:
                if binvert == 0: select b
                if binvert == 1: select notb
            Then drive mux1_out.next with the selected value.
        Example pattern (NOT the final answer):
            if binvert:
                mux1_out.next = 0
            else:
                mux1_out.next = 0
        """
        mux1_out.next = 0  # TODO: replace with correct logic

    # ------------------------------
    # AND gate: a AND mux1_out -> and_out
    # ------------------------------
    @always_comb
    def comb_and():
        """
        TODO:
            Implement bitwise AND between a and mux1_out.
            Keep only the LSB using '& 1' at the end.
        Example pattern (NOT the final answer):
            and_out.next = 0
        """
        and_out.next = 0  # TODO: replace with correct expression

    # ------------------------------
    # OR gate: a OR mux1_out -> or_out
    # ------------------------------
    @always_comb
    def comb_or():
        """
        TODO:
            Implement bitwise OR between a and mux1_out.
            Keep only the LSB using '& 1' at the end.
        Example pattern (NOT the final answer):
            or_out.next = 0
        """
        or_out.next = 0  # TODO: replace with correct expression

    # ------------------------------
    # Full adder: a, mux1_out, carryin -> adder_sum, carryout
    # ------------------------------
    @always_comb
    def comb_adder():
        """
        TODO:
            Implement a 1-bit full adder with inputs:
                a, mux1_out, carryin

            Outputs:
                adder_sum: sum bit
                carryout: carry-out bit

            Use bitwise operators (&, ^, |) and keep only the LSB where appropriate.

        Example pattern (NOT the final answer):
            adder_sum.next = 0
            carryout.next  = 0
        """
        adder_sum.next = 0   # TODO: replace with full-adder sum logic
        carryout.next  = 0   # TODO: replace with full-adder carry logic

    # ------------------------------
    # 4-to-1 MUX: selects final result based on operation
    # ------------------------------
    @always_comb
    def comb_mux_4_1():
        """
        TODO:
            Implement a 4-to-1 multiplexer for 'result' based on 'operation':
                operation == 0: use AND result
                operation == 1: use OR result
                operation == 2: use ADD result (adder_sum)
                operation == 3: define behavior (e.g., set to 0 or something else)

            Use if-elif-else and remember to assign to result.next.

        Example pattern (NOT the final answer):
            if operation == 0:
                result.next = 0
            elif operation == 1:
                result.next = 0
            elif operation == 2:
                result.next = 0
            else:
                result.next = 0
        """
        result.next = 0  # TODO: replace with correct mux logic

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

        a, b, carryin, binvert = [Signal(bool(0)) for _ in range(4)]

        # operation has two bits
        operation = Signal(intbv(0)[2:])

        # instantiate ALU
        alu1 = ALU1bit(a, b, carryin, binvert, operation, result, carryout)

        @instance
        def stimulus():
            print("op a b cin bneg | cout res")
            for op in args.op:
                assert 0 <= op <= 3
                for i in range(16):
                    # use MyHDL intbv to split bits
                    bi = intbv(i)
                    # bi[0], bi[1], ... are bits of i
                    a.next       = bi[0]
                    b.next       = bi[1]
                    carryin.next = bi[2]
                    binvert.next = bi[3]

                    operation.next = op
                    yield delay(10)
                    print("{} {} {} {}   {}    | {}    {}".format(
                        bin(op, 2),
                        int(a), int(b), int(carryin), int(binvert),
                        int(carryout), int(result)
                    ))

            # stop simulation
            raise StopSimulation()

        return alu1, stimulus

    parser = argparse.ArgumentParser(description='Testing 1-bit ALU')
    parser.add_argument('op', type=int, nargs='*',
                        default=[0, 1, 2],
                        help='operation')
    parser.add_argument('--trace', action='store_true', help='generate trace')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose')

    args = parser.parse_args()
    if args.verbose:
        print(args)

    tb = test_comb(args)
    tb.config_sim(trace=args.trace)
    tb.run_sim()
