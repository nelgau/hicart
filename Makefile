TESTROM := roms/sm64.z64

.PHONY: send-gateware
send-gateware:
	$(MAKE) -C gateware send

.PHONY: program-gateware
program-gateware:
	$(MAKE) -C gateware program

.PHONY: program-software
program-software:
	$(MAKE) -C software program

.PHONY: program-testrom
program-testrom: $(TESTROM)
	ecpprog -d s:0x0403:0x6010:FT5YLSVU -I B -o 8M $(TESTROM)

.PHONY: n64-up
n64-up: send-gateware
	scripts/set_power_state.sh --silent --state 0
	scripts/set_power_state.sh --silent --state 1

.PHONY: n64-down
n64-down:
	scripts/set_power_state.sh --silent --state 0