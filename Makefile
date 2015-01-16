PROJECT_NAME = offlinedatacollector
STATIC_LIBS_DIR = ./$(PROJECT_NAME)/static/libs

LESS_VERSION = 2.1.0
MODERNIZR_VERSION = 2.8.3
JQUERY_VERSION = 1.11.2
UNDERSCORE_VERSION = 1.7.0
BACKBONE_VERSION = 1.1.2
LESSHAT_VERSION = 3.0.2
OFFLINE_VERSION = 0.7.11
DUAL_STORAGE_VERSION = 1.3.1

default: lint test

test:
	# Run all tests and report coverage
	# Requires coverage
	coverage run manage.py test
	coverage report -m --fail-under 80

lint-py:
	# Check for Python formatting issues
	# Requires flake8
	flake8 .

lint-js:
	# Check JS for any problems
	# Requires jshint
	find -name "*.js" -not -path "${STATIC_LIBS_DIR}*" -not -path "./node_modules/*" -print0 | xargs -0 jshint

lint: lint-py lint-js

$(STATIC_LIBS_DIR):
	mkdir -p $@

$(STATIC_LIBS_DIR)/less.js: $(STATIC_LIBS_DIR)
	wget https://cdnjs.cloudflare.com/ajax/libs/less.js/$(LESS_VERSION)/less.js -O $@

LIBS := $(STATIC_LIBS_DIR)/less.js

$(STATIC_LIBS_DIR)/modernizr.js: $(STATIC_LIBS_DIR)
	wget https://cdnjs.cloudflare.com/ajax/libs/modernizr/$(MODERNIZR_VERSION)/modernizr.js -O $@

LIBS += $(STATIC_LIBS_DIR)/modernizr.js

$(STATIC_LIBS_DIR)/jquery.js: $(STATIC_LIBS_DIR)
	wget https://cdnjs.cloudflare.com/ajax/libs/jquery/$(JQUERY_VERSION)/jquery.js -O $@

LIBS += $(STATIC_LIBS_DIR)/jquery.js

$(STATIC_LIBS_DIR)/underscore.js: $(STATIC_LIBS_DIR)
	wget https://cdnjs.cloudflare.com/ajax/libs/underscore.js/${UNDERSCORE_VERSION}/underscore.js -O $@

LIBS += $(STATIC_LIBS_DIR)/underscore.js

$(STATIC_LIBS_DIR)/backbone.js: $(STATIC_LIBS_DIR)
	wget https://cdnjs.cloudflare.com/ajax/libs/backbone.js/${BACKBONE_VERSION}/backbone.js -O $@

LIBS += $(STATIC_LIBS_DIR)/backbone.js

$(STATIC_LIBS_DIR)/offline.min.js: $(STATIC_LIBS_DIR)
	wget https://raw.githubusercontent.com/HubSpot/offline/v$(OFFLINE_VERSION)/offline.min.js -O $@

LIBS += $(STATIC_LIBS_DIR)/offline.min.js

$(STATIC_LIBS_DIR)/lesshat.less: $(STATIC_LIBS_DIR)
	wget https://raw.githubusercontent.com/madebysource/lesshat/v${LESSHAT_VERSION}/build/lesshat.less -O $@

LIBS += $(STATIC_LIBS_DIR)/lesshat.less

$(STATIC_LIBS_DIR)/backbone.dualstorage.js: $(STATIC_LIBS_DIR)
	wget https://raw.githubusercontent.com/nilbus/Backbone.dualStorage/v${DUAL_STORAGE_VERSION}/backbone.dualstorage.js -O $@

LIBS += $(STATIC_LIBS_DIR)/backbone.dualstorage.js

update-static-libs: $(LIBS)

generate-secret: length = 32
generate-secret:
	# Generate a random string of desired length
	@strings /dev/urandom | grep -o '[[:alnum:]]' | head -n $(length) | tr -d '\n'; echo

conf/pillar/%/deploy.pub:
	# Generate SSH deploy key for a given environment
	ssh-keygen -t rsa -b 4096 -f $(basename $@ .pub) -C "$*@${PROJECT_NAME}"

conf/pillar/%/secrets.sls: conf/pillar/%/deploy.pub
	# Creates new secrets file for a given environment and includes the deploy key
	cp ./conf/pillar/secrets.ex $@
	@echo '' >> $@
	@echo 'github_deploy_key: |' >> $@
	@cat $(basename $< .pub) | sed "s/^/  /" >> $@
	@sed -i "s/DB_PASSWORD: XXXXXX/DB_PASSWORD: `strings /dev/urandom | grep -o '[[:alnum:]]' | head -n 24 | tr -d '\n'; echo`/" $@
	@sed -i "s/BROKER_PASSWORD: XXXXXX/BROKER_PASSWORD: `strings /dev/urandom | grep -o '[[:alnum:]]' | head -n 24 | tr -d '\n'; echo`/" $@
	@sed -i "s/SECRET_KEY: XXXXXX/SECRET_KEY: `strings /dev/urandom | grep -o '[[:alnum:]]' | head -n 64 | tr -d '\n'; echo`/" $@

bootstrap-pillars: conf/pillar/staging/secrets.sls conf/pillar/production/secrets.sls

.PHONY: default test lint lint-py lint-js generate-secret

.PRECIOUS: conf/pillar/%/deploy.pub conf/pillar/%/secrets.sls
