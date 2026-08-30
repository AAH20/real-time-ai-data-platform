# Security policy

Do not commit customer data, cloud credentials, connection strings or production telemetry. Report suspected vulnerabilities privately through the repository security-advisory workflow.

The included scenario is synthetic. The Azure template creates no secrets and disables the streaming service by default. Production deployments require private networking, managed identities, least-privilege RBAC, encryption controls and a documented data-retention policy.
