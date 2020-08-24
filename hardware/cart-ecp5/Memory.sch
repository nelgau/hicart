EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A3 16535 11693
encoding utf-8
Sheet 4 5
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L ng_memory:S27KS0641 U2
U 1 1 5F47DAAE
P 3950 4500
F 0 "U2" H 4250 5300 60  0000 C CNN
F 1 "S27KS0641" H 4450 5200 60  0000 C CNN
F 2 "ng_package_bga:BGA-24_6.0x8.0mm_Layout5x5_P1.0mm_Pad0.4mm" H 3150 6450 60  0001 C CNN
F 3 "https://www.cypress.com/file/183506/download" H 3150 6450 60  0001 C CNN
	1    3950 4500
	1    0    0    -1  
$EndComp
Text GLabel 4550 4000 2    50   BiDi ~ 0
HRAM_DQ0
Text GLabel 4550 4100 2    50   BiDi ~ 0
HRAM_DQ1
Text GLabel 4550 4200 2    50   BiDi ~ 0
HRAM_DQ2
Text GLabel 4550 4300 2    50   BiDi ~ 0
HRAM_DQ3
Text GLabel 4550 4400 2    50   BiDi ~ 0
HRAM_DQ4
Text GLabel 4550 4500 2    50   BiDi ~ 0
HRAM_DQ5
Text GLabel 4550 4600 2    50   BiDi ~ 0
HRAM_DQ6
Text GLabel 4550 4700 2    50   BiDi ~ 0
HRAM_DQ7
Text GLabel 4550 4900 2    50   BiDi ~ 0
HRAM_RWDS
NoConn ~ 3350 4800
NoConn ~ 3350 4900
Text GLabel 3350 4000 0    50   Input ~ 0
HRAM_CS#
Text GLabel 3350 4100 0    50   Input ~ 0
HRAM_CK+
Text GLabel 3350 4200 0    50   Input ~ 0
HRAM_CK-
Text GLabel 3350 4300 0    50   Input ~ 0
HRAM_RESET#
Wire Wire Line
	3850 3750 3850 3650
Wire Wire Line
	3850 3650 3950 3650
Wire Wire Line
	4050 3650 4050 3750
Wire Wire Line
	3950 3750 3950 3650
Connection ~ 3950 3650
Wire Wire Line
	3950 3650 4050 3650
Wire Wire Line
	3850 3650 3850 3550
Wire Wire Line
	3850 3550 3750 3550
Connection ~ 3850 3650
Text GLabel 3750 3550 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	3850 5150 3850 5250
Wire Wire Line
	3850 5250 3950 5250
Wire Wire Line
	3950 5250 3950 5150
Wire Wire Line
	3950 5250 4050 5250
Wire Wire Line
	4050 5250 4050 5150
Connection ~ 3950 5250
Wire Wire Line
	3850 5250 3850 5350
Connection ~ 3850 5250
$Comp
L ng_power:GND #PWR0103
U 1 1 5F3CB04C
P 3850 5350
F 0 "#PWR0103" H 3850 5100 50  0001 C CNN
F 1 "GND" H 3853 5224 50  0000 C CNN
F 2 "" H 3750 5000 50  0001 C CNN
F 3 "" H 3850 5350 50  0001 C CNN
	1    3850 5350
	1    0    0    -1  
$EndComp
$EndSCHEMATC
