param(
    [Parameter(Mandatory = $true)]
    [string]$RemoteUrl
)

$ErrorActionPreference = "Stop"

git remote get-url origin *> $null
if ($LASTEXITCODE -ne 0) {
    git remote add origin $RemoteUrl
} else {
    git remote set-url origin $RemoteUrl
}

git branch -M main
git push -u origin main
