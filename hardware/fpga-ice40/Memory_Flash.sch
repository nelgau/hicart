EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 7 12
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
L Device:C C?
U 1 1 5F8E1312
P 5600 5500
AR Path="/5F8E1312" Ref="C?"  Part="1" 
AR Path="/5F8CA8A2/5F8E1312" Ref="C15"  Part="1" 
F 0 "C15" H 5550 5600 50  0000 R CNN
F 1 "100n" H 5550 5400 50  0000 R CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 5638 5350 50  0001 C CNN
F 3 "~" H 5600 5500 50  0001 C CNN
	1    5600 5500
	-1   0    0    -1  
$EndComp
Wire Wire Line
	5500 5200 5600 5200
Connection ~ 5600 5200
Wire Wire Line
	5600 5200 5600 5350
Wire Wire Line
	5500 5800 5600 5800
Wire Wire Line
	5600 5800 5600 5900
Connection ~ 5600 5800
$Comp
L Device:C C?
U 1 1 5F8E131E
P 5600 3400
AR Path="/5F8E131E" Ref="C?"  Part="1" 
AR Path="/5F8CA8A2/5F8E131E" Ref="C14"  Part="1" 
F 0 "C14" H 5550 3500 50  0000 R CNN
F 1 "100n" H 5550 3300 50  0000 R CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 5638 3250 50  0001 C CNN
F 3 "~" H 5600 3400 50  0001 C CNN
	1    5600 3400
	-1   0    0    -1  
$EndComp
Connection ~ 5600 3100
Wire Wire Line
	5600 3100 5600 3250
Wire Wire Line
	5600 3700 5600 3800
Connection ~ 5600 3700
Text GLabel 3850 5200 0    50   Input ~ 0
FLASH_SSn
Text GLabel 3850 5300 0    50   Input ~ 0
FLASH_SCK
Text GLabel 3850 5500 0    50   Input ~ 0
FLASH_MOSI|IO0
Text GLabel 3850 5600 0    50   Input ~ 0
FLASH_MISO|IO1
Text GLabel 3850 5700 0    50   Input ~ 0
FLASH_IO2
Text GLabel 3850 5800 0    50   Input ~ 0
FLASH_IO3
Wire Wire Line
	5500 3700 5600 3700
Wire Wire Line
	5500 3100 5600 3100
Wire Wire Line
	3850 5800 4250 5800
Connection ~ 4250 5800
Wire Wire Line
	4250 5800 4400 5800
Wire Wire Line
	3850 5500 4400 5500
Wire Wire Line
	3850 5600 4400 5600
Wire Wire Line
	4250 4600 4250 4700
Wire Wire Line
	3850 5200 3950 5200
Wire Wire Line
	4150 4700 4150 4600
Connection ~ 4150 4600
Wire Wire Line
	4150 4600 4250 4600
Wire Wire Line
	4050 4700 4050 4600
Connection ~ 4050 4600
Wire Wire Line
	4050 4600 4150 4600
Wire Wire Line
	3950 4600 4050 4600
Wire Wire Line
	3950 4700 3950 4600
Connection ~ 3950 5200
Wire Wire Line
	3950 5200 4400 5200
Wire Wire Line
	4250 5100 4250 5800
Wire Wire Line
	3950 5100 3950 5200
$Comp
L Device:R_Pack04 RN?
U 1 1 5F8E1343
P 4150 4900
AR Path="/5F8E1343" Ref="RN?"  Part="1" 
AR Path="/5F8CA8A2/5F8E1343" Ref="RN2"  Part="1" 
F 0 "RN2" H 4338 4946 50  0000 L CNN
F 1 "10k" H 4338 4855 50  0000 L CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 4425 4900 50  0001 C CNN
F 3 "~" H 4150 4900 50  0001 C CNN
	1    4150 4900
	1    0    0    -1  
$EndComp
Text GLabel 5500 4850 0    50   UnSpc ~ 0
P3V3
Text GLabel 3850 4600 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	3850 4600 3950 4600
Connection ~ 3950 4600
Text GLabel 5500 2750 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	5600 2750 5600 3100
Wire Wire Line
	5600 2750 5500 2750
Wire Wire Line
	5600 4850 5600 5200
Wire Wire Line
	5600 4850 5500 4850
$Comp
L ng_power:GND #PWR?
U 1 1 5F8E1352
P 5600 5900
AR Path="/5F8E1352" Ref="#PWR?"  Part="1" 
AR Path="/5F8CA8A2/5F8E1352" Ref="#PWR014"  Part="1" 
F 0 "#PWR014" H 5600 5650 50  0001 C CNN
F 1 "GND" H 5603 5774 50  0000 C CNN
F 2 "" H 5500 5550 50  0001 C CNN
F 3 "" H 5600 5900 50  0001 C CNN
	1    5600 5900
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR?
U 1 1 5F8E1358
P 5600 3800
AR Path="/5F8E1358" Ref="#PWR?"  Part="1" 
AR Path="/5F8CA8A2/5F8E1358" Ref="#PWR012"  Part="1" 
F 0 "#PWR012" H 5600 3550 50  0001 C CNN
F 1 "GND" H 5603 3674 50  0000 C CNN
F 2 "" H 5500 3450 50  0001 C CNN
F 3 "" H 5600 3800 50  0001 C CNN
	1    5600 3800
	1    0    0    -1  
$EndComp
Connection ~ 7900 3000
Wire Wire Line
	7800 3000 7900 3000
Wire Wire Line
	7900 2650 7900 3000
Wire Wire Line
	7900 3700 7900 3800
$Comp
L ng_power:GND #PWR?
U 1 1 5F8E1362
P 7900 3800
AR Path="/5F8E1362" Ref="#PWR?"  Part="1" 
AR Path="/5F8CA8A2/5F8E1362" Ref="#PWR013"  Part="1" 
F 0 "#PWR013" H 7900 3550 50  0001 C CNN
F 1 "GND" H 7903 3674 50  0000 C CNN
F 2 "" H 7800 3450 50  0001 C CNN
F 3 "" H 7900 3800 50  0001 C CNN
	1    7900 3800
	1    0    0    -1  
$EndComp
Wire Wire Line
	7800 3700 7900 3700
$Comp
L ng_memory:S25FL256SAGMFI01 U?
U 1 1 5F8E1369
P 7700 2900
AR Path="/5F8E1369" Ref="U?"  Part="1" 
AR Path="/5F8CA8A2/5F8E1369" Ref="U5"  Part="1" 
F 0 "U5" H 8600 3050 50  0000 R CNN
F 1 "S25FL256SAGMFI01" H 8600 2950 50  0000 R CNN
F 2 "Package_SO:SOIC-16W_7.5x10.3mm_P1.27mm" H 8150 1950 50  0001 C CNN
F 3 "https://www.cypress.com/file/448601/download" H 9100 2900 50  0001 C CNN
	1    7700 2900
	-1   0    0    -1  
$EndComp
Connection ~ 3950 2500
Wire Wire Line
	3850 2500 3950 2500
Text GLabel 3850 2500 0    50   UnSpc ~ 0
P3V3
$Comp
L Device:R_Pack04 RN?
U 1 1 5F8E1372
P 4150 2800
AR Path="/5F8E1372" Ref="RN?"  Part="1" 
AR Path="/5F8CA8A2/5F8E1372" Ref="RN1"  Part="1" 
F 0 "RN1" H 4338 2846 50  0000 L CNN
F 1 "10k" H 4338 2755 50  0000 L CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 4425 2800 50  0001 C CNN
F 3 "~" H 4150 2800 50  0001 C CNN
	1    4150 2800
	1    0    0    -1  
$EndComp
Wire Wire Line
	3950 3100 4400 3100
Connection ~ 3950 3100
Wire Wire Line
	3950 3000 3950 3100
Wire Wire Line
	3950 2600 3950 2500
Wire Wire Line
	3950 2500 4050 2500
Wire Wire Line
	4050 2500 4150 2500
Connection ~ 4050 2500
Wire Wire Line
	4050 2600 4050 2500
Wire Wire Line
	4150 2500 4250 2500
Connection ~ 4150 2500
Wire Wire Line
	4150 2600 4150 2500
Wire Wire Line
	3850 3100 3950 3100
Wire Wire Line
	4250 2500 4250 2600
Wire Wire Line
	3850 3500 4400 3500
Wire Wire Line
	3850 3400 4400 3400
Wire Wire Line
	4250 3700 4400 3700
Connection ~ 4250 3700
Text GLabel 3850 3700 0    50   Input ~ 0
CONFIG_IO3
Text GLabel 3850 3600 0    50   Input ~ 0
CONFIG_IO2
Text GLabel 3850 3500 0    50   Input ~ 0
CONFIG_MISO|IO1
Text GLabel 3850 3400 0    50   Input ~ 0
CONFIG_MOSI|IO0
Text GLabel 3850 3200 0    50   Input ~ 0
CONFIG_SCK
Text GLabel 3850 3100 0    50   Input ~ 0
CONFIG_SSn
Wire Wire Line
	4250 3000 4250 3700
Wire Wire Line
	3850 3700 4250 3700
Wire Wire Line
	7900 2650 6600 2650
Wire Wire Line
	7800 3100 7900 3100
Wire Wire Line
	7900 3000 7900 3100
Text GLabel 6700 3700 0    50   Input ~ 0
CONFIG_IO3
Text GLabel 6700 3600 0    50   Input ~ 0
CONFIG_IO2
Text GLabel 6700 3500 0    50   Input ~ 0
CONFIG_MISO|IO1
Text GLabel 6700 3400 0    50   Input ~ 0
CONFIG_MOSI|IO0
Text GLabel 6700 3200 0    50   Input ~ 0
CONFIG_SCK
Text GLabel 6700 3100 0    50   Input ~ 0
CONFIG_SSn
Text GLabel 6500 2750 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	6600 2650 6600 2750
Wire Wire Line
	6600 3000 6700 3000
Connection ~ 7900 5100
Wire Wire Line
	7800 5100 7900 5100
Wire Wire Line
	7900 4750 7900 5100
Wire Wire Line
	7900 5800 7900 5900
$Comp
L ng_power:GND #PWR?
U 1 1 5F8E13A1
P 7900 5900
AR Path="/5F8E13A1" Ref="#PWR?"  Part="1" 
AR Path="/5F8CA8A2/5F8E13A1" Ref="#PWR015"  Part="1" 
F 0 "#PWR015" H 7900 5650 50  0001 C CNN
F 1 "GND" H 7903 5774 50  0000 C CNN
F 2 "" H 7800 5550 50  0001 C CNN
F 3 "" H 7900 5900 50  0001 C CNN
	1    7900 5900
	1    0    0    -1  
$EndComp
Wire Wire Line
	7800 5800 7900 5800
$Comp
L ng_memory:S25FL256SAGMFI01 U?
U 1 1 5F8E13A8
P 7700 5000
AR Path="/5F8E13A8" Ref="U?"  Part="1" 
AR Path="/5F8CA8A2/5F8E13A8" Ref="U7"  Part="1" 
F 0 "U7" H 8600 5150 50  0000 R CNN
F 1 "S25FL256SAGMFI01" H 8600 5050 50  0000 R CNN
F 2 "Package_SO:SOIC-16W_7.5x10.3mm_P1.27mm" H 8150 4050 50  0001 C CNN
F 3 "https://www.cypress.com/file/448601/download" H 9100 5000 50  0001 C CNN
	1    7700 5000
	-1   0    0    -1  
$EndComp
Wire Wire Line
	7800 5200 7900 5200
Wire Wire Line
	7900 5100 7900 5200
Text GLabel 6500 4850 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	6600 4750 6600 4850
Wire Wire Line
	6600 5100 6700 5100
Wire Wire Line
	6600 4750 7900 4750
Text GLabel 6700 5200 0    50   Input ~ 0
FLASH_SSn
Text GLabel 6700 5300 0    50   Input ~ 0
FLASH_SCK
Text GLabel 6700 5500 0    50   Input ~ 0
FLASH_MOSI|IO0
Text GLabel 6700 5600 0    50   Input ~ 0
FLASH_MISO|IO1
Text GLabel 6700 5700 0    50   Input ~ 0
FLASH_IO2
Text GLabel 6700 5800 0    50   Input ~ 0
FLASH_IO3
Wire Notes Line
	2950 2300 8100 2300
Wire Notes Line
	8100 2300 8100 4100
Wire Notes Line
	8100 4100 2950 4100
Wire Notes Line
	2950 4100 2950 2300
Wire Notes Line
	2950 4400 8100 4400
Wire Notes Line
	2950 6200 2950 4400
Wire Notes Line
	8100 4400 8100 6200
Wire Notes Line
	8100 6200 2950 6200
$Comp
L ng_memory:W25Q32JVSS U?
U 1 1 5F8E13C2
P 5400 3000
AR Path="/5F8E13C2" Ref="U?"  Part="1" 
AR Path="/5F8CA8A2/5F8E13C2" Ref="U6"  Part="1" 
F 0 "U6" H 6300 3150 50  0000 R CNN
F 1 "W25Q32JVSS" H 6300 3050 50  0000 R CNN
F 2 "local_hacks:SOIC-8_5.275x5.275mm_P1.27mm__No_CrtYd" H 5900 2150 50  0001 C CNN
F 3 "https://www.mouser.com/datasheet/2/949/w25q32jv_dtr_revg_03272018_plus-1489786.pdf" H 6400 2700 50  0001 C CNN
	1    5400 3000
	-1   0    0    -1  
$EndComp
Wire Wire Line
	5600 3550 5600 3700
$Comp
L ng_memory:W25Q32JVSS U?
U 1 1 5F8E13C9
P 5400 5100
AR Path="/5F8E13C9" Ref="U?"  Part="1" 
AR Path="/5F8CA8A2/5F8E13C9" Ref="U8"  Part="1" 
F 0 "U8" H 6300 5250 50  0000 R CNN
F 1 "W25Q32JVSS" H 6300 5150 50  0000 R CNN
F 2 "local_hacks:SOIC-8_5.275x5.275mm_P1.27mm__No_CrtYd" H 5900 4250 50  0001 C CNN
F 3 "https://www.mouser.com/datasheet/2/949/w25q32jv_dtr_revg_03272018_plus-1489786.pdf" H 6400 4800 50  0001 C CNN
	1    5400 5100
	-1   0    0    -1  
$EndComp
Wire Wire Line
	5600 5650 5600 5800
Wire Wire Line
	6500 2750 6600 2750
Connection ~ 6600 2750
Wire Wire Line
	6600 2750 6600 3000
Wire Wire Line
	6500 4850 6600 4850
Connection ~ 6600 4850
Wire Wire Line
	6600 4850 6600 5100
Wire Wire Line
	3850 3200 4150 3200
Wire Wire Line
	4050 3000 4050 3600
Wire Wire Line
	3850 3600 4050 3600
Connection ~ 4050 3600
Wire Wire Line
	4050 3600 4400 3600
Wire Wire Line
	4150 3000 4150 3200
Connection ~ 4150 3200
Wire Wire Line
	4150 3200 4400 3200
Wire Wire Line
	3850 5300 4150 5300
Wire Wire Line
	3850 5700 4050 5700
Wire Wire Line
	4050 5100 4050 5700
Connection ~ 4050 5700
Wire Wire Line
	4050 5700 4400 5700
Wire Wire Line
	4150 5100 4150 5300
Connection ~ 4150 5300
Wire Wire Line
	4150 5300 4400 5300
$EndSCHEMATC
