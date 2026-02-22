.PHONY: setup dev dev-full

setup:
	./scripts/setup.sh

dev:
	cd ui/multi-agent-app && npm run dev:suite

dev-full:
	cd ui/multi-agent-app && npm run dev:suite:full
