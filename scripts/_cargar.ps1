$config = Get-Content "config.json" -Encoding UTF8 | ConvertFrom-Json

$dataPath = "data/biblia_es.json"
$biblia = Get-Content $dataPath -Encoding UTF8 | ConvertFrom-Json