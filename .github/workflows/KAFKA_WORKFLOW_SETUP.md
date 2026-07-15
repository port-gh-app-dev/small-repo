# Kafka Exporter Workflow Setup Guide

## Overview

The Kafka Exporter Workflow (`.github/workflows/port-kafka.yaml`) integrates with Port.io to export Kafka cluster metadata including clusters, brokers, topics, and consumer groups.

## Current Status

### ✅ Fixed Issues
- **Docker env file whitespace error** (July 2026)
  - The workflow previously failed with `docker: invalid env file (.sail-env): variable contains whitespaces`
  - **Fix**: JSON configuration is now validated and minified before being passed to the Docker container
  - **Commits**: `75a41c0`, `9af9e6a`

### ❌ Outstanding Issue: Invalid Kafka Broker Configuration

**Problem**: The workflow times out after 30 minutes trying to connect to a non-existent Kafka broker.

**Error**:
```
localhost:9092/bootstrap: Connect to ipv4#127.0.0.1:9092 failed: Connection refused
```

**Root Cause**: The GitHub secret `OCEAN__INTEGRATION__CONFIG__CLUSTER_CONF_MAPPING` is configured to connect to `localhost:9092`, which doesn't exist in GitHub Actions runners.

## Required Configuration

### GitHub Secrets

The workflow requires three secrets to be configured in repository settings:

1. **`OCEAN__PORT__CLIENT_ID`**
   - Port.io API client ID
   - Obtain from: Port.io Dashboard → Settings → Credentials

2. **`OCEAN__PORT__CLIENT_SECRET`**
   - Port.io API client secret
   - Obtain from: Port.io Dashboard → Settings → Credentials

3. **`OCEAN__INTEGRATION__CONFIG__CLUSTER_CONF_MAPPING`**
   - JSON object mapping cluster names to Kafka connection configurations
   - **Current value** (invalid):
     ```json
     {
       "internal-cluster": {
         "bootstrap.servers": "localhost:9092",
         "security.protocol": "PLAINTEXT"
       }
     }
     ```

### Fixing the Kafka Broker Configuration

Choose one of the following approaches:

#### Option 1: Point to a Real Kafka Cluster (Recommended)

Update the `OCEAN__INTEGRATION__CONFIG__CLUSTER_CONF_MAPPING` secret with a valid, accessible Kafka broker:

```json
{
  "production-cluster": {
    "bootstrap.servers": "kafka-broker.example.com:9092",
    "security.protocol": "SASL_SSL",
    "sasl.mechanism": "PLAIN",
    "sasl.username": "your-username",
    "sasl.password": "your-password"
  }
}
```

**Requirements**:
- The Kafka broker must be accessible from GitHub Actions runners (public internet or configured with appropriate network access)
- Use proper authentication (SASL_SSL, mutual TLS, etc.)
- Ensure the broker accepts connections from GitHub's IP ranges

#### Option 2: Set Up a Test Kafka Instance in the Workflow

Modify the workflow to start a local Kafka instance using Docker:

```yaml
jobs:
  run-integration:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    services:
      zookeeper:
        image: confluentinc/cp-zookeeper:latest
        env:
          ZOOKEEPER_CLIENT_PORT: 2181
          ZOOKEEPER_TICK_TIME: 2000
      kafka:
        image: confluentinc/cp-kafka:latest
        ports:
          - 9092:9092
        env:
          KAFKA_BROKER_ID: 1
          KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
          KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
          KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    steps:
      - name: Wait for Kafka
        run: |
          timeout 60 bash -c 'until nc -z localhost 9092; do sleep 1; done'
      # ... rest of the workflow
```

#### Option 3: Disable the Workflow

If the Kafka integration is not currently needed:

1. Remove or comment out the `push` trigger in `.github/workflows/port-kafka.yaml`:
   ```yaml
   on:
     workflow_dispatch:  # Keep manual trigger only
     # push:
     #   branches: [main]
   ```

2. Run the workflow manually when needed via GitHub UI → Actions → Kafka Exporter Workflow → Run workflow

## Testing the Fix

After updating the configuration:

1. **Manual test**:
   ```bash
   # Navigate to GitHub UI
   Actions → Kafka Exporter Workflow → Run workflow → Run workflow
   ```

2. **Verify success**:
   - Workflow completes in < 5 minutes
   - No "Connection refused" errors in logs
   - Port.io dashboard shows imported Kafka entities

3. **Check Port.io**:
   - Navigate to Port.io → Catalog
   - Verify entities: `kafkaCluster`, `kafkaBroker`, `kafkaTopic`, `kafkaConsumerGroup`

## Troubleshooting

### Workflow times out after 30 minutes
- **Cause**: Cannot connect to Kafka broker
- **Solution**: Verify broker address is correct and accessible

### "Connection refused" errors
- **Cause**: Kafka broker is not reachable
- **Solution**: Check network connectivity, firewall rules, and broker configuration

### "Authentication failed" errors
- **Cause**: Invalid credentials or auth mechanism
- **Solution**: Verify SASL credentials, SSL certificates, and security protocol

## References

- [Port.io Kafka Integration Documentation](https://docs.getport.io/build-your-software-catalog/sync-data-to-catalog/cloud-providers/kafka)
- [Port Ocean Sail GitHub Action](https://github.com/port-labs/ocean-sail)
- Failed workflow run (for reference): [#29428574702](https://github.com/port-gh-app-dev/small-repo/actions/runs/29428574702)
- Successful validation test: [#29428738168](https://github.com/port-gh-app-dev/small-repo/actions/runs/29428738168) (timed out due to Kafka connection issue)

## History

- **2026-07-15**: Fixed Docker env file whitespace error with JSON minification
- **2026-07-15**: Identified Kafka broker configuration issue (localhost:9092)
- **2025-09-26 to 2026-07-15**: 22+ consecutive workflow failures due to validation errors
