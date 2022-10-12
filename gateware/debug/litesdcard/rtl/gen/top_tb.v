`timescale 1ns/1ps

module top_tb;

    reg clk;
    reg rst;

    initial
    begin
        clk = 0;
        rst = 0;
    end

    always
    begin
        #5 clk = ~clk;
    end

    top top_instance(
        .clk$1(clk),
        .rst(rst)
    );

endmodule


module waveform;
   initial begin
      $dumpfile ("traces/out_gen.vcd");
      $dumpvars (0, top_tb);
      #1;
   end
endmodule
