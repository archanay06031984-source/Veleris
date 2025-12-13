$urls = @(
  'https://veleris.in/favicon.svg',
  'https://veleris.in/assets/seo/favicon.svg',
  'https://veleris.in/favicon.ico'
)

foreach ($u in $urls) {
  Write-Output "=== $u ==="
  try {
    $r = Invoke-WebRequest -Uri $u -UseBasicParsing -Method Head -ErrorAction Stop
    Write-Output ("Status: " + $r.StatusCode)
    Write-Output ("Content-Type: " + $r.Headers['Content-Type'])
  } catch {
    Write-Output ("Error: " + $_.Exception.Message)
  }
  Write-Output ""
}
