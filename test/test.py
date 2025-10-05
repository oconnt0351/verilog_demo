# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge

@cocotb.test()
async def test_counter(dut):
    dut._log.info("Start counter test")

    # Set the clock period to 10 ns (100 MHz)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Apply reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1

    # Check that counter starts from 0
    await RisingEdge(dut.clk)
    assert int(dut.uo_out.value) == 0, f"Expected 0, got {int(dut.uo_out.value)}"

    # Check a few increments
    for expected in range(1, 6):
        await RisingEdge(dut.clk)
        got = int(dut.uo_out.value)
        assert got == expected, f"Expected {expected}, got {got}"
        dut._log.info(f"Counter value = {got}")

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
