# Multiple Containers within same Workload's Application

This recipe defines a single workload, with a single application that
has 2 containers running - our sample python application and sample
postgres database.

Since they're running inside same application, they can reach each other
via `localhost` and it's not necessary to explicitly expose ports of the database
inside the recipe, just the docker image.
So in order to configure our sample application to interact
with our database, we can do that by adding following key-value configuration entry
in configuration portal - `CONNECTION_STRING = postgres://hackathon:hackathon@localhost:5432/hackathon_db`

> Note: since they are within same application, that also means if one of them
crashes, the whole application (and all containers within) will restart
