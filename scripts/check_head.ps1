$urls = @(
    'https://veleris.in/',
    'https://veleris.in/collections.html',
    'https://veleris.in/collection-minimal.html',
    'https://veleris.in/collection-abstract.html',
    'https://veleris.in/collection-nature.html',
    'https://veleris.in/collection-anime.html'
)

$opts = [System.Text.RegularExpressions.RegexOptions]::Singleline -bor [System.Text.RegularExpressions.RegexOptions]::IgnoreCase

foreach ($u in $urls) {
    Write-Output "=== $u ==="
    try {
        $r = Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec 30
        Write-Output "Status: $($r.StatusCode)"
        $content = $r.Content

        # Title
        $m = [regex]::Match($content, '<title[^>]*>(.*?)</title>', $opts)
        $title = if ($m.Success) { $m.Groups[1].Value.Trim() } else { '(none)' }
        Write-Output "Title: $title"

        # Canonical (look for href value inside link rel=canonical)
        $canonPattern = @'
<link[^>]*rel=(?:"|')?canonical(?:"|')?[^>]*href=(?:"|')([^"']+)(?:"|')
'@
        $m = [regex]::Match($content, $canonPattern, $opts)
        $canonical = if ($m.Success) { $m.Groups[1].Value } else { '(none)' }
        Write-Output "Canonical: $canonical"

        # og:image
        $ogPattern = @'
<meta[^>]*(?:property|name)=(?:"|')og:image(?:"|')[^>]*content=(?:"|')([^"']+)(?:"|')
'@
        $m = [regex]::Match($content, $ogPattern, $opts)
        $og = if ($m.Success) { $m.Groups[1].Value } else { '(none)' }
        Write-Output "og:image: $og"

    } catch {
        Write-Output "Fetch error: $($_.Exception.Message)"
    }
}
