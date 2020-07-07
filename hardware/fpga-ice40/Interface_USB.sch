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
P 7250 2750
AR Path="/5F314850" Ref="U?"  Part="1" 
AR Path="/5F302051/5F314850" Ref="U9"  Part="1" 
F 0 "U9" H 7250 3300 50  0000 L CNN
F 1 "FT245RL" H 7250 3200 50  0000 L CNN
F 2 "Package_SO:SSOP-28_5.3x10.2mm_P0.65mm" H 7400 3200 50  0001 C CNN
F 3 "https://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT245R.pdf" H 7400 3200 50  0001 C CNN
F 4 "FT245RL-REEL" H 7250 2750 50  0001 C CNN "MPN"
	1    7250 2750
	1    0    0    -1  
$EndComp
Wire Wire Line
	7000 3850 7000 3750
Wire Wire Line
	7000 3750 7100 3750
Wire Wire Line
	7000 4150 7000 4250
Wire Wire Line
	8100 4250 8100 4100
Wire Wire Line
	7700 4100 7700 4250
Connection ~ 7700 4250
Wire Wire Line
	7700 4250 7800 4250
Wire Wire Line
	7800 4100 7800 4250
Connection ~ 7800 4250
Wire Wire Line
	7800 4250 7900 4250
Wire Wire Line
	7900 4100 7900 4250
Connection ~ 7900 4250
Wire Wire Line
	7900 4250 8000 4250
Wire Wire Line
	8000 4100 8000 4250
Connection ~ 8000 4250
Wire Wire Line
	8000 4250 8100 4250
$Comp
L ng_power:GND #PWR?
U 1 1 5F314866
P 6700 4350
AR Path="/5F314866" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F314866" Ref="#PWR025"  Part="1" 
F 0 "#PWR025" H 6700 4100 50  0001 C CNN
F 1 "GND" H 6703 4224 50  0000 C CNN
F 2 "" H 6600 4000 50  0001 C CNN
F 3 "" H 6700 4350 50  0001 C CNN
	1    6700 4350
	1    0    0    -1  
$EndComp
Wire Wire Line
	6700 4350 6700 4250
NoConn ~ 7100 3450
NoConn ~ 7100 3550
$Comp
L Device:C C?
U 1 1 5F31486F
P 7000 4000
AR Path="/5F31486F" Ref="C?"  Part="1" 
AR Path="/5F302051/5F31486F" Ref="C22"  Part="1" 
F 0 "C22" H 7050 4100 50  0000 L CNN
F 1 "100n" H 7050 3900 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 7038 3850 50  0001 C CNN
F 3 "~" H 7000 4000 50  0001 C CNN
F 4 "CL10B104KB8NNNC" H 7000 4000 50  0001 C CNN "MPN"
	1    7000 4000
	1    0    0    -1  
$EndComp
Text GLabel 6600 2750 0    50   Input ~ 0
USB_D-
Text GLabel 6600 2850 0    50   Input ~ 0
USB_D+
Text GLabel 8650 2450 2    50   Input ~ 0
FIFO_D0
Text GLabel 8650 2550 2    50   Input ~ 0
FIFO_D1
Text GLabel 8650 2650 2    50   Input ~ 0
FIFO_D2
Text GLabel 8650 2750 2    50   Input ~ 0
FIFO_D3
Text GLabel 8650 2850 2    50   Input ~ 0
FIFO_D4
Text GLabel 8650 3050 2    50   Input ~ 0
FIFO_D6
Text GLabel 8650 3150 2    50   Input ~ 0
FIFO_D7
Text GLabel 8650 2950 2    50   Input ~ 0
FIFO_D5
Text GLabel 8650 3350 2    50   Input ~ 0
FIFO_RXFn
Text GLabel 8650 3550 2    50   Input ~ 0
FIFO_RDn
Text GLabel 8650 3650 2    50   Input ~ 0
FIFO_WR
Text GLabel 8650 3450 2    50   Input ~ 0
FIFO_TXEn
$Comp
L Device:R R?
U 1 1 5F314883
P 9250 3600
AR Path="/5F314883" Ref="R?"  Part="1" 
AR Path="/5F302051/5F314883" Ref="R4"  Part="1" 
F 0 "R4" H 9320 3646 50  0000 L CNN
F 1 "10k" H 9320 3555 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 9180 3600 50  0001 C CNN
F 3 "~" H 9250 3600 50  0001 C CNN
F 4 "RC0603FR-0710KL" H 9250 3600 50  0001 C CNN "MPN"
	1    9250 3600
	1    0    0    -1  
$EndComp
Wire Wire Line
	8650 3850 9250 3850
Wire Wire Line
	9250 3850 9250 3750
Wire Wire Line
	9250 3450 9250 3350
Wire Wire Line
	7000 2550 7100 2550
Text GLabel 9350 3350 2    50   UnSpc ~ 0
P3V3
Wire Wire Line
	9250 3350 9350 3350
Wire Wire Line
	7000 3750 7000 2550
Connection ~ 7000 3750
Wire Wire Line
	6600 2750 7100 2750
Wire Wire Line
	6600 2850 7100 2850
Wire Wire Line
	6600 2450 6700 2450
Text GLabel 6600 2450 0    50   UnSpc ~ 0
USB_5V
Wire Wire Line
	6600 3150 7100 3150
Text GLabel 6600 3150 0    50   Input ~ 0
USB_DETn
Text Label 7000 3700 1    50   ~ 0
USB_VIO
Text Label 8700 3850 0    50   ~ 0
USB_PWRENn
$Comp
L Device:R R?
U 1 1 5F3148AD
P 3050 4450
AR Path="/5F3148AD" Ref="R?"  Part="1" 
AR Path="/5F302051/5F3148AD" Ref="R3"  Part="1" 
F 0 "R3" H 3120 4496 50  0000 L CNN
F 1 "6k8" H 3120 4405 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 2980 4450 50  0001 C CNN
F 3 "~" H 3050 4450 50  0001 C CNN
F 4 "RC0603FR-076K8L" H 3050 4450 50  0001 C CNN "MPN"
	1    3050 4450
	1    0    0    -1  
$EndComp
Wire Wire Line
	3050 5100 3050 5200
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148BA
P 3050 5200
AR Path="/5F3148BA" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148BA" Ref="#PWR024"  Part="1" 
F 0 "#PWR024" H 3050 4950 50  0001 C CNN
F 1 "GND" H 3053 5074 50  0000 C CNN
F 2 "" H 2950 4850 50  0001 C CNN
F 3 "" H 3050 5200 50  0001 C CNN
	1    3050 5200
	1    0    0    -1  
$EndComp
Wire Wire Line
	3050 4600 3050 4700
Wire Wire Line
	3050 4300 3050 4200
Wire Wire Line
	3050 4200 2950 4200
Wire Wire Line
	3050 4700 3400 4700
Connection ~ 3050 4700
Wire Wire Line
	3050 4700 3050 4800
Text GLabel 3500 4700 2    50   Input ~ 0
USB_DETn
$Comp
L Device:C C?
U 1 1 5F3148C7
P 6700 4000
AR Path="/5F3148C7" Ref="C?"  Part="1" 
AR Path="/5F302051/5F3148C7" Ref="C21"  Part="1" 
F 0 "C21" H 6750 4100 50  0000 L CNN
F 1 "100n" H 6750 3900 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 6738 3850 50  0001 C CNN
F 3 "~" H 6700 4000 50  0001 C CNN
F 4 "CL10B104KB8NNNC" H 6700 4000 50  0001 C CNN "MPN"
	1    6700 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	6700 3850 6700 2450
Connection ~ 6700 2450
Wire Wire Line
	6700 2450 7100 2450
Wire Wire Line
	6700 4150 6700 4250
Wire Wire Line
	6700 4250 7000 4250
Connection ~ 7000 4250
Connection ~ 6700 4250
Wire Wire Line
	7000 4250 7700 4250
$Comp
L Device:C C?
U 1 1 5F3148D5
P 3900 2700
AR Path="/5F3148D5" Ref="C?"  Part="1" 
AR Path="/5F302051/5F3148D5" Ref="C18"  Part="1" 
F 0 "C18" H 3950 2800 50  0000 L CNN
F 1 "100n" H 3950 2600 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3938 2550 50  0001 C CNN
F 3 "~" H 3900 2700 50  0001 C CNN
F 4 "CL10B104KB8NNNC" H 3900 2700 50  0001 C CNN "MPN"
	1    3900 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	3900 2450 3900 2550
Wire Wire Line
	3900 2850 3900 2950
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148DE
P 3900 2950
AR Path="/5F3148DE" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148DE" Ref="#PWR021"  Part="1" 
F 0 "#PWR021" H 3900 2700 50  0001 C CNN
F 1 "GND" H 3903 2824 50  0000 C CNN
F 2 "" H 3800 2600 50  0001 C CNN
F 3 "" H 3900 2950 50  0001 C CNN
	1    3900 2950
	1    0    0    -1  
$EndComp
$Comp
L Device:Ferrite_Bead FB?
U 1 1 5F3148E5
P 4150 2450
AR Path="/5F3148E5" Ref="FB?"  Part="1" 
AR Path="/5F302051/5F3148E5" Ref="FB1"  Part="1" 
F 0 "FB1" V 3876 2450 50  0000 C CNN
F 1 "33R, 3A" V 3967 2450 50  0000 C CNN
F 2 "Inductor_SMD:L_0603_1608Metric" V 4080 2450 50  0001 C CNN
F 3 "~" H 4150 2450 50  0001 C CNN
F 4 "BLM18PG330SN1D" V 4150 2450 50  0001 C CNN "MPN"
	1    4150 2450
	0    1    1    0   
$EndComp
Wire Wire Line
	4000 2450 3900 2450
$Comp
L Device:C C?
U 1 1 5F3148ED
P 4700 2700
AR Path="/5F3148ED" Ref="C?"  Part="1" 
AR Path="/5F302051/5F3148ED" Ref="C19"  Part="1" 
F 0 "C19" H 4750 2800 50  0000 L CNN
F 1 "4u7" H 4750 2600 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 4738 2550 50  0001 C CNN
F 3 "~" H 4700 2700 50  0001 C CNN
F 4 "CL10A475KA8NQNC" H 4700 2700 50  0001 C CNN "MPN"
	1    4700 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	4700 2450 4700 2550
Wire Wire Line
	4700 2850 4700 2950
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148F5
P 4700 2950
AR Path="/5F3148F5" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148F5" Ref="#PWR022"  Part="1" 
F 0 "#PWR022" H 4700 2700 50  0001 C CNN
F 1 "GND" H 4703 2824 50  0000 C CNN
F 2 "" H 4600 2600 50  0001 C CNN
F 3 "" H 4700 2950 50  0001 C CNN
	1    4700 2950
	1    0    0    -1  
$EndComp
Text GLabel 4800 2450 2    50   UnSpc ~ 0
USB_5V
Text GLabel 2950 4200 0    50   UnSpc ~ 0
USB_5V
$Comp
L ng_conn:USB_B_Micro J?
U 1 1 5F314899
P 2850 2650
AR Path="/5F314899" Ref="J?"  Part="1" 
AR Path="/5F302051/5F314899" Ref="J5"  Part="1" 
F 0 "J5" H 2650 3100 50  0000 L CNN
F 1 "USB_B_Micro" H 2650 3000 50  0000 L CNN
F 2 "Connector_USB:USB_Micro-B_Molex_47346-0001" H 3000 2650 50  0001 C CNN
F 3 "https://www.molex.com/pdm_docs/sd/473460001_sd.pdf" H 3000 2650 50  0001 C CNN
F 4 "47346-0001" H 2850 2650 50  0001 C CNN "MPN"
	1    2850 2650
	1    0    0    -1  
$EndComp
Text Label 2750 3400 1    50   ~ 0
USB_SHD
Connection ~ 2750 3250
Wire Wire Line
	2750 3450 2750 3250
Wire Wire Line
	2850 3450 2750 3450
Wire Wire Line
	2750 3250 2750 3050
Wire Wire Line
	2850 3250 2750 3250
Wire Wire Line
	3250 3450 3250 3550
Connection ~ 3250 3450
Wire Wire Line
	3150 3450 3250 3450
Wire Wire Line
	3250 3250 3250 3450
Connection ~ 3250 3250
Wire Wire Line
	3150 3250 3250 3250
$Comp
L Device:C C?
U 1 1 5F314906
P 3000 3450
AR Path="/5F314906" Ref="C?"  Part="1" 
AR Path="/5F302051/5F314906" Ref="C20"  Part="1" 
F 0 "C20" V 2850 3450 50  0000 C CNN
F 1 "10n" V 2750 3450 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3038 3300 50  0001 C CNN
F 3 "~" H 3000 3450 50  0001 C CNN
F 4 "CL10B103KC8NNNC" H 3000 3450 50  0001 C CNN "MPN"
	1    3000 3450
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R?
U 1 1 5F314900
P 3000 3250
AR Path="/5F314900" Ref="R?"  Part="1" 
AR Path="/5F302051/5F314900" Ref="R2"  Part="1" 
F 0 "R2" V 2800 3250 50  0000 C CNN
F 1 "100k" V 2900 3250 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 2930 3250 50  0001 C CNN
F 3 "~" H 3000 3250 50  0001 C CNN
F 4 "RC0603JR-07100KL" H 3000 3250 50  0001 C CNN "MPN"
	1    3000 3250
	0    1    1    0   
$EndComp
Text GLabel 3250 2650 2    50   Input ~ 0
xUSB_D+
Text GLabel 3250 2550 2    50   Input ~ 0
xUSB_D-
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148A5
P 3250 3550
AR Path="/5F3148A5" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148A5" Ref="#PWR023"  Part="1" 
F 0 "#PWR023" H 3250 3300 50  0001 C CNN
F 1 "GND" H 3253 3424 50  0000 C CNN
F 2 "" H 3150 3200 50  0001 C CNN
F 3 "" H 3250 3550 50  0001 C CNN
	1    3250 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	3150 2650 3250 2650
Wire Wire Line
	3150 2550 3250 2550
Wire Wire Line
	3150 2450 3900 2450
Wire Wire Line
	3250 2850 3250 3250
Wire Wire Line
	3150 2850 3250 2850
NoConn ~ 3150 2750
Connection ~ 3900 2450
Text Label 3250 2450 0    50   ~ 0
USB_VBUS
Text Notes 3400 4550 0    50   ~ 0
USB_DETn < 3.3V\nfor compatibility\nwith FPGA IO bank
$Comp
L Power_Protection:USBLC6-2SC6 U11
U 1 1 5F06782E
P 5200 4750
F 0 "U11" H 5350 5200 50  0000 L CNN
F 1 "USBLC6-2SC6" H 5350 5100 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23-6" H 4450 5150 50  0001 C CNN
F 3 "http://www2.st.com/resource/en/datasheet/CD00050750.pdf" H 5400 5100 50  0001 C CNN
	1    5200 4750
	1    0    0    -1  
$EndComp
Text GLabel 4700 4850 0    50   Input ~ 0
xUSB_D-
Text GLabel 5700 4850 2    50   Input ~ 0
xUSB_D+
Text GLabel 4700 4650 0    50   Input ~ 0
USB_D-
Text GLabel 5700 4650 2    50   Input ~ 0
USB_D+
Wire Wire Line
	4750 4150 5200 4150
Wire Wire Line
	5200 4150 5200 4250
Wire Wire Line
	5200 5250 5200 5350
$Comp
L ng_power:GND #PWR?
U 1 1 5F084D77
P 5200 5350
AR Path="/5F084D77" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F084D77" Ref="#PWR036"  Part="1" 
F 0 "#PWR036" H 5200 5100 50  0001 C CNN
F 1 "GND" H 5203 5224 50  0000 C CNN
F 2 "" H 5100 5000 50  0001 C CNN
F 3 "" H 5200 5350 50  0001 C CNN
	1    5200 5350
	1    0    0    -1  
$EndComp
Text Label 4750 4150 0    50   ~ 0
USB_VBUS
Text Notes 3500 3400 0    50   ~ 0
USBLC6 requires 100n (C18) on VBUS,\nnot 10n as would be expected
Wire Wire Line
	4300 2450 4400 2450
$Comp
L Device:C C?
U 1 1 5F099C98
P 4400 2700
AR Path="/5F099C98" Ref="C?"  Part="1" 
AR Path="/5F302051/5F099C98" Ref="C48"  Part="1" 
F 0 "C48" H 4450 2800 50  0000 L CNN
F 1 "100n" H 4450 2600 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 4438 2550 50  0001 C CNN
F 3 "~" H 4400 2700 50  0001 C CNN
F 4 "CL10B104KB8NNNC" H 4400 2700 50  0001 C CNN "MPN"
	1    4400 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	4400 2450 4400 2550
Wire Wire Line
	4400 2850 4400 2950
$Comp
L ng_power:GND #PWR?
U 1 1 5F099CA4
P 4400 2950
AR Path="/5F099CA4" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F099CA4" Ref="#PWR037"  Part="1" 
F 0 "#PWR037" H 4400 2700 50  0001 C CNN
F 1 "GND" H 4403 2824 50  0000 C CNN
F 2 "" H 4300 2600 50  0001 C CNN
F 3 "" H 4400 2950 50  0001 C CNN
	1    4400 2950
	1    0    0    -1  
$EndComp
Connection ~ 4400 2450
Wire Wire Line
	4400 2450 4700 2450
Connection ~ 4700 2450
Wire Wire Line
	4700 2450 4800 2450
Wire Wire Line
	3400 4800 3400 4700
Connection ~ 3400 4700
Wire Wire Line
	3400 4700 3500 4700
Wire Wire Line
	3400 5100 3400 5200
$Comp
L ng_power:GND #PWR?
U 1 1 5F312C25
P 3400 5200
AR Path="/5F312C25" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F312C25" Ref="#PWR039"  Part="1" 
F 0 "#PWR039" H 3400 4950 50  0001 C CNN
F 1 "GND" H 3403 5074 50  0000 C CNN
F 2 "" H 3300 4850 50  0001 C CNN
F 3 "" H 3400 5200 50  0001 C CNN
	1    3400 5200
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 5F3148B3
P 3050 4950
AR Path="/5F3148B3" Ref="R?"  Part="1" 
AR Path="/5F302051/5F3148B3" Ref="R5"  Part="1" 
F 0 "R5" H 3120 4996 50  0000 L CNN
F 1 "10k" H 3120 4905 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 2980 4950 50  0001 C CNN
F 3 "~" H 3050 4950 50  0001 C CNN
F 4 "RC0603FR-0710KL" H 3050 4950 50  0001 C CNN "MPN"
	1    3050 4950
	1    0    0    -1  
$EndComp
$Comp
L Device:C C49
U 1 1 5F31C8F6
P 3400 4950
F 0 "C49" H 3515 4996 50  0000 L CNN
F 1 "DNP" H 3515 4905 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3438 4800 50  0001 C CNN
F 3 "~" H 3400 4950 50  0001 C CNN
	1    3400 4950
	1    0    0    -1  
$EndComp
$EndSCHEMATC
