# SourceDefender benchmark methodology

The focused matrix covers GPT-6.1 Terra, GPT-6.1 Sol, GPT-6 Astra, and Daybreak Blue at the available Codex effort levels. Each measured configuration gets a fresh agent-practice incident: Orbital uplink, JavaScript, Zero trust, seed `benchmark-20261029`. New hard-mode incidents contain no pre-incident Git commits, baseline, or Git objects. The benchmark uses a fixed local engine build and verifies the incident boundary. Older runs and infrastructure-only pilots are excluded.

The benchmark asks agents to investigate and repair files, use the game validation tool, and request hints if they choose. Agents are instructed not to restore an external baseline, read game implementation or other trials, execute generated project code, or delegate. Multi-agent capability is disabled for all settings, including ultra; ultra results therefore do not measure its automatic-delegation feature.

The runner requests each model and effort through Codex CLI flags. CLI output does not independently attest the provider's internal routing. Each configuration has at most one valid scored result; interrupted requests caused by account usage limits are retried as fresh incidents, preserving earlier transcripts. The timeout is 600 seconds per attempt. Up to three trials run concurrently; their actual overlaps vary, so timings may be affected by system and service contention.

The horizontal axis is the game score. The vertical axis is scored game time, including time penalties, in minutes. SourceDefender's score is calculated from scored time, validations, and hints, so these axes are mathematically dependent. The CSV also records wall time, hints, attempts, penalties, and reported token use where available. A run that did not contain the incident has no final score and is listed separately rather than plotted at zero.

Only one seed and one scenario are used, with one scored run per configuration: these points are exploratory and do not establish general model rankings or statistical significance. SourceDefender uses bounded static checks for known attacks, not a comprehensive security audit.

Trial records and generated incidents are separated; a guarded MCP launcher only permits the assigned incident parent and data directory. Windows workspace-write mode rejected even allowed edits on this host, so the CLI agents use full filesystem access with instructions to stay in their trial; this is not a secure sandbox or independently enforced read isolation. The repository and test fixtures are locally accessible to the host. Transcript checks are limited and cannot prove all actions were compliant.

The [results CSV](results.csv) contains the 24 scored configurations and the [PNG graph](score-vs-time.png) plots them. Earlier interrupted requests are not scored.
