EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 3 8
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Connection ~ 4250 4500
NoConn ~ 3650 3600
NoConn ~ 3650 4500
Wire Wire Line
	3450 3300 3650 3300
Wire Wire Line
	3450 4000 3650 4000
Wire Wire Line
	3450 4100 3650 4100
Wire Wire Line
	3450 4200 3650 4200
Wire Wire Line
	3450 4300 3650 4300
Wire Wire Line
	3450 4400 3650 4400
Wire Wire Line
	3450 4600 3650 4600
Wire Wire Line
	3450 4700 3650 4700
Wire Wire Line
	3450 4800 3650 4800
Wire Wire Line
	3450 4900 3650 4900
Wire Wire Line
	3450 5000 3650 5000
Wire Wire Line
	4150 3600 4250 3600
Wire Wire Line
	4150 3300 4350 3300
Wire Wire Line
	4150 4000 4350 4000
Wire Wire Line
	4150 4100 4350 4100
Wire Wire Line
	4150 4200 4350 4200
Wire Wire Line
	4150 4300 4350 4300
Wire Wire Line
	4150 4400 4350 4400
Wire Wire Line
	4150 4600 4350 4600
Wire Wire Line
	4150 4700 4350 4700
Wire Wire Line
	4150 4800 4350 4800
Wire Wire Line
	4150 4900 4350 4900
Wire Wire Line
	4150 5000 4350 5000
Wire Wire Line
	4250 3600 4250 3700
Wire Wire Line
	4250 4500 4150 4500
Wire Wire Line
	4250 4500 4250 5100
$Comp
L Connector_Generic:Conn_02x20_Odd_Even J?
U 1 1 5F1CD119
P 3850 4000
AR Path="/5F1CD119" Ref="J?"  Part="1" 
AR Path="/5F133F50/5F1CD119" Ref="J4"  Part="1" 
F 0 "J4" H 3900 5050 50  0000 C CNN
F 1 "Conn_02x20_Odd_Even" H 3900 5025 50  0001 C CNN
F 2 "local_conn:PinHeader_2x20_P2.54mm_Horizontal" H 3850 4000 50  0001 C CNN
F 3 "~" H 3850 4000 50  0001 C CNN
	1    3850 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	4150 3700 4250 3700
Connection ~ 4250 3700
Wire Wire Line
	4250 3700 4250 3800
Wire Wire Line
	4150 3800 4250 3800
Connection ~ 4250 3800
Wire Wire Line
	4250 3800 4250 3900
Wire Wire Line
	4150 3900 4250 3900
Connection ~ 4250 3900
Wire Wire Line
	4250 3900 4250 4500
Wire Wire Line
	3650 3900 3550 3900
Wire Wire Line
	3550 3900 3550 3800
Wire Wire Line
	3550 3700 3650 3700
Wire Wire Line
	3650 3800 3550 3800
Connection ~ 3550 3800
Wire Wire Line
	3550 3800 3550 3700
Wire Wire Line
	3550 3700 3450 3700
Connection ~ 3550 3700
NoConn ~ 3650 3100
NoConn ~ 3650 3200
NoConn ~ 3650 3400
NoConn ~ 3650 3500
NoConn ~ 4150 3100
NoConn ~ 4150 3200
NoConn ~ 4150 3400
NoConn ~ 4150 3500
Text GLabel 3450 3300 0    50   Input ~ 0
N64_COLD_RESETn
Text GLabel 4350 3300 2    50   Input ~ 0
N64_OS_EVENTn
$Comp
L ng_power:GND #PWR?
U 1 1 5F1CD13A
P 4250 5100
F 0 "#PWR?" H 4250 4850 50  0001 C CNN
F 1 "GND" H 4253 4974 50  0000 C CNN
F 2 "" H 4150 4750 50  0001 C CNN
F 3 "" H 4250 5100 50  0001 C CNN
	1    4250 5100
	1    0    0    -1  
$EndComp
Text GLabel 3450 4000 0    50   Input ~ 0
N64_AD7
Text GLabel 3450 4100 0    50   Input ~ 0
N64_AD6
Text GLabel 3450 4200 0    50   Input ~ 0
N64_AD5
Text GLabel 3450 4300 0    50   Input ~ 0
N64_AD4
Text GLabel 3450 4400 0    50   Input ~ 0
N64_ALE_H
Text GLabel 3450 4600 0    50   Input ~ 0
N64_ALE_L
Text GLabel 3450 4700 0    50   Input ~ 0
N64_AD3
Text GLabel 3450 4800 0    50   Input ~ 0
N64_AD2
Text GLabel 3450 4900 0    50   Input ~ 0
N64_AD1
Text GLabel 3450 5000 0    50   Input ~ 0
N64_AD0
Text GLabel 4350 4000 2    50   Input ~ 0
N64_AD8
Text GLabel 4350 4100 2    50   Input ~ 0
N64_AD9
Text GLabel 4350 4200 2    50   Input ~ 0
N64_AD10
Text GLabel 4350 4300 2    50   Input ~ 0
N64_AD11
Text GLabel 4350 4400 2    50   Input ~ 0
N64_READn
Text GLabel 4350 4600 2    50   Input ~ 0
N64_WRITEn
Text GLabel 4350 4700 2    50   Input ~ 0
N64_AD12
Text GLabel 4350 4800 2    50   Input ~ 0
N64_AD13
Text GLabel 4350 4900 2    50   Input ~ 0
N64_AD14
Text GLabel 4350 5000 2    50   Input ~ 0
N64_AD15
Text GLabel 3450 3700 0    50   UnSpc ~ 0
N64_3V3
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD155
P 6250 3400
AR Path="/5F1CD155" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD155" Ref="RN4"  Part="1" 
F 0 "RN4" V 5833 3400 50  0000 C CNN
F 1 "33R" V 5924 3400 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 6525 3400 50  0001 C CNN
F 3 "~" H 6250 3400 50  0001 C CNN
	1    6250 3400
	0    1    1    0   
$EndComp
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD15B
P 6250 4100
AR Path="/5F1CD15B" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD15B" Ref="RN5"  Part="1" 
F 0 "RN5" V 5833 4100 50  0000 C CNN
F 1 "33R" V 5924 4100 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 6525 4100 50  0001 C CNN
F 3 "~" H 6250 4100 50  0001 C CNN
	1    6250 4100
	0    1    1    0   
$EndComp
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD161
P 6250 4800
AR Path="/5F1CD161" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD161" Ref="RN6"  Part="1" 
F 0 "RN6" V 5833 4800 50  0000 C CNN
F 1 "33R" V 5924 4800 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 6525 4800 50  0001 C CNN
F 3 "~" H 6250 4800 50  0001 C CNN
	1    6250 4800
	0    1    1    0   
$EndComp
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD167
P 8100 3400
AR Path="/5F1CD167" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD167" Ref="RN7"  Part="1" 
F 0 "RN7" V 7683 3400 50  0000 C CNN
F 1 "33R" V 7774 3400 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 8375 3400 50  0001 C CNN
F 3 "~" H 8100 3400 50  0001 C CNN
	1    8100 3400
	0    1    1    0   
$EndComp
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD16D
P 8100 4100
AR Path="/5F1CD16D" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD16D" Ref="RN8"  Part="1" 
F 0 "RN8" V 7683 4100 50  0000 C CNN
F 1 "33R" V 7774 4100 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 8375 4100 50  0001 C CNN
F 3 "~" H 8100 4100 50  0001 C CNN
	1    8100 4100
	0    1    1    0   
$EndComp
Text GLabel 6050 3300 0    50   Input ~ 0
N64_AD0
Text GLabel 6050 3200 0    50   Input ~ 0
N64_AD15
Text GLabel 6050 3400 0    50   Input ~ 0
N64_AD14
Text GLabel 6050 3500 0    50   Input ~ 0
N64_AD1
Text GLabel 6050 4000 0    50   Input ~ 0
N64_AD2
Text GLabel 6050 4200 0    50   Input ~ 0
N64_AD3
Text GLabel 6050 4600 0    50   Input ~ 0
N64_ALE_L
Text GLabel 6050 4900 0    50   Input ~ 0
N64_ALE_H
Text GLabel 6050 4700 0    50   Input ~ 0
N64_WRITEn
Text GLabel 6050 4800 0    50   Input ~ 0
N64_READn
Text GLabel 6050 3900 0    50   Input ~ 0
N64_AD13
Text GLabel 6050 4100 0    50   Input ~ 0
N64_AD12
Text GLabel 7900 3200 0    50   Input ~ 0
N64_AD11
Text GLabel 7900 3400 0    50   Input ~ 0
N64_AD10
Text GLabel 7900 3900 0    50   Input ~ 0
N64_AD9
Text GLabel 7900 4100 0    50   Input ~ 0
N64_AD8
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD183
P 8100 4800
AR Path="/5F1CD183" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD183" Ref="RN9"  Part="1" 
F 0 "RN9" V 7683 4800 50  0000 C CNN
F 1 "33R" V 7774 4800 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 8375 4800 50  0001 C CNN
F 3 "~" H 8100 4800 50  0001 C CNN
	1    8100 4800
	0    1    1    0   
$EndComp
Text GLabel 7900 4700 0    50   Input ~ 0
N64_COLD_RESETn
Text GLabel 7900 4600 0    50   Input ~ 0
N64_OS_EVENTn
NoConn ~ 7900 4800
NoConn ~ 7900 4900
NoConn ~ 8300 4800
NoConn ~ 8300 4900
Text GLabel 7900 3300 0    50   Input ~ 0
N64_AD4
Text GLabel 7900 3500 0    50   Input ~ 0
N64_AD5
Text GLabel 7900 4000 0    50   Input ~ 0
N64_AD6
Text GLabel 7900 4200 0    50   Input ~ 0
N64_AD7
Text GLabel 6450 3300 2    50   Input ~ 0
N64_AD0_IC
Text GLabel 6450 3200 2    50   Input ~ 0
N64_AD15_IC
Text GLabel 6450 3400 2    50   Input ~ 0
N64_AD14_IC
Text GLabel 6450 3500 2    50   Input ~ 0
N64_AD1_IC
Text GLabel 6450 4000 2    50   Input ~ 0
N64_AD2_IC
Text GLabel 6450 4200 2    50   Input ~ 0
N64_AD3_IC
Text GLabel 6450 4600 2    50   Input ~ 0
N64_ALE_L_IC
Text GLabel 6450 4900 2    50   Input ~ 0
N64_ALE_H_IC
Text GLabel 6450 4700 2    50   Input ~ 0
N64_WRITEn_IC
Text GLabel 6450 4800 2    50   Input ~ 0
N64_READn_IC
Text GLabel 6450 3900 2    50   Input ~ 0
N64_AD13_IC
Text GLabel 6450 4100 2    50   Input ~ 0
N64_AD12_IC
Text GLabel 8300 3200 2    50   Input ~ 0
N64_AD11_IC
Text GLabel 8300 3400 2    50   Input ~ 0
N64_AD10_IC
Text GLabel 8300 3900 2    50   Input ~ 0
N64_AD9_IC
Text GLabel 8300 4100 2    50   Input ~ 0
N64_AD8_IC
Text GLabel 8300 4700 2    50   Input ~ 0
N64_COLD_RESETn_IC
Text GLabel 8300 4600 2    50   Input ~ 0
N64_OS_EVENTn_IC
Text GLabel 8300 3300 2    50   Input ~ 0
N64_AD4_IC
Text GLabel 8300 3500 2    50   Input ~ 0
N64_AD5_IC
Text GLabel 8300 4000 2    50   Input ~ 0
N64_AD6_IC
Text GLabel 8300 4200 2    50   Input ~ 0
N64_AD7_IC
$EndSCHEMATC
