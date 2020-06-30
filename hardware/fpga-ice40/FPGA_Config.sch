EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 11 12
Title "Ferk-Cart iCE40 Devboard"
Date "2020-06-29"
Rev "r0.1"
Comp "Designed by: Nelson Gauthier"
Comment1 "Licensed under CERN OHL v.1.2"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L ng_fpga_lattice_ice40:iCE40HX4K-TQ144 U?
U 5 1 5F5C1B8F
P 4100 3450
AR Path="/5F5C1B8F" Ref="U?"  Part="5" 
AR Path="/5F5B53E5/5F5C1B8F" Ref="U1"  Part="5" 
F 0 "U1" H 5000 3700 60  0000 R CNN
F 1 "iCE40HX4K-TQ144" H 5000 3600 60  0000 R CNN
F 2 "Package_QFP:TQFP-144_20x20mm_P0.5mm" H 4300 3500 60  0001 L CNN
F 3 "https://www.mouser.com/datasheet/2/225/FPGA-DS-02029-3-5-iCE40-LP-HX-Family-Data-Sheet-1022803.pdf" H 4300 3300 60  0001 L CNN
F 4 "iCE40HX4K-TQ144" H 4300 3400 60  0001 L CNN "manf#"
	5    4100 3450
	-1   0    0    -1  
$EndComp
$Comp
L ng_fpga_lattice_ice40:iCE40HX4K-TQ144 U?
U 8 1 5F5C1B96
P 4100 4800
AR Path="/5F5C1B96" Ref="U?"  Part="8" 
AR Path="/5F5B53E5/5F5C1B96" Ref="U1"  Part="8" 
F 0 "U1" H 4500 5050 60  0000 R CNN
F 1 "iCE40HX4K-TQ144" H 4500 4950 60  0000 R CNN
F 2 "Package_QFP:TQFP-144_20x20mm_P0.5mm" H 4300 4850 60  0001 L CNN
F 3 "https://www.mouser.com/datasheet/2/225/FPGA-DS-02029-3-5-iCE40-LP-HX-Family-Data-Sheet-1022803.pdf" H 4300 4650 60  0001 L CNN
F 4 "iCE40HX4K-TQ144" H 4300 4750 60  0001 L CNN "manf#"
	8    4100 4800
	-1   0    0    -1  
$EndComp
Text GLabel 4100 3750 2    50   Input ~ 0
CONFIG_MOSI|IO0
Text GLabel 4100 3850 2    50   Input ~ 0
CONFIG_MISO|IO1
Text GLabel 4100 3950 2    50   Input ~ 0
CONFIG_SCK
Text GLabel 4100 4050 2    50   Input ~ 0
CONFIG_SSn
Text GLabel 4400 3450 2    50   Input ~ 0
FPGA_CDONE
Text GLabel 4400 3550 2    50   Input ~ 0
FPGA_CRESETn
Wire Wire Line
	4100 3550 4200 3550
Wire Wire Line
	4200 3250 4200 3550
Connection ~ 4200 3550
Wire Wire Line
	4100 3450 4300 3450
$Comp
L Device:R R?
U 1 1 5F5C1BA6
P 4200 3100
AR Path="/5F5C1BA6" Ref="R?"  Part="1" 
AR Path="/5F5B53E5/5F5C1BA6" Ref="R8"  Part="1" 
F 0 "R8" V 4250 3250 50  0000 L CNN
F 1 "10k" V 4250 2950 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 4130 3100 50  0001 C CNN
F 3 "~" H 4200 3100 50  0001 C CNN
	1    4200 3100
	1    0    0    -1  
$EndComp
Wire Wire Line
	4200 3550 4400 3550
Wire Wire Line
	4300 3450 4300 3250
Connection ~ 4300 3450
Wire Wire Line
	4300 3450 4400 3450
Wire Wire Line
	4200 2950 4200 2750
Wire Wire Line
	4200 2750 4300 2750
Wire Wire Line
	4300 2750 4300 2950
$Comp
L Device:R R?
U 1 1 5F5C1BB3
P 4300 3100
AR Path="/5F5C1BB3" Ref="R?"  Part="1" 
AR Path="/5F5B53E5/5F5C1BB3" Ref="R9"  Part="1" 
F 0 "R9" V 4350 3250 50  0000 L CNN
F 1 "10k" V 4350 2950 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 4230 3100 50  0001 C CNN
F 3 "~" H 4300 3100 50  0001 C CNN
	1    4300 3100
	1    0    0    -1  
$EndComp
Text GLabel 4100 2750 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	4100 2750 4200 2750
Connection ~ 4200 2750
$Comp
L Oscillator:ECS-2520MV-xxx-xx X?
U 1 1 5F5C1BBC
P 6750 5050
AR Path="/5F5C1BBC" Ref="X?"  Part="1" 
AR Path="/5F5B53E5/5F5C1BBC" Ref="X1"  Part="1" 
F 0 "X1" H 6450 5300 50  0000 L CNN
F 1 "ECS-2520MV-xxx-xx" H 6850 5300 50  0000 L CNN
F 2 "ng_time:Oscillator_2.5x2.0" H 7200 4700 50  0001 C CNN
F 3 "https://www.ecsxtal.com/store/pdf/ECS-2520MV.pdf" H 6575 5175 50  0001 C CNN
	1    6750 5050
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR?
U 1 1 5F5C1BC2
P 6750 5450
AR Path="/5F5C1BC2" Ref="#PWR?"  Part="1" 
AR Path="/5F5B53E5/5F5C1BC2" Ref="#PWR032"  Part="1" 
F 0 "#PWR032" H 6750 5200 50  0001 C CNN
F 1 "GND" H 6753 5324 50  0000 C CNN
F 2 "" H 6650 5100 50  0001 C CNN
F 3 "" H 6750 5450 50  0001 C CNN
	1    6750 5450
	1    0    0    -1  
$EndComp
Text GLabel 6150 4650 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	6350 5050 6250 5050
Wire Wire Line
	6250 5050 6250 4950
Wire Wire Line
	6250 4650 6750 4650
Wire Wire Line
	6750 4650 6750 4750
Wire Wire Line
	6150 4650 6250 4650
Wire Wire Line
	6750 5450 6750 5350
Text GLabel 7150 5050 2    50   Input ~ 0
CLK_50MHZ
$Comp
L Device:C C?
U 1 1 5F5C1BD0
P 6050 5200
AR Path="/5F5C1BD0" Ref="C?"  Part="1" 
AR Path="/5F5B53E5/5F5C1BD0" Ref="C44"  Part="1" 
F 0 "C44" H 6165 5246 50  0000 L CNN
F 1 "100n" H 6165 5155 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 6088 5050 50  0001 C CNN
F 3 "~" H 6050 5200 50  0001 C CNN
	1    6050 5200
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR?
U 1 1 5F5C1BD6
P 6050 5450
AR Path="/5F5C1BD6" Ref="#PWR?"  Part="1" 
AR Path="/5F5B53E5/5F5C1BD6" Ref="#PWR031"  Part="1" 
F 0 "#PWR031" H 6050 5200 50  0001 C CNN
F 1 "GND" H 6053 5324 50  0000 C CNN
F 2 "" H 5950 5100 50  0001 C CNN
F 3 "" H 6050 5450 50  0001 C CNN
	1    6050 5450
	1    0    0    -1  
$EndComp
Wire Wire Line
	6050 5450 6050 5350
Wire Wire Line
	6050 5050 6050 4950
Wire Wire Line
	6050 4950 6250 4950
Connection ~ 6250 4950
Wire Wire Line
	6250 4950 6250 4650
Connection ~ 6250 4650
$Comp
L 74xGxx:74AHC1G08 U10
U 1 1 5EFB1490
P 6950 3750
F 0 "U10" H 7000 4000 50  0000 L CNN
F 1 "SN74LVC1G08DBVR" H 7000 3900 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23-5" H 6950 3750 50  0001 C CNN
F 3 "http://www.ti.com/lit/sg/scyt129e/scyt129e.pdf" H 6950 3750 50  0001 C CNN
	1    6950 3750
	1    0    0    -1  
$EndComp
Wire Wire Line
	6950 3850 6950 3950
Wire Wire Line
	6950 3650 6950 3000
Wire Wire Line
	6950 3000 6550 3000
$Comp
L ng_power:GND #PWR035
U 1 1 5EFB47F2
P 6950 3950
F 0 "#PWR035" H 6950 3700 50  0001 C CNN
F 1 "GND" H 6953 3824 50  0000 C CNN
F 2 "" H 6850 3600 50  0001 C CNN
F 3 "" H 6950 3950 50  0001 C CNN
	1    6950 3950
	1    0    0    -1  
$EndComp
Text GLabel 7200 3750 2    50   Input ~ 0
FPGA_CRESETn
Wire Wire Line
	6450 3500 6450 3800
$Comp
L Device:R R?
U 1 1 5EFB670F
P 6450 3350
AR Path="/5EFB670F" Ref="R?"  Part="1" 
AR Path="/5F5B53E5/5EFB670F" Ref="R12"  Part="1" 
F 0 "R12" V 6500 3500 50  0000 L CNN
F 1 "10k" V 6500 3200 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 6380 3350 50  0001 C CNN
F 3 "~" H 6450 3350 50  0001 C CNN
	1    6450 3350
	1    0    0    -1  
$EndComp
Wire Wire Line
	6550 3700 6550 3500
Wire Wire Line
	6450 3200 6450 3000
Wire Wire Line
	6450 3000 6550 3000
Wire Wire Line
	6550 3000 6550 3200
$Comp
L Device:R R?
U 1 1 5EFB671D
P 6550 3350
AR Path="/5EFB671D" Ref="R?"  Part="1" 
AR Path="/5F5B53E5/5EFB671D" Ref="R13"  Part="1" 
F 0 "R13" V 6600 3500 50  0000 L CNN
F 1 "10k" V 6600 3200 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 6480 3350 50  0001 C CNN
F 3 "~" H 6550 3350 50  0001 C CNN
	1    6550 3350
	1    0    0    -1  
$EndComp
Text GLabel 6350 3000 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	6350 3000 6450 3000
Connection ~ 6450 3000
Connection ~ 6550 3000
Wire Wire Line
	6650 3700 6550 3700
Connection ~ 6550 3700
Wire Wire Line
	6550 3700 6350 3700
Wire Wire Line
	6650 3800 6450 3800
Connection ~ 6450 3800
Wire Wire Line
	6450 3800 6350 3800
Text GLabel 6350 3800 0    50   Input ~ 0
FLASH_CRESETn
Text GLabel 6350 3700 0    50   Input ~ 0
CONFIG_CRESETn
$EndSCHEMATC
