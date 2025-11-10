# Portfolio Website

Personal portfolio website showcasing projects, experience, and skills.

## Deployment to GitHub Pages

This site is configured to automatically deploy to GitHub Pages using GitHub Actions.

### Setup Instructions

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Add GitHub Pages deployment"
   git push origin main
   ```

2. **Enable GitHub Pages in your repository:**
   - Go to your repository on GitHub: `https://github.com/Yukkta-Seelam/Website-new`
   - Click on **Settings** (top menu)
   - Scroll down to **Pages** in the left sidebar
   - Under **Source**, select **GitHub Actions** (NOT "Deploy from a branch")
   - Click **Save**
   - **Important:** If you see "Deploy from a branch" selected, change it to "GitHub Actions"

3. **Check the Actions tab:**
   - Go to the **Actions** tab in your repository
   - You should see a workflow run after pushing
   - Wait for it to complete (green checkmark)
   - If it fails, check the error messages

4. **Access your site:**
   - After successful deployment, your site will be available at:
   - `https://yukkta-seelam.github.io/Website-new/`
   - It may take a few minutes after the workflow completes

### Troubleshooting 404 Errors

If you're getting a 404 error:

1. **Verify GitHub Pages is enabled:**
   - Go to Settings → Pages
   - Make sure **Source** is set to **GitHub Actions** (not a branch)
   - If you see "Your site is live at...", note the URL

2. **Check the Actions tab:**
   - Go to **Actions** tab
   - Look for "Deploy to GitHub Pages" workflow
   - Make sure it completed successfully (green checkmark)
   - If it failed, click on it to see error details

3. **Verify repository visibility:**
   - Your repository must be **public** (or you need GitHub Pro for private repos)
   - Go to Settings → General → Danger Zone → Change repository visibility

4. **Wait a few minutes:**
   - After enabling Pages, it can take 5-10 minutes for the site to be available
   - Clear your browser cache or try incognito mode

5. **Check the URL:**
   - Make sure you're using the correct URL format:
   - `https://yukkta-seelam.github.io/Website-new/` (with the repository name)
   - NOT `https://yukkta-seelam.github.io/` (without repository name)

6. **Verify files are pushed:**
   - Make sure `index.html` is in the root directory
   - Make sure `.github/workflows/deploy.yml` exists
   - Make sure `.nojekyll` file exists (this file is included)

### Manual Workflow Trigger

If the workflow didn't run automatically:
- Go to **Actions** tab
- Click on "Deploy to GitHub Pages" workflow
- Click "Run workflow" button
- Select the branch (main) and click "Run workflow"

### Notes

- The workflow file is located at `.github/workflows/deploy.yml`
- The `.nojekyll` file tells GitHub Pages to serve all files (including those starting with `_`)
- All files in the root directory will be served as static files

