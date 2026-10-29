$word = New-Object -ComObject Word.Application
$word.Visible = $false
$file = (Resolve-Path "docs/Bao_Cao_Do_An_Quan_Ly_Thu_Vien_AI_100Trang.docx").Path
$doc = $word.Documents.Open($file)
$pages = $doc.ComputeStatistics(2)
Write-Host "EXACT PAGE COUNT:" $pages
$doc.Close([ref]$false)
$word.Quit()
