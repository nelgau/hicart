EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 4 12
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
P 3800 3950
AR Path="/5F5C1B8F" Ref="U?"  Part="5" 
AR Path="/5F5B53E5/5F5C1B8F" Ref="U1"  Part="5" 
F 0 "U1" H 4700 4200 60  0000 R CNN
F 1 "iCE40HX4K-TQ144" H 4700 4100 60  0000 R CNN
F 2 "Package_QFP:TQFP-144_20x20mm_P0.5mm" H 4000 4000 60  0001 L CNN
F 3 "https://www.mouser.com/datasheet/2/225/FPGA-DS-02029-3-5-iCE40-LP-HX-Family-Data-Sheet-1022803.pdf" H 4000 3800 60  0001 L CNN
F 4 "iCE40HX4K-TQ144" H 4000 3900 60  0001 L CNN "manf#"
	5    3800 3950
	-1   0    0    -1  
$EndComp
$Comp
L ng_fpga_lattice_ice40:iCE40HX4K-TQ144 U?
U 8 1 5F5C1B96
P 5650 3950
AR Path="/5F5C1B96" Ref="U?"  Part="8" 
AR Path="/5F5B53E5/5F5C1B96" Ref="U1"  Part="8" 
F 0 "U1" H 6050 4200 60  0000 R CNN
F 1 "iCE40HX4K-TQ144" H 6050 4100 60  0000 R CNN
F 2 "Package_QFP:TQFP-144_20x20mm_P0.5mm" H 5850 4000 60  0001 L CNN
F 3 "https://www.mouser.com/datasheet/2/225/FPGA-DS-02029-3-5-iCE40-LP-HX-Family-Data-Sheet-1022803.pdf" H 5850 3800 60  0001 L CNN
F 4 "iCE40HX4K-TQ144" H 5850 3900 60  0001 L CNN "manf#"
	8    5650 3950
	-1   0    0    -1  
$EndComp
Text GLabel 3800 4250 2    50   Input ~ 0
CONFIG_MOSI|IO0
Text GLabel 3800 4350 2    50   Input ~ 0
CONFIG_MISO|IO1
Text GLabel 3800 4450 2    50   Input ~ 0
CONFIG_SCK
Text GLabel 3800 4550 2    50   Input ~ 0
CONFIG_SSn
Text GLabel 4100 3950 2    50   Input ~ 0
FPGA_CDONE
Text GLabel 4100 4050 2    50   Input ~ 0
FPGA_CRESETn
Wire Wire Line
	3800 4050 3900 4050
Wire Wire Line
	3900 3750 3900 4050
Connection ~ 3900 4050
Wire Wire Line
	3800 3950 4000 3950
$Comp
L Device:R R?
U 1 1 5F5C1BA6
P 3900 3600
AR Path="/5F5C1BA6" Ref="R?"  Part="1" 
AR Path="/5F5B53E5/5F5C1BA6" Ref="R1"  Part="1" 
F 0 "R1" V 3950 3750 50  0000 L CNN
F 1 "10k" V 3950 3450 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 3830 3600 50  0001 C CNN
F 3 "~" H 3900 3600 50  0001 C CNN
	1    3900 3600
	1    0    0    -1  
$EndComp
Wire Wire Line
	3900 4050 4100 4050
Wire Wire Line
	4000 3950 4000 3750
Connection ~ 4000 3950
Wire Wire Line
	4000 3950 4100 3950
Wire Wire Line
	3900 3450 3900 3250
Wire Wire Line
	3900 3250 4000 3250
Wire Wire Line
	4000 3250 4000 3450
$Comp
L Device:R R?
U 1 1 5F5C1BB3
P 4000 3600
AR Path="/5F5C1BB3" Ref="R?"  Part="1" 
AR Path="/5F5B53E5/5F5C1BB3" Ref="R2"  Part="1" 
F 0 "R2" V 4050 3750 50  0000 L CNN
F 1 "10k" V 4050 3450 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 3930 3600 50  0001 C CNN
F 3 "~" H 4000 3600 50  0001 C CNN
	1    4000 3600
	1    0    0    -1  
$EndComp
Text GLabel 3800 3250 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	3800 3250 3900 3250
Connection ~ 3900 3250
$Comp
L Oscillator:ECS-2520MV-xxx-xx X?
U 1 1 5F5C1BBC
P 7400 4250
AR Path="/5F5C1BBC" Ref="X?"  Part="1" 
AR Path="/5F5B53E5/5F5C1BBC" Ref="X1"  Part="1" 
F 0 "X1" H 7500 4500 50  0000 L CNN
F 1 "ECS-2520MV-xxx-xx" H 7450 4000 50  0000 L CNN
F 2 "ng_time:Oscillator_2.5x2.0" H 7850 3900 50  0001 C CNN
F 3 "https://www.ecsxtal.com/store/pdf/ECS-2520MV.pdf" H 7225 4375 50  0001 C CNN
	1    7400 4250
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR?
U 1 1 5F5C1BC2
P 7400 4650
AR Path="/5F5C1BC2" Ref="#PWR?"  Part="1" 
AR Path="/5F5B53E5/5F5C1BC2" Ref="#PWR0133"  Part="1" 
F 0 "#PWR0133" H 7400 4400 50  0001 C CNN
F 1 "GND" H 7403 4524 50  0000 C CNN
F 2 "" H 7300 4300 50  0001 C CNN
F 3 "" H 7400 4650 50  0001 C CNN
	1    7400 4650
	1    0    0    -1  
$EndComp
Text GLabel 6800 3850 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	7000 4250 6900 4250
Wire Wire Line
	6900 4250 6900 4150
Wire Wire Line
	6900 3850 7400 3850
Wire Wire Line
	7400 3850 7400 3950
Wire Wire Line
	6800 3850 6900 3850
Wire Wire Line
	7400 4650 7400 4550
Text GLabel 7800 4250 2    50   Input ~ 0
CLK_50MHZ
$Comp
L Device:C C?
U 1 1 5F5C1BD0
P 6700 4400
AR Path="/5F5C1BD0" Ref="C?"  Part="1" 
AR Path="/5F5B53E5/5F5C1BD0" Ref="C43"  Part="1" 
F 0 "C43" H 6815 4446 50  0000 L CNN
F 1 "100n" H 6815 4355 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 6738 4250 50  0001 C CNN
F 3 "~" H 6700 4400 50  0001 C CNN
	1    6700 4400
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR?
U 1 1 5F5C1BD6
P 6700 4650
AR Path="/5F5C1BD6" Ref="#PWR?"  Part="1" 
AR Path="/5F5B53E5/5F5C1BD6" Ref="#PWR0134"  Part="1" 
F 0 "#PWR0134" H 6700 4400 50  0001 C CNN
F 1 "GND" H 6703 4524 50  0000 C CNN
F 2 "" H 6600 4300 50  0001 C CNN
F 3 "" H 6700 4650 50  0001 C CNN
	1    6700 4650
	1    0    0    -1  
$EndComp
Wire Wire Line
	6700 4650 6700 4550
Wire Wire Line
	6700 4250 6700 4150
Wire Wire Line
	6700 4150 6900 4150
Connection ~ 6900 4150
Wire Wire Line
	6900 4150 6900 3850
Connection ~ 6900 3850
$EndSCHEMATC
