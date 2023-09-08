
.PHONY: build
build:
	docker build \
		--platform=linux/amd64 \
		-f python-test.Dockerfile \
		-t registry.rcd.clemson.edu/dndawso/vipergs-carla-test/python-test .
	docker push registry.rcd.clemson.edu/dndawso/vipergs-carla-test/python-test

auth: rcd-reg-cred.yaml
rcd-reg-cred.yaml:
	@printf  "Password: " && \
		read -s pass && \
		docker login -u carla-test-registry -p "$$pass" registry.rcd.clemson.edu && \
		kubectl -n carla-test create secret docker-registry rcd-reg-cred \
			--docker-server="registry.rcd.clemson.edu" \
			--docker-username="carla-test-registry" \
			--docker-password="$$pass" \
			--dry-run="client" \
			-o yaml > rcd-reg-cred.yaml

deploy: rcd-reg-cred.yaml
	kubectl apply -f rcd-reg-cred.yaml
	kubectl apply -f deployment.yaml
	# Hack -- since we are just using the latest tag, we may need kill the pod
	# and have it pull any new images from the registry.  Ideally you shouldn't
	# use this hack, instead tag each image you create and then update the tag
	# in the deployment.yaml (perhaps using things like skaffold).
	kubectl -n carla-test delete pod $$(kubectl -n carla-test get pods -o jsonpath="{.items[*].metadata.name}")

connect:
	kubectl -n carla-test port-forward $$(kubectl -n carla-test get pods -o jsonpath="{.items[*].metadata.name}") 1935:1935
	# NOTE: this next command can take up to 60 seconds to start streaming
	ffplay  rtmp://localhost:1935/live/test

clean:
	rm -f rcd-reg-cred.yaml
