EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 7 13
Title "Ferk-Cart iCE40 Devboard"
Date "2020-06-29"
Rev "r0.1"
Comp "Designed by: Nelson Gauthier"
Comment1 "Licensed under CERN OHL v.1.2"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Wire Wire Line
	5850 3850 6050 3850
Wire Wire Line
	5850 3550 6050 3550
Wire Wire Line
	5350 3850 5250 3850
Wire Wire Line
	5350 3750 5250 3750
Wire Wire Line
	5350 3650 5250 3650
Wire Wire Line
	5850 3950 6050 3950
Text GLabel 6050 3850 2    50   Input ~ 0
FPGA_CDONE
Text GLabel 5250 3750 0    50   Input ~ 0
CONFIG_MOSI|IO0
Text GLabel 5250 3850 0    50   Input ~ 0
CONFIG_MISO|IO1
Text GLabel 5250 3650 0    50   Input ~ 0
CONFIG_SCK
Text GLabel 6050 3950 2    50   Input ~ 0
CONFIG_SSn
Text GLabel 6050 5350 2    50   Input ~ 0
FLASH_SSn
Text GLabel 5250 5050 0    50   Input ~ 0
FLASH_SCK
Text GLabel 5250 5150 0    50   Input ~ 0
FLASH_MOSI|IO0
Text GLabel 5250 5250 0    50   Input ~ 0
FLASH_MISO|IO1
Wire Wire Line
	5850 3250 5950 3250
Text GLabel 5850 3250 0    50   UnSpc ~ 0
P3V3
$Comp
L ng_power:GND #PWR?
U 1 1 5F90AA21
P 5950 4050
AR Path="/5F90AA21" Ref="#PWR?"  Part="1" 
AR Path="/5F8FED6E/5F90AA21" Ref="#PWR019"  Part="1" 
F 0 "#PWR019" H 5950 3800 50  0001 C CNN
F 1 "GND" H 5953 3924 50  0000 C CNN
F 2 "" H 5850 3700 50  0001 C CNN
F 3 "" H 5950 4050 50  0001 C CNN
	1    5950 4050
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_02x05_Odd_Even J?
U 1 1 5F90AA27
P 5550 3750
AR Path="/5F90AA27" Ref="J?"  Part="1" 
AR Path="/5F8FED6E/5F90AA27" Ref="J3"  Part="1" 
F 0 "J3" H 5500 4050 50  0000 L CNN
F 1 "FTSH-105-01-L-DV-K" H 5600 4076 50  0001 C CNN
F 2 "ng_conn:Samtec_FTSH-105-XX-X-DV-Mating" H 5550 3750 50  0001 C CNN
F 3 "~" H 5550 3750 50  0001 C CNN
F 4 "FTSH-105-01-L-DV-K" H 5550 3750 50  0001 C CNN "MPN"
	1    5550 3750
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_02x05_Odd_Even J?
U 1 1 5F90AA2D
P 5550 5150
AR Path="/5F90AA2D" Ref="J?"  Part="1" 
AR Path="/5F8FED6E/5F90AA2D" Ref="J4"  Part="1" 
F 0 "J4" H 5500 5450 50  0000 L CNN
F 1 "FTSH-105-01-L-DV-K" H 5600 5476 50  0001 C CNN
F 2 "ng_conn:Samtec_FTSH-105-XX-X-DV-Mating" H 5550 5150 50  0001 C CNN
F 3 "~" H 5550 5150 50  0001 C CNN
F 4 "FTSH-105-01-L-DV-K" H 5550 5150 50  0001 C CNN "MPN"
	1    5550 5150
	1    0    0    -1  
$EndComp
Wire Wire Line
	5950 3750 5950 4050
Wire Wire Line
	5950 3250 5950 3650
Wire Wire Line
	5350 5250 5250 5250
Wire Wire Line
	5350 5150 5250 5150
Wire Wire Line
	5350 5050 5250 5050
Wire Wire Line
	5850 5350 6050 5350
$Comp
L ng_power:GND #PWR?
U 1 1 5F90AA41
P 5950 5450
AR Path="/5F90AA41" Ref="#PWR?"  Part="1" 
AR Path="/5F8FED6E/5F90AA41" Ref="#PWR020"  Part="1" 
F 0 "#PWR020" H 5950 5200 50  0001 C CNN
F 1 "GND" H 5953 5324 50  0000 C CNN
F 2 "" H 5850 5100 50  0001 C CNN
F 3 "" H 5950 5450 50  0001 C CNN
	1    5950 5450
	1    0    0    -1  
$EndComp
Wire Wire Line
	5850 4950 6050 4950
Text GLabel 5250 5350 0    50   Input ~ 0
FLASH_IO2
Wire Wire Line
	5250 4950 5350 4950
Text GLabel 5250 4950 0    50   Input ~ 0
FLASH_IO3
Text GLabel 6050 4950 2    50   Input ~ 0
FLASH_CRESETn
Text GLabel 6050 3550 2    50   Input ~ 0
CONFIG_CRESETn
Wire Wire Line
	5850 5250 6050 5250
Wire Wire Line
	5350 3550 5250 3550
Text GLabel 5250 3550 0    50   Input ~ 0
CONFIG_IO3
Wire Wire Line
	5950 3750 5850 3750
Wire Wire Line
	5950 3650 5850 3650
Wire Wire Line
	5850 4650 5950 4650
Wire Wire Line
	5950 4650 5950 5050
Wire Wire Line
	5950 5050 5850 5050
Wire Wire Line
	5850 5150 5950 5150
Wire Wire Line
	5950 5150 5950 5450
Text GLabel 5850 4650 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	5350 3950 5250 3950
Text GLabel 5250 3950 0    50   Input ~ 0
CONFIG_IO2
Wire Wire Line
	5250 5350 5350 5350
Text GLabel 6050 5250 2    50   Input ~ 0
FPGA_CDONE
$EndSCHEMATC
