EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 3 12
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
L Regulator_Linear:AZ1117-1.2 U?
U 1 1 5F820EB8
P 3950 3400
AR Path="/5F820EB8" Ref="U?"  Part="1" 
AR Path="/5F7F68FE/5F820EB8" Ref="U2"  Part="1" 
F 0 "U2" H 3950 3642 50  0000 C CNN
F 1 "AZ1117-1.2" H 3950 3551 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-223-3_TabPin2" H 3950 3650 50  0001 C CIN
F 3 "https://www.diodes.com/assets/Datasheets/AZ1117.pdf" H 3950 3400 50  0001 C CNN
	1    3950 3400
	1    0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 5F820EBE
P 3450 3650
AR Path="/5F820EBE" Ref="C?"  Part="1" 
AR Path="/5F7F68FE/5F820EBE" Ref="C1"  Part="1" 
F 0 "C1" H 3500 3750 50  0000 L CNN
F 1 "10u" H 3500 3550 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 3488 3500 50  0001 C CNN
F 3 "~" H 3450 3650 50  0001 C CNN
	1    3450 3650
	1    0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 5F820EC4
P 4450 3650
AR Path="/5F820EC4" Ref="C?"  Part="1" 
AR Path="/5F7F68FE/5F820EC4" Ref="C2"  Part="1" 
F 0 "C2" H 4500 3750 50  0000 L CNN
F 1 "10u" H 4500 3550 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 4488 3500 50  0001 C CNN
F 3 "~" H 4450 3650 50  0001 C CNN
	1    4450 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	3450 3500 3450 3400
Connection ~ 3450 3400
Wire Wire Line
	3450 3400 3650 3400
Wire Wire Line
	4250 3400 4450 3400
Wire Wire Line
	4450 3500 4450 3400
Connection ~ 4450 3400
Wire Wire Line
	4450 3400 4550 3400
Wire Wire Line
	3450 3800 3450 3900
$Comp
L ng_power:GND #PWR?
U 1 1 5F820ED2
P 3450 3900
AR Path="/5F820ED2" Ref="#PWR?"  Part="1" 
AR Path="/5F7F68FE/5F820ED2" Ref="#PWR01"  Part="1" 
F 0 "#PWR01" H 3450 3650 50  0001 C CNN
F 1 "GND" H 3453 3774 50  0000 C CNN
F 2 "" H 3350 3550 50  0001 C CNN
F 3 "" H 3450 3900 50  0001 C CNN
	1    3450 3900
	1    0    0    -1  
$EndComp
Wire Wire Line
	4450 3800 4450 3900
$Comp
L ng_power:GND #PWR?
U 1 1 5F820ED9
P 4450 3900
AR Path="/5F820ED9" Ref="#PWR?"  Part="1" 
AR Path="/5F7F68FE/5F820ED9" Ref="#PWR03"  Part="1" 
F 0 "#PWR03" H 4450 3650 50  0001 C CNN
F 1 "GND" H 4453 3774 50  0000 C CNN
F 2 "" H 4350 3550 50  0001 C CNN
F 3 "" H 4450 3900 50  0001 C CNN
	1    4450 3900
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR?
U 1 1 5F820EDF
P 3950 3900
AR Path="/5F820EDF" Ref="#PWR?"  Part="1" 
AR Path="/5F7F68FE/5F820EDF" Ref="#PWR02"  Part="1" 
F 0 "#PWR02" H 3950 3650 50  0001 C CNN
F 1 "GND" H 3953 3774 50  0000 C CNN
F 2 "" H 3850 3550 50  0001 C CNN
F 3 "" H 3950 3900 50  0001 C CNN
	1    3950 3900
	1    0    0    -1  
$EndComp
Wire Wire Line
	3950 3900 3950 3700
Wire Wire Line
	3350 3400 3450 3400
Text GLabel 4550 3400 2    50   UnSpc ~ 0
USB_3V3
$Comp
L Regulator_Linear:AZ1117-1.2 U?
U 1 1 5F820EE8
P 3950 4600
AR Path="/5F820EE8" Ref="U?"  Part="1" 
AR Path="/5F7F68FE/5F820EE8" Ref="U3"  Part="1" 
F 0 "U3" H 3950 4842 50  0000 C CNN
F 1 "AZ1117-1.2" H 3950 4751 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-223-3_TabPin2" H 3950 4850 50  0001 C CIN
F 3 "https://www.diodes.com/assets/Datasheets/AZ1117.pdf" H 3950 4600 50  0001 C CNN
	1    3950 4600
	1    0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 5F820EEE
P 3450 4850
AR Path="/5F820EEE" Ref="C?"  Part="1" 
AR Path="/5F7F68FE/5F820EEE" Ref="C5"  Part="1" 
F 0 "C5" H 3500 4950 50  0000 L CNN
F 1 "10u" H 3500 4750 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 3488 4700 50  0001 C CNN
F 3 "~" H 3450 4850 50  0001 C CNN
	1    3450 4850
	1    0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 5F820EF4
P 4450 4850
AR Path="/5F820EF4" Ref="C?"  Part="1" 
AR Path="/5F7F68FE/5F820EF4" Ref="C6"  Part="1" 
F 0 "C6" H 4500 4950 50  0000 L CNN
F 1 "10u" H 4500 4750 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 4488 4700 50  0001 C CNN
F 3 "~" H 4450 4850 50  0001 C CNN
	1    4450 4850
	1    0    0    -1  
$EndComp
Wire Wire Line
	3450 4700 3450 4600
Connection ~ 3450 4600
Wire Wire Line
	3450 4600 3650 4600
Wire Wire Line
	4250 4600 4450 4600
Wire Wire Line
	4450 4700 4450 4600
Connection ~ 4450 4600
Wire Wire Line
	4450 4600 4550 4600
Wire Wire Line
	3450 5000 3450 5100
$Comp
L ng_power:GND #PWR?
U 1 1 5F820F02
P 3450 5100
AR Path="/5F820F02" Ref="#PWR?"  Part="1" 
AR Path="/5F7F68FE/5F820F02" Ref="#PWR06"  Part="1" 
F 0 "#PWR06" H 3450 4850 50  0001 C CNN
F 1 "GND" H 3453 4974 50  0000 C CNN
F 2 "" H 3350 4750 50  0001 C CNN
F 3 "" H 3450 5100 50  0001 C CNN
	1    3450 5100
	1    0    0    -1  
$EndComp
Wire Wire Line
	4450 5000 4450 5100
$Comp
L ng_power:GND #PWR?
U 1 1 5F820F09
P 4450 5100
AR Path="/5F820F09" Ref="#PWR?"  Part="1" 
AR Path="/5F7F68FE/5F820F09" Ref="#PWR08"  Part="1" 
F 0 "#PWR08" H 4450 4850 50  0001 C CNN
F 1 "GND" H 4453 4974 50  0000 C CNN
F 2 "" H 4350 4750 50  0001 C CNN
F 3 "" H 4450 5100 50  0001 C CNN
	1    4450 5100
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR?
U 1 1 5F820F0F
P 3950 5100
AR Path="/5F820F0F" Ref="#PWR?"  Part="1" 
AR Path="/5F7F68FE/5F820F0F" Ref="#PWR07"  Part="1" 
F 0 "#PWR07" H 3950 4850 50  0001 C CNN
F 1 "GND" H 3953 4974 50  0000 C CNN
F 2 "" H 3850 4750 50  0001 C CNN
F 3 "" H 3950 5100 50  0001 C CNN
	1    3950 5100
	1    0    0    -1  
$EndComp
Wire Wire Line
	3950 5100 3950 4900
Wire Wire Line
	3350 4600 3450 4600
Text GLabel 3350 4600 0    50   UnSpc ~ 0
P3V3
Text GLabel 4550 4600 2    50   UnSpc ~ 0
P1V2
Wire Wire Line
	6800 4150 6800 4250
$Comp
L Device:C C?
U 1 1 5F820F1C
P 6800 4400
AR Path="/5F820F1C" Ref="C?"  Part="1" 
AR Path="/5F7F68FE/5F820F1C" Ref="C4"  Part="1" 
F 0 "C4" H 6850 4500 50  0000 L CNN
F 1 "10u" H 6850 4300 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 6838 4250 50  0001 C CNN
F 3 "~" H 6800 4400 50  0001 C CNN
	1    6800 4400
	1    0    0    -1  
$EndComp
Wire Wire Line
	6800 4550 6800 4650
$Comp
L ng_power:GND #PWR?
U 1 1 5F820F23
P 6800 4650
AR Path="/5F820F23" Ref="#PWR?"  Part="1" 
AR Path="/5F7F68FE/5F820F23" Ref="#PWR05"  Part="1" 
F 0 "#PWR05" H 6800 4400 50  0001 C CNN
F 1 "GND" H 6803 4524 50  0000 C CNN
F 2 "" H 6700 4300 50  0001 C CNN
F 3 "" H 6800 4650 50  0001 C CNN
	1    6800 4650
	1    0    0    -1  
$EndComp
Text GLabel 3350 3400 0    50   UnSpc ~ 0
USB_5V
$Comp
L Connector_Generic:Conn_01x03 J?
U 1 1 5F820F2A
P 6200 4050
AR Path="/5F820F2A" Ref="J?"  Part="1" 
AR Path="/5F7F68FE/5F820F2A" Ref="J1"  Part="1" 
F 0 "J1" H 6200 3850 50  0000 C CNN
F 1 "Conn_01x03" H 6118 3816 50  0001 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 6200 4050 50  0001 C CNN
F 3 "~" H 6200 4050 50  0001 C CNN
	1    6200 4050
	-1   0    0    1   
$EndComp
Wire Wire Line
	6400 3950 6500 3950
Wire Wire Line
	6400 4050 7550 4050
Wire Wire Line
	6400 4150 6800 4150
Text GLabel 7000 3950 2    50   UnSpc ~ 0
USB_3V3
Text GLabel 7000 4150 2    50   UnSpc ~ 0
N64_3V3
Text GLabel 7550 4050 2    50   UnSpc ~ 0
P3V3
Wire Wire Line
	6500 3950 6500 4250
$Comp
L Device:C C?
U 1 1 5F820F39
P 6500 4400
AR Path="/5F820F39" Ref="C?"  Part="1" 
AR Path="/5F7F68FE/5F820F39" Ref="C3"  Part="1" 
F 0 "C3" H 6550 4500 50  0000 L CNN
F 1 "10u" H 6550 4300 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 6538 4250 50  0001 C CNN
F 3 "~" H 6500 4400 50  0001 C CNN
	1    6500 4400
	1    0    0    -1  
$EndComp
Wire Wire Line
	6500 4550 6500 4650
$Comp
L ng_power:GND #PWR?
U 1 1 5F820F40
P 6500 4650
AR Path="/5F820F40" Ref="#PWR?"  Part="1" 
AR Path="/5F7F68FE/5F820F40" Ref="#PWR04"  Part="1" 
F 0 "#PWR04" H 6500 4400 50  0001 C CNN
F 1 "GND" H 6503 4524 50  0000 C CNN
F 2 "" H 6400 4300 50  0001 C CNN
F 3 "" H 6500 4650 50  0001 C CNN
	1    6500 4650
	1    0    0    -1  
$EndComp
Connection ~ 6500 3950
Wire Wire Line
	6500 3950 7000 3950
Connection ~ 6800 4150
Wire Wire Line
	6800 4150 7000 4150
$EndSCHEMATC
