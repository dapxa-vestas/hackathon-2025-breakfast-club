# Multiple Applications within same Workload

This recipe defines a single workload, with separate applications for
our sample project and sample database.

Since they're separate applications within same workload, for them to communicate,
it's required to explicitly expose the port that other application wants to reach.
Additionally, we can reach different application within same workload by their name,
thus in order for our sample project to communicate with sample database, we need to
add following key-value configuration entry in configuration portal:
`CONNECTION_STRING = postgres://hackathon:hackathon@hackathon-database:5432/hackathon_db`
