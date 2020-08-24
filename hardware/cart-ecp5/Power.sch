EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 6 6
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
L Device:C C?
U 1 1 5F820F1C
P 2450 3050
AR Path="/5F820F1C" Ref="C?"  Part="1" 
AR Path="/5F7F68FE/5F820F1C" Ref="C4"  Part="1" 
AR Path="/5F483803/5F820F1C" Ref="C?"  Part="1" 
F 0 "C?" H 2500 3150 50  0000 L CNN
F 1 "10u" H 2500 2950 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 2488 2900 50  0001 C CNN
F 3 "~" H 2450 3050 50  0001 C CNN
F 4 "" H 2450 3050 50  0001 C CNN "MPN"
	1    2450 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	2450 3200 2450 3300
Text GLabel 1650 2800 0    50   UnSpc ~ 0
USB_3V3
Text GLabel 1650 2700 0    50   UnSpc ~ 0
N64_3V3
Text GLabel 4950 2700 2    50   UnSpc ~ 0
MUX_3V3
$Comp
L Device:C C?
U 1 1 5F820F39
P 1850 3050
AR Path="/5F820F39" Ref="C?"  Part="1" 
AR Path="/5F7F68FE/5F820F39" Ref="C3"  Part="1" 
AR Path="/5F483803/5F820F39" Ref="C?"  Part="1" 
F 0 "C?" H 1900 3150 50  0000 L CNN
F 1 "10u" H 1900 2950 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 1888 2900 50  0001 C CNN
F 3 "~" H 1850 3050 50  0001 C CNN
F 4 "" H 1850 3050 50  0001 C CNN "MPN"
	1    1850 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	1850 3200 1850 3300
$Comp
L ng_pmic:TPS2111A U?
U 1 1 5F0BC865
P 4200 3150
F 0 "U?" H 3950 3850 50  0000 L CNN
F 1 "TPS2111A" H 3950 3750 50  0000 L CNN
F 2 "Package_SO:TSSOP-8_4.4x3mm_P0.65mm" H 4200 2550 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/tps2111a.pdf" H 4450 3100 50  0001 C CNN
	1    4200 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	3750 3100 3850 3100
NoConn ~ 3850 3000
Wire Wire Line
	3850 3600 3750 3600
$Comp
L Device:R R?
U 1 1 5F0C9498
P 3450 3650
F 0 "R?" H 3520 3696 50  0000 L CNN
F 1 "R" H 3520 3605 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 3380 3650 50  0001 C CNN
F 3 "~" H 3450 3650 50  0001 C CNN
	1    3450 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	3450 3500 3450 3400
Wire Wire Line
	3450 3400 3850 3400
Wire Wire Line
	3450 3800 3450 3900
Wire Wire Line
	3450 3900 3750 3900
Wire Wire Line
	3750 3600 3750 3900
Wire Wire Line
	3750 3600 3750 3100
Connection ~ 3750 3600
$Comp
L Device:R R?
U 1 1 5F0CC46B
P 3150 3650
F 0 "R?" H 3220 3696 50  0000 L CNN
F 1 "R" H 3220 3605 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 3080 3650 50  0001 C CNN
F 3 "~" H 3150 3650 50  0001 C CNN
	1    3150 3650
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 5F0CCC27
P 3150 3050
F 0 "R?" H 3220 3096 50  0000 L CNN
F 1 "R" H 3220 3005 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 3080 3050 50  0001 C CNN
F 3 "~" H 3150 3050 50  0001 C CNN
	1    3150 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	3850 2800 3150 2800
Wire Wire Line
	3150 2900 3150 2800
Connection ~ 3150 2800
Wire Wire Line
	3850 3300 3150 3300
Wire Wire Line
	3150 3200 3150 3300
Wire Wire Line
	3150 3300 3150 3500
Connection ~ 3150 3300
Wire Wire Line
	3150 3800 3150 3900
Wire Wire Line
	3150 3900 3450 3900
Connection ~ 3450 3900
$Comp
L Device:C C?
U 1 1 5F0D7A04
P 2750 3050
AR Path="/5F0D7A04" Ref="C?"  Part="1" 
AR Path="/5F7F68FE/5F0D7A04" Ref="C53"  Part="1" 
AR Path="/5F483803/5F0D7A04" Ref="C?"  Part="1" 
F 0 "C?" H 2800 3150 50  0000 L CNN
F 1 "100n" H 2800 2950 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 2788 2900 50  0001 C CNN
F 3 "~" H 2750 3050 50  0001 C CNN
F 4 "" H 2750 3050 50  0001 C CNN "MPN"
	1    2750 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	2750 3200 2750 3300
$Comp
L Device:C C?
U 1 1 5F0D7A1A
P 2150 3050
AR Path="/5F0D7A1A" Ref="C?"  Part="1" 
AR Path="/5F7F68FE/5F0D7A1A" Ref="C52"  Part="1" 
AR Path="/5F483803/5F0D7A1A" Ref="C?"  Part="1" 
F 0 "C?" H 2200 3150 50  0000 L CNN
F 1 "100n" H 2200 2950 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 2188 2900 50  0001 C CNN
F 3 "~" H 2150 3050 50  0001 C CNN
F 4 "" H 2150 3050 50  0001 C CNN "MPN"
	1    2150 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	2150 3200 2150 3300
Wire Wire Line
	1650 2700 1850 2700
$Comp
L Device:C C?
U 1 1 5F0EC68D
P 4750 2950
AR Path="/5F0EC68D" Ref="C?"  Part="1" 
AR Path="/5F7F68FE/5F0EC68D" Ref="C51"  Part="1" 
AR Path="/5F483803/5F0EC68D" Ref="C?"  Part="1" 
F 0 "C?" H 4800 3050 50  0000 L CNN
F 1 "10u" H 4800 2850 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 4788 2800 50  0001 C CNN
F 3 "~" H 4750 2950 50  0001 C CNN
F 4 "" H 4750 2950 50  0001 C CNN "MPN"
	1    4750 2950
	1    0    0    -1  
$EndComp
Wire Wire Line
	4750 3100 4750 3200
$Comp
L ng_power:GND #PWR?
U 1 1 5F0EC698
P 4750 3200
AR Path="/5F0EC698" Ref="#PWR?"  Part="1" 
AR Path="/5F7F68FE/5F0EC698" Ref="#PWR0101"  Part="1" 
AR Path="/5F483803/5F0EC698" Ref="#PWR0101"  Part="1" 
F 0 "#PWR0101" H 4750 2950 50  0001 C CNN
F 1 "GND" H 4753 3074 50  0000 C CNN
F 2 "" H 4650 2850 50  0001 C CNN
F 3 "" H 4750 3200 50  0001 C CNN
	1    4750 3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	4550 2700 4750 2700
Wire Wire Line
	4750 2800 4750 2700
Connection ~ 4750 2700
Wire Wire Line
	4750 2700 4950 2700
Wire Wire Line
	1650 2800 2450 2800
Wire Wire Line
	2750 2900 2750 2800
Connection ~ 2750 2800
Wire Wire Line
	2750 2800 3150 2800
Wire Wire Line
	2450 2900 2450 2800
Connection ~ 2450 2800
Wire Wire Line
	2450 2800 2750 2800
Wire Wire Line
	2150 2900 2150 2700
Connection ~ 2150 2700
Wire Wire Line
	2150 2700 3850 2700
Wire Wire Line
	1850 2900 1850 2700
Connection ~ 1850 2700
Wire Wire Line
	1850 2700 2150 2700
Wire Wire Line
	1850 3300 2150 3300
Connection ~ 2150 3300
Wire Wire Line
	2150 3300 2450 3300
Connection ~ 2450 3300
Wire Wire Line
	2450 3300 2750 3300
$Comp
L ng_power:GND #PWR0102
U 1 1 5F107C1A
P 1850 3400
F 0 "#PWR0102" H 1850 3150 50  0001 C CNN
F 1 "GND" H 1853 3274 50  0000 C CNN
F 2 "" H 1750 3050 50  0001 C CNN
F 3 "" H 1850 3400 50  0001 C CNN
	1    1850 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	1850 3400 1850 3300
Connection ~ 1850 3300
Connection ~ 3750 3900
Wire Wire Line
	3750 4000 3750 3900
$Comp
L ng_power:GND #PWR0103
U 1 1 5F0D220D
P 3750 4000
F 0 "#PWR0103" H 3750 3750 50  0001 C CNN
F 1 "GND" H 3753 3874 50  0000 C CNN
F 2 "" H 3650 3650 50  0001 C CNN
F 3 "" H 3750 4000 50  0001 C CNN
	1    3750 4000
	1    0    0    -1  
$EndComp
$Comp
L Jumper:SolderJumper_2_Open JP?
U 1 1 5F195E7A
P 3550 4750
F 0 "JP?" H 3550 4863 50  0000 C CNN
F 1 "SolderJumper_2_Open" H 3550 4864 50  0001 C CNN
F 2 "Jumper:SolderJumper-2_P1.3mm_Open_TrianglePad1.0x1.5mm" H 3550 4750 50  0001 C CNN
F 3 "~" H 3550 4750 50  0001 C CNN
	1    3550 4750
	1    0    0    -1  
$EndComp
Wire Wire Line
	3400 4750 3300 4750
Wire Wire Line
	3700 4750 3800 4750
$Comp
L Jumper:SolderJumper_2_Open JP?
U 1 1 5F19BE9B
P 3550 5000
F 0 "JP?" H 3550 5113 50  0000 C CNN
F 1 "SolderJumper_2_Open" H 3550 5114 50  0001 C CNN
F 2 "Jumper:SolderJumper-2_P1.3mm_Open_TrianglePad1.0x1.5mm" H 3550 5000 50  0001 C CNN
F 3 "~" H 3550 5000 50  0001 C CNN
	1    3550 5000
	1    0    0    -1  
$EndComp
Wire Wire Line
	3400 5000 3300 5000
Wire Wire Line
	3700 5000 3800 5000
$Comp
L Jumper:SolderJumper_2_Open JP?
U 1 1 5F19D934
P 3550 5250
F 0 "JP?" H 3550 5363 50  0000 C CNN
F 1 "SolderJumper_2_Open" H 3550 5364 50  0001 C CNN
F 2 "Jumper:SolderJumper-2_P1.3mm_Open_TrianglePad1.0x1.5mm" H 3550 5250 50  0001 C CNN
F 3 "~" H 3550 5250 50  0001 C CNN
	1    3550 5250
	1    0    0    -1  
$EndComp
Wire Wire Line
	3400 5250 3300 5250
Wire Wire Line
	3700 5250 3800 5250
Text GLabel 3300 4750 0    50   UnSpc ~ 0
MUX_3V3
Text GLabel 3300 5000 0    50   UnSpc ~ 0
N64_3V3
Text GLabel 3300 5250 0    50   UnSpc ~ 0
USB_3V3
Wire Wire Line
	3800 4750 3800 5000
Connection ~ 3800 5000
Wire Wire Line
	3800 5000 3800 5250
Wire Wire Line
	3800 4750 3900 4750
Connection ~ 3800 4750
Text GLabel 3900 4750 2    50   UnSpc ~ 0
P3V3
Text GLabel 6400 1800 0    50   UnSpc ~ 0
USB_5V
Wire Wire Line
	9200 2300 9200 2400
Wire Wire Line
	9200 2300 9500 2300
$Comp
L ng_power:GND #PWR?
U 1 1 5F497FD8
P 9200 2400
F 0 "#PWR?" H 9200 2150 50  0001 C CNN
F 1 "GND" H 9203 2274 50  0000 C CNN
F 2 "" H 9100 2050 50  0001 C CNN
F 3 "" H 9200 2400 50  0001 C CNN
	1    9200 2400
	1    0    0    -1  
$EndComp
Wire Wire Line
	9500 2200 9500 2300
Wire Wire Line
	9500 1800 9950 1800
Connection ~ 9500 1800
Wire Wire Line
	9500 1800 9500 1900
$Comp
L Device:C C?
U 1 1 5F497FD0
P 9500 2050
F 0 "C?" H 9550 2150 50  0000 L CNN
F 1 "22u" H 9550 1950 50  0000 L CNN
F 2 "" H 9538 1900 50  0001 C CNN
F 3 "~" H 9500 2050 50  0001 C CNN
	1    9500 2050
	1    0    0    -1  
$EndComp
Wire Wire Line
	8000 2300 8000 2000
Wire Wire Line
	8000 2000 7800 2000
Wire Wire Line
	8700 2200 8700 2300
Wire Wire Line
	8700 1900 8700 1800
$Comp
L Device:C C?
U 1 1 5F497FC1
P 8700 2050
F 0 "C?" H 8815 2096 50  0000 L CNN
F 1 "DNP" H 8815 2005 50  0000 L CNN
F 2 "" H 8738 1900 50  0001 C CNN
F 3 "~" H 8700 2050 50  0001 C CNN
	1    8700 2050
	1    0    0    -1  
$EndComp
Connection ~ 8700 1800
Wire Wire Line
	8300 1800 8700 1800
Wire Wire Line
	8300 1900 8300 1800
Wire Wire Line
	8000 2300 8300 2300
Wire Wire Line
	8700 2300 8300 2300
Connection ~ 8300 2300
Wire Wire Line
	8300 2300 8300 2200
$Comp
L Device:R R?
U 1 1 5F497FB6
P 8300 2050
F 0 "R?" H 8370 2096 50  0000 L CNN
F 1 "453k" H 8370 2005 50  0000 L CNN
F 2 "" V 8230 2050 50  0001 C CNN
F 3 "~" H 8300 2050 50  0001 C CNN
	1    8300 2050
	1    0    0    -1  
$EndComp
Connection ~ 8300 1800
Wire Wire Line
	8200 1800 8300 1800
Text GLabel 9950 1800 2    50   UnSpc ~ 0
USB_3V3
$Comp
L ng_power:GND #PWR?
U 1 1 5F497FAD
P 8300 2800
F 0 "#PWR?" H 8300 2550 50  0001 C CNN
F 1 "GND" H 8303 2674 50  0000 C CNN
F 2 "" H 8200 2450 50  0001 C CNN
F 3 "" H 8300 2800 50  0001 C CNN
	1    8300 2800
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR?
U 1 1 5F497FA7
P 6600 2300
F 0 "#PWR?" H 6600 2050 50  0001 C CNN
F 1 "GND" H 6603 2174 50  0000 C CNN
F 2 "" H 6500 1950 50  0001 C CNN
F 3 "" H 6600 2300 50  0001 C CNN
	1    6600 2300
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR?
U 1 1 5F497FA1
P 7400 2300
F 0 "#PWR?" H 7400 2050 50  0001 C CNN
F 1 "GND" H 7403 2174 50  0000 C CNN
F 2 "" H 7300 1950 50  0001 C CNN
F 3 "" H 7400 2300 50  0001 C CNN
	1    7400 2300
	1    0    0    -1  
$EndComp
Wire Wire Line
	6900 1800 7000 1800
Connection ~ 6900 1800
Wire Wire Line
	6900 2000 6900 1800
Wire Wire Line
	7000 2000 6900 2000
Wire Wire Line
	6600 2200 6600 2300
Wire Wire Line
	6600 1800 6400 1800
Wire Wire Line
	6600 1800 6900 1800
Connection ~ 6600 1800
Wire Wire Line
	6600 1800 6600 1900
$Comp
L Device:C C?
U 1 1 5F497F92
P 6600 2050
F 0 "C?" H 6715 2096 50  0000 L CNN
F 1 "4u7" H 6715 2005 50  0000 L CNN
F 2 "" H 6638 1900 50  0001 C CNN
F 3 "~" H 6600 2050 50  0001 C CNN
	1    6600 2050
	1    0    0    -1  
$EndComp
Wire Wire Line
	7400 2200 7400 2300
Wire Wire Line
	8300 2700 8300 2800
Connection ~ 9200 2300
Wire Wire Line
	9200 2200 9200 2300
Wire Wire Line
	9200 1800 9500 1800
Wire Wire Line
	8700 1800 9200 1800
Connection ~ 9200 1800
Wire Wire Line
	9200 1800 9200 1900
$Comp
L Device:C C?
U 1 1 5F497F88
P 9200 2050
F 0 "C?" H 9250 2150 50  0000 L CNN
F 1 "22u" H 9250 1950 50  0000 L CNN
F 2 "" H 9238 1900 50  0001 C CNN
F 3 "~" H 9200 2050 50  0001 C CNN
	1    9200 2050
	1    0    0    -1  
$EndComp
Wire Wire Line
	8300 2400 8300 2300
Wire Wire Line
	7900 1800 7800 1800
$Comp
L Device:R R?
U 1 1 5F497F80
P 8300 2550
F 0 "R?" H 8370 2596 50  0000 L CNN
F 1 "100k" H 8370 2505 50  0000 L CNN
F 2 "" V 8230 2550 50  0001 C CNN
F 3 "~" H 8300 2550 50  0001 C CNN
	1    8300 2550
	1    0    0    -1  
$EndComp
$Comp
L Device:L L?
U 1 1 5F497F7A
P 8050 1800
F 0 "L?" V 8240 1800 50  0000 C CNN
F 1 "2u2" V 8149 1800 50  0000 C CNN
F 2 "" H 8050 1800 50  0001 C CNN
F 3 "~" H 8050 1800 50  0001 C CNN
	1    8050 1800
	0    -1   -1   0   
$EndComp
$Comp
L ng_regulator:TLV62568DBV U?
U 1 1 5F497F74
P 7400 1850
F 0 "U?" H 7400 2167 50  0000 C CNN
F 1 "TLV62568DBV" H 7400 2076 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23-5" H 7400 1400 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/tlv62568.pdf" H 7400 1800 50  0001 C CNN
	1    7400 1850
	1    0    0    -1  
$EndComp
Text GLabel 6400 3600 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	9200 4100 9200 4200
Wire Wire Line
	9200 4100 9500 4100
$Comp
L ng_power:GND #PWR?
U 1 1 5F44452F
P 9200 4200
F 0 "#PWR?" H 9200 3950 50  0001 C CNN
F 1 "GND" H 9203 4074 50  0000 C CNN
F 2 "" H 9100 3850 50  0001 C CNN
F 3 "" H 9200 4200 50  0001 C CNN
	1    9200 4200
	1    0    0    -1  
$EndComp
Wire Wire Line
	9500 4000 9500 4100
Wire Wire Line
	9500 3600 9950 3600
Connection ~ 9500 3600
Wire Wire Line
	9500 3600 9500 3700
$Comp
L Device:C C?
U 1 1 5F44453D
P 9500 3850
F 0 "C?" H 9550 3950 50  0000 L CNN
F 1 "22u" H 9550 3750 50  0000 L CNN
F 2 "" H 9538 3700 50  0001 C CNN
F 3 "~" H 9500 3850 50  0001 C CNN
	1    9500 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	8000 4100 8000 3800
Wire Wire Line
	8000 3800 7800 3800
Wire Wire Line
	8700 4000 8700 4100
Wire Wire Line
	8700 3700 8700 3600
$Comp
L Device:C C?
U 1 1 5F44454B
P 8700 3850
F 0 "C?" H 8815 3896 50  0000 L CNN
F 1 "DNP" H 8815 3805 50  0000 L CNN
F 2 "" H 8738 3700 50  0001 C CNN
F 3 "~" H 8700 3850 50  0001 C CNN
	1    8700 3850
	1    0    0    -1  
$EndComp
Connection ~ 8700 3600
Wire Wire Line
	8300 3600 8700 3600
Wire Wire Line
	8300 3700 8300 3600
Wire Wire Line
	8000 4100 8300 4100
Wire Wire Line
	8700 4100 8300 4100
Connection ~ 8300 4100
Wire Wire Line
	8300 4100 8300 4000
$Comp
L Device:R R?
U 1 1 5F44455C
P 8300 3850
F 0 "R?" H 8370 3896 50  0000 L CNN
F 1 "82k5" H 8370 3805 50  0000 L CNN
F 2 "" V 8230 3850 50  0001 C CNN
F 3 "~" H 8300 3850 50  0001 C CNN
	1    8300 3850
	1    0    0    -1  
$EndComp
Connection ~ 8300 3600
Wire Wire Line
	8200 3600 8300 3600
Text GLabel 9950 3600 2    50   UnSpc ~ 0
P1V1
$Comp
L ng_power:GND #PWR?
U 1 1 5F444569
P 8300 4600
F 0 "#PWR?" H 8300 4350 50  0001 C CNN
F 1 "GND" H 8303 4474 50  0000 C CNN
F 2 "" H 8200 4250 50  0001 C CNN
F 3 "" H 8300 4600 50  0001 C CNN
	1    8300 4600
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR?
U 1 1 5F444573
P 6600 4100
F 0 "#PWR?" H 6600 3850 50  0001 C CNN
F 1 "GND" H 6603 3974 50  0000 C CNN
F 2 "" H 6500 3750 50  0001 C CNN
F 3 "" H 6600 4100 50  0001 C CNN
	1    6600 4100
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR?
U 1 1 5F44457D
P 7400 4100
F 0 "#PWR?" H 7400 3850 50  0001 C CNN
F 1 "GND" H 7403 3974 50  0000 C CNN
F 2 "" H 7300 3750 50  0001 C CNN
F 3 "" H 7400 4100 50  0001 C CNN
	1    7400 4100
	1    0    0    -1  
$EndComp
Wire Wire Line
	6900 3600 7000 3600
Connection ~ 6900 3600
Wire Wire Line
	6900 3800 6900 3600
Wire Wire Line
	7000 3800 6900 3800
Wire Wire Line
	6600 4000 6600 4100
Wire Wire Line
	6600 3600 6400 3600
Wire Wire Line
	6600 3600 6900 3600
Connection ~ 6600 3600
Wire Wire Line
	6600 3600 6600 3700
$Comp
L Device:C C?
U 1 1 5F444590
P 6600 3850
F 0 "C?" H 6715 3896 50  0000 L CNN
F 1 "4u7" H 6715 3805 50  0000 L CNN
F 2 "" H 6638 3700 50  0001 C CNN
F 3 "~" H 6600 3850 50  0001 C CNN
	1    6600 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	7400 4000 7400 4100
Wire Wire Line
	8300 4500 8300 4600
Connection ~ 9200 4100
Wire Wire Line
	9200 4000 9200 4100
Wire Wire Line
	9200 3600 9500 3600
Wire Wire Line
	8700 3600 9200 3600
Connection ~ 9200 3600
Wire Wire Line
	9200 3600 9200 3700
$Comp
L Device:C C?
U 1 1 5F4445A2
P 9200 3850
F 0 "C?" H 9250 3950 50  0000 L CNN
F 1 "22u" H 9250 3750 50  0000 L CNN
F 2 "" H 9238 3700 50  0001 C CNN
F 3 "~" H 9200 3850 50  0001 C CNN
	1    9200 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	8300 4200 8300 4100
Wire Wire Line
	7900 3600 7800 3600
$Comp
L Device:R R?
U 1 1 5F4445AE
P 8300 4350
F 0 "R?" H 8370 4396 50  0000 L CNN
F 1 "100k" H 8370 4305 50  0000 L CNN
F 2 "" V 8230 4350 50  0001 C CNN
F 3 "~" H 8300 4350 50  0001 C CNN
	1    8300 4350
	1    0    0    -1  
$EndComp
$Comp
L Device:L L?
U 1 1 5F4445B8
P 8050 3600
F 0 "L?" V 8240 3600 50  0000 C CNN
F 1 "2u2" V 8149 3600 50  0000 C CNN
F 2 "" H 8050 3600 50  0001 C CNN
F 3 "~" H 8050 3600 50  0001 C CNN
	1    8050 3600
	0    -1   -1   0   
$EndComp
$Comp
L ng_regulator:TLV62568DBV U?
U 1 1 5F4445C2
P 7400 3650
F 0 "U?" H 7400 3967 50  0000 C CNN
F 1 "TLV62568DBV" H 7400 3876 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23-5" H 7400 3200 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/tlv62568.pdf" H 7400 3600 50  0001 C CNN
	1    7400 3650
	1    0    0    -1  
$EndComp
$Comp
L ng_regulator:LDO_SOT-23-5 U?
U 1 1 5F46E54C
P 7400 5350
F 0 "U?" H 7400 5667 50  0000 C CNN
F 1 "TLV73325PDBV" H 7400 5576 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23-5" H 7400 4900 50  0001 C CNN
F 3 "https://www.ti.com/lit/ds/symlink/tlv733p.pdf" H 7400 5300 50  0001 C CNN
	1    7400 5350
	1    0    0    -1  
$EndComp
Text GLabel 6400 5300 0    50   UnSpc ~ 0
P3V3
$Comp
L ng_power:GND #PWR?
U 1 1 5F46F2DB
P 6600 5800
F 0 "#PWR?" H 6600 5550 50  0001 C CNN
F 1 "GND" H 6603 5674 50  0000 C CNN
F 2 "" H 6500 5450 50  0001 C CNN
F 3 "" H 6600 5800 50  0001 C CNN
	1    6600 5800
	1    0    0    -1  
$EndComp
Wire Wire Line
	6900 5300 7000 5300
Connection ~ 6900 5300
Wire Wire Line
	6900 5500 6900 5300
Wire Wire Line
	7000 5500 6900 5500
Wire Wire Line
	6600 5700 6600 5800
Wire Wire Line
	6600 5300 6400 5300
Wire Wire Line
	6600 5300 6900 5300
Connection ~ 6600 5300
Wire Wire Line
	6600 5300 6600 5400
$Comp
L Device:C C?
U 1 1 5F46F2EE
P 6600 5550
F 0 "C?" H 6715 5596 50  0000 L CNN
F 1 "1u" H 6715 5505 50  0000 L CNN
F 2 "" H 6638 5400 50  0001 C CNN
F 3 "~" H 6600 5550 50  0001 C CNN
	1    6600 5550
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR?
U 1 1 5F473694
P 7400 5800
F 0 "#PWR?" H 7400 5550 50  0001 C CNN
F 1 "GND" H 7403 5674 50  0000 C CNN
F 2 "" H 7300 5450 50  0001 C CNN
F 3 "" H 7400 5800 50  0001 C CNN
	1    7400 5800
	1    0    0    -1  
$EndComp
Wire Wire Line
	7400 5700 7400 5800
$Comp
L ng_power:GND #PWR?
U 1 1 5F47743E
P 8000 5800
F 0 "#PWR?" H 8000 5550 50  0001 C CNN
F 1 "GND" H 8003 5674 50  0000 C CNN
F 2 "" H 7900 5450 50  0001 C CNN
F 3 "" H 8000 5800 50  0001 C CNN
	1    8000 5800
	1    0    0    -1  
$EndComp
Wire Wire Line
	8000 5700 8000 5800
Wire Wire Line
	8000 5300 7800 5300
Wire Wire Line
	8000 5300 8200 5300
Connection ~ 8000 5300
Wire Wire Line
	8000 5300 8000 5400
$Comp
L Device:C C?
U 1 1 5F47744D
P 8000 5550
F 0 "C?" H 8115 5596 50  0000 L CNN
F 1 "1u" H 8115 5505 50  0000 L CNN
F 2 "" H 8038 5400 50  0001 C CNN
F 3 "~" H 8000 5550 50  0001 C CNN
	1    8000 5550
	1    0    0    -1  
$EndComp
Text GLabel 8200 5300 2    50   UnSpc ~ 0
P2V5
$EndSCHEMATC
