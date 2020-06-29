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
Wire Wire Line
	5750 3950 5950 3950
Wire Wire Line
	5250 4050 5150 4050
Wire Wire Line
	5250 3950 5150 3950
Wire Wire Line
	5250 3850 5150 3850
Wire Wire Line
	5250 3650 5150 3650
Wire Wire Line
	5750 4050 5950 4050
Text GLabel 5950 3950 2    50   Input ~ 0
FPGA_CDONE
Text GLabel 5150 4050 0    50   Input ~ 0
FPGA_CRESETn
Text GLabel 5150 3850 0    50   Input ~ 0
CONFIG_MOSI|IO0
Text GLabel 5150 3950 0    50   Input ~ 0
CONFIG_MISO|IO1
Text GLabel 5150 3650 0    50   Input ~ 0
CONFIG_SCK
Text GLabel 5950 4050 2    50   Input ~ 0
CONFIG_SSn
Text GLabel 5950 5350 2    50   Input ~ 0
FLASH_SSn
Text GLabel 5150 4950 0    50   Input ~ 0
FLASH_SCK
Text GLabel 5150 5150 0    50   Input ~ 0
FLASH_MOSI|IO0
Text GLabel 5150 5250 0    50   Input ~ 0
FLASH_MISO|IO1
Wire Wire Line
	5850 3450 5950 3450
Text GLabel 5850 3450 0    50   UnSpc ~ 0
P3V3
$Comp
L ng_power:GND #PWR?
U 1 1 5F90AA21
P 5850 4150
AR Path="/5F90AA21" Ref="#PWR?"  Part="1" 
AR Path="/5F8FED6E/5F90AA21" Ref="#PWR019"  Part="1" 
F 0 "#PWR019" H 5850 3900 50  0001 C CNN
F 1 "GND" H 5853 4024 50  0000 C CNN
F 2 "" H 5750 3800 50  0001 C CNN
F 3 "" H 5850 4150 50  0001 C CNN
	1    5850 4150
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_02x05_Odd_Even J?
U 1 1 5F90AA27
P 5450 3850
AR Path="/5F90AA27" Ref="J?"  Part="1" 
AR Path="/5F8FED6E/5F90AA27" Ref="J3"  Part="1" 
F 0 "J3" H 5500 4150 50  0000 C CNN
F 1 "Conn_02x05_Odd_Even" H 5500 4176 50  0001 C CNN
F 2 "ng_conn:Samtec_FTSH-105-XX-X-DV-Mating" H 5450 3850 50  0001 C CNN
F 3 "~" H 5450 3850 50  0001 C CNN
	1    5450 3850
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_02x05_Odd_Even J?
U 1 1 5F90AA2D
P 5450 5150
AR Path="/5F90AA2D" Ref="J?"  Part="1" 
AR Path="/5F8FED6E/5F90AA2D" Ref="J4"  Part="1" 
F 0 "J4" H 5500 5450 50  0000 C CNN
F 1 "Conn_02x05_Odd_Even" H 5500 5476 50  0001 C CNN
F 2 "ng_conn:Samtec_FTSH-105-XX-X-DV-Mating" H 5450 5150 50  0001 C CNN
F 3 "~" H 5450 5150 50  0001 C CNN
	1    5450 5150
	1    0    0    -1  
$EndComp
Wire Wire Line
	5750 3650 5850 3650
Wire Wire Line
	5850 3650 5850 3750
Wire Wire Line
	5750 3750 5850 3750
Connection ~ 5850 3750
Wire Wire Line
	5850 3750 5850 4150
Wire Wire Line
	5750 3850 5950 3850
Wire Wire Line
	5950 3450 5950 3850
NoConn ~ 5250 3750
Wire Wire Line
	5250 5250 5150 5250
Wire Wire Line
	5250 5150 5150 5150
Wire Wire Line
	5250 4950 5150 4950
Wire Wire Line
	5750 5350 5950 5350
Wire Wire Line
	5850 4750 5950 4750
Text GLabel 5850 4750 0    50   UnSpc ~ 0
P3V3
$Comp
L ng_power:GND #PWR?
U 1 1 5F90AA41
P 5850 5450
AR Path="/5F90AA41" Ref="#PWR?"  Part="1" 
AR Path="/5F8FED6E/5F90AA41" Ref="#PWR020"  Part="1" 
F 0 "#PWR020" H 5850 5200 50  0001 C CNN
F 1 "GND" H 5853 5324 50  0000 C CNN
F 2 "" H 5750 5100 50  0001 C CNN
F 3 "" H 5850 5450 50  0001 C CNN
	1    5850 5450
	1    0    0    -1  
$EndComp
Wire Wire Line
	5750 4950 5850 4950
Wire Wire Line
	5850 4950 5850 5050
Wire Wire Line
	5750 5050 5850 5050
Connection ~ 5850 5050
Wire Wire Line
	5850 5050 5850 5450
Wire Wire Line
	5750 5150 5950 5150
Wire Wire Line
	5950 4750 5950 5150
NoConn ~ 5750 5250
Wire Wire Line
	5250 5350 5150 5350
Text GLabel 5150 5350 0    50   Input ~ 0
FLASH_IO2
Wire Wire Line
	5150 5050 5250 5050
Text GLabel 5150 5050 0    50   Input ~ 0
FLASH_IO3
$EndSCHEMATC
