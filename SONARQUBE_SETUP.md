# SonarQube Setup Instructions

## Issue
The Build workflow is failing due to an invalid or missing `SONAR_TOKEN` secret. The SonarQube scan cannot authenticate with SonarCloud API (HTTP 403 error).

## Root Cause
The `SONAR_TOKEN` secret is either:
- Not configured in repository settings
- Expired or revoked
- Missing necessary permissions

## Error Message
```
ERROR Failed to query JRE metadata: GET https://api.sonarcloud.io/analysis/jres?os=linux&arch=x86_64 failed with HTTP 403
```

## Solution

### Step 1: Generate a SonarCloud Token
1. Go to [SonarCloud](https://sonarcloud.io/)
2. Log in with your account
3. Navigate to **My Account** → **Security** → **Generate Token**
4. Create a new token with the following permissions:
   - **Execute Analysis** (required for scanning)
   - Set expiration as needed (or use "No expiration")
5. Copy the generated token

### Step 2: Configure the GitHub Secret
1. Go to your repository on GitHub: `https://github.com/port-gh-app-dev/small-repo`
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `SONAR_TOKEN`
5. Value: Paste the token from Step 1
6. Click **Add secret**

### Step 3: Verify SonarCloud Project Configuration
Ensure your SonarCloud project is configured correctly:
- **Project Key:** `port-gh-app-dev_small-repo`
- **Organization:** `port-gh-app-dev`

You can verify this in the `sonar-project.properties` file in the repository root.

### Step 4: Test the Workflow
After configuring the secret:
1. Push a new commit or re-run the failed workflow
2. The Build workflow should now complete successfully
3. View results on SonarCloud: `https://sonarcloud.io/dashboard?id=port-gh-app-dev_small-repo`

## Temporary Workaround
Until the token is configured, the Build workflow will skip the SonarQube scan with a warning instead of failing. This allows other CI/CD processes to continue.

## Additional Notes
- The workflow has been updated to use `sonarqube-scan-action@v6` (latest version)
- The previous version (v5) was deprecated and contained security vulnerabilities
- If you don't want to use SonarQube scanning, you can delete the `.github/workflows/build.yaml` file

## Related Links
- [SonarCloud Documentation](https://docs.sonarcloud.io/)
- [GitHub Actions Integration Guide](https://docs.sonarcloud.io/advanced-setup/ci-based-analysis/github-actions-for-sonarcloud/)
- [SonarQube Scan Action](https://github.com/SonarSource/sonarqube-scan-action)
