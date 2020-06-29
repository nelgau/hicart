EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 4 8
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
L ng_ftdi:FT245RL U?
U 1 1 5F314850
P 6600 3500
AR Path="/5F314850" Ref="U?"  Part="1" 
AR Path="/5F302051/5F314850" Ref="U7"  Part="1" 
F 0 "U7" H 7225 4065 50  0000 C CNN
F 1 "FT245RL" H 7225 3974 50  0000 C CNN
F 2 "Package_SO:SSOP-28_5.3x10.2mm_P0.65mm" H 6750 3950 50  0001 C CNN
F 3 "https://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT245R.pdf" H 6750 3950 50  0001 C CNN
	1    6600 3500
	1    0    0    -1  
$EndComp
Wire Wire Line
	6350 4600 6350 4500
Wire Wire Line
	6350 4500 6450 4500
Wire Wire Line
	6350 4900 6350 5000
Wire Wire Line
	7450 5000 7450 4850
Wire Wire Line
	7050 4850 7050 5000
Connection ~ 7050 5000
Wire Wire Line
	7050 5000 7150 5000
Wire Wire Line
	7150 4850 7150 5000
Connection ~ 7150 5000
Wire Wire Line
	7150 5000 7250 5000
Wire Wire Line
	7250 4850 7250 5000
Connection ~ 7250 5000
Wire Wire Line
	7250 5000 7350 5000
Wire Wire Line
	7350 4850 7350 5000
Connection ~ 7350 5000
Wire Wire Line
	7350 5000 7450 5000
$Comp
L ng_power:GND #PWR?
U 1 1 5F314866
P 6050 5100
AR Path="/5F314866" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F314866" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 6050 4850 50  0001 C CNN
F 1 "GND" H 6053 4974 50  0000 C CNN
F 2 "" H 5950 4750 50  0001 C CNN
F 3 "" H 6050 5100 50  0001 C CNN
	1    6050 5100
	1    0    0    -1  
$EndComp
Wire Wire Line
	6050 5100 6050 5000
NoConn ~ 6450 4200
NoConn ~ 6450 4300
$Comp
L Device:C C?
U 1 1 5F31486F
P 6350 4750
AR Path="/5F31486F" Ref="C?"  Part="1" 
AR Path="/5F302051/5F31486F" Ref="C33"  Part="1" 
F 0 "C33" H 6400 4850 50  0000 L CNN
F 1 "100n" H 6400 4650 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 6388 4600 50  0001 C CNN
F 3 "~" H 6350 4750 50  0001 C CNN
	1    6350 4750
	1    0    0    -1  
$EndComp
Text GLabel 5950 3500 0    50   Input ~ 0
USB_D-
Text GLabel 5950 3600 0    50   Input ~ 0
USB_D+
Text GLabel 8000 3200 2    50   Input ~ 0
FIFO_D0
Text GLabel 8000 3300 2    50   Input ~ 0
FIFO_D1
Text GLabel 8000 3400 2    50   Input ~ 0
FIFO_D2
Text GLabel 8000 3500 2    50   Input ~ 0
FIFO_D3
Text GLabel 8000 3600 2    50   Input ~ 0
FIFO_D4
Text GLabel 8000 3800 2    50   Input ~ 0
FIFO_D6
Text GLabel 8000 3900 2    50   Input ~ 0
FIFO_D7
Text GLabel 8000 3700 2    50   Input ~ 0
FIFO_D5
Text GLabel 8000 4100 2    50   Input ~ 0
FIFO_RXFn
Text GLabel 8000 4300 2    50   Input ~ 0
FIFO_RDn
Text GLabel 8000 4400 2    50   Input ~ 0
FIFO_WR
Text GLabel 8000 4200 2    50   Input ~ 0
FIFO_TXEn
$Comp
L Device:R R?
U 1 1 5F314883
P 8600 4350
AR Path="/5F314883" Ref="R?"  Part="1" 
AR Path="/5F302051/5F314883" Ref="R9"  Part="1" 
F 0 "R9" H 8670 4396 50  0000 L CNN
F 1 "10k" H 8670 4305 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 8530 4350 50  0001 C CNN
F 3 "~" H 8600 4350 50  0001 C CNN
	1    8600 4350
	1    0    0    -1  
$EndComp
Wire Wire Line
	8000 4600 8600 4600
Wire Wire Line
	8600 4600 8600 4500
Wire Wire Line
	8600 4200 8600 4100
Wire Wire Line
	6350 3300 6450 3300
Text GLabel 8700 4100 2    50   UnSpc ~ 0
P3V3
Wire Wire Line
	8600 4100 8700 4100
Wire Wire Line
	6350 4500 6350 3300
Connection ~ 6350 4500
Wire Wire Line
	5950 3500 6450 3500
Wire Wire Line
	5950 3600 6450 3600
Wire Wire Line
	5950 3200 6050 3200
Text GLabel 5950 3200 0    50   UnSpc ~ 0
USB_5V
Wire Wire Line
	5950 3900 6450 3900
Text GLabel 5950 3900 0    50   Input ~ 0
USB_DETn
Text Label 6350 4450 1    50   ~ 0
USB_VIO
Text Label 8050 4600 0    50   ~ 0
USB_PWRENn
NoConn ~ 3400 3500
Wire Wire Line
	3400 3600 3500 3600
Wire Wire Line
	3500 3600 3500 4000
Wire Wire Line
	3400 3200 4050 3200
Wire Wire Line
	3400 3300 3500 3300
Wire Wire Line
	3400 3400 3500 3400
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148A5
P 3500 4300
AR Path="/5F3148A5" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148A5" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 3500 4050 50  0001 C CNN
F 1 "GND" H 3503 4174 50  0000 C CNN
F 2 "" H 3400 3950 50  0001 C CNN
F 3 "" H 3500 4300 50  0001 C CNN
	1    3500 4300
	1    0    0    -1  
$EndComp
Text GLabel 3500 3300 2    50   Input ~ 0
USB_D-
Text GLabel 3500 3400 2    50   Input ~ 0
USB_D+
$Comp
L Device:R R?
U 1 1 5F3148AD
P 4550 4350
AR Path="/5F3148AD" Ref="R?"  Part="1" 
AR Path="/5F302051/5F3148AD" Ref="R3"  Part="1" 
F 0 "R3" H 4620 4396 50  0000 L CNN
F 1 "6k8" H 4620 4305 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 4480 4350 50  0001 C CNN
F 3 "~" H 4550 4350 50  0001 C CNN
	1    4550 4350
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 5F3148B3
P 4550 4850
AR Path="/5F3148B3" Ref="R?"  Part="1" 
AR Path="/5F302051/5F3148B3" Ref="R4"  Part="1" 
F 0 "R4" H 4620 4896 50  0000 L CNN
F 1 "10k" H 4620 4805 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 4480 4850 50  0001 C CNN
F 3 "~" H 4550 4850 50  0001 C CNN
	1    4550 4850
	1    0    0    -1  
$EndComp
Wire Wire Line
	4550 5000 4550 5100
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148BA
P 4550 5100
AR Path="/5F3148BA" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148BA" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 4550 4850 50  0001 C CNN
F 1 "GND" H 4553 4974 50  0000 C CNN
F 2 "" H 4450 4750 50  0001 C CNN
F 3 "" H 4550 5100 50  0001 C CNN
	1    4550 5100
	1    0    0    -1  
$EndComp
Wire Wire Line
	4550 4500 4550 4600
Wire Wire Line
	4550 4200 4550 4100
Wire Wire Line
	4550 4100 4450 4100
Wire Wire Line
	4550 4600 4650 4600
Connection ~ 4550 4600
Wire Wire Line
	4550 4600 4550 4700
Text GLabel 4650 4600 2    50   Input ~ 0
USB_DETn
$Comp
L Device:C C?
U 1 1 5F3148C7
P 6050 4750
AR Path="/5F3148C7" Ref="C?"  Part="1" 
AR Path="/5F302051/5F3148C7" Ref="C41"  Part="1" 
F 0 "C41" H 6100 4850 50  0000 L CNN
F 1 "100n" H 6100 4650 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 6088 4600 50  0001 C CNN
F 3 "~" H 6050 4750 50  0001 C CNN
	1    6050 4750
	1    0    0    -1  
$EndComp
Wire Wire Line
	6050 4600 6050 3200
Connection ~ 6050 3200
Wire Wire Line
	6050 3200 6450 3200
Wire Wire Line
	6050 4900 6050 5000
Wire Wire Line
	6050 5000 6350 5000
Connection ~ 6350 5000
Connection ~ 6050 5000
Wire Wire Line
	6350 5000 7050 5000
$Comp
L Device:C C?
U 1 1 5F3148D5
P 4050 3450
AR Path="/5F3148D5" Ref="C?"  Part="1" 
AR Path="/5F302051/5F3148D5" Ref="C39"  Part="1" 
F 0 "C39" H 4100 3550 50  0000 L CNN
F 1 "10n" H 4100 3350 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 4088 3300 50  0001 C CNN
F 3 "~" H 4050 3450 50  0001 C CNN
	1    4050 3450
	1    0    0    -1  
$EndComp
Text Label 3500 3200 0    50   ~ 0
USB_VBUS
Wire Wire Line
	4050 3200 4050 3300
Wire Wire Line
	4050 3600 4050 3700
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148DE
P 4050 3700
AR Path="/5F3148DE" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148DE" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 4050 3450 50  0001 C CNN
F 1 "GND" H 4053 3574 50  0000 C CNN
F 2 "" H 3950 3350 50  0001 C CNN
F 3 "" H 4050 3700 50  0001 C CNN
	1    4050 3700
	1    0    0    -1  
$EndComp
$Comp
L Device:Ferrite_Bead FB?
U 1 1 5F3148E5
P 4300 3200
AR Path="/5F3148E5" Ref="FB?"  Part="1" 
AR Path="/5F302051/5F3148E5" Ref="FB1"  Part="1" 
F 0 "FB1" V 4026 3200 50  0000 C CNN
F 1 "33R, 500mA" V 4117 3200 50  0000 C CNN
F 2 "Inductor_SMD:L_0603_1608Metric" V 4230 3200 50  0001 C CNN
F 3 "~" H 4300 3200 50  0001 C CNN
F 4 "742792605" V 4300 3200 50  0001 C CNN "MPN"
	1    4300 3200
	0    1    1    0   
$EndComp
Wire Wire Line
	4150 3200 4050 3200
Connection ~ 4050 3200
$Comp
L Device:C C?
U 1 1 5F3148ED
P 4550 3450
AR Path="/5F3148ED" Ref="C?"  Part="1" 
AR Path="/5F302051/5F3148ED" Ref="C40"  Part="1" 
F 0 "C40" H 4600 3550 50  0000 L CNN
F 1 "10n" H 4600 3350 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 4588 3300 50  0001 C CNN
F 3 "~" H 4550 3450 50  0001 C CNN
	1    4550 3450
	1    0    0    -1  
$EndComp
Wire Wire Line
	4550 3200 4550 3300
Wire Wire Line
	4550 3600 4550 3700
$Comp
L ng_power:GND #PWR?
U 1 1 5F3148F5
P 4550 3700
AR Path="/5F3148F5" Ref="#PWR?"  Part="1" 
AR Path="/5F302051/5F3148F5" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 4550 3450 50  0001 C CNN
F 1 "GND" H 4553 3574 50  0000 C CNN
F 2 "" H 4450 3350 50  0001 C CNN
F 3 "" H 4550 3700 50  0001 C CNN
	1    4550 3700
	1    0    0    -1  
$EndComp
Wire Wire Line
	4450 3200 4550 3200
Connection ~ 4550 3200
Wire Wire Line
	4550 3200 4650 3200
Text GLabel 4650 3200 2    50   UnSpc ~ 0
USB_5V
Text GLabel 4450 4100 0    50   UnSpc ~ 0
USB_5V
$Comp
L Device:R R?
U 1 1 5F314900
P 3250 4000
AR Path="/5F314900" Ref="R?"  Part="1" 
AR Path="/5F302051/5F314900" Ref="R6"  Part="1" 
F 0 "R6" V 3050 4000 50  0000 C CNN
F 1 "100k" V 3150 4000 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 3180 4000 50  0001 C CNN
F 3 "~" H 3250 4000 50  0001 C CNN
	1    3250 4000
	0    1    1    0   
$EndComp
$Comp
L Device:C C?
U 1 1 5F314906
P 3250 4200
AR Path="/5F314906" Ref="C?"  Part="1" 
AR Path="/5F302051/5F314906" Ref="C42"  Part="1" 
F 0 "C42" V 3100 4200 50  0000 C CNN
F 1 "10n" V 3000 4200 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3288 4050 50  0001 C CNN
F 3 "~" H 3250 4200 50  0001 C CNN
	1    3250 4200
	0    -1   -1   0   
$EndComp
Wire Wire Line
	3400 4000 3500 4000
Connection ~ 3500 4000
Wire Wire Line
	3500 4000 3500 4200
Wire Wire Line
	3400 4200 3500 4200
Connection ~ 3500 4200
Wire Wire Line
	3500 4200 3500 4300
Wire Wire Line
	3100 4000 3000 4000
Wire Wire Line
	3000 4000 3000 3800
Wire Wire Line
	3100 4200 3000 4200
Wire Wire Line
	3000 4200 3000 4000
Connection ~ 3000 4000
Text Label 3000 4150 1    50   ~ 0
USB_SHD
$Comp
L ng_conn:USB_B_Micro J?
U 1 1 5F314899
P 3100 3400
AR Path="/5F314899" Ref="J?"  Part="1" 
AR Path="/5F302051/5F314899" Ref="J5"  Part="1" 
F 0 "J5" H 3157 3867 50  0000 C CNN
F 1 "USB_B_Micro" H 3157 3776 50  0000 C CNN
F 2 "Connector_USB:USB_Micro-B_Molex_47346-0001" H 3250 3400 50  0001 C CNN
F 3 "~" H 3250 3400 50  0001 C CNN
	1    3100 3400
	1    0    0    -1  
$EndComp
$EndSCHEMATC
