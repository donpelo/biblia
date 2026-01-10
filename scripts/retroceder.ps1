. .\scripts\_cargar.ps1

\ = \.last_chapter
\ = \.last_verse

\ = \.chapters.\.PSObject.Properties.Name | Sort-Object {[int]\}

\ = \.IndexOf(\)

if (\ -gt 0) {
    \.last_verse = \[\ - 1]
}

\ | ConvertTo-Json -Depth 10 | Set-Content config.json -Encoding UTF8