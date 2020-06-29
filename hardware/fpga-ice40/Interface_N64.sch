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
Connection ~ 3900 4800
NoConn ~ 3300 3900
NoConn ~ 3300 4800
Wire Wire Line
	3100 3600 3300 3600
Wire Wire Line
	3100 4300 3300 4300
Wire Wire Line
	3100 4400 3300 4400
Wire Wire Line
	3100 4500 3300 4500
Wire Wire Line
	3100 4600 3300 4600
Wire Wire Line
	3100 4700 3300 4700
Wire Wire Line
	3100 4900 3300 4900
Wire Wire Line
	3100 5000 3300 5000
Wire Wire Line
	3100 5100 3300 5100
Wire Wire Line
	3100 5200 3300 5200
Wire Wire Line
	3100 5300 3300 5300
Wire Wire Line
	3800 3900 3900 3900
Wire Wire Line
	3800 3600 4000 3600
Wire Wire Line
	3800 4300 4000 4300
Wire Wire Line
	3800 4400 4000 4400
Wire Wire Line
	3800 4500 4000 4500
Wire Wire Line
	3800 4600 4000 4600
Wire Wire Line
	3800 4700 4000 4700
Wire Wire Line
	3800 4900 4000 4900
Wire Wire Line
	3800 5000 4000 5000
Wire Wire Line
	3800 5100 4000 5100
Wire Wire Line
	3800 5200 4000 5200
Wire Wire Line
	3800 5300 4000 5300
Wire Wire Line
	3900 3900 3900 4000
Wire Wire Line
	3900 4800 3800 4800
Wire Wire Line
	3900 4800 3900 5400
$Comp
L Connector_Generic:Conn_02x20_Odd_Even J?
U 1 1 5F1CD119
P 3500 4300
AR Path="/5F1CD119" Ref="J?"  Part="1" 
AR Path="/5F133F50/5F1CD119" Ref="J4"  Part="1" 
F 0 "J4" H 3550 5350 50  0000 C CNN
F 1 "Conn_02x20_Odd_Even" H 3550 5325 50  0001 C CNN
F 2 "local_conn:PinHeader_2x20_P2.54mm_Horizontal" H 3500 4300 50  0001 C CNN
F 3 "~" H 3500 4300 50  0001 C CNN
	1    3500 4300
	1    0    0    -1  
$EndComp
Wire Wire Line
	3800 4000 3900 4000
Connection ~ 3900 4000
Wire Wire Line
	3900 4000 3900 4100
Wire Wire Line
	3800 4100 3900 4100
Connection ~ 3900 4100
Wire Wire Line
	3900 4100 3900 4200
Wire Wire Line
	3800 4200 3900 4200
Connection ~ 3900 4200
Wire Wire Line
	3900 4200 3900 4800
Wire Wire Line
	3300 4200 3200 4200
Wire Wire Line
	3200 4200 3200 4100
Wire Wire Line
	3200 4000 3300 4000
Wire Wire Line
	3300 4100 3200 4100
Connection ~ 3200 4100
Wire Wire Line
	3200 4100 3200 4000
Wire Wire Line
	3200 4000 3100 4000
Connection ~ 3200 4000
NoConn ~ 3300 3400
NoConn ~ 3300 3500
NoConn ~ 3300 3700
NoConn ~ 3300 3800
NoConn ~ 3800 3400
NoConn ~ 3800 3500
NoConn ~ 3800 3700
NoConn ~ 3800 3800
Text GLabel 3100 3600 0    50   Input ~ 0
N64_COLD_RESETn
Text GLabel 4000 3600 2    50   Input ~ 0
N64_OS_EVENTn
$Comp
L ng_power:GND #PWR0126
U 1 1 5F1CD13A
P 3900 5400
F 0 "#PWR0126" H 3900 5150 50  0001 C CNN
F 1 "GND" H 3903 5274 50  0000 C CNN
F 2 "" H 3800 5050 50  0001 C CNN
F 3 "" H 3900 5400 50  0001 C CNN
	1    3900 5400
	1    0    0    -1  
$EndComp
Text GLabel 3100 4300 0    50   Input ~ 0
N64_AD7
Text GLabel 3100 4400 0    50   Input ~ 0
N64_AD6
Text GLabel 3100 4500 0    50   Input ~ 0
N64_AD5
Text GLabel 3100 4600 0    50   Input ~ 0
N64_AD4
Text GLabel 3100 4700 0    50   Input ~ 0
N64_ALE_H
Text GLabel 3100 4900 0    50   Input ~ 0
N64_ALE_L
Text GLabel 3100 5000 0    50   Input ~ 0
N64_AD3
Text GLabel 3100 5100 0    50   Input ~ 0
N64_AD2
Text GLabel 3100 5200 0    50   Input ~ 0
N64_AD1
Text GLabel 3100 5300 0    50   Input ~ 0
N64_AD0
Text GLabel 4000 4300 2    50   Input ~ 0
N64_AD8
Text GLabel 4000 4400 2    50   Input ~ 0
N64_AD9
Text GLabel 4000 4500 2    50   Input ~ 0
N64_AD10
Text GLabel 4000 4600 2    50   Input ~ 0
N64_AD11
Text GLabel 4000 4700 2    50   Input ~ 0
N64_READn
Text GLabel 4000 4900 2    50   Input ~ 0
N64_WRITEn
Text GLabel 4000 5000 2    50   Input ~ 0
N64_AD12
Text GLabel 4000 5100 2    50   Input ~ 0
N64_AD13
Text GLabel 4000 5200 2    50   Input ~ 0
N64_AD14
Text GLabel 4000 5300 2    50   Input ~ 0
N64_AD15
Text GLabel 3100 4000 0    50   UnSpc ~ 0
N64_3V3
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD155
P 5900 3700
AR Path="/5F1CD155" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD155" Ref="RN4"  Part="1" 
F 0 "RN4" V 5483 3700 50  0000 C CNN
F 1 "33R" V 5574 3700 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 6175 3700 50  0001 C CNN
F 3 "~" H 5900 3700 50  0001 C CNN
	1    5900 3700
	0    1    1    0   
$EndComp
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD15B
P 5900 4400
AR Path="/5F1CD15B" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD15B" Ref="RN5"  Part="1" 
F 0 "RN5" V 5483 4400 50  0000 C CNN
F 1 "33R" V 5574 4400 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 6175 4400 50  0001 C CNN
F 3 "~" H 5900 4400 50  0001 C CNN
	1    5900 4400
	0    1    1    0   
$EndComp
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD161
P 5900 5100
AR Path="/5F1CD161" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD161" Ref="RN6"  Part="1" 
F 0 "RN6" V 5483 5100 50  0000 C CNN
F 1 "33R" V 5574 5100 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 6175 5100 50  0001 C CNN
F 3 "~" H 5900 5100 50  0001 C CNN
	1    5900 5100
	0    1    1    0   
$EndComp
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD167
P 7750 3700
AR Path="/5F1CD167" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD167" Ref="RN7"  Part="1" 
F 0 "RN7" V 7333 3700 50  0000 C CNN
F 1 "33R" V 7424 3700 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 8025 3700 50  0001 C CNN
F 3 "~" H 7750 3700 50  0001 C CNN
	1    7750 3700
	0    1    1    0   
$EndComp
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD16D
P 7750 4400
AR Path="/5F1CD16D" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD16D" Ref="RN8"  Part="1" 
F 0 "RN8" V 7333 4400 50  0000 C CNN
F 1 "33R" V 7424 4400 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 8025 4400 50  0001 C CNN
F 3 "~" H 7750 4400 50  0001 C CNN
	1    7750 4400
	0    1    1    0   
$EndComp
Text GLabel 5700 3600 0    50   Input ~ 0
N64_AD0
Text GLabel 5700 3500 0    50   Input ~ 0
N64_AD15
Text GLabel 5700 3700 0    50   Input ~ 0
N64_AD14
Text GLabel 5700 3800 0    50   Input ~ 0
N64_AD1
Text GLabel 5700 4300 0    50   Input ~ 0
N64_AD2
Text GLabel 5700 4500 0    50   Input ~ 0
N64_AD3
Text GLabel 5700 4900 0    50   Input ~ 0
N64_ALE_L
Text GLabel 5700 5200 0    50   Input ~ 0
N64_ALE_H
Text GLabel 5700 5000 0    50   Input ~ 0
N64_WRITEn
Text GLabel 5700 5100 0    50   Input ~ 0
N64_READn
Text GLabel 5700 4200 0    50   Input ~ 0
N64_AD13
Text GLabel 5700 4400 0    50   Input ~ 0
N64_AD12
Text GLabel 7550 3500 0    50   Input ~ 0
N64_AD11
Text GLabel 7550 3700 0    50   Input ~ 0
N64_AD10
Text GLabel 7550 4200 0    50   Input ~ 0
N64_AD9
Text GLabel 7550 4400 0    50   Input ~ 0
N64_AD8
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD183
P 7750 5100
AR Path="/5F1CD183" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD183" Ref="RN9"  Part="1" 
F 0 "RN9" V 7333 5100 50  0000 C CNN
F 1 "33R" V 7424 5100 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 8025 5100 50  0001 C CNN
F 3 "~" H 7750 5100 50  0001 C CNN
	1    7750 5100
	0    1    1    0   
$EndComp
Text GLabel 7550 5000 0    50   Input ~ 0
N64_COLD_RESETn
Text GLabel 7550 4900 0    50   Input ~ 0
N64_OS_EVENTn
NoConn ~ 7550 5100
NoConn ~ 7550 5200
NoConn ~ 7950 5100
NoConn ~ 7950 5200
Text GLabel 7550 3600 0    50   Input ~ 0
N64_AD4
Text GLabel 7550 3800 0    50   Input ~ 0
N64_AD5
Text GLabel 7550 4300 0    50   Input ~ 0
N64_AD6
Text GLabel 7550 4500 0    50   Input ~ 0
N64_AD7
Text GLabel 6100 3600 2    50   Input ~ 0
N64_AD0_IC
Text GLabel 6100 3500 2    50   Input ~ 0
N64_AD15_IC
Text GLabel 6100 3700 2    50   Input ~ 0
N64_AD14_IC
Text GLabel 6100 3800 2    50   Input ~ 0
N64_AD1_IC
Text GLabel 6100 4300 2    50   Input ~ 0
N64_AD2_IC
Text GLabel 6100 4500 2    50   Input ~ 0
N64_AD3_IC
Text GLabel 6100 4900 2    50   Input ~ 0
N64_ALE_L_IC
Text GLabel 6100 5200 2    50   Input ~ 0
N64_ALE_H_IC
Text GLabel 6100 5000 2    50   Input ~ 0
N64_WRITEn_IC
Text GLabel 6100 5100 2    50   Input ~ 0
N64_READn_IC
Text GLabel 6100 4200 2    50   Input ~ 0
N64_AD13_IC
Text GLabel 6100 4400 2    50   Input ~ 0
N64_AD12_IC
Text GLabel 7950 3500 2    50   Input ~ 0
N64_AD11_IC
Text GLabel 7950 3700 2    50   Input ~ 0
N64_AD10_IC
Text GLabel 7950 4200 2    50   Input ~ 0
N64_AD9_IC
Text GLabel 7950 4400 2    50   Input ~ 0
N64_AD8_IC
Text GLabel 7950 5000 2    50   Input ~ 0
N64_COLD_RESETn_IC
Text GLabel 7950 4900 2    50   Input ~ 0
N64_OS_EVENTn_IC
Text GLabel 7950 3600 2    50   Input ~ 0
N64_AD4_IC
Text GLabel 7950 3800 2    50   Input ~ 0
N64_AD5_IC
Text GLabel 7950 4300 2    50   Input ~ 0
N64_AD6_IC
Text GLabel 7950 4500 2    50   Input ~ 0
N64_AD7_IC
$EndSCHEMATC
