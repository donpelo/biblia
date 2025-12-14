. .\scripts\_cargar.ps1

\ = \.chapters.PSObject.Properties.Name | Sort-Object {[int]\}
\ = \.IndexOf(\.last_chapter)

if (\ -gt 0) {
    \ = \[\ - 1]
    \.last_chapter = \
    \.last_verse = '1'
}

\ | ConvertTo-Json -Depth 10 | Set-Content config.json -Encoding UTF8