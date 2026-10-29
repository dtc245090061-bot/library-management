$word = New-Object -ComObject Word.Application
$word.Visible = $false
$file = (Resolve-Path "docs/Bao_Cao_Do_An_Quan_Ly_Thu_Vien_AI_100Trang.docx").Path
$doc = $word.Documents.Open($file)

# Update all fields in document (TOC, page numbers)
foreach ($section in $doc.Sections) {
    $section.Headers(1).Range.Fields.Update() | Out-Null
    $section.Footers(1).Range.Fields.Update() | Out-Null
}
$doc.Fields.Update() | Out-Null

$pages = $doc.ComputeStatistics(2)
Write-Host "FINAL EXACT WORD PAGE COUNT:" $pages

$doc.Save()
$doc.Close([ref]$false)
$word.Quit()
