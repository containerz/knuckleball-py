# Copyright (c) 2016, Rodrigo Alves Lima
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
#        following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#        following disclaimer in the documentation and/or other materials provided with the distribution.
#
#     3. Neither the name of knuckleball-py nor the names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# $(call test_judge,cmd,ret)
define test_judge
ifeq ($2,0)
	expression = "\033[32m$1\033[m"
else
	expression = "\033[31m$1\033[m"
endif
endef

# $(call run_test,cmd)
define run_test
$(eval RET := $(shell python3 $1 2> /dev/null; echo $$?))
$(eval $(call test_judge,$1,$(RET)))
@echo $(expression)
endef

.PHONY: all test

all: setUp test tearDown

setUp:
	{ knuckleball -q --bind 127.0.0.1 --port 8001 --password securepassword & echo $$! > server.PID; }

test:
	$(call run_test,unit_tests.py)

tearDown:
	kill `cat server.PID` && rm server.PID
