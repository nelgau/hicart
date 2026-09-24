### 2026-09-13

Yosys 0.39+147 (git sha1 0a854cf4c, clang++ 15.0.0 -fPIC -Os)
"nextpnr-ecp5" -- Next Generation Place and Route (Version nextpnr-0.6-93-g3e1e7838)
Project Trellis ecppack Version 1.4-45-gbe909ba

### 2026-09-14

Yosys 0.69 (YoWASP)
NextPNR-ECP5 0.11.1 (YoWASP)

### 2026-09-23

Yosys 0.68 (YoWASP)
NextPNR-ECP5 0.11.1 (YoWASP)

Reason: Yosys 0.69 optimizes away ~500 LUTs depending on whether a signal, used nowhere
else, is driven combinationally by a constant bit. If the signal exists and is driven,
the design builds and runs successfully on the FPGA.
