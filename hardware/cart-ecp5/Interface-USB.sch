EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 7 7
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Wire Wire Line
	8550 1450 8550 1350
Wire Wire Line
	8550 1350 8650 1350
Wire Wire Line
	8650 1350 8650 1450
Wire Wire Line
	8650 1350 8750 1350
Wire Wire Line
	8750 1350 8750 1450
Connection ~ 8650 1350
Wire Wire Line
	8950 1450 8950 1350
Wire Wire Line
	8950 1350 9050 1350
Wire Wire Line
	9050 1350 9050 1450
Wire Wire Line
	9050 1350 9150 1350
Wire Wire Line
	9150 1350 9150 1450
Connection ~ 9050 1350
Wire Wire Line
	9150 1350 9250 1350
Wire Wire Line
	9250 1350 9250 1450
Connection ~ 9150 1350
Wire Wire Line
	9150 5850 9150 5950
Wire Wire Line
	9150 5950 9050 5950
Wire Wire Line
	7450 5550 7550 5550
Wire Wire Line
	8250 5850 8250 5950
Connection ~ 8250 5950
Wire Wire Line
	8450 5850 8450 5950
Connection ~ 8450 5950
Wire Wire Line
	8550 5850 8550 5950
Connection ~ 8550 5950
Wire Wire Line
	8550 5950 8450 5950
Wire Wire Line
	8650 5850 8650 5950
Connection ~ 8650 5950
Wire Wire Line
	8650 5950 8550 5950
Wire Wire Line
	8750 5850 8750 5950
Connection ~ 8750 5950
Wire Wire Line
	8750 5950 8650 5950
Wire Wire Line
	8850 5850 8850 5950
Connection ~ 8850 5950
Wire Wire Line
	8850 5950 8750 5950
Wire Wire Line
	8950 5850 8950 5950
Connection ~ 8950 5950
Wire Wire Line
	8950 5950 8850 5950
Wire Wire Line
	9050 5850 9050 5950
Connection ~ 9050 5950
Wire Wire Line
	9050 5950 8950 5950
NoConn ~ 7550 5050
NoConn ~ 9950 5350
NoConn ~ 9950 5450
Wire Wire Line
	8550 1350 8550 1050
Connection ~ 8550 1350
Wire Wire Line
	8950 1350 8950 1250
Connection ~ 8950 1350
Wire Wire Line
	8450 5950 8250 5950
Wire Wire Line
	8250 5950 8250 6050
Wire Wire Line
	7450 5550 7450 5650
Wire Wire Line
	7550 1750 6450 1750
Wire Wire Line
	7550 1950 7350 1950
Wire Wire Line
	7350 2050 7350 1950
Wire Wire Line
	7050 2350 7050 2450
Wire Wire Line
	7050 1950 7050 2050
$Comp
L Device:C C36
U 1 1 5F1F46DB
P 5150 4600
F 0 "C36" H 4950 4700 50  0000 L CNN
F 1 "100n" H 4900 4500 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 5188 4450 50  0001 C CNN
F 3 "~" H 5150 4600 50  0001 C CNN
	1    5150 4600
	1    0    0    -1  
$EndComp
Wire Wire Line
	5450 4650 5350 4650
Wire Wire Line
	5350 4650 5350 4850
Wire Wire Line
	6350 3550 6250 3550
Connection ~ 6450 3550
Wire Wire Line
	6350 3550 6350 3850
Wire Wire Line
	6450 3550 6550 3550
Wire Wire Line
	6450 3550 6450 3850
Wire Wire Line
	6350 3550 6450 3550
Wire Wire Line
	6550 3850 6550 3550
Wire Wire Line
	6450 4450 6450 4150
Wire Wire Line
	6250 4450 6450 4450
Wire Wire Line
	6550 4350 6550 4150
$Comp
L Device:R R23
U 1 1 5F1F46FF
P 6450 4000
F 0 "R23" V 6400 4150 50  0000 L CNN
F 1 "10k" V 6400 3700 50  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" V 6380 4000 50  0001 C CNN
F 3 "~" H 6450 4000 50  0001 C CNN
	1    6450 4000
	1    0    0    -1  
$EndComp
$Comp
L Device:R R24
U 1 1 5F1F4705
P 6550 4000
F 0 "R24" V 6500 4150 50  0000 L CNN
F 1 "10k" V 6500 3700 50  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" V 6480 4000 50  0001 C CNN
F 3 "~" H 6550 4000 50  0001 C CNN
	1    6550 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	7550 4350 6550 4350
Wire Wire Line
	7550 4450 6450 4450
Connection ~ 6450 4450
Wire Wire Line
	6350 4650 6350 4150
Wire Wire Line
	5150 4750 5150 4850
Wire Wire Line
	7550 3650 7450 3650
Wire Wire Line
	7550 3850 7450 3850
Wire Wire Line
	7150 3650 7050 3650
Wire Wire Line
	7150 3850 7050 3850
Wire Wire Line
	7050 3850 7050 3950
$Comp
L ng_memory:93C46BT-I_OT U10
U 1 1 5F1F475A
P 5850 4550
F 0 "U10" H 5550 5000 50  0000 L CNN
F 1 "93C46BT-I_OT" H 5550 4900 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23-6" H 5850 4300 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/20001749K.pdf" H 5850 4550 50  0001 C CNN
	1    5850 4550
	1    0    0    -1  
$EndComp
$Comp
L ng_osc:DSC60xx X2
U 1 1 5F1F4760
P 6550 5350
F 0 "X2" H 6200 5700 50  0000 L CNN
F 1 "DSC60xx" H 6200 5600 50  0000 L CNN
F 2 "ng_time:Oscillator_2.5x2.0" H 7250 5000 50  0001 C CNN
F 3 "" H 6450 5350 50  0001 C CNN
F 4 "12 MHz" H 6900 5600 50  0000 R CNN "Freq"
	1    6550 5350
	1    0    0    -1  
$EndComp
Wire Wire Line
	7000 5250 7550 5250
Wire Wire Line
	7000 5450 7100 5450
Wire Wire Line
	7100 5450 7100 5550
$Comp
L Device:C C37
U 1 1 5F1F476F
P 5800 5500
F 0 "C37" H 5600 5600 50  0000 L CNN
F 1 "100n" H 5550 5400 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 5838 5350 50  0001 C CNN
F 3 "~" H 5800 5500 50  0001 C CNN
	1    5800 5500
	1    0    0    -1  
$EndComp
Wire Wire Line
	5800 5650 5800 5750
Wire Wire Line
	6100 5450 6000 5450
Wire Wire Line
	6000 5450 6000 5250
Wire Wire Line
	6000 5250 6100 5250
Wire Wire Line
	7050 2450 7350 2450
Wire Wire Line
	7350 1950 7050 1950
Wire Wire Line
	7350 2350 7350 2450
Connection ~ 7350 1950
$Comp
L Device:C C38
U 1 1 5F1F4791
P 7050 2200
F 0 "C38" H 7000 2300 50  0000 R CNN
F 1 "4u7" H 7000 2100 50  0000 R CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 7088 2050 50  0001 C CNN
F 3 "~" H 7050 2200 50  0001 C CNN
	1    7050 2200
	-1   0    0    -1  
$EndComp
$Comp
L Device:C C39
U 1 1 5F1F4797
P 7350 2200
F 0 "C39" H 7300 2300 50  0000 R CNN
F 1 "100n" H 7300 2100 50  0000 R CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 7388 2050 50  0001 C CNN
F 3 "~" H 7350 2200 50  0001 C CNN
	1    7350 2200
	-1   0    0    -1  
$EndComp
Wire Wire Line
	5050 4350 5150 4350
Wire Wire Line
	5450 4350 5150 4350
Connection ~ 5150 4350
Wire Wire Line
	5150 4350 5150 4450
Wire Wire Line
	6000 5250 5800 5250
Connection ~ 6000 5250
Wire Wire Line
	5800 5250 5800 5350
$Comp
L Device:C C21
U 1 1 5F1F47A6
P 2000 5200
F 0 "C21" H 2050 5300 50  0000 L CNN
F 1 "4u7" H 2050 5100 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 2038 5050 50  0001 C CNN
F 3 "~" H 2000 5200 50  0001 C CNN
	1    2000 5200
	1    0    0    -1  
$EndComp
$Comp
L Device:C C23
U 1 1 5F1F47B2
P 2300 5200
F 0 "C23" H 2350 5300 50  0000 L CNN
F 1 "100n" H 2350 5100 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 2338 5050 50  0001 C CNN
F 3 "~" H 2300 5200 50  0001 C CNN
	1    2300 5200
	1    0    0    -1  
$EndComp
Wire Wire Line
	2000 5350 2000 5450
Wire Wire Line
	2000 5450 2000 5550
Wire Wire Line
	2300 5350 2300 5450
Wire Wire Line
	2000 5450 2300 5450
Wire Wire Line
	1600 4950 1500 4950
Wire Wire Line
	6250 4650 6350 4650
Connection ~ 6550 4350
Wire Wire Line
	6250 4350 6550 4350
Connection ~ 6350 3550
Wire Wire Line
	7550 4550 7450 4550
Wire Wire Line
	7450 4650 7450 4550
Wire Wire Line
	7350 4650 7450 4650
$Comp
L Device:R R20
U 1 1 5F1F4860
P 7200 4650
F 0 "R20" V 7250 4500 50  0000 R CNN
F 1 "2k2" V 7250 4800 50  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" V 7130 4650 50  0001 C CNN
F 3 "~" H 7200 4650 50  0001 C CNN
	1    7200 4650
	0    1    1    0   
$EndComp
Wire Wire Line
	8250 1250 8250 1450
Wire Wire Line
	8350 1150 8350 1450
Wire Wire Line
	4300 6000 4300 6100
Wire Wire Line
	4300 6400 4300 6500
Wire Wire Line
	7450 2950 7550 2950
Wire Wire Line
	7450 3050 7550 3050
Wire Wire Line
	4450 1350 4550 1350
Connection ~ 4450 1350
Wire Wire Line
	4150 1350 4450 1350
Connection ~ 4150 1350
Wire Wire Line
	4150 1750 4150 1850
Wire Wire Line
	4150 1350 4150 1450
$Comp
L Device:C C4
U 1 1 5F184C9E
P 4150 1600
AR Path="/5F184C9E" Ref="C4"  Part="1" 
AR Path="/5F302051/5F184C9E" Ref="C?"  Part="1" 
AR Path="/5F4552C5/5F184C9E" Ref="C33"  Part="1" 
F 0 "C33" H 4200 1700 50  0000 L CNN
F 1 "100n" H 4200 1500 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 4188 1450 50  0001 C CNN
F 3 "~" H 4150 1600 50  0001 C CNN
F 4 "" H 4150 1600 50  0001 C CNN "MPN"
	1    4150 1600
	1    0    0    -1  
$EndComp
Wire Wire Line
	4050 1350 4150 1350
Text Notes 3900 2200 0    50   ~ 0
USBLC6 requires 100n (C18) on VBUS,\nnot 10n as would be expected
Text Label 4850 2800 2    50   ~ 0
USB_VBUS
$Comp
L ng_power:GND #PWR0107
U 1 1 5F184C94
P 4950 3800
AR Path="/5F184C94" Ref="#PWR0107"  Part="1" 
AR Path="/5F302051/5F184C94" Ref="#PWR?"  Part="1" 
AR Path="/5F4552C5/5F184C94" Ref="#PWR040"  Part="1" 
F 0 "#PWR040" H 4950 3550 50  0001 C CNN
F 1 "GND" H 4953 3674 50  0000 C CNN
F 2 "" H 4850 3450 50  0001 C CNN
F 3 "" H 4950 3800 50  0001 C CNN
	1    4950 3800
	1    0    0    -1  
$EndComp
Wire Wire Line
	4950 3700 4950 3800
Wire Wire Line
	4950 2800 4950 2900
Wire Wire Line
	4850 2800 4950 2800
$Comp
L Power_Protection:USBLC6-2SC6 U?
U 1 1 5F184C87
P 4950 3300
AR Path="/5F302051/5F184C87" Ref="U?"  Part="1" 
AR Path="/5F184C87" Ref="U3"  Part="1" 
AR Path="/5F4552C5/5F184C87" Ref="U9"  Part="1" 
F 0 "U9" H 5100 3750 50  0000 L CNN
F 1 "USBLC6-2SC6" H 5100 3650 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23-6" H 4200 3700 50  0001 C CNN
F 3 "http://www2.st.com/resource/en/datasheet/CD00050750.pdf" H 5150 3650 50  0001 C CNN
	1    4950 3300
	1    0    0    -1  
$EndComp
Text Label 2250 1350 0    50   ~ 0
USB_VBUS
Connection ~ 3650 1350
Wire Wire Line
	2150 1350 3650 1350
$Comp
L Device:R R1
U 1 1 5F184C70
P 1550 3600
AR Path="/5F184C70" Ref="R1"  Part="1" 
AR Path="/5F302051/5F184C70" Ref="R?"  Part="1" 
AR Path="/5F4552C5/5F184C70" Ref="R14"  Part="1" 
F 0 "R14" H 1600 3650 50  0000 L CNN
F 1 "100k" H 1600 3550 50  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" V 1480 3600 50  0001 C CNN
F 3 "~" H 1550 3600 50  0001 C CNN
F 4 "" H 1550 3600 50  0001 C CNN "MPN"
	1    1550 3600
	1    0    0    -1  
$EndComp
$Comp
L Device:C C6
U 1 1 5F184C69
P 1250 3600
AR Path="/5F184C69" Ref="C6"  Part="1" 
AR Path="/5F302051/5F184C69" Ref="C?"  Part="1" 
AR Path="/5F4552C5/5F184C69" Ref="C20"  Part="1" 
F 0 "C20" H 1300 3700 50  0000 L CNN
F 1 "10n" H 1300 3500 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 1288 3450 50  0001 C CNN
F 3 "~" H 1250 3600 50  0001 C CNN
F 4 "" H 1250 3600 50  0001 C CNN "MPN"
	1    1250 3600
	1    0    0    -1  
$EndComp
Text Label 1250 3250 1    50   ~ 0
USB_SHD
Text GLabel 4550 1350 2    50   UnSpc ~ 0
USB_5V
Wire Wire Line
	4450 1750 4450 1850
Wire Wire Line
	4450 1350 4450 1450
$Comp
L Device:C C5
U 1 1 5F184C45
P 4450 1600
AR Path="/5F184C45" Ref="C5"  Part="1" 
AR Path="/5F302051/5F184C45" Ref="C?"  Part="1" 
AR Path="/5F4552C5/5F184C45" Ref="C35"  Part="1" 
F 0 "C35" H 4500 1700 50  0000 L CNN
F 1 "4u7" H 4500 1500 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 4488 1450 50  0001 C CNN
F 3 "~" H 4450 1600 50  0001 C CNN
F 4 "" H 4450 1600 50  0001 C CNN "MPN"
	1    4450 1600
	1    0    0    -1  
$EndComp
Wire Wire Line
	3750 1350 3650 1350
$Comp
L Device:Ferrite_Bead FB1
U 1 1 5F184C3D
P 3900 1350
AR Path="/5F184C3D" Ref="FB1"  Part="1" 
AR Path="/5F302051/5F184C3D" Ref="FB?"  Part="1" 
AR Path="/5F4552C5/5F184C3D" Ref="FB3"  Part="1" 
F 0 "FB3" V 3626 1350 50  0000 C CNN
F 1 "33R" V 3717 1350 50  0000 C CNN
F 2 "Inductor_SMD:L_0402_1005Metric" V 3830 1350 50  0001 C CNN
F 3 "~" H 3900 1350 50  0001 C CNN
	1    3900 1350
	0    1    1    0   
$EndComp
$Comp
L ng_power:GND #PWR0108
U 1 1 5F184C36
P 3650 1950
AR Path="/5F184C36" Ref="#PWR0108"  Part="1" 
AR Path="/5F302051/5F184C36" Ref="#PWR?"  Part="1" 
AR Path="/5F4552C5/5F184C36" Ref="#PWR039"  Part="1" 
F 0 "#PWR039" H 3650 1700 50  0001 C CNN
F 1 "GND" H 3653 1824 50  0000 C CNN
F 2 "" H 3550 1600 50  0001 C CNN
F 3 "" H 3650 1950 50  0001 C CNN
	1    3650 1950
	1    0    0    -1  
$EndComp
Wire Wire Line
	3650 1750 3650 1850
Wire Wire Line
	3650 1350 3650 1450
$Comp
L Device:C C3
U 1 1 5F184C2E
P 3650 1600
AR Path="/5F184C2E" Ref="C3"  Part="1" 
AR Path="/5F302051/5F184C2E" Ref="C?"  Part="1" 
AR Path="/5F4552C5/5F184C2E" Ref="C28"  Part="1" 
F 0 "C28" H 3700 1700 50  0000 L CNN
F 1 "100n" H 3700 1500 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 3688 1450 50  0001 C CNN
F 3 "~" H 3650 1600 50  0001 C CNN
F 4 "" H 3650 1600 50  0001 C CNN "MPN"
	1    3650 1600
	1    0    0    -1  
$EndComp
Wire Wire Line
	1900 4950 2000 4950
Wire Wire Line
	2000 5050 2000 4950
Connection ~ 2000 4950
Wire Wire Line
	2000 4950 2300 4950
Wire Wire Line
	2300 5050 2300 4950
Connection ~ 2300 4950
Wire Wire Line
	2300 4950 2400 4950
Connection ~ 2000 5450
$Comp
L ng_power:GND #PWR0109
U 1 1 5F2EE1D5
P 2000 5550
AR Path="/5F2EE1D5" Ref="#PWR0109"  Part="1" 
AR Path="/5F302051/5F2EE1D5" Ref="#PWR?"  Part="1" 
AR Path="/5F4552C5/5F2EE1D5" Ref="#PWR032"  Part="1" 
F 0 "#PWR032" H 2000 5300 50  0001 C CNN
F 1 "GND" H 2003 5424 50  0000 C CNN
F 2 "" H 1900 5200 50  0001 C CNN
F 3 "" H 2000 5550 50  0001 C CNN
	1    2000 5550
	1    0    0    -1  
$EndComp
Text GLabel 1500 4950 0    50   UnSpc ~ 0
P3V3
$Comp
L Device:C C22
U 1 1 5F3604FB
P 2000 6250
F 0 "C22" H 2050 6350 50  0000 L CNN
F 1 "4u7" H 2050 6150 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 2038 6100 50  0001 C CNN
F 3 "~" H 2000 6250 50  0001 C CNN
	1    2000 6250
	1    0    0    -1  
$EndComp
$Comp
L Device:C C24
U 1 1 5F360505
P 2300 6250
F 0 "C24" H 2350 6350 50  0000 L CNN
F 1 "100n" H 2350 6150 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 2338 6100 50  0001 C CNN
F 3 "~" H 2300 6250 50  0001 C CNN
	1    2300 6250
	1    0    0    -1  
$EndComp
Wire Wire Line
	2000 6400 2000 6500
Wire Wire Line
	2000 6500 2000 6600
Wire Wire Line
	2300 6400 2300 6500
Wire Wire Line
	2000 6500 2300 6500
Wire Wire Line
	1600 6000 1500 6000
Wire Wire Line
	1900 6000 2000 6000
Wire Wire Line
	2000 6100 2000 6000
Connection ~ 2000 6000
Wire Wire Line
	2000 6000 2300 6000
Wire Wire Line
	2300 6100 2300 6000
Connection ~ 2300 6000
Wire Wire Line
	2300 6000 2400 6000
Connection ~ 2000 6500
$Comp
L ng_power:GND #PWR0110
U 1 1 5F360526
P 2000 6600
AR Path="/5F360526" Ref="#PWR0110"  Part="1" 
AR Path="/5F302051/5F360526" Ref="#PWR?"  Part="1" 
AR Path="/5F4552C5/5F360526" Ref="#PWR033"  Part="1" 
F 0 "#PWR033" H 2000 6350 50  0001 C CNN
F 1 "GND" H 2003 6474 50  0000 C CNN
F 2 "" H 1900 6250 50  0001 C CNN
F 3 "" H 2000 6600 50  0001 C CNN
	1    2000 6600
	1    0    0    -1  
$EndComp
Text GLabel 1500 6000 0    50   UnSpc ~ 0
P3V3
$Comp
L Device:C C26
U 1 1 5F1F48FA
P 3400 5200
F 0 "C26" H 3450 5300 50  0000 L CNN
F 1 "100n" H 3450 5100 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 3438 5050 50  0001 C CNN
F 3 "~" H 3400 5200 50  0001 C CNN
	1    3400 5200
	1    0    0    -1  
$EndComp
$Comp
L Device:C C29
U 1 1 5F1F48F4
P 3700 5200
F 0 "C29" H 3750 5300 50  0000 L CNN
F 1 "100n" H 3750 5100 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 3738 5050 50  0001 C CNN
F 3 "~" H 3700 5200 50  0001 C CNN
	1    3700 5200
	1    0    0    -1  
$EndComp
$Comp
L Device:C C31
U 1 1 5F1F48EE
P 4000 5200
F 0 "C31" H 4050 5300 50  0000 L CNN
F 1 "100n" H 4050 5100 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 4038 5050 50  0001 C CNN
F 3 "~" H 4000 5200 50  0001 C CNN
	1    4000 5200
	1    0    0    -1  
$EndComp
Wire Wire Line
	3400 5050 3400 4950
Wire Wire Line
	3400 4950 3700 4950
Wire Wire Line
	4000 4950 4000 5050
Wire Wire Line
	3400 5350 3400 5450
Wire Wire Line
	3400 5450 3700 5450
Wire Wire Line
	4000 5350 4000 5450
Wire Wire Line
	3700 5350 3700 5450
Connection ~ 3700 5450
Wire Wire Line
	3700 5450 4000 5450
Wire Wire Line
	3700 5050 3700 4950
Connection ~ 3700 4950
Wire Wire Line
	3700 4950 4000 4950
Wire Wire Line
	3400 5450 3400 5550
Connection ~ 3400 5450
Connection ~ 4000 6500
Connection ~ 4000 6000
Wire Wire Line
	4000 6000 4300 6000
Wire Wire Line
	4000 6500 4300 6500
$Comp
L Device:C C34
U 1 1 5F1F48C6
P 4300 6250
F 0 "C34" H 4350 6350 50  0000 L CNN
F 1 "100n" H 4350 6150 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 4338 6100 50  0001 C CNN
F 3 "~" H 4300 6250 50  0001 C CNN
	1    4300 6250
	1    0    0    -1  
$EndComp
Connection ~ 3400 6500
Wire Wire Line
	3400 6500 3400 6600
Wire Wire Line
	3700 6000 4000 6000
Connection ~ 3700 6000
Wire Wire Line
	3700 6100 3700 6000
Wire Wire Line
	3700 6500 4000 6500
Connection ~ 3700 6500
Wire Wire Line
	3700 6400 3700 6500
Wire Wire Line
	4000 6400 4000 6500
Wire Wire Line
	3400 6500 3700 6500
Wire Wire Line
	3400 6400 3400 6500
Wire Wire Line
	4000 6000 4000 6100
Wire Wire Line
	3400 6000 3700 6000
Wire Wire Line
	3400 6100 3400 6000
$Comp
L Device:C C32
U 1 1 5F1F48A4
P 4000 6250
F 0 "C32" H 4050 6350 50  0000 L CNN
F 1 "100n" H 4050 6150 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 4038 6100 50  0001 C CNN
F 3 "~" H 4000 6250 50  0001 C CNN
	1    4000 6250
	1    0    0    -1  
$EndComp
$Comp
L Device:C C30
U 1 1 5F1F489E
P 3700 6250
F 0 "C30" H 3750 6350 50  0000 L CNN
F 1 "100n" H 3750 6150 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 3738 6100 50  0001 C CNN
F 3 "~" H 3700 6250 50  0001 C CNN
	1    3700 6250
	1    0    0    -1  
$EndComp
$Comp
L Device:C C27
U 1 1 5F1F4898
P 3400 6250
F 0 "C27" H 3450 6350 50  0000 L CNN
F 1 "100n" H 3450 6150 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 3438 6100 50  0001 C CNN
F 3 "~" H 3400 6250 50  0001 C CNN
	1    3400 6250
	1    0    0    -1  
$EndComp
Wire Wire Line
	3400 4950 3300 4950
Wire Wire Line
	3400 6000 3300 6000
Text GLabel 3300 6000 0    50   UnSpc ~ 0
P3V3
Text GLabel 6250 3550 0    50   UnSpc ~ 0
P3V3
$Comp
L ng_power:GND #PWR0111
U 1 1 5F44E168
P 3400 5550
AR Path="/5F44E168" Ref="#PWR0111"  Part="1" 
AR Path="/5F302051/5F44E168" Ref="#PWR?"  Part="1" 
AR Path="/5F4552C5/5F44E168" Ref="#PWR037"  Part="1" 
F 0 "#PWR037" H 3400 5300 50  0001 C CNN
F 1 "GND" H 3403 5424 50  0000 C CNN
F 2 "" H 3300 5200 50  0001 C CNN
F 3 "" H 3400 5550 50  0001 C CNN
	1    3400 5550
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR0112
U 1 1 5F44E5CF
P 3400 6600
AR Path="/5F44E5CF" Ref="#PWR0112"  Part="1" 
AR Path="/5F302051/5F44E5CF" Ref="#PWR?"  Part="1" 
AR Path="/5F4552C5/5F44E5CF" Ref="#PWR038"  Part="1" 
F 0 "#PWR038" H 3400 6350 50  0001 C CNN
F 1 "GND" H 3403 6474 50  0000 C CNN
F 2 "" H 3300 6250 50  0001 C CNN
F 3 "" H 3400 6600 50  0001 C CNN
	1    3400 6600
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR0113
U 1 1 5F44E9B1
P 8250 6050
AR Path="/5F44E9B1" Ref="#PWR0113"  Part="1" 
AR Path="/5F302051/5F44E9B1" Ref="#PWR?"  Part="1" 
AR Path="/5F4552C5/5F44E9B1" Ref="#PWR048"  Part="1" 
F 0 "#PWR048" H 8250 5800 50  0001 C CNN
F 1 "GND" H 8253 5924 50  0000 C CNN
F 2 "" H 8150 5700 50  0001 C CNN
F 3 "" H 8250 6050 50  0001 C CNN
	1    8250 6050
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR0114
U 1 1 5F44EE8A
P 7450 5650
AR Path="/5F44EE8A" Ref="#PWR0114"  Part="1" 
AR Path="/5F302051/5F44EE8A" Ref="#PWR?"  Part="1" 
AR Path="/5F4552C5/5F44EE8A" Ref="#PWR047"  Part="1" 
F 0 "#PWR047" H 7450 5400 50  0001 C CNN
F 1 "GND" H 7453 5524 50  0000 C CNN
F 2 "" H 7350 5300 50  0001 C CNN
F 3 "" H 7450 5650 50  0001 C CNN
	1    7450 5650
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR0115
U 1 1 5F44F292
P 7100 5550
AR Path="/5F44F292" Ref="#PWR0115"  Part="1" 
AR Path="/5F302051/5F44F292" Ref="#PWR?"  Part="1" 
AR Path="/5F4552C5/5F44F292" Ref="#PWR045"  Part="1" 
F 0 "#PWR045" H 7100 5300 50  0001 C CNN
F 1 "GND" H 7103 5424 50  0000 C CNN
F 2 "" H 7000 5200 50  0001 C CNN
F 3 "" H 7100 5550 50  0001 C CNN
	1    7100 5550
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR0116
U 1 1 5F44F69A
P 5800 5750
AR Path="/5F44F69A" Ref="#PWR0116"  Part="1" 
AR Path="/5F302051/5F44F69A" Ref="#PWR?"  Part="1" 
AR Path="/5F4552C5/5F44F69A" Ref="#PWR043"  Part="1" 
F 0 "#PWR043" H 5800 5500 50  0001 C CNN
F 1 "GND" H 5803 5624 50  0000 C CNN
F 2 "" H 5700 5400 50  0001 C CNN
F 3 "" H 5800 5750 50  0001 C CNN
	1    5800 5750
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR0117
U 1 1 5F44FA7C
P 5350 4850
AR Path="/5F44FA7C" Ref="#PWR0117"  Part="1" 
AR Path="/5F302051/5F44FA7C" Ref="#PWR?"  Part="1" 
AR Path="/5F4552C5/5F44FA7C" Ref="#PWR042"  Part="1" 
F 0 "#PWR042" H 5350 4600 50  0001 C CNN
F 1 "GND" H 5353 4724 50  0000 C CNN
F 2 "" H 5250 4500 50  0001 C CNN
F 3 "" H 5350 4850 50  0001 C CNN
	1    5350 4850
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR0118
U 1 1 5F44FFB4
P 5150 4850
AR Path="/5F44FFB4" Ref="#PWR0118"  Part="1" 
AR Path="/5F302051/5F44FFB4" Ref="#PWR?"  Part="1" 
AR Path="/5F4552C5/5F44FFB4" Ref="#PWR041"  Part="1" 
F 0 "#PWR041" H 5150 4600 50  0001 C CNN
F 1 "GND" H 5153 4724 50  0000 C CNN
F 2 "" H 5050 4500 50  0001 C CNN
F 3 "" H 5150 4850 50  0001 C CNN
	1    5150 4850
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR0119
U 1 1 5F45034A
P 7050 3950
AR Path="/5F45034A" Ref="#PWR0119"  Part="1" 
AR Path="/5F302051/5F45034A" Ref="#PWR?"  Part="1" 
AR Path="/5F4552C5/5F45034A" Ref="#PWR044"  Part="1" 
F 0 "#PWR044" H 7050 3700 50  0001 C CNN
F 1 "GND" H 7053 3824 50  0000 C CNN
F 2 "" H 6950 3600 50  0001 C CNN
F 3 "" H 7050 3950 50  0001 C CNN
	1    7050 3950
	1    0    0    -1  
$EndComp
Text GLabel 5050 4350 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	5800 5250 5700 5250
Text GLabel 5700 5250 0    50   UnSpc ~ 0
P3V3
Text GLabel 7050 3650 0    50   UnSpc ~ 0
P3V3
Text GLabel 6350 1750 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	6950 1950 7050 1950
Connection ~ 7050 1950
Text GLabel 8950 1250 1    50   UnSpc ~ 0
P3V3
Connection ~ 5800 5250
Connection ~ 3400 4950
Connection ~ 3400 6000
Text Label 5450 3400 0    50   ~ 0
xUSB_D-
Wire Wire Line
	4550 3200 4450 3200
Wire Wire Line
	4550 3400 4450 3400
Wire Wire Line
	5450 3400 5350 3400
Wire Wire Line
	5350 3200 5450 3200
Text Label 5450 3200 0    50   ~ 0
USB_D-
Connection ~ 4150 1850
Wire Wire Line
	4150 1850 4450 1850
Wire Wire Line
	3650 1950 3650 1850
$Comp
L Device:Ferrite_Bead FB2
U 1 1 5FA45036
P 1750 4950
AR Path="/5FA45036" Ref="FB2"  Part="1" 
AR Path="/5F302051/5FA45036" Ref="FB?"  Part="1" 
AR Path="/5F4552C5/5FA45036" Ref="FB1"  Part="1" 
F 0 "FB1" V 1476 4950 50  0000 C CNN
F 1 "600R" V 1567 4950 50  0000 C CNN
F 2 "Inductor_SMD:L_0402_1005Metric" V 1680 4950 50  0001 C CNN
F 3 "~" H 1750 4950 50  0001 C CNN
F 4 "" V 1750 4950 50  0001 C CNN "MPN"
	1    1750 4950
	0    1    1    0   
$EndComp
$Comp
L Device:Ferrite_Bead FB3
U 1 1 5FA46223
P 1750 6000
AR Path="/5FA46223" Ref="FB3"  Part="1" 
AR Path="/5F302051/5FA46223" Ref="FB?"  Part="1" 
AR Path="/5F4552C5/5FA46223" Ref="FB2"  Part="1" 
F 0 "FB2" V 1476 6000 50  0000 C CNN
F 1 "600R" V 1567 6000 50  0000 C CNN
F 2 "Inductor_SMD:L_0402_1005Metric" V 1680 6000 50  0001 C CNN
F 3 "~" H 1750 6000 50  0001 C CNN
F 4 "" V 1750 6000 50  0001 C CNN "MPN"
	1    1750 6000
	0    1    1    0   
$EndComp
Text Label 7100 5250 0    50   ~ 0
USB_CLK
Text Label 6650 4350 0    50   ~ 0
USB_EECS
Text Label 6650 4450 0    50   ~ 0
USB_EECLK
Text Label 6650 4550 0    50   ~ 0
USB_EEDATA
Wire Wire Line
	6350 4650 7050 4650
Connection ~ 6350 4650
Text Label 6650 4650 0    50   ~ 0
USB_EEDO
$Comp
L Device:R R19
U 1 1 5FBDF481
P 6350 4000
F 0 "R19" V 6300 4150 50  0000 L CNN
F 1 "10k" V 6300 3700 50  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" V 6280 4000 50  0001 C CNN
F 3 "~" H 6350 4000 50  0001 C CNN
F 4 "" V 6350 4000 50  0001 C CNN "MPN"
	1    6350 4000
	1    0    0    -1  
$EndComp
$Comp
L Connector:USB_C_Receptacle_USB2.0 J5
U 1 1 5F216B5E
P 1550 1950
F 0 "J5" H 1150 2800 50  0000 L CNN
F 1 "USB_C_USB2.0" H 1150 2700 50  0000 L CNN
F 2 "ng_conn:USB_C_Receptacle_HRO_TYPE-C-31-M-12" H 1700 1950 50  0001 C CNN
F 3 "https://www.usb.org/sites/default/files/documents/usb_type-c.zip" H 1700 1950 50  0001 C CNN
	1    1550 1950
	1    0    0    -1  
$EndComp
NoConn ~ 2150 2450
NoConn ~ 2150 2550
$Comp
L Device:R R22
U 1 1 5F1F4785
P 7300 3850
F 0 "R22" V 7250 4050 50  0000 C CNN
F 1 "12k, 1%" V 7200 3850 50  0000 C CNN
F 2 "Resistor_SMD:R_0402_1005Metric" V 7230 3850 50  0001 C CNN
F 3 "~" H 7300 3850 50  0001 C CNN
	1    7300 3850
	0    1    1    0   
$EndComp
$Comp
L Device:R R21
U 1 1 5F1F4742
P 7300 3650
F 0 "R21" V 7250 3850 50  0000 C CNN
F 1 "10k" V 7200 3650 50  0000 C CNN
F 2 "Resistor_SMD:R_0402_1005Metric" V 7230 3650 50  0001 C CNN
F 3 "~" H 7300 3650 50  0001 C CNN
	1    7300 3650
	0    1    1    0   
$EndComp
Wire Wire Line
	2150 1550 3250 1550
Wire Wire Line
	2950 1650 2150 1650
Wire Wire Line
	2150 1850 2250 1850
Wire Wire Line
	2250 1850 2250 1950
Wire Wire Line
	2250 1950 2150 1950
Wire Wire Line
	2150 2050 2250 2050
Wire Wire Line
	2250 2050 2250 2150
Wire Wire Line
	2250 2150 2150 2150
Wire Wire Line
	2250 1950 2350 1950
Connection ~ 2250 1950
Wire Wire Line
	2250 2050 2350 2050
Connection ~ 2250 2050
Wire Wire Line
	3650 1850 4150 1850
$Comp
L ng_power:GND #PWR02
U 1 1 5F375E75
P 1550 2950
AR Path="/5F375E75" Ref="#PWR02"  Part="1" 
AR Path="/5F302051/5F375E75" Ref="#PWR?"  Part="1" 
AR Path="/5F4552C5/5F375E75" Ref="#PWR031"  Part="1" 
F 0 "#PWR031" H 1550 2700 50  0001 C CNN
F 1 "GND" H 1553 2824 50  0000 C CNN
F 2 "" H 1450 2600 50  0001 C CNN
F 3 "" H 1550 2950 50  0001 C CNN
	1    1550 2950
	1    0    0    -1  
$EndComp
Wire Wire Line
	1550 2950 1550 2850
$Comp
L Device:R R17
U 1 1 5F4401E3
P 2950 1900
F 0 "R17" H 3020 1946 50  0000 L CNN
F 1 "5k1" H 3020 1855 50  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" V 2880 1900 50  0001 C CNN
F 3 "~" H 2950 1900 50  0001 C CNN
	1    2950 1900
	1    0    0    -1  
$EndComp
$Comp
L Device:R R18
U 1 1 5F457E9E
P 3250 1900
F 0 "R18" H 3320 1946 50  0000 L CNN
F 1 "5k1" H 3320 1855 50  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" V 3180 1900 50  0001 C CNN
F 3 "~" H 3250 1900 50  0001 C CNN
	1    3250 1900
	1    0    0    -1  
$EndComp
Wire Wire Line
	3250 1550 3250 1750
Wire Wire Line
	2950 1650 2950 1750
Wire Wire Line
	2950 2050 2950 2150
Wire Wire Line
	2950 2150 3250 2150
Wire Wire Line
	3250 2150 3250 2050
Connection ~ 3650 1850
$Comp
L ng_power:GND #PWR01
U 1 1 5F54C875
P 2950 2250
AR Path="/5F54C875" Ref="#PWR01"  Part="1" 
AR Path="/5F302051/5F54C875" Ref="#PWR?"  Part="1" 
AR Path="/5F4552C5/5F54C875" Ref="#PWR035"  Part="1" 
F 0 "#PWR035" H 2950 2000 50  0001 C CNN
F 1 "GND" H 2953 2124 50  0000 C CNN
F 2 "" H 2850 1900 50  0001 C CNN
F 3 "" H 2950 2250 50  0001 C CNN
	1    2950 2250
	1    0    0    -1  
$EndComp
Wire Wire Line
	2950 2250 2950 2150
Connection ~ 2950 2150
Wire Wire Line
	1250 3450 1250 3350
Wire Wire Line
	1250 3350 1550 3350
Wire Wire Line
	1550 3350 1550 3450
Wire Wire Line
	1250 3750 1250 3850
Wire Wire Line
	1250 3850 1550 3850
Wire Wire Line
	1550 3850 1550 3750
$Comp
L ng_power:GND #PWR03
U 1 1 5F590735
P 1250 3950
AR Path="/5F590735" Ref="#PWR03"  Part="1" 
AR Path="/5F302051/5F590735" Ref="#PWR?"  Part="1" 
AR Path="/5F4552C5/5F590735" Ref="#PWR030"  Part="1" 
F 0 "#PWR030" H 1250 3700 50  0001 C CNN
F 1 "GND" H 1253 3824 50  0000 C CNN
F 2 "" H 1150 3600 50  0001 C CNN
F 3 "" H 1250 3950 50  0001 C CNN
	1    1250 3950
	1    0    0    -1  
$EndComp
Wire Wire Line
	1250 3950 1250 3850
Connection ~ 1250 3850
Wire Wire Line
	1250 3350 1250 2850
Connection ~ 1250 3350
Text Label 2250 1550 0    50   ~ 0
USB_CC1
Text Label 2250 1650 0    50   ~ 0
USB_CC2
Text Notes 6150 5700 0    50   ~ 0
+/-30ppm, <150pS
Text Label 4450 3400 2    50   ~ 0
xUSB_D+
Text Label 4450 3200 2    50   ~ 0
USB_D+
Text Label 7450 3050 2    50   ~ 0
USB_D+
Text Label 7450 2950 2    50   ~ 0
USB_D-
Text Label 2350 2050 0    50   ~ 0
xUSB_D+
Text Label 2350 1950 0    50   ~ 0
xUSB_D-
$Comp
L ng_power:GND #PWR046
U 1 1 5F7012B4
P 6450 2550
F 0 "#PWR046" H 6450 2300 50  0001 C CNN
F 1 "GND" H 6453 2424 50  0000 C CNN
F 2 "" H 6350 2200 50  0001 C CNN
F 3 "" H 6450 2550 50  0001 C CNN
	1    6450 2550
	1    0    0    -1  
$EndComp
Text GLabel 9950 1750 2    50   BiDi ~ 0
USB_AD0
Text GLabel 9950 1850 2    50   BiDi ~ 0
USB_AD1
Text GLabel 9950 1950 2    50   BiDi ~ 0
USB_AD2
Text GLabel 9950 2050 2    50   BiDi ~ 0
USB_AD3
Text GLabel 9950 2150 2    50   BiDi ~ 0
USB_AD4
Text GLabel 9950 2250 2    50   BiDi ~ 0
USB_AD5
Text GLabel 9950 2350 2    50   BiDi ~ 0
USB_AD6
Text GLabel 9950 2450 2    50   BiDi ~ 0
USB_AD7
Text GLabel 9950 2650 2    50   BiDi ~ 0
USB_AC0
Text GLabel 9950 2750 2    50   BiDi ~ 0
USB_AC1
Text GLabel 9950 2850 2    50   BiDi ~ 0
USB_AC2
Text GLabel 9950 2950 2    50   BiDi ~ 0
USB_AC3
Text GLabel 9950 3050 2    50   BiDi ~ 0
USB_AC4
Text GLabel 9950 3150 2    50   BiDi ~ 0
USB_AC5
Text GLabel 9950 3250 2    50   BiDi ~ 0
USB_AC6
Text GLabel 9950 3350 2    50   BiDi ~ 0
USB_AC7
Connection ~ 7450 4550
Wire Wire Line
	6250 4550 7450 4550
Text GLabel 9950 3550 2    50   BiDi ~ 0
USB_BD0
Text GLabel 9950 3650 2    50   BiDi ~ 0
USB_BD1
Text GLabel 9950 3750 2    50   BiDi ~ 0
USB_BD2
Text GLabel 9950 3850 2    50   BiDi ~ 0
USB_BD3
Text GLabel 9950 3950 2    50   BiDi ~ 0
USB_BD4
Text GLabel 9950 4050 2    50   BiDi ~ 0
USB_BD5
Text GLabel 9950 4150 2    50   BiDi ~ 0
USB_BD6
Text GLabel 9950 4250 2    50   BiDi ~ 0
USB_BD7
Text GLabel 9950 4450 2    50   BiDi ~ 0
USB_BC0
Text GLabel 9950 4550 2    50   BiDi ~ 0
USB_BC1
Text GLabel 9950 4650 2    50   BiDi ~ 0
USB_BC2
Text GLabel 9950 4750 2    50   BiDi ~ 0
USB_BC3
Text GLabel 9950 4850 2    50   BiDi ~ 0
USB_BC4
Text GLabel 9950 4950 2    50   BiDi ~ 0
USB_BC5
Text GLabel 9950 5050 2    50   BiDi ~ 0
USB_BC6
Text GLabel 9950 5150 2    50   BiDi ~ 0
USB_BC7
$Comp
L Device:R R?
U 1 1 5F3148AD
P 2850 3000
AR Path="/5F3148AD" Ref="R?"  Part="1" 
AR Path="/5F302051/5F3148AD" Ref="R3"  Part="1" 
AR Path="/5F4552C5/5F3148AD" Ref="R15"  Part="1" 
F 0 "R15" H 2920 3046 50  0000 L CNN
F 1 "6k8" H 2920 2955 50  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" V 2780 3000 50  0001 C CNN
F 3 "~" H 2850 3000 50  0001 C CNN
F 4 "" H 2850 3000 50  0001 C CNN "MPN"
	1    2850 3000
	1    0    0    -1  
$EndComp
Wire Wire Line
	2850 3650 2850 3750
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148BA
P 2850 3750
AR Path="/5F3148BA" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148BA" Ref="#PWR024"  Part="1" 
AR Path="/5F4552C5/5F3148BA" Ref="#PWR034"  Part="1" 
F 0 "#PWR034" H 2850 3500 50  0001 C CNN
F 1 "GND" H 2853 3624 50  0000 C CNN
F 2 "" H 2750 3400 50  0001 C CNN
F 3 "" H 2850 3750 50  0001 C CNN
	1    2850 3750
	1    0    0    -1  
$EndComp
Wire Wire Line
	2850 3150 2850 3250
Wire Wire Line
	2850 2850 2850 2750
Wire Wire Line
	2850 2750 2750 2750
Wire Wire Line
	2850 3250 3200 3250
Connection ~ 2850 3250
Wire Wire Line
	2850 3250 2850 3350
Text GLabel 3300 3250 2    50   Output ~ 0
USB_DET
Text GLabel 2750 2750 0    50   UnSpc ~ 0
USB_5V
Text Notes 3200 3100 0    50   ~ 0
USB_DETn < 3.3V\nfor compatibility\nwith FPGA IO bank
Wire Wire Line
	3200 3350 3200 3250
Connection ~ 3200 3250
Wire Wire Line
	3200 3250 3300 3250
Wire Wire Line
	3200 3650 3200 3750
$Comp
L ng_power:GND #PWR?
U 1 1 5F312C25
P 3200 3750
AR Path="/5F312C25" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F312C25" Ref="#PWR039"  Part="1" 
AR Path="/5F4552C5/5F312C25" Ref="#PWR036"  Part="1" 
F 0 "#PWR036" H 3200 3500 50  0001 C CNN
F 1 "GND" H 3203 3624 50  0000 C CNN
F 2 "" H 3100 3400 50  0001 C CNN
F 3 "" H 3200 3750 50  0001 C CNN
	1    3200 3750
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 5F3148B3
P 2850 3500
AR Path="/5F3148B3" Ref="R?"  Part="1" 
AR Path="/5F302051/5F3148B3" Ref="R5"  Part="1" 
AR Path="/5F4552C5/5F3148B3" Ref="R16"  Part="1" 
F 0 "R16" H 2920 3546 50  0000 L CNN
F 1 "10k" H 2920 3455 50  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" V 2780 3500 50  0001 C CNN
F 3 "~" H 2850 3500 50  0001 C CNN
F 4 "" H 2850 3500 50  0001 C CNN "MPN"
	1    2850 3500
	1    0    0    -1  
$EndComp
$Comp
L Device:C C25
U 1 1 5F31C8F6
P 3200 3500
F 0 "C25" H 3315 3546 50  0000 L CNN
F 1 "DNP" H 3315 3455 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 3238 3350 50  0001 C CNN
F 3 "~" H 3200 3500 50  0001 C CNN
	1    3200 3500
	1    0    0    -1  
$EndComp
$Comp
L ng_ftdi:FT2232HQ U11
U 1 1 5F48BD9E
P 8750 3650
F 0 "U11" H 7700 5850 50  0000 L CNN
F 1 "FT2232HQ" H 7700 5750 50  0000 L CNN
F 2 "Package_DFN_QFN:QFN-64-1EP_9x9mm_P0.5mm_EP4.35x4.35mm" H 8750 3650 50  0001 C CNN
F 3 "https://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT2232H.pdf" H 8750 3650 50  0001 C CNN
	1    8750 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	9150 5950 9250 5950
Wire Wire Line
	9250 5950 9250 5850
Connection ~ 9150 5950
$Comp
L Device:C C40
U 1 1 5F865B3F
P 6450 2200
F 0 "C40" H 6400 2300 50  0000 R CNN
F 1 "100n" H 6400 2100 50  0000 R CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 6488 2050 50  0001 C CNN
F 3 "~" H 6450 2200 50  0001 C CNN
	1    6450 2200
	-1   0    0    -1  
$EndComp
Wire Wire Line
	6450 2050 6450 1750
Connection ~ 6450 1750
Wire Wire Line
	6450 1750 6350 1750
Wire Wire Line
	6450 2350 6450 2450
Wire Wire Line
	6450 2450 7050 2450
Wire Wire Line
	6450 2450 6450 2550
Connection ~ 6450 2450
Connection ~ 7050 2450
Text Label 3300 4950 2    50   ~ 0
USB_1V8
Text Label 6950 1950 2    50   ~ 0
USB_1V8
Wire Wire Line
	8250 1250 8150 1250
Wire Wire Line
	8350 1150 8150 1150
Text Label 8150 1250 2    50   ~ 0
USB_VPHY
Text Label 8150 1150 2    50   ~ 0
USB_VPLL
Wire Wire Line
	8550 1050 8150 1050
Text Label 8150 1050 2    50   ~ 0
USB_1V8
Text Label 2400 4950 0    50   ~ 0
USB_VPHY
Text Label 2400 6000 0    50   ~ 0
USB_VPLL
$EndSCHEMATC
