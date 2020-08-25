EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 5 7
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
L ng_n64:N64_Cartridge_Bus J3
U 1 1 5F443545
P 3000 4050
F 0 "J3" H 2450 5800 60  0000 L CNN
F 1 "N64_Cartridge_Bus" H 2450 2300 60  0000 L CNN
F 2 "ng_n64:N64_Cartridge_Edge" H 3600 550 60  0001 C CNN
F 3 "" H 3700 1700 60  0000 C CNN
	1    3000 4050
	1    0    0    -1  
$EndComp
Wire Wire Line
	2300 2750 2200 2750
Wire Wire Line
	2200 2750 2200 2650
Wire Wire Line
	2200 2450 2300 2450
Wire Wire Line
	2300 2550 2200 2550
Connection ~ 2200 2550
Wire Wire Line
	2200 2550 2200 2450
Wire Wire Line
	2300 2650 2200 2650
Connection ~ 2200 2650
Wire Wire Line
	2200 2650 2200 2550
Wire Wire Line
	2200 2450 2100 2450
Connection ~ 2200 2450
Text GLabel 2100 2450 0    50   UnSpc ~ 0
N64_3V3
Wire Wire Line
	2300 4550 2200 4550
Wire Wire Line
	2200 4550 2200 4650
Wire Wire Line
	2300 5650 2200 5650
Connection ~ 2200 5650
Wire Wire Line
	2200 5650 2200 5750
Wire Wire Line
	2300 5550 2200 5550
Wire Wire Line
	2200 5550 2200 5650
Wire Wire Line
	2300 5450 2200 5450
Connection ~ 2200 5450
Wire Wire Line
	2200 5450 2200 5550
Wire Wire Line
	2300 5350 2200 5350
Connection ~ 2200 5350
Wire Wire Line
	2200 5350 2200 5450
Wire Wire Line
	2300 5250 2200 5250
Connection ~ 2200 5250
Wire Wire Line
	2200 5250 2200 5350
Wire Wire Line
	2300 5150 2200 5150
Connection ~ 2200 5150
Wire Wire Line
	2200 5150 2200 5250
Wire Wire Line
	2300 5050 2200 5050
Connection ~ 2200 5050
Wire Wire Line
	2200 5050 2200 5150
Wire Wire Line
	2300 4950 2200 4950
Connection ~ 2200 4950
Wire Wire Line
	2200 4950 2200 5050
Wire Wire Line
	2300 4850 2200 4850
Connection ~ 2200 4850
Wire Wire Line
	2200 4850 2200 4950
Wire Wire Line
	2300 4750 2200 4750
Connection ~ 2200 4750
Wire Wire Line
	2200 4750 2200 4850
Wire Wire Line
	2300 4650 2200 4650
Connection ~ 2200 4650
Wire Wire Line
	2200 4650 2200 4750
Wire Wire Line
	3700 2450 3800 2450
Wire Wire Line
	3700 2550 3800 2550
Wire Wire Line
	3700 2650 3800 2650
Wire Wire Line
	3700 2750 3800 2750
Wire Wire Line
	3700 2850 3800 2850
Wire Wire Line
	3700 2950 3800 2950
Wire Wire Line
	3700 3050 3800 3050
Wire Wire Line
	3700 3150 3800 3150
Wire Wire Line
	3700 3250 3800 3250
Wire Wire Line
	3700 3350 3800 3350
Wire Wire Line
	3700 3450 3800 3450
Wire Wire Line
	3700 3550 3800 3550
Wire Wire Line
	3700 3650 3800 3650
Wire Wire Line
	3700 3750 3800 3750
Wire Wire Line
	3700 3850 3800 3850
Wire Wire Line
	3700 3950 3800 3950
Wire Wire Line
	3700 4150 3800 4150
Wire Wire Line
	3700 4250 3800 4250
Wire Wire Line
	3700 4350 3800 4350
Wire Wire Line
	3700 4450 3800 4450
Wire Wire Line
	3700 4750 3800 4750
Wire Wire Line
	3700 4950 3800 4950
Wire Wire Line
	3700 5050 3800 5050
Wire Wire Line
	3700 5250 3800 5250
Wire Wire Line
	3700 5350 3800 5350
Connection ~ 2200 5550
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD155
P 7100 2100
AR Path="/5F1CD155" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD155" Ref="RN4"  Part="1" 
AR Path="/5F43B1FD/5F1CD155" Ref="RN4"  Part="1" 
F 0 "RN4" V 6683 2100 50  0000 C CNN
F 1 "33R, 1%" V 6774 2100 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 7375 2100 50  0001 C CNN
F 3 "~" H 7100 2100 50  0001 C CNN
F 4 "YC164-FR-0733RL" H 7100 2100 50  0001 C CNN "MPN"
	1    7100 2100
	0    1    1    0   
$EndComp
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD15B
P 7100 2800
AR Path="/5F1CD15B" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD15B" Ref="RN6"  Part="1" 
AR Path="/5F43B1FD/5F1CD15B" Ref="RN6"  Part="1" 
F 0 "RN6" V 6683 2800 50  0000 C CNN
F 1 "33R, 1%" V 6774 2800 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 7375 2800 50  0001 C CNN
F 3 "~" H 7100 2800 50  0001 C CNN
F 4 "YC164-FR-0733RL" H 7100 2800 50  0001 C CNN "MPN"
	1    7100 2800
	0    1    1    0   
$EndComp
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD161
P 7100 3500
AR Path="/5F1CD161" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD161" Ref="RN8"  Part="1" 
AR Path="/5F43B1FD/5F1CD161" Ref="RN8"  Part="1" 
F 0 "RN8" V 6683 3500 50  0000 C CNN
F 1 "33R, 1%" V 6774 3500 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 7375 3500 50  0001 C CNN
F 3 "~" H 7100 3500 50  0001 C CNN
F 4 "YC164-FR-0733RL" H 7100 3500 50  0001 C CNN "MPN"
	1    7100 3500
	0    1    1    0   
$EndComp
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD167
P 8950 2100
AR Path="/5F1CD167" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD167" Ref="RN5"  Part="1" 
AR Path="/5F43B1FD/5F1CD167" Ref="RN5"  Part="1" 
F 0 "RN5" V 8533 2100 50  0000 C CNN
F 1 "33R, 1%" V 8624 2100 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 9225 2100 50  0001 C CNN
F 3 "~" H 8950 2100 50  0001 C CNN
F 4 "YC164-FR-0733RL" H 8950 2100 50  0001 C CNN "MPN"
	1    8950 2100
	0    1    1    0   
$EndComp
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD16D
P 8950 2800
AR Path="/5F1CD16D" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD16D" Ref="RN7"  Part="1" 
AR Path="/5F43B1FD/5F1CD16D" Ref="RN7"  Part="1" 
F 0 "RN7" V 8533 2800 50  0000 C CNN
F 1 "33R, 1%" V 8624 2800 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 9225 2800 50  0001 C CNN
F 3 "~" H 8950 2800 50  0001 C CNN
F 4 "YC164-FR-0733RL" H 8950 2800 50  0001 C CNN "MPN"
	1    8950 2800
	0    1    1    0   
$EndComp
$Comp
L Device:R_Pack04 RN?
U 1 1 5F1CD183
P 8950 3500
AR Path="/5F1CD183" Ref="RN?"  Part="1" 
AR Path="/5F133F50/5F1CD183" Ref="RN9"  Part="1" 
AR Path="/5F43B1FD/5F1CD183" Ref="RN9"  Part="1" 
F 0 "RN9" V 8533 3500 50  0000 C CNN
F 1 "33R, 1%" V 8624 3500 50  0000 C CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 9225 3500 50  0001 C CNN
F 3 "~" H 8950 3500 50  0001 C CNN
F 4 "YC164-FR-0733RL" H 8950 3500 50  0001 C CNN "MPN"
	1    8950 3500
	0    1    1    0   
$EndComp
Text GLabel 7300 2000 2    50   Input ~ 0
N64_AD0
Text GLabel 7300 1900 2    50   Input ~ 0
N64_AD15
Text GLabel 7300 2100 2    50   Input ~ 0
N64_AD14
Text GLabel 7300 2200 2    50   Input ~ 0
N64_AD1
Text GLabel 7300 2700 2    50   Input ~ 0
N64_AD2
Text GLabel 7300 2900 2    50   Input ~ 0
N64_AD3
Text GLabel 7300 3300 2    50   Input ~ 0
N64_ALE_L
Text GLabel 7300 3600 2    50   Input ~ 0
N64_ALE_H
Text GLabel 7300 3400 2    50   Input ~ 0
N64_WRITE#
Text GLabel 7300 3500 2    50   Input ~ 0
N64_READ#
Text GLabel 7300 2600 2    50   Input ~ 0
N64_AD13
Text GLabel 7300 2800 2    50   Input ~ 0
N64_AD12
Text GLabel 9150 1900 2    50   Input ~ 0
N64_AD11
Text GLabel 9150 2100 2    50   Input ~ 0
N64_AD10
Text GLabel 9150 2600 2    50   Input ~ 0
N64_AD9
Text GLabel 9150 2800 2    50   Input ~ 0
N64_AD8
Text GLabel 9150 3400 2    50   Input ~ 0
N64_COLD_RESET#
Text GLabel 9150 3300 2    50   Input ~ 0
N64_OS_EVENT#
Text GLabel 9150 2000 2    50   Input ~ 0
N64_AD4
Text GLabel 9150 2200 2    50   Input ~ 0
N64_AD5
Text GLabel 9150 2700 2    50   Input ~ 0
N64_AD6
Text GLabel 9150 2900 2    50   Input ~ 0
N64_AD7
NoConn ~ 8750 3600
NoConn ~ 8750 3500
NoConn ~ 9150 3500
NoConn ~ 9150 3600
NoConn ~ 3700 5550
NoConn ~ 3700 5650
Text Label 3800 2450 0    50   ~ 0
xN64_AD0
Text Label 3800 2550 0    50   ~ 0
xN64_AD1
Text Label 3800 2650 0    50   ~ 0
xN64_AD2
Text Label 3800 2750 0    50   ~ 0
xN64_AD3
Text Label 3800 2850 0    50   ~ 0
xN64_AD4
Text Label 3800 2950 0    50   ~ 0
xN64_AD5
Text Label 3800 3050 0    50   ~ 0
xN64_AD6
Text Label 3800 3150 0    50   ~ 0
xN64_AD7
Text Label 3800 3250 0    50   ~ 0
xN64_AD8
Text Label 3800 3350 0    50   ~ 0
xN64_AD9
Text Label 3800 3450 0    50   ~ 0
xN64_AD10
Text Label 3800 3550 0    50   ~ 0
xN64_AD11
Text Label 3800 3650 0    50   ~ 0
xN64_AD12
Text Label 3800 3750 0    50   ~ 0
xN64_AD13
Text Label 3800 3850 0    50   ~ 0
xN64_AD14
Text Label 3800 3950 0    50   ~ 0
xN64_AD15
Text Label 3800 4150 0    50   ~ 0
xN64_ALE_L
Text Label 3800 4250 0    50   ~ 0
xN64_ALE_H
Text Label 3800 4350 0    50   ~ 0
xN64_READ#
Text Label 3800 4450 0    50   ~ 0
xN64_WRITE#
Text Label 3800 4750 0    50   ~ 0
N64_S_CLK
Text Label 3800 4950 0    50   ~ 0
xN64_COLD_RESET#
Text Label 3800 5050 0    50   ~ 0
xN64_OS_EVENT#
Text Label 3800 5250 0    50   ~ 0
N64_CIC_DATA1
Text Label 3800 5350 0    50   ~ 0
N64_CIC_DATA2
NoConn ~ 3700 4650
NoConn ~ 2300 2950
NoConn ~ 2300 3050
Wire Wire Line
	6900 1900 6800 1900
Wire Wire Line
	6900 2000 6800 2000
Wire Wire Line
	6900 2100 6800 2100
Wire Wire Line
	6900 2200 6800 2200
Wire Wire Line
	6900 2600 6800 2600
Wire Wire Line
	6900 2700 6800 2700
Wire Wire Line
	6900 2800 6800 2800
Wire Wire Line
	6900 2900 6800 2900
Wire Wire Line
	6900 3300 6800 3300
Wire Wire Line
	6900 3400 6800 3400
Wire Wire Line
	6900 3500 6800 3500
Wire Wire Line
	6900 3600 6800 3600
Text Label 6800 1900 2    50   ~ 0
xN64_AD15
Text Label 6800 2000 2    50   ~ 0
xN64_AD0
Text Label 6800 2100 2    50   ~ 0
xN64_AD14
Text Label 6800 2200 2    50   ~ 0
xN64_AD1
Text Label 6800 2600 2    50   ~ 0
xN64_AD13
Text Label 6800 2700 2    50   ~ 0
xN64_AD2
Text Label 6800 2800 2    50   ~ 0
xN64_AD12
Text Label 6800 2900 2    50   ~ 0
xN64_AD3
Text Label 8650 1900 2    50   ~ 0
xN64_AD11
Text Label 8650 2000 2    50   ~ 0
xN64_AD4
Text Label 8650 2100 2    50   ~ 0
xN64_AD10
Text Label 8650 2200 2    50   ~ 0
xN64_AD5
Wire Wire Line
	8750 1900 8650 1900
Wire Wire Line
	8750 2000 8650 2000
Wire Wire Line
	8750 2100 8650 2100
Wire Wire Line
	8750 2200 8650 2200
Wire Wire Line
	8750 2600 8650 2600
Wire Wire Line
	8750 2700 8650 2700
Wire Wire Line
	8750 2800 8650 2800
Wire Wire Line
	8750 2900 8650 2900
Wire Wire Line
	8750 3300 8650 3300
Wire Wire Line
	8750 3400 8650 3400
Text Label 8650 2700 2    50   ~ 0
xN64_AD6
Text Label 8650 2600 2    50   ~ 0
xN64_AD9
Text Label 8650 2900 2    50   ~ 0
xN64_AD7
Text Label 8650 2800 2    50   ~ 0
xN64_AD8
Text Label 8650 3300 2    50   ~ 0
xN64_OS_EVENT#
Text Label 8650 3400 2    50   ~ 0
xN64_COLD_RESET#
Text Label 6800 3300 2    50   ~ 0
xN64_ALE_L
Text Label 6800 3400 2    50   ~ 0
xN64_WRITE#
Text Label 6800 3500 2    50   ~ 0
xN64_READ#
Text Label 6800 3600 2    50   ~ 0
xN64_ALE_H
$Comp
L MCU_Microchip_ATtiny:ATtiny25-20SU U4
U 1 1 5F5E9784
P 7450 4950
F 0 "U4" H 6921 4996 50  0000 R CNN
F 1 "ATtiny25-20SU" H 6921 4905 50  0000 R CNN
F 2 "Package_SO:SOIJ-8_5.3x5.3mm_P1.27mm" H 7450 4950 50  0001 C CIN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/atmel-2586-avr-8-bit-microcontroller-attiny25-attiny45-attiny85_datasheet.pdf" H 7450 4950 50  0001 C CNN
	1    7450 4950
	-1   0    0    -1  
$EndComp
Wire Wire Line
	7450 4350 7450 4250
Wire Wire Line
	7450 4250 7350 4250
Wire Wire Line
	7450 5550 7450 5650
$Comp
L ng_power:GND #PWR013
U 1 1 5F5EFD38
P 2200 5750
F 0 "#PWR013" H 2200 5500 50  0001 C CNN
F 1 "GND" H 2203 5624 50  0000 C CNN
F 2 "" H 2100 5400 50  0001 C CNN
F 3 "" H 2200 5750 50  0001 C CNN
	1    2200 5750
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR015
U 1 1 5F5F0698
P 7450 5650
F 0 "#PWR015" H 7450 5400 50  0001 C CNN
F 1 "GND" H 7453 5524 50  0000 C CNN
F 2 "" H 7350 5300 50  0001 C CNN
F 3 "" H 7450 5650 50  0001 C CNN
	1    7450 5650
	-1   0    0    -1  
$EndComp
Text GLabel 7350 4250 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	6850 4650 6750 4650
Wire Wire Line
	6850 4750 6100 4750
Wire Wire Line
	6850 4850 6100 4850
Wire Wire Line
	6850 4950 6100 4950
Wire Wire Line
	6850 5150 6100 5150
Wire Wire Line
	6750 4650 6750 5250
$Comp
L ng_power:GND #PWR014
U 1 1 5F607950
P 6750 5650
F 0 "#PWR014" H 6750 5400 50  0001 C CNN
F 1 "GND" H 6753 5524 50  0000 C CNN
F 2 "" H 6650 5300 50  0001 C CNN
F 3 "" H 6750 5650 50  0001 C CNN
	1    6750 5650
	-1   0    0    -1  
$EndComp
Text Label 6100 4750 2    50   ~ 0
N64_CIC_DATA2
Text Label 6100 4950 2    50   ~ 0
N64_S_CLK
Text Label 6100 4850 2    50   ~ 0
N64_CIC_DATA1
Text GLabel 6100 5150 0    50   Input ~ 0
N64_COLD_RESET#
Text Label 6650 5150 2    50   ~ 0
CIC_RESET#
Wire Wire Line
	6750 4650 6650 4650
Connection ~ 6750 4650
Text Label 6650 4650 2    50   ~ 0
CIC_MOSI
Text Label 6650 4750 2    50   ~ 0
CIC_MISO
$Comp
L Device:R R6
U 1 1 5F61BC6C
P 6750 5400
F 0 "R6" H 6680 5354 50  0000 R CNN
F 1 "10k" H 6680 5445 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 6680 5400 50  0001 C CNN
F 3 "~" H 6750 5400 50  0001 C CNN
	1    6750 5400
	1    0    0    1   
$EndComp
Wire Wire Line
	6750 5650 6750 5550
Text Label 6650 4850 2    50   ~ 0
CIC_SCK
NoConn ~ 6850 5050
$Comp
L Connector_Generic:Conn_01x05 J4
U 1 1 5F631439
P 9700 4950
F 0 "J4" H 9780 4992 50  0000 L CNN
F 1 "Conn_01x05" H 9780 4901 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical" H 9700 4950 50  0001 C CNN
F 3 "~" H 9700 4950 50  0001 C CNN
	1    9700 4950
	1    0    0    -1  
$EndComp
Wire Wire Line
	9500 4750 9400 4750
Wire Wire Line
	9400 4750 9400 5250
$Comp
L ng_power:GND #PWR016
U 1 1 5F634AA1
P 9400 5250
F 0 "#PWR016" H 9400 5000 50  0001 C CNN
F 1 "GND" H 9403 5124 50  0000 C CNN
F 2 "" H 9300 4900 50  0001 C CNN
F 3 "" H 9400 5250 50  0001 C CNN
	1    9400 5250
	1    0    0    -1  
$EndComp
Wire Wire Line
	9500 4850 9300 4850
Wire Wire Line
	9500 4950 9300 4950
Wire Wire Line
	9500 5050 9300 5050
Wire Wire Line
	9500 5150 9300 5150
Text Label 9300 4850 2    50   ~ 0
CIC_SCK
Text Label 9300 4950 2    50   ~ 0
CIC_MISO
Text Label 9300 5050 2    50   ~ 0
CIC_MOSI
Text Label 9300 5150 2    50   ~ 0
CIC_RESET#
$EndSCHEMATC
