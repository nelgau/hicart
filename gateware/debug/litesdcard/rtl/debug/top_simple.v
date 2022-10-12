`timescale 1ns/1ps

module top(
    input wire clk,
    input wire rst
);

    reg           sdcard_cd       = 1'd0;
    wire          sdcard_clk;
    reg           sdcard_cmd_i    = 1'd0;
    wire          sdcard_cmd_o;
    wire          sdcard_cmd_oe;
    reg   [3:0]   sdcard_dat_i    = 4'd0;
    wire  [3:0]   sdcard_dat_o;
    wire  [3:0]   sdcard_dat_oe;

    wire          wb_ctrl_ack;
    reg   [29:0]  wb_ctrl_adr     = 30'd0;
    reg   [1:0]   wb_ctrl_bte     = 2'd0;
    reg   [2:0]   wb_ctrl_cti     = 3'd0;
    reg           wb_ctrl_cyc;
    wire  [31:0]  wb_ctrl_dat_r;
    reg   [31:0]  wb_ctrl_dat_w   = 32'd0;
    wire          wb_ctrl_err;
    reg   [3:0]   wb_ctrl_sel     = 4'd0;
    reg           wb_ctrl_stb;
    reg           wb_ctrl_we;

    reg           wb_dma_ack      = 1'd0;
    wire  [29:0]  wb_dma_adr;
    wire  [1:0]   wb_dma_bte;
    wire  [2:0]   wb_dma_cti;
    wire          wb_dma_cyc;
    reg   [31:0]  wb_dma_dat_r    = 32'd0;
    wire  [31:0]  wb_dma_dat_w;
    reg           wb_dma_err      = 1'd0;
    wire  [3:0]   wb_dma_sel;
    wire          wb_dma_stb;
    wire          wb_dma_we;

    litesdcard_core litesdcard (
        .clk(clk),
        .rst(rst),
        .irq(irq),
        .sdcard_cd(sdcard_cd),
        .sdcard_clk(sdcard_clk),
        .sdcard_cmd_i(sdcard_cmd_i),
        .sdcard_cmd_o(sdcard_cmd_o),
        .sdcard_cmd_oe(sdcard_cmd_oe),
        .sdcard_dat_i(sdcard_dat_i),
        .sdcard_dat_o(sdcard_dat_o),
        .sdcard_dat_oe(sdcard_dat_oe),
        .wb_ctrl_ack(wb_ctrl_ack),
        .wb_ctrl_adr(wb_ctrl_adr),
        .wb_ctrl_bte(wb_ctrl_bte),
        .wb_ctrl_cti(wb_ctrl_cti),
        .wb_ctrl_cyc(wb_ctrl_cyc),
        .wb_ctrl_dat_r(wb_ctrl_dat_r),
        .wb_ctrl_dat_w(wb_ctrl_dat_w),
        .wb_ctrl_err(wb_ctrl_err),
        .wb_ctrl_sel(wb_ctrl_sel),
        .wb_ctrl_stb(wb_ctrl_stb),
        .wb_ctrl_we(wb_ctrl_we),
        .wb_dma_ack(wb_dma_ack),
        .wb_dma_adr(wb_dma_adr),
        .wb_dma_bte(wb_dma_bte),
        .wb_dma_cti(wb_dma_cti),
        .wb_dma_cyc(wb_dma_cyc),
        .wb_dma_dat_r(wb_dma_dat_r),
        .wb_dma_dat_w(wb_dma_dat_w),
        .wb_dma_err(wb_dma_err),
        .wb_dma_sel(wb_dma_sel),
        .wb_dma_stb(wb_dma_stb),
        .wb_dma_we(wb_dma_we)
    );

endmodule