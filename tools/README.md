# Værktøj

`backlog.py` er teksten til køreplanen. Kør den for at genskabe `issues.yaml` og `docs/roadmap.md`.

`create_github_issues.py` opretter labels, milepæle og issues ud fra `issues.yaml`. Det kræver `gh` som en bruger der må skrive til `rastermanden/openCycloComputer`. Scriptet springer det over, der allerede findes.

Cloud-agenten der oprettede repoet kunne ikke kalde den API (HTTP 403). Derfor ligger backloggen i filerne indtil scriptet er kørt lokalt.
