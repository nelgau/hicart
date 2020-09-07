EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 7
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Sheet
S 1800 2750 1750 1000
U 5F4290F0
F0 "FPGA-Power" 50
F1 "FPGA-Power.sch" 50
$EndSheet
$Sheet
S 1800 1450 1800 900 
U 5F3E46DE
F0 "FPGA-IO" 50
F1 "FPGA-IO.sch" 50
$EndSheet
$Sheet
S 3900 1450 1750 900 
U 5F7B735C
F0 "Memory" 50
F1 "Memory.sch" 50
$EndSheet
$Sheet
S 6000 1450 1500 900 
U 5F43B1FD
F0 "Interface-N64" 50
F1 "Interface-N64.sch" 50
$EndSheet
$Sheet
S 8000 1450 1550 900 
U 5F483803
F0 "Power" 50
F1 "Power.sch" 50
$EndSheet
$Sheet
S 6000 2700 1500 950 
U 5F4552C5
F0 "Interface-USB" 50
F1 "Interface-USB.sch" 50
$EndSheet
Text Notes 12000 1600 0    50   ~ 0
LENGTH MATCHING:\nid: hyperram_dq\nnetnames: "^(HRAM_DQ[0-7])$"\ntolerance: 50 mil\nvialength: 1.6 mm
Text Notes 12000 2700 0    50   ~ 0
LENGTH MATCHING:\nid: hyperram_rwds_to_dq\nnetnames: "^(HRAM_RWDS)$"\nreflength: group hyperram_dq\ntolerance: 25 mil\nvialength: 1.6 mm
Text Notes 12000 2100 0    50   ~ 0
LENGTH MATCHING:\nid: hyperram_clk\nnetnames: "^(HRAM_CK_[PN])$"\ntolerance: 10 mil\nvialength: 1.6 mm
Text Notes 12000 3300 0    50   ~ 0
LENGTH MATCHING:\nid: hyperram_clk_to_dq\nnetnames: "^(HRAM_CK_[PN])$"\nreflength: group hyperram_dq\ntolerance: 500 mil\nvialength: 1.6 mm
Text Notes 12000 3900 0    50   ~ 0
LENGTH MATCHING:\nid: hyperram_clk_to_rwds\nnetnames: "^(HRAM_CK_[PN])$"\nreflength: group hyperram_rwds_to_dq\ntolerance: 1500 mil\nvialength: 1.6 mm
Text Notes 12000 4500 0    50   ~ 0
LENGTH MATCHING:\nid: hyperram_cs_to_clk\nnetnames: "^(HRAM_CS_B)$"\nreflength: group hyperram_clk\ntolerance: 1500 mil\nvialength: 1.6 mm
Text Notes 12000 5100 0    50   ~ 0
LENGTH MATCHING:\nid: hyperram_reset_to_cs\nnetnames: "^(HRAM_RESET_B)$"\nreflength: group hyperram_cs_to_clk\ntolerance: 2000 mil\nvialength: 1.6 mm
Text Notes 12000 900  0    50   ~ 0
Notes:\n\nWhen computing a group's reflength, the script takes the average of\nthe group's shortest and longest nets. Intuitively, this seems to allow\nfor tolerances to be violated by these extremal nets. I think it's more\ncorrect to evaluate reflength tolerance by exhaustively checking all\npossible pairs of nets (e.g., one drawn from each of the two groups).  
$EndSCHEMATC
