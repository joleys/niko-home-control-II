# Enabling Statistics in Niko Home Control II Integration

This guide explains how to enable and import statistics for existing users of the Niko Home Control II Home Assistant integration. If you are upgrading or have previously installed the integration, follow these steps to ensure your historical and recent measurement data (energy, gas, water) is available in Home Assistant statistics.

## Step 1: Import Historical and Recent Statistics

Existing users must manually trigger the import of both long-term and recent statistics. This is a one-time operation to bring all available historical data into Home Assistant.

**Service to Call:** `nhc2.import_statistics` (**Developer Tools → Actions**)

**Parameters:**
- `import_type`: Set to `both` to import both long-term and recent data.

**Example YAML:**
```yaml
service: nhc2.import_statistics
data:
  import_type: both
```

## Step 2: Enable Periodic Statistics Updates

After importing, you must enable periodic statistics updates through the integration options:

1. Go to **Settings → Devices & Services → Integrations** in Home Assistant.
2. Find **Niko Home Control II** and click **Options**.
3. Enable the toggle for **Statistics**.
4. Save your changes.

Once enabled, the integration will automatically import new measurement data every hour.

## Troubleshooting
- If you encounter issues or duplicate data, check and manage the statistics through **Developer Tools → Statistics**

---
For more information, see the main [README.md](./README.md) and [Statistics Import section](./README.md#statistics-import).
