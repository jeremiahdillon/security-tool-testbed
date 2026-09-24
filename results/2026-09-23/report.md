# Round report

## Summary

| tool | precision | recall | F1 | TP | FN | FP | bonus |
|---|---|---|---|---|---|---|---|
| codeql | 0.73 | 0.73 | 0.73 | 8 | 3 | 3 | 0 |
| coderabbit | 1.00 | 0.78 | 0.88 | 7 | 2 | 0 | 3 |
| dependabot | 0.92 | 1.00 | 0.96 | 12 | 0 | 1 | 1 |
| gitar | 1.00 | 1.00 | 1.00 | 8 | 0 | 0 | 7 |
| sonar | 0.62 | 0.43 | 0.51 | 18 | 24 | 11 | 0 |

> precision/F1 = n/a means the tool reported nothing scoreable. False positives are counted only for unmatched findings that point into `cases/`.

## Detection matrix

| case | type | location | codeql | coderabbit | dependabot | gitar | sonar |
|---|---|---|---|---|---|---|---|
| codereview-asyncbug-001 | logic-bug | cases/code-review/js/notifier.js:8 | - | hit | - | hit | - |
| codereview-offbyone-001 | logic-bug | cases/code-review/js/pagination.js:13 | - | hit | - | hit | - |
| deps-java-001 | vulnerable-dependency | cases/dependencies/java/pom.xml:14 | - | - | hit | - | miss |
| deps-java-001 | vulnerable-dependency | cases/dependencies/java/pom.xml:19 | - | - | hit | - | miss |
| deps-java-001 | vulnerable-dependency | cases/dependencies/java/pom.xml:24 | - | - | hit | - | miss |
| deps-js-001 | vulnerable-dependency | cases/dependencies/js/package.json:7 | - | - | hit | bonus | miss |
| deps-js-001 | vulnerable-dependency | cases/dependencies/js/package.json:8 | - | - | hit | bonus | miss |
| deps-js-001 | vulnerable-dependency | cases/dependencies/js/package.json:9 | - | - | hit | bonus | miss |
| deps-js-001 | vulnerable-dependency | cases/dependencies/js/package.json:10 | - | - | hit | bonus | miss |
| deps-py-001 | vulnerable-dependency | cases/dependencies/python/requirements.txt:2 | - | - | hit | - | miss |
| deps-py-001 | vulnerable-dependency | cases/dependencies/python/requirements.txt:3 | - | - | hit | - | miss |
| deps-py-001 | vulnerable-dependency | cases/dependencies/python/requirements.txt:4 | - | - | hit | - | miss |
| deps-py-001 | vulnerable-dependency | cases/dependencies/python/requirements.txt:5 | - | - | hit | - | miss |
| deps-py-001 | vulnerable-dependency | cases/dependencies/python/requirements.txt:6 | - | - | hit | - | miss |
| iac-docker-001 | iac-misconfig | cases/iac-ci/Dockerfile:1 | - | - | - | - | hit |
| iac-docker-001 | iac-misconfig | cases/iac-ci/Dockerfile:7 | - | - | - | - | hit |
| iac-workflow-001 | iac-misconfig | cases/iac-ci/pr-build.yml:4 | - | - | - | - | miss |
| iac-workflow-001 | iac-misconfig | cases/iac-ci/pr-build.yml:7 | - | - | - | - | miss |
| iac-workflow-001 | iac-misconfig | cases/iac-ci/pr-build.yml:15 | - | - | - | - | miss |
| license-001 | license-risk | cases/license/pom.xml:20 | - | - | - | - | - |
| sast-java-deserialization-001 | insecure-deserialization | cases/sast/java/docsvc/src/main/java/com/example/docsvc/DocumentController.java:32 | hit | - | - | - | miss |
| sast-java-xxe-001 | xxe | cases/sast/java/docsvc/src/main/java/com/example/docsvc/DocumentController.java:23 | hit | - | - | - | miss |
| sast-js-cmdi-001 | command-injection | cases/sast/js/taskflow/routes/attachments.js:14 | hit | hit | - | hit | hit |
| sast-js-cmdi-001 | path-traversal | cases/sast/js/taskflow/routes/attachments.js:12 | miss | bonus | - | hit | miss |
| sast-js-hardcoded-secret-001 | hardcoded-secret | cases/sast/js/taskflow/lib/config.js:11 | miss | miss | - | hit | miss |
| sast-js-hardcoded-secret-001 | hardcoded-secret | cases/sast/js/taskflow/lib/config.js:15 | miss | miss | - | hit | miss |
| sast-js-sqli-001 | sql-injection | cases/sast/js/taskflow/routes/tasks.js:11 | hit | hit | - | hit | hit |
| sast-js-ssrf-001 | ssrf | cases/sast/js/taskflow/routes/webhooks.js:10 | hit | bonus | - | hit | hit |
| sast-py-deserialization-001 | insecure-deserialization | cases/sast/python/reportsvc/app.py:37 | hit | hit | - | - | hit |
| sast-py-pathtraversal-001 | path-traversal | cases/sast/python/reportsvc/app.py:19 | hit | hit | - | - | hit |
| sast-py-weakcrypto-001 | weak-crypto | cases/sast/python/reportsvc/app.py:27 | hit | hit | - | - | hit |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:9 | - | - | - | - | miss |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:10 | - | - | - | - | hit |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:15 | - | - | - | - | hit |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:16 | - | - | - | - | hit |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:17 | - | - | - | - | hit |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:20 | - | - | - | - | miss |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:21 | - | - | - | - | miss |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:26 | - | - | - | - | hit |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:27 | - | - | - | - | hit |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:30 | - | - | - | - | miss |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:34 | - | - | - | - | hit |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/appsettings.json:6 | - | - | - | - | hit |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/appsettings.json:9 | - | - | - | - | hit |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/gcp-service-account.json:5 | - | - | - | - | hit |
| supply-chain-001 | malicious-dependency | cases/supply-chain/package.json:8 | - | bonus | - | bonus | - |
| supply-chain-001 | malicious-dependency | cases/supply-chain/package.json:9 | - | - | - | bonus | - |
| supply-chain-001 | malicious-dependency | cases/supply-chain/package.json:10 | - | - | bonus | bonus | - |

## Explainability (CodeRabbit): 3/3 summaries matched

| case | summary matched? | expected summary |
|---|---|---|
| codereview-offbyone-001 | yes | Returns the most recent pageSize items from a list. |
| codereview-asyncbug-001 | yes | Emails every task owner that their report is ready. |
| sast-js-hardcoded-secret-001 | yes | Central configuration module with defaults for local development. |

### codeql: missed (3)
- sast-js-cmdi-001 (path-traversal @ cases/sast/js/taskflow/routes/attachments.js:12)
- sast-js-hardcoded-secret-001 (hardcoded-secret @ cases/sast/js/taskflow/lib/config.js:11)
- sast-js-hardcoded-secret-001 (hardcoded-secret @ cases/sast/js/taskflow/lib/config.js:15)

### codeql: unmatched findings to triage (3)
- js/missing-rate-limiting @ cases/sast/js/taskflow/routes/attachments.js:10
- js/missing-rate-limiting @ cases/sast/js/taskflow/routes/tasks.js:6
- js/missing-rate-limiting @ cases/sast/js/taskflow/routes/tasks.js:20

### coderabbit: missed (2)
- sast-js-hardcoded-secret-001 (hardcoded-secret @ cases/sast/js/taskflow/lib/config.js:11)
- sast-js-hardcoded-secret-001 (hardcoded-secret @ cases/sast/js/taskflow/lib/config.js:15)

### dependabot: unmatched findings to triage (1)
- GHSA-m6vm-37g8-gqvh @ cases/license/pom.xml:None

### sonar: missed (24)
- deps-java-001 (vulnerable-dependency @ cases/dependencies/java/pom.xml:14)
- deps-java-001 (vulnerable-dependency @ cases/dependencies/java/pom.xml:19)
- deps-java-001 (vulnerable-dependency @ cases/dependencies/java/pom.xml:24)
- deps-js-001 (vulnerable-dependency @ cases/dependencies/js/package.json:7)
- deps-js-001 (vulnerable-dependency @ cases/dependencies/js/package.json:8)
- deps-js-001 (vulnerable-dependency @ cases/dependencies/js/package.json:9)
- deps-js-001 (vulnerable-dependency @ cases/dependencies/js/package.json:10)
- deps-py-001 (vulnerable-dependency @ cases/dependencies/python/requirements.txt:2)
- deps-py-001 (vulnerable-dependency @ cases/dependencies/python/requirements.txt:3)
- deps-py-001 (vulnerable-dependency @ cases/dependencies/python/requirements.txt:4)
- deps-py-001 (vulnerable-dependency @ cases/dependencies/python/requirements.txt:5)
- deps-py-001 (vulnerable-dependency @ cases/dependencies/python/requirements.txt:6)
- iac-workflow-001 (iac-misconfig @ cases/iac-ci/pr-build.yml:4)
- iac-workflow-001 (iac-misconfig @ cases/iac-ci/pr-build.yml:7)
- iac-workflow-001 (iac-misconfig @ cases/iac-ci/pr-build.yml:15)
- sast-java-deserialization-001 (insecure-deserialization @ cases/sast/java/docsvc/src/main/java/com/example/docsvc/DocumentController.java:32)
- sast-java-xxe-001 (xxe @ cases/sast/java/docsvc/src/main/java/com/example/docsvc/DocumentController.java:23)
- sast-js-cmdi-001 (path-traversal @ cases/sast/js/taskflow/routes/attachments.js:12)
- sast-js-hardcoded-secret-001 (hardcoded-secret @ cases/sast/js/taskflow/lib/config.js:11)
- sast-js-hardcoded-secret-001 (hardcoded-secret @ cases/sast/js/taskflow/lib/config.js:15)
- secrets-billing-worker-001 (hardcoded-secret @ cases/billing-worker/config/settings.py:9)
- secrets-billing-worker-001 (hardcoded-secret @ cases/billing-worker/config/settings.py:20)
- secrets-billing-worker-001 (hardcoded-secret @ cases/billing-worker/config/settings.py:21)
- secrets-billing-worker-001 (hardcoded-secret @ cases/billing-worker/config/settings.py:30)

### sonar: unmatched findings to triage (11)
- json:S6418 @ cases/billing-worker/config/appsettings.json:9
- text:S8564 @ cases/dependencies/js/package.json:None
- docker:S6506 @ cases/iac-ci/Dockerfile:7
- docker:S8482 @ cases/iac-ci/Dockerfile:7
- docker:S6470 @ cases/iac-ci/Dockerfile:9
- javascript:S5689 @ cases/sast/js/taskflow/index.js:8
- text:S8564 @ cases/sast/js/taskflow/package.json:None
- python:S4502 @ cases/sast/python/reportsvc/app.py:9
- python:S8392 @ cases/sast/python/reportsvc/app.py:47
- text:S8564 @ cases/supply-chain/package.json:None
- text:S8564 @ cases/supply-chain/package.json:None
