# ========================================
# GitHub Setup Script for Smart Rescuer
# ========================================

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🚀 Smart Rescuer - GitHub Setup" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check for Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git is not installed! Please install it from https://git-scm.com/" -ForegroundColor Red
    exit 1
}

# 2. Init Local Repo
if (-not (Test-Path ".git")) {
    Write-Host "[1/4] Initializing local Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git initialized" -ForegroundColor Green
} else {
    Write-Host "[1/4] Git repository already exists" -ForegroundColor Yellow
}

# 3. Add Files
Write-Host ""
Write-Host "[2/4] Adding files..." -ForegroundColor Yellow
git add .
Write-Host "✅ Files added" -ForegroundColor Green

# 4. Commit
Write-Host ""
Write-Host "[3/4] Committing changes..." -ForegroundColor Yellow
$commitMsg = Read-Host "Enter commit message (Press Enter for 'Initial deploy')"
if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "Initial deploy for VPS"
}
git commit -m "$commitMsg"
Write-Host "✅ Changes committed" -ForegroundColor Green

# 5. Connect to GitHub
Write-Host ""
Write-Host "[4/4] Connecting to GitHub..." -ForegroundColor Yellow

$remoteUrl = git remote get-url origin 2>$null
if ($remoteUrl) {
    Write-Host "Repository linked to: $remoteUrl" -ForegroundColor Cyan
    $newUrl = Read-Host "Do you want to change the URL? (Leave empty to keep)"
    if (-not [string]::IsNullOrWhiteSpace($newUrl)) {
        git remote set-url origin $newUrl
        Write-Host "✅ URL updated" -ForegroundColor Green
    }
} else {
    Write-Host "⚠️ No remote repository linked!" -ForegroundColor Red
    Write-Host "1. Go to https://github.com/new" -ForegroundColor White
    Write-Host "2. Create a new repository (do NOT add README/gitignore)" -ForegroundColor White
    Write-Host "3. Copy the HTTPS URL" -ForegroundColor White
    $repoUrl = Read-Host "Paste the repository URL here (e.g., https://github.com/user/repo.git)"
    
    if (-not [string]::IsNullOrWhiteSpace($repoUrl)) {
        git remote add origin $repoUrl
        Write-Host "✅ Repository linked" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
        git branch -M main
        git push -u origin main
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "🎉 Successfully pushed to GitHub!" -ForegroundColor Green
        } else {
            Write-Host "❌ Push failed. Check your URL or credentials." -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "NEXT STEPS ON VPS:" -ForegroundColor Yellow
Write-Host "1. Connect to VPS: ssh root@76.13.40.84" -ForegroundColor White
Write-Host "2. Clone Repo: git clone <REPO_URL>" -ForegroundColor White
Write-Host "3. Enter Folder: cd <REPO_NAME>" -ForegroundColor White
Write-Host "4. Run Deploy: bash vps-deploy-complete.sh" -ForegroundColor White
Write-Host "==========================================" -ForegroundColor Cyan
