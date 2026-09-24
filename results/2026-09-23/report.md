# Round report

## Summary

| tool | precision | recall | F1 | TP | FN | FP | bonus |
|---|---|---|---|---|---|---|---|
| coderabbit | 1.00 | 0.78 | 0.88 | 7 | 2 | 0 | 3 |
| gitar | 1.00 | 1.00 | 1.00 | 8 | 0 | 0 | 7 |

> precision/F1 = n/a means the tool reported nothing scoreable. False positives are counted only for unmatched findings that point into `cases/`.

## Detection matrix

| case | type | location | coderabbit | gitar |
|---|---|---|---|---|
| codereview-asyncbug-001 | logic-bug | cases/code-review/js/notifier.js:8 | hit | hit |
| codereview-offbyone-001 | logic-bug | cases/code-review/js/pagination.js:13 | hit | hit |
| deps-java-001 | vulnerable-dependency | cases/dependencies/java/pom.xml:14 | - | - |
| deps-java-001 | vulnerable-dependency | cases/dependencies/java/pom.xml:19 | - | - |
| deps-java-001 | vulnerable-dependency | cases/dependencies/java/pom.xml:24 | - | - |
| deps-js-001 | vulnerable-dependency | cases/dependencies/js/package.json:7 | - | bonus |
| deps-js-001 | vulnerable-dependency | cases/dependencies/js/package.json:8 | - | bonus |
| deps-js-001 | vulnerable-dependency | cases/dependencies/js/package.json:9 | - | bonus |
| deps-js-001 | vulnerable-dependency | cases/dependencies/js/package.json:10 | - | bonus |
| deps-py-001 | vulnerable-dependency | cases/dependencies/python/requirements.txt:2 | - | - |
| deps-py-001 | vulnerable-dependency | cases/dependencies/python/requirements.txt:3 | - | - |
| deps-py-001 | vulnerable-dependency | cases/dependencies/python/requirements.txt:4 | - | - |
| deps-py-001 | vulnerable-dependency | cases/dependencies/python/requirements.txt:5 | - | - |
| deps-py-001 | vulnerable-dependency | cases/dependencies/python/requirements.txt:6 | - | - |
| iac-docker-001 | iac-misconfig | cases/iac-ci/Dockerfile:1 | - | - |
| iac-docker-001 | iac-misconfig | cases/iac-ci/Dockerfile:7 | - | - |
| iac-workflow-001 | iac-misconfig | cases/iac-ci/pr-build.yml:4 | - | - |
| iac-workflow-001 | iac-misconfig | cases/iac-ci/pr-build.yml:7 | - | - |
| iac-workflow-001 | iac-misconfig | cases/iac-ci/pr-build.yml:15 | - | - |
| license-001 | license-risk | cases/license/pom.xml:20 | - | - |
| sast-java-deserialization-001 | insecure-deserialization | cases/sast/java/docsvc/src/main/java/com/example/docsvc/DocumentController.java:32 | - | - |
| sast-java-xxe-001 | xxe | cases/sast/java/docsvc/src/main/java/com/example/docsvc/DocumentController.java:23 | - | - |
| sast-js-cmdi-001 | command-injection | cases/sast/js/taskflow/routes/attachments.js:14 | hit | hit |
| sast-js-cmdi-001 | path-traversal | cases/sast/js/taskflow/routes/attachments.js:12 | bonus | hit |
| sast-js-hardcoded-secret-001 | hardcoded-secret | cases/sast/js/taskflow/lib/config.js:11 | miss | hit |
| sast-js-hardcoded-secret-001 | hardcoded-secret | cases/sast/js/taskflow/lib/config.js:15 | miss | hit |
| sast-js-sqli-001 | sql-injection | cases/sast/js/taskflow/routes/tasks.js:11 | hit | hit |
| sast-js-ssrf-001 | ssrf | cases/sast/js/taskflow/routes/webhooks.js:10 | bonus | hit |
| sast-py-deserialization-001 | insecure-deserialization | cases/sast/python/reportsvc/app.py:37 | hit | - |
| sast-py-pathtraversal-001 | path-traversal | cases/sast/python/reportsvc/app.py:19 | hit | - |
| sast-py-weakcrypto-001 | weak-crypto | cases/sast/python/reportsvc/app.py:27 | hit | - |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:9 | - | - |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:10 | - | - |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:15 | - | - |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:16 | - | - |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:17 | - | - |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:20 | - | - |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:21 | - | - |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:26 | - | - |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:27 | - | - |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:30 | - | - |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/settings.py:34 | - | - |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/appsettings.json:6 | - | - |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/appsettings.json:9 | - | - |
| secrets-billing-worker-001 | hardcoded-secret | cases/billing-worker/config/gcp-service-account.json:5 | - | - |
| supply-chain-001 | malicious-dependency | cases/supply-chain/package.json:8 | bonus | bonus |
| supply-chain-001 | malicious-dependency | cases/supply-chain/package.json:9 | - | bonus |
| supply-chain-001 | malicious-dependency | cases/supply-chain/package.json:10 | - | bonus |

## Explainability (CodeRabbit): 3/3 summaries matched

| case | summary matched? | expected summary |
|---|---|---|
| codereview-offbyone-001 | yes | Returns the most recent pageSize items from a list. |
| codereview-asyncbug-001 | yes | Emails every task owner that their report is ready. |
| sast-js-hardcoded-secret-001 | yes | Central configuration module with defaults for local development. |

### coderabbit: missed (2)
- sast-js-hardcoded-secret-001 (hardcoded-secret @ cases/sast/js/taskflow/lib/config.js:11)
- sast-js-hardcoded-secret-001 (hardcoded-secret @ cases/sast/js/taskflow/lib/config.js:15)
