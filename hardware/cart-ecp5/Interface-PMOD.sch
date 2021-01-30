EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 9 9
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
	6500 3500 6600 3500
Wire Wire Line
	6500 3600 6600 3600
Wire Wire Line
	6500 3700 6600 3700
Wire Wire Line
	6500 3800 6600 3800
Wire Wire Line
	5900 3500 6000 3500
Wire Wire Line
	5900 3600 6000 3600
Wire Wire Line
	5900 3700 6000 3700
Wire Wire Line
	5900 3800 6000 3800
Wire Wire Line
	5700 3900 6000 3900
Wire Wire Line
	5900 4000 6000 4000
Text GLabel 5900 3500 0    50   BiDi ~ 0
PMOD_P1_D0
Text GLabel 5900 3600 0    50   BiDi ~ 0
PMOD_P1_D1
Text GLabel 5900 3700 0    50   BiDi ~ 0
PMOD_P1_D2
Text GLabel 5900 3800 0    50   BiDi ~ 0
PMOD_P1_D3
Text GLabel 6600 3500 2    50   BiDi ~ 0
PMOD_P1_D4
Text GLabel 6600 3600 2    50   BiDi ~ 0
PMOD_P1_D5
Text GLabel 6600 3700 2    50   BiDi ~ 0
PMOD_P1_D6
Text GLabel 6600 3800 2    50   BiDi ~ 0
PMOD_P1_D7
Wire Wire Line
	6500 4000 6600 4000
Wire Wire Line
	6500 3900 6800 3900
Wire Wire Line
	6600 4000 6600 4100
Text GLabel 6600 4100 3    50   UnSpc ~ 0
P3V3
Wire Wire Line
	6800 3900 6800 4000
$Comp
L ng_power:GND #PWR073
U 1 1 60317E7E
P 6800 4000
F 0 "#PWR073" H 6800 3750 50  0001 C CNN
F 1 "GND" H 6803 3874 50  0000 C CNN
F 2 "" H 6700 3650 50  0001 C CNN
F 3 "" H 6800 4000 50  0001 C CNN
	1    6800 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	5900 4000 5900 4100
Wire Wire Line
	5700 3900 5700 4000
$Comp
L ng_power:GND #PWR08
U 1 1 60318851
P 5700 4000
F 0 "#PWR08" H 5700 3750 50  0001 C CNN
F 1 "GND" H 5703 3874 50  0000 C CNN
F 2 "" H 5600 3650 50  0001 C CNN
F 3 "" H 5700 4000 50  0001 C CNN
	1    5700 4000
	1    0    0    -1  
$EndComp
Text GLabel 5900 4100 3    50   UnSpc ~ 0
P3V3
$Comp
L Connector_Generic:Conn_02x06_Odd_Even J6
U 1 1 6031AC36
P 6200 3800
F 0 "J6" H 6250 3275 50  0000 C CNN
F 1 "Conn_02x06_Odd_Even" H 6250 3366 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_2x06_P2.54mm_Horizontal" H 6200 3800 50  0001 C CNN
F 3 "~" H 6200 3800 50  0001 C CNN
	1    6200 3800
	1    0    0    1   
$EndComp
$EndSCHEMATC
