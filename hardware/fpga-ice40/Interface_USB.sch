EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 8 12
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
L ng_ftdi:FT245RL U?
U 1 1 5F314850
P 6300 3550
AR Path="/5F314850" Ref="U?"  Part="1" 
AR Path="/5F302051/5F314850" Ref="U9"  Part="1" 
F 0 "U9" H 6300 4100 50  0000 L CNN
F 1 "FT245RL" H 6300 4000 50  0000 L CNN
F 2 "Package_SO:SSOP-28_5.3x10.2mm_P0.65mm" H 6450 4000 50  0001 C CNN
F 3 "https://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT245R.pdf" H 6450 4000 50  0001 C CNN
F 4 "FT245RL-REEL" H 6300 3550 50  0001 C CNN "MPN"
	1    6300 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	6050 4650 6050 4550
Wire Wire Line
	6050 4550 6150 4550
Wire Wire Line
	6050 4950 6050 5050
Wire Wire Line
	7150 5050 7150 4900
Wire Wire Line
	6750 4900 6750 5050
Connection ~ 6750 5050
Wire Wire Line
	6750 5050 6850 5050
Wire Wire Line
	6850 4900 6850 5050
Connection ~ 6850 5050
Wire Wire Line
	6850 5050 6950 5050
Wire Wire Line
	6950 4900 6950 5050
Connection ~ 6950 5050
Wire Wire Line
	6950 5050 7050 5050
Wire Wire Line
	7050 4900 7050 5050
Connection ~ 7050 5050
Wire Wire Line
	7050 5050 7150 5050
$Comp
L ng_power:GND #PWR?
U 1 1 5F314866
P 5750 5150
AR Path="/5F314866" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F314866" Ref="#PWR025"  Part="1" 
F 0 "#PWR025" H 5750 4900 50  0001 C CNN
F 1 "GND" H 5753 5024 50  0000 C CNN
F 2 "" H 5650 4800 50  0001 C CNN
F 3 "" H 5750 5150 50  0001 C CNN
	1    5750 5150
	1    0    0    -1  
$EndComp
Wire Wire Line
	5750 5150 5750 5050
NoConn ~ 6150 4250
NoConn ~ 6150 4350
$Comp
L Device:C C?
U 1 1 5F31486F
P 6050 4800
AR Path="/5F31486F" Ref="C?"  Part="1" 
AR Path="/5F302051/5F31486F" Ref="C22"  Part="1" 
F 0 "C22" H 6100 4900 50  0000 L CNN
F 1 "100n" H 6100 4700 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 6088 4650 50  0001 C CNN
F 3 "~" H 6050 4800 50  0001 C CNN
F 4 "CL10B104KB8NNNC" H 6050 4800 50  0001 C CNN "MPN"
	1    6050 4800
	1    0    0    -1  
$EndComp
Text GLabel 5650 3550 0    50   Input ~ 0
USB_D-
Text GLabel 5650 3650 0    50   Input ~ 0
USB_D+
Text GLabel 7700 3250 2    50   Input ~ 0
FIFO_D0
Text GLabel 7700 3350 2    50   Input ~ 0
FIFO_D1
Text GLabel 7700 3450 2    50   Input ~ 0
FIFO_D2
Text GLabel 7700 3550 2    50   Input ~ 0
FIFO_D3
Text GLabel 7700 3650 2    50   Input ~ 0
FIFO_D4
Text GLabel 7700 3850 2    50   Input ~ 0
FIFO_D6
Text GLabel 7700 3950 2    50   Input ~ 0
FIFO_D7
Text GLabel 7700 3750 2    50   Input ~ 0
FIFO_D5
Text GLabel 7700 4150 2    50   Input ~ 0
FIFO_RXFn
Text GLabel 7700 4350 2    50   Input ~ 0
FIFO_RDn
Text GLabel 7700 4450 2    50   Input ~ 0
FIFO_WR
Text GLabel 7700 4250 2    50   Input ~ 0
FIFO_TXEn
$Comp
L Device:R R?
U 1 1 5F314883
P 8300 4400
AR Path="/5F314883" Ref="R?"  Part="1" 
AR Path="/5F302051/5F314883" Ref="R4"  Part="1" 
F 0 "R4" H 8370 4446 50  0000 L CNN
F 1 "10k" H 8370 4355 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 8230 4400 50  0001 C CNN
F 3 "~" H 8300 4400 50  0001 C CNN
F 4 "RC0603FR-0710KL" H 8300 4400 50  0001 C CNN "MPN"
	1    8300 4400
	1    0    0    -1  
$EndComp
Wire Wire Line
	7700 4650 8300 4650
Wire Wire Line
	8300 4650 8300 4550
Wire Wire Line
	8300 4250 8300 4150
Wire Wire Line
	6050 3350 6150 3350
Text GLabel 8400 4150 2    50   UnSpc ~ 0
P3V3
Wire Wire Line
	8300 4150 8400 4150
Wire Wire Line
	6050 4550 6050 3350
Connection ~ 6050 4550
Wire Wire Line
	5650 3550 6150 3550
Wire Wire Line
	5650 3650 6150 3650
Wire Wire Line
	5650 3250 5750 3250
Text GLabel 5650 3250 0    50   UnSpc ~ 0
USB_5V
Wire Wire Line
	5650 3950 6150 3950
Text GLabel 5650 3950 0    50   Input ~ 0
USB_DETn
Text Label 6050 4500 1    50   ~ 0
USB_VIO
Text Label 7750 4650 0    50   ~ 0
USB_PWRENn
$Comp
L Device:R R?
U 1 1 5F3148AD
P 3900 4400
AR Path="/5F3148AD" Ref="R?"  Part="1" 
AR Path="/5F302051/5F3148AD" Ref="R3"  Part="1" 
F 0 "R3" H 3970 4446 50  0000 L CNN
F 1 "6k8" H 3970 4355 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 3830 4400 50  0001 C CNN
F 3 "~" H 3900 4400 50  0001 C CNN
F 4 "RC0603FR-076K8L" H 3900 4400 50  0001 C CNN "MPN"
	1    3900 4400
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 5F3148B3
P 3900 4900
AR Path="/5F3148B3" Ref="R?"  Part="1" 
AR Path="/5F302051/5F3148B3" Ref="R5"  Part="1" 
F 0 "R5" H 3970 4946 50  0000 L CNN
F 1 "10k" H 3970 4855 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 3830 4900 50  0001 C CNN
F 3 "~" H 3900 4900 50  0001 C CNN
F 4 "RC0603FR-0710KL" H 3900 4900 50  0001 C CNN "MPN"
	1    3900 4900
	1    0    0    -1  
$EndComp
Wire Wire Line
	3900 5050 3900 5150
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148BA
P 3900 5150
AR Path="/5F3148BA" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148BA" Ref="#PWR024"  Part="1" 
F 0 "#PWR024" H 3900 4900 50  0001 C CNN
F 1 "GND" H 3903 5024 50  0000 C CNN
F 2 "" H 3800 4800 50  0001 C CNN
F 3 "" H 3900 5150 50  0001 C CNN
	1    3900 5150
	1    0    0    -1  
$EndComp
Wire Wire Line
	3900 4550 3900 4650
Wire Wire Line
	3900 4250 3900 4150
Wire Wire Line
	3900 4150 3800 4150
Wire Wire Line
	3900 4650 4000 4650
Connection ~ 3900 4650
Wire Wire Line
	3900 4650 3900 4750
Text GLabel 4000 4650 2    50   Input ~ 0
USB_DETn
$Comp
L Device:C C?
U 1 1 5F3148C7
P 5750 4800
AR Path="/5F3148C7" Ref="C?"  Part="1" 
AR Path="/5F302051/5F3148C7" Ref="C21"  Part="1" 
F 0 "C21" H 5800 4900 50  0000 L CNN
F 1 "100n" H 5800 4700 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 5788 4650 50  0001 C CNN
F 3 "~" H 5750 4800 50  0001 C CNN
F 4 "CL10B104KB8NNNC" H 5750 4800 50  0001 C CNN "MPN"
	1    5750 4800
	1    0    0    -1  
$EndComp
Wire Wire Line
	5750 4650 5750 3250
Connection ~ 5750 3250
Wire Wire Line
	5750 3250 6150 3250
Wire Wire Line
	5750 4950 5750 5050
Wire Wire Line
	5750 5050 6050 5050
Connection ~ 6050 5050
Connection ~ 5750 5050
Wire Wire Line
	6050 5050 6750 5050
$Comp
L Device:C C?
U 1 1 5F3148D5
P 3900 3500
AR Path="/5F3148D5" Ref="C?"  Part="1" 
AR Path="/5F302051/5F3148D5" Ref="C18"  Part="1" 
F 0 "C18" H 3950 3600 50  0000 L CNN
F 1 "10n" H 3950 3400 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3938 3350 50  0001 C CNN
F 3 "~" H 3900 3500 50  0001 C CNN
F 4 "CL10B103KC8NNNC" H 3900 3500 50  0001 C CNN "MPN"
	1    3900 3500
	1    0    0    -1  
$EndComp
Wire Wire Line
	3900 3250 3900 3350
Wire Wire Line
	3900 3650 3900 3750
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148DE
P 3900 3750
AR Path="/5F3148DE" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148DE" Ref="#PWR021"  Part="1" 
F 0 "#PWR021" H 3900 3500 50  0001 C CNN
F 1 "GND" H 3903 3624 50  0000 C CNN
F 2 "" H 3800 3400 50  0001 C CNN
F 3 "" H 3900 3750 50  0001 C CNN
	1    3900 3750
	1    0    0    -1  
$EndComp
$Comp
L Device:Ferrite_Bead FB?
U 1 1 5F3148E5
P 4150 3250
AR Path="/5F3148E5" Ref="FB?"  Part="1" 
AR Path="/5F302051/5F3148E5" Ref="FB1"  Part="1" 
F 0 "FB1" V 3876 3250 50  0000 C CNN
F 1 "33R, 3A" V 3967 3250 50  0000 C CNN
F 2 "Inductor_SMD:L_0603_1608Metric" V 4080 3250 50  0001 C CNN
F 3 "~" H 4150 3250 50  0001 C CNN
F 4 "BLM18PG330SN1D" V 4150 3250 50  0001 C CNN "MPN"
	1    4150 3250
	0    1    1    0   
$EndComp
Wire Wire Line
	4000 3250 3900 3250
$Comp
L Device:C C?
U 1 1 5F3148ED
P 4400 3500
AR Path="/5F3148ED" Ref="C?"  Part="1" 
AR Path="/5F302051/5F3148ED" Ref="C19"  Part="1" 
F 0 "C19" H 4450 3600 50  0000 L CNN
F 1 "4u7" H 4450 3400 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 4438 3350 50  0001 C CNN
F 3 "~" H 4400 3500 50  0001 C CNN
F 4 "CL10A475KA8NQNC" H 4400 3500 50  0001 C CNN "MPN"
	1    4400 3500
	1    0    0    -1  
$EndComp
Wire Wire Line
	4400 3250 4400 3350
Wire Wire Line
	4400 3650 4400 3750
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148F5
P 4400 3750
AR Path="/5F3148F5" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148F5" Ref="#PWR022"  Part="1" 
F 0 "#PWR022" H 4400 3500 50  0001 C CNN
F 1 "GND" H 4403 3624 50  0000 C CNN
F 2 "" H 4300 3400 50  0001 C CNN
F 3 "" H 4400 3750 50  0001 C CNN
	1    4400 3750
	1    0    0    -1  
$EndComp
Wire Wire Line
	4300 3250 4400 3250
Connection ~ 4400 3250
Wire Wire Line
	4400 3250 4500 3250
Text GLabel 4500 3250 2    50   UnSpc ~ 0
USB_5V
Text GLabel 3800 4150 0    50   UnSpc ~ 0
USB_5V
$Comp
L ng_conn:USB_B_Micro J?
U 1 1 5F314899
P 2850 3450
AR Path="/5F314899" Ref="J?"  Part="1" 
AR Path="/5F302051/5F314899" Ref="J5"  Part="1" 
F 0 "J5" H 2650 3900 50  0000 L CNN
F 1 "USB_B_Micro" H 2650 3800 50  0000 L CNN
F 2 "Connector_USB:USB_Micro-B_Molex_47346-0001" H 3000 3450 50  0001 C CNN
F 3 "https://www.molex.com/pdm_docs/sd/473460001_sd.pdf" H 3000 3450 50  0001 C CNN
F 4 "47346-0001" H 2850 3450 50  0001 C CNN "MPN"
	1    2850 3450
	1    0    0    -1  
$EndComp
Text Label 2750 4200 1    50   ~ 0
USB_SHD
Connection ~ 2750 4050
Wire Wire Line
	2750 4250 2750 4050
Wire Wire Line
	2850 4250 2750 4250
Wire Wire Line
	2750 4050 2750 3850
Wire Wire Line
	2850 4050 2750 4050
Wire Wire Line
	3250 4250 3250 4350
Connection ~ 3250 4250
Wire Wire Line
	3150 4250 3250 4250
Wire Wire Line
	3250 4050 3250 4250
Connection ~ 3250 4050
Wire Wire Line
	3150 4050 3250 4050
$Comp
L Device:C C?
U 1 1 5F314906
P 3000 4250
AR Path="/5F314906" Ref="C?"  Part="1" 
AR Path="/5F302051/5F314906" Ref="C20"  Part="1" 
F 0 "C20" V 2850 4250 50  0000 C CNN
F 1 "10n" V 2750 4250 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3038 4100 50  0001 C CNN
F 3 "~" H 3000 4250 50  0001 C CNN
F 4 "CL10B103KC8NNNC" H 3000 4250 50  0001 C CNN "MPN"
	1    3000 4250
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R?
U 1 1 5F314900
P 3000 4050
AR Path="/5F314900" Ref="R?"  Part="1" 
AR Path="/5F302051/5F314900" Ref="R2"  Part="1" 
F 0 "R2" V 2800 4050 50  0000 C CNN
F 1 "100k" V 2900 4050 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 2930 4050 50  0001 C CNN
F 3 "~" H 3000 4050 50  0001 C CNN
F 4 "RC0603JR-07100KL" H 3000 4050 50  0001 C CNN "MPN"
	1    3000 4050
	0    1    1    0   
$EndComp
Text GLabel 3250 3450 2    50   Input ~ 0
USB_D+
Text GLabel 3250 3350 2    50   Input ~ 0
USB_D-
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148A5
P 3250 4350
AR Path="/5F3148A5" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148A5" Ref="#PWR023"  Part="1" 
F 0 "#PWR023" H 3250 4100 50  0001 C CNN
F 1 "GND" H 3253 4224 50  0000 C CNN
F 2 "" H 3150 4000 50  0001 C CNN
F 3 "" H 3250 4350 50  0001 C CNN
	1    3250 4350
	1    0    0    -1  
$EndComp
Wire Wire Line
	3150 3450 3250 3450
Wire Wire Line
	3150 3350 3250 3350
Wire Wire Line
	3150 3250 3900 3250
Wire Wire Line
	3250 3650 3250 4050
Wire Wire Line
	3150 3650 3250 3650
NoConn ~ 3150 3550
Connection ~ 3900 3250
Text Label 3250 3250 0    50   ~ 0
USB_VBUS
Text Notes 4200 5150 0    50   ~ 0
USB_DETn < 3.3V\nfor compatibility\nwith FPGA IO bank
$EndSCHEMATC
