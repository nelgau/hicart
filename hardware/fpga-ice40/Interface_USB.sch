EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 8 13
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
P 6750 2950
AR Path="/5F314850" Ref="U?"  Part="1" 
AR Path="/5F302051/5F314850" Ref="U9"  Part="1" 
F 0 "U9" H 6750 3500 50  0000 L CNN
F 1 "FT245RL" H 6750 3400 50  0000 L CNN
F 2 "Package_SO:SSOP-28_5.3x10.2mm_P0.65mm" H 6900 3400 50  0001 C CNN
F 3 "https://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT245R.pdf" H 6900 3400 50  0001 C CNN
F 4 "FT245RL-REEL" H 6750 2950 50  0001 C CNN "MPN"
	1    6750 2950
	1    0    0    -1  
$EndComp
Wire Wire Line
	6500 4050 6500 3950
Wire Wire Line
	6500 3950 6600 3950
Wire Wire Line
	6500 4350 6500 4450
Wire Wire Line
	7600 4450 7600 4300
Wire Wire Line
	7200 4300 7200 4450
Connection ~ 7200 4450
Wire Wire Line
	7200 4450 7300 4450
Wire Wire Line
	7300 4300 7300 4450
Connection ~ 7300 4450
Wire Wire Line
	7300 4450 7400 4450
Wire Wire Line
	7400 4300 7400 4450
Connection ~ 7400 4450
Wire Wire Line
	7400 4450 7500 4450
Wire Wire Line
	7500 4300 7500 4450
Connection ~ 7500 4450
Wire Wire Line
	7500 4450 7600 4450
NoConn ~ 6600 3750
$Comp
L Device:C C?
U 1 1 5F31486F
P 6500 4200
AR Path="/5F31486F" Ref="C?"  Part="1" 
AR Path="/5F302051/5F31486F" Ref="C22"  Part="1" 
F 0 "C22" H 6550 4300 50  0000 L CNN
F 1 "100n" H 6550 4100 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 6538 4050 50  0001 C CNN
F 3 "~" H 6500 4200 50  0001 C CNN
F 4 "CL10B104KB8NNNC" H 6500 4200 50  0001 C CNN "MPN"
	1    6500 4200
	1    0    0    -1  
$EndComp
Text GLabel 8150 2650 2    50   Input ~ 0
FIFO_D0
Text GLabel 8150 2750 2    50   Input ~ 0
FIFO_D1
Text GLabel 8150 2850 2    50   Input ~ 0
FIFO_D2
Text GLabel 8150 2950 2    50   Input ~ 0
FIFO_D3
Text GLabel 8150 3050 2    50   Input ~ 0
FIFO_D4
Text GLabel 8150 3250 2    50   Input ~ 0
FIFO_D6
Text GLabel 8150 3350 2    50   Input ~ 0
FIFO_D7
Text GLabel 8150 3150 2    50   Input ~ 0
FIFO_D5
Text GLabel 8150 3550 2    50   Input ~ 0
FIFO_RXFn
Text GLabel 8150 3750 2    50   Input ~ 0
FIFO_RDn
Text GLabel 8150 3850 2    50   Input ~ 0
FIFO_WR
Text GLabel 8150 3650 2    50   Input ~ 0
FIFO_TXEn
$Comp
L Device:R R?
U 1 1 5F314883
P 8750 3800
AR Path="/5F314883" Ref="R?"  Part="1" 
AR Path="/5F302051/5F314883" Ref="R4"  Part="1" 
F 0 "R4" H 8820 3846 50  0000 L CNN
F 1 "10k" H 8820 3755 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 8680 3800 50  0001 C CNN
F 3 "~" H 8750 3800 50  0001 C CNN
F 4 "RC0603FR-0710KL" H 8750 3800 50  0001 C CNN "MPN"
	1    8750 3800
	1    0    0    -1  
$EndComp
Wire Wire Line
	8150 4050 8750 4050
Wire Wire Line
	8750 4050 8750 3950
Wire Wire Line
	8750 3650 8750 3550
Text GLabel 8850 3550 2    50   UnSpc ~ 0
P3V3
Wire Wire Line
	8750 3550 8850 3550
Text Label 8200 4050 0    50   ~ 0
USB_PWRENn
$Comp
L Device:R R?
U 1 1 5F3148AD
P 2450 4900
AR Path="/5F3148AD" Ref="R?"  Part="1" 
AR Path="/5F302051/5F3148AD" Ref="R3"  Part="1" 
F 0 "R3" H 2520 4946 50  0000 L CNN
F 1 "6k8" H 2520 4855 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 2380 4900 50  0001 C CNN
F 3 "~" H 2450 4900 50  0001 C CNN
F 4 "RC0603FR-076K8L" H 2450 4900 50  0001 C CNN "MPN"
	1    2450 4900
	1    0    0    -1  
$EndComp
Wire Wire Line
	2450 5550 2450 5650
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148BA
P 2450 5650
AR Path="/5F3148BA" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148BA" Ref="#PWR024"  Part="1" 
F 0 "#PWR024" H 2450 5400 50  0001 C CNN
F 1 "GND" H 2453 5524 50  0000 C CNN
F 2 "" H 2350 5300 50  0001 C CNN
F 3 "" H 2450 5650 50  0001 C CNN
	1    2450 5650
	1    0    0    -1  
$EndComp
Wire Wire Line
	2450 5050 2450 5150
Wire Wire Line
	2450 4750 2450 4650
Wire Wire Line
	2450 4650 2350 4650
Wire Wire Line
	2450 5150 2800 5150
Connection ~ 2450 5150
Wire Wire Line
	2450 5150 2450 5250
Text GLabel 2900 5150 2    50   Input ~ 0
USB_DETn
Wire Wire Line
	6500 4450 7200 4450
$Comp
L Device:C C?
U 1 1 5F3148D5
P 3350 3100
AR Path="/5F3148D5" Ref="C?"  Part="1" 
AR Path="/5F302051/5F3148D5" Ref="C18"  Part="1" 
F 0 "C18" H 3400 3200 50  0000 L CNN
F 1 "100n" H 3400 3000 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3388 2950 50  0001 C CNN
F 3 "~" H 3350 3100 50  0001 C CNN
F 4 "CL10B104KB8NNNC" H 3350 3100 50  0001 C CNN "MPN"
	1    3350 3100
	1    0    0    -1  
$EndComp
Wire Wire Line
	3350 2850 3350 2950
Wire Wire Line
	3350 3250 3350 3350
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148DE
P 3350 3350
AR Path="/5F3148DE" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148DE" Ref="#PWR021"  Part="1" 
F 0 "#PWR021" H 3350 3100 50  0001 C CNN
F 1 "GND" H 3353 3224 50  0000 C CNN
F 2 "" H 3250 3000 50  0001 C CNN
F 3 "" H 3350 3350 50  0001 C CNN
	1    3350 3350
	1    0    0    -1  
$EndComp
$Comp
L Device:Ferrite_Bead FB?
U 1 1 5F3148E5
P 3600 2850
AR Path="/5F3148E5" Ref="FB?"  Part="1" 
AR Path="/5F302051/5F3148E5" Ref="FB1"  Part="1" 
F 0 "FB1" V 3326 2850 50  0000 C CNN
F 1 "33R, 3A" V 3417 2850 50  0000 C CNN
F 2 "Inductor_SMD:L_0603_1608Metric" V 3530 2850 50  0001 C CNN
F 3 "~" H 3600 2850 50  0001 C CNN
F 4 "BLM18PG330SN1D" V 3600 2850 50  0001 C CNN "MPN"
	1    3600 2850
	0    1    1    0   
$EndComp
Wire Wire Line
	3450 2850 3350 2850
$Comp
L Device:C C?
U 1 1 5F3148ED
P 4150 3100
AR Path="/5F3148ED" Ref="C?"  Part="1" 
AR Path="/5F302051/5F3148ED" Ref="C19"  Part="1" 
F 0 "C19" H 4200 3200 50  0000 L CNN
F 1 "4u7" H 4200 3000 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 4188 2950 50  0001 C CNN
F 3 "~" H 4150 3100 50  0001 C CNN
F 4 "CL10A475KA8NQNC" H 4150 3100 50  0001 C CNN "MPN"
	1    4150 3100
	1    0    0    -1  
$EndComp
Wire Wire Line
	4150 2850 4150 2950
Wire Wire Line
	4150 3250 4150 3350
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148F5
P 4150 3350
AR Path="/5F3148F5" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148F5" Ref="#PWR022"  Part="1" 
F 0 "#PWR022" H 4150 3100 50  0001 C CNN
F 1 "GND" H 4153 3224 50  0000 C CNN
F 2 "" H 4050 3000 50  0001 C CNN
F 3 "" H 4150 3350 50  0001 C CNN
	1    4150 3350
	1    0    0    -1  
$EndComp
Text GLabel 4250 2850 2    50   UnSpc ~ 0
USB_5V
Text GLabel 2350 4650 0    50   UnSpc ~ 0
USB_5V
$Comp
L ng_conn:USB_B_Micro J?
U 1 1 5F314899
P 2300 3050
AR Path="/5F314899" Ref="J?"  Part="1" 
AR Path="/5F302051/5F314899" Ref="J5"  Part="1" 
F 0 "J5" H 2100 3500 50  0000 L CNN
F 1 "USB_B_Micro" H 2100 3400 50  0000 L CNN
F 2 "Connector_USB:USB_Micro-B_Molex_47346-0001" H 2450 3050 50  0001 C CNN
F 3 "https://www.molex.com/pdm_docs/sd/473460001_sd.pdf" H 2450 3050 50  0001 C CNN
F 4 "47346-0001" H 2300 3050 50  0001 C CNN "MPN"
	1    2300 3050
	1    0    0    -1  
$EndComp
Text Label 2200 3800 1    50   ~ 0
USB_SHD
Connection ~ 2200 3650
Wire Wire Line
	2200 3850 2200 3650
Wire Wire Line
	2300 3850 2200 3850
Wire Wire Line
	2200 3650 2200 3450
Wire Wire Line
	2300 3650 2200 3650
Wire Wire Line
	2700 3850 2700 3950
Connection ~ 2700 3850
Wire Wire Line
	2600 3850 2700 3850
Wire Wire Line
	2700 3650 2700 3850
Connection ~ 2700 3650
Wire Wire Line
	2600 3650 2700 3650
$Comp
L Device:C C?
U 1 1 5F314906
P 2450 3850
AR Path="/5F314906" Ref="C?"  Part="1" 
AR Path="/5F302051/5F314906" Ref="C20"  Part="1" 
F 0 "C20" V 2300 3850 50  0000 C CNN
F 1 "10n" V 2200 3850 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 2488 3700 50  0001 C CNN
F 3 "~" H 2450 3850 50  0001 C CNN
F 4 "CL10B103KC8NNNC" H 2450 3850 50  0001 C CNN "MPN"
	1    2450 3850
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R?
U 1 1 5F314900
P 2450 3650
AR Path="/5F314900" Ref="R?"  Part="1" 
AR Path="/5F302051/5F314900" Ref="R2"  Part="1" 
F 0 "R2" V 2250 3650 50  0000 C CNN
F 1 "100k" V 2350 3650 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 2380 3650 50  0001 C CNN
F 3 "~" H 2450 3650 50  0001 C CNN
F 4 "RC0603JR-07100KL" H 2450 3650 50  0001 C CNN "MPN"
	1    2450 3650
	0    1    1    0   
$EndComp
Text GLabel 2700 3050 2    50   Input ~ 0
xUSB_D+
Text GLabel 2700 2950 2    50   Input ~ 0
xUSB_D-
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148A5
P 2700 3950
AR Path="/5F3148A5" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148A5" Ref="#PWR023"  Part="1" 
F 0 "#PWR023" H 2700 3700 50  0001 C CNN
F 1 "GND" H 2703 3824 50  0000 C CNN
F 2 "" H 2600 3600 50  0001 C CNN
F 3 "" H 2700 3950 50  0001 C CNN
	1    2700 3950
	1    0    0    -1  
$EndComp
Wire Wire Line
	2600 3050 2700 3050
Wire Wire Line
	2600 2950 2700 2950
Wire Wire Line
	2600 2850 3350 2850
Wire Wire Line
	2700 3250 2700 3650
Wire Wire Line
	2600 3250 2700 3250
NoConn ~ 2600 3150
Connection ~ 3350 2850
Text Label 2700 2850 0    50   ~ 0
USB_VBUS
Text Notes 2800 5000 0    50   ~ 0
USB_DETn < 3.3V\nfor compatibility\nwith FPGA IO bank
$Comp
L Power_Protection:USBLC6-2SC6 U11
U 1 1 5F06782E
P 4600 5200
F 0 "U11" H 4750 5650 50  0000 L CNN
F 1 "USBLC6-2SC6" H 4750 5550 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23-6" H 3850 5600 50  0001 C CNN
F 3 "http://www2.st.com/resource/en/datasheet/CD00050750.pdf" H 4800 5550 50  0001 C CNN
	1    4600 5200
	1    0    0    -1  
$EndComp
Text GLabel 4100 5300 0    50   Input ~ 0
xUSB_D-
Text GLabel 5100 5300 2    50   Input ~ 0
xUSB_D+
Text GLabel 4100 5100 0    50   Input ~ 0
USB_D-
Text GLabel 5100 5100 2    50   Input ~ 0
USB_D+
Wire Wire Line
	4150 4600 4600 4600
Wire Wire Line
	4600 4600 4600 4700
Wire Wire Line
	4600 5700 4600 5800
$Comp
L ng_power:GND #PWR?
U 1 1 5F084D77
P 4600 5800
AR Path="/5F084D77" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F084D77" Ref="#PWR036"  Part="1" 
F 0 "#PWR036" H 4600 5550 50  0001 C CNN
F 1 "GND" H 4603 5674 50  0000 C CNN
F 2 "" H 4500 5450 50  0001 C CNN
F 3 "" H 4600 5800 50  0001 C CNN
	1    4600 5800
	1    0    0    -1  
$EndComp
Text Label 4150 4600 0    50   ~ 0
USB_VBUS
Text Notes 2950 3800 0    50   ~ 0
USBLC6 requires 100n (C18) on VBUS,\nnot 10n as would be expected
Wire Wire Line
	3750 2850 3850 2850
$Comp
L Device:C C?
U 1 1 5F099C98
P 3850 3100
AR Path="/5F099C98" Ref="C?"  Part="1" 
AR Path="/5F302051/5F099C98" Ref="C48"  Part="1" 
F 0 "C48" H 3900 3200 50  0000 L CNN
F 1 "100n" H 3900 3000 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3888 2950 50  0001 C CNN
F 3 "~" H 3850 3100 50  0001 C CNN
F 4 "CL10B104KB8NNNC" H 3850 3100 50  0001 C CNN "MPN"
	1    3850 3100
	1    0    0    -1  
$EndComp
Wire Wire Line
	3850 2850 3850 2950
Wire Wire Line
	3850 3250 3850 3350
$Comp
L ng_power:GND #PWR?
U 1 1 5F099CA4
P 3850 3350
AR Path="/5F099CA4" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F099CA4" Ref="#PWR037"  Part="1" 
F 0 "#PWR037" H 3850 3100 50  0001 C CNN
F 1 "GND" H 3853 3224 50  0000 C CNN
F 2 "" H 3750 3000 50  0001 C CNN
F 3 "" H 3850 3350 50  0001 C CNN
	1    3850 3350
	1    0    0    -1  
$EndComp
Connection ~ 3850 2850
Wire Wire Line
	3850 2850 4150 2850
Connection ~ 4150 2850
Wire Wire Line
	4150 2850 4250 2850
Wire Wire Line
	2800 5250 2800 5150
Connection ~ 2800 5150
Wire Wire Line
	2800 5150 2900 5150
Wire Wire Line
	2800 5550 2800 5650
$Comp
L ng_power:GND #PWR?
U 1 1 5F312C25
P 2800 5650
AR Path="/5F312C25" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F312C25" Ref="#PWR039"  Part="1" 
F 0 "#PWR039" H 2800 5400 50  0001 C CNN
F 1 "GND" H 2803 5524 50  0000 C CNN
F 2 "" H 2700 5300 50  0001 C CNN
F 3 "" H 2800 5650 50  0001 C CNN
	1    2800 5650
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 5F3148B3
P 2450 5400
AR Path="/5F3148B3" Ref="R?"  Part="1" 
AR Path="/5F302051/5F3148B3" Ref="R5"  Part="1" 
F 0 "R5" H 2520 5446 50  0000 L CNN
F 1 "10k" H 2520 5355 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 2380 5400 50  0001 C CNN
F 3 "~" H 2450 5400 50  0001 C CNN
F 4 "RC0603FR-0710KL" H 2450 5400 50  0001 C CNN "MPN"
	1    2450 5400
	1    0    0    -1  
$EndComp
$Comp
L Device:C C49
U 1 1 5F31C8F6
P 2800 5400
F 0 "C49" H 2915 5446 50  0000 L CNN
F 1 "DNP" H 2915 5355 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 2838 5250 50  0001 C CNN
F 3 "~" H 2800 5400 50  0001 C CNN
	1    2800 5400
	1    0    0    -1  
$EndComp
Connection ~ 6500 4450
Wire Wire Line
	5950 3050 5950 3150
$Comp
L Device:C C?
U 1 1 5F110C16
P 5950 2900
AR Path="/5F110C16" Ref="C?"  Part="1" 
AR Path="/5F302051/5F110C16" Ref="C50"  Part="1" 
F 0 "C50" H 6000 3000 50  0000 L CNN
F 1 "100n" H 6000 2800 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 5988 2750 50  0001 C CNN
F 3 "~" H 5950 2900 50  0001 C CNN
F 4 "CL10B104KB8NNNC" H 5950 2900 50  0001 C CNN "MPN"
	1    5950 2900
	1    0    0    -1  
$EndComp
Text GLabel 5550 2650 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	5650 3150 5950 3150
Wire Wire Line
	5650 3050 5650 3150
$Comp
L Device:C C?
U 1 1 5F3148C7
P 5650 2900
AR Path="/5F3148C7" Ref="C?"  Part="1" 
AR Path="/5F302051/5F3148C7" Ref="C21"  Part="1" 
F 0 "C21" H 5700 3000 50  0000 L CNN
F 1 "100n" H 5700 2800 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 5688 2750 50  0001 C CNN
F 3 "~" H 5650 2900 50  0001 C CNN
F 4 "CL10B104KB8NNNC" H 5650 2900 50  0001 C CNN "MPN"
	1    5650 2900
	1    0    0    -1  
$EndComp
Wire Wire Line
	6500 4550 6500 4450
$Comp
L ng_power:GND #PWR?
U 1 1 5F314866
P 6500 4550
AR Path="/5F314866" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F314866" Ref="#PWR025"  Part="1" 
F 0 "#PWR025" H 6500 4300 50  0001 C CNN
F 1 "GND" H 6503 4424 50  0000 C CNN
F 2 "" H 6400 4200 50  0001 C CNN
F 3 "" H 6500 4550 50  0001 C CNN
	1    6500 4550
	1    0    0    -1  
$EndComp
Text GLabel 6600 3350 0    50   Input ~ 0
USB_DETn
Text GLabel 6600 3050 0    50   Input ~ 0
USB_D+
Text GLabel 6600 2950 0    50   Input ~ 0
USB_D-
Wire Wire Line
	6500 2650 6600 2650
Wire Wire Line
	6500 2650 6500 2750
Wire Wire Line
	6500 2750 6600 2750
Wire Wire Line
	6500 2650 5950 2650
Connection ~ 6500 2650
Wire Wire Line
	5650 2750 5650 2650
Connection ~ 5650 2650
Wire Wire Line
	5650 2650 5550 2650
Wire Wire Line
	5950 2750 5950 2650
Connection ~ 5950 2650
Wire Wire Line
	5950 2650 5650 2650
Wire Wire Line
	5650 3250 5650 3150
$Comp
L ng_power:GND #PWR?
U 1 1 5F0EA5AA
P 5650 3250
AR Path="/5F0EA5AA" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F0EA5AA" Ref="#PWR05"  Part="1" 
F 0 "#PWR05" H 5650 3000 50  0001 C CNN
F 1 "GND" H 5653 3124 50  0000 C CNN
F 2 "" H 5550 2900 50  0001 C CNN
F 3 "" H 5650 3250 50  0001 C CNN
	1    5650 3250
	1    0    0    -1  
$EndComp
Connection ~ 5650 3150
Wire Wire Line
	6500 3950 6400 3950
Connection ~ 6500 3950
Text Label 6400 3950 2    50   ~ 0
USB_3V3
Text Label 6400 3650 2    50   ~ 0
USB_CLK
$Comp
L Oscillator:ECS-2520MV-xxx-xx X?
U 1 1 5F1A94D9
P 7400 5500
AR Path="/5F1A94D9" Ref="X?"  Part="1" 
AR Path="/5F5B53E5/5F1A94D9" Ref="X?"  Part="1" 
AR Path="/5F302051/5F1A94D9" Ref="X2"  Part="1" 
F 0 "X2" H 7100 5750 50  0000 L CNN
F 1 "12MHz" H 7500 5750 50  0000 L CNN
F 2 "ng_time:Oscillator_2.5x2.0" H 7850 5150 50  0001 C CNN
F 3 "https://ecsxtal.com/store/pdf/ECS-2520MV.pdf" H 7225 5625 50  0001 C CNN
F 4 "ECS-2520MV-120-BN-TR" H 7400 5500 50  0001 C CNN "MPN"
	1    7400 5500
	1    0    0    -1  
$EndComp
$Comp
L ng_power:GND #PWR?
U 1 1 5F1A94DF
P 7400 5900
AR Path="/5F1A94DF" Ref="#PWR?"  Part="1" 
AR Path="/5F5B53E5/5F1A94DF" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F1A94DF" Ref="#PWR041"  Part="1" 
F 0 "#PWR041" H 7400 5650 50  0001 C CNN
F 1 "GND" H 7403 5774 50  0000 C CNN
F 2 "" H 7300 5550 50  0001 C CNN
F 3 "" H 7400 5900 50  0001 C CNN
	1    7400 5900
	1    0    0    -1  
$EndComp
Text GLabel 6600 5100 0    50   UnSpc ~ 0
P3V3
Wire Wire Line
	7000 5500 6900 5500
Wire Wire Line
	6900 5100 7400 5100
Wire Wire Line
	7400 5100 7400 5200
Wire Wire Line
	7400 5900 7400 5800
$Comp
L ng_power:GND #PWR?
U 1 1 5F1A94EB
P 6700 5600
AR Path="/5F1A94EB" Ref="#PWR?"  Part="1" 
AR Path="/5F5B53E5/5F1A94EB" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F1A94EB" Ref="#PWR040"  Part="1" 
F 0 "#PWR040" H 6700 5350 50  0001 C CNN
F 1 "GND" H 6703 5474 50  0000 C CNN
F 2 "" H 6600 5250 50  0001 C CNN
F 3 "" H 6700 5600 50  0001 C CNN
	1    6700 5600
	1    0    0    -1  
$EndComp
Wire Wire Line
	6700 5600 6700 5500
Connection ~ 6900 5100
Wire Wire Line
	6900 5100 6900 5500
Wire Wire Line
	6600 5100 6700 5100
Wire Wire Line
	6700 5200 6700 5100
Connection ~ 6700 5100
Wire Wire Line
	6700 5100 6900 5100
$Comp
L Device:C C?
U 1 1 5F1A94F9
P 6700 5350
AR Path="/5F1A94F9" Ref="C?"  Part="1" 
AR Path="/5F5B53E5/5F1A94F9" Ref="C?"  Part="1" 
AR Path="/5F302051/5F1A94F9" Ref="C55"  Part="1" 
F 0 "C55" H 6600 5400 50  0000 R CNN
F 1 "100n" H 6600 5300 50  0000 R CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 6738 5200 50  0001 C CNN
F 3 "~" H 6700 5350 50  0001 C CNN
F 4 "CL10B104KB8NNNC" H 6700 5350 50  0001 C CNN "MPN"
	1    6700 5350
	1    0    0    -1  
$EndComp
Wire Wire Line
	6400 3650 6600 3650
Wire Wire Line
	7800 5500 7900 5500
Text Label 7900 5500 0    50   ~ 0
USB_CLK
$EndSCHEMATC
