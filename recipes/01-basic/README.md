# Basic Workload Recipe

Defines a workload with a single application and single container that runs
docker image built using this repository's code.

No other optional properties are defined, meaning:

- This application is not stateful
- It doesn't have any volumes, so any possible data written to disk
is lost if application restarts
- It doesn't expose any ports so no other application can access it
