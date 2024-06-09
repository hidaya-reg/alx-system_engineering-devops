# Postmortem Report: Website Outage on June 1, 2024

## Issue Summary

**Duration:**  
June 1, 2024, 14:00 - June 1, 2024, 16:30 (UTC)

**Impact:**  
The primary e-commerce platform experienced a total outage. Users were unable to access the website, resulting in an inability to browse or purchase products. Approximately 100% of users were affected during this period, resulting in an estimated revenue loss of $150,000.

**Root Cause:**  
The outage was caused by a misconfigured database connection pool limit, which was inadvertently set too low during a routine maintenance update.

## Timeline

- **14:00** - Issue detected by automated monitoring alert indicating a spike in 500 error responses.
- **14:02** - On-call engineer notified via pager duty.
- **14:05** - Initial investigation began; logs showed database connection errors.
- **14:15** - Database team consulted; initial suspicion was a database server crash.
- **14:30** - Misleading path: Database server health checked; no issues found.
- **14:45** - Web server logs reviewed, revealing connection pool errors.
- **15:00** - Configuration files inspected, and the incorrect connection pool limit identified.
- **15:10** - Misleading path: Temporary increase of pool limit attempted, but not applied correctly due to configuration syntax error.
- **15:30** - Correct configuration update applied and deployed.
- **15:45** - Web services gradually restored as connections stabilized.
- **16:30** - Full functionality confirmed restored.

## Root Cause and Resolution

**Root Cause:**  
During a routine maintenance update, a configuration file for the database connection pool was edited. The `max_connections` parameter was mistakenly set to 50 instead of the intended 500. This limited the number of simultaneous connections the web servers could establish with the database, causing the servers to quickly exhaust available connections and throw 500 errors.

**Resolution:**  
The issue was resolved by:
1. Identifying the incorrect configuration in the `database_config.yml` file.
2. Correcting the `max_connections` parameter to 500.
3. Restarting the web servers to apply the new configuration.

## Corrective and Preventative Measures

**Improvements and Fixes:**
1. **Review Configuration Management:** Enhance review processes for configuration changes to prevent misconfigurations.
2. **Automated Testing:** Implement automated tests for configuration files to catch errors before deployment.
3. **Increase Monitoring Granularity:** Add more detailed monitoring for database connection metrics to detect anomalies faster.

**Tasks:**
- **Patch Web Server Configuration:** Ensure all servers are using the corrected configuration file.
- **Implement Configuration Validation:** Add scripts to validate configuration files before deployment.
- **Enhance Monitoring:**
  - Add specific alerts for high database connection usage.
  - Increase log verbosity for connection errors.
- **Conduct Training:** Provide training sessions for engineers on the importance of configuration management and error handling.
- **Update Documentation:** Document the incident and the resolution steps in the internal knowledge base for future reference.

By addressing these areas, we aim to prevent similar incidents in the future and improve overall system reliability.
