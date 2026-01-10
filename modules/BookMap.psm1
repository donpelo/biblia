Set-StrictMode -Version Latest

function Get-BookMap-Es {
  # Mapeo estándar 1-66 (protestante). Tu dataset usa IDs numéricos.
  $m = @{}

  $m["1"]="Genesis"; $m["2"]="Exodo"; $m["3"]="Levitico"; $m["4"]="Numeros"; $m["5"]="Deuteronomio"
  $m["6"]="Josue"; $m["7"]="Jueces"; $m["8"]="Rut"; $m["9"]="1 Samuel"; $m["10"]="2 Samuel"
  $m["11"]="1 Reyes"; $m["12"]="2 Reyes"; $m["13"]="1 Cronicas"; $m["14"]="2 Cronicas"; $m["15"]="Esdras"
  $m["16"]="Nehemias"; $m["17"]="Ester"; $m["18"]="Job"; $m["19"]="Salmos"; $m["20"]="Proverbios"
  $m["21"]="Eclesiastes"; $m["22"]="Cantares"; $m["23"]="Isaias"; $m["24"]="Jeremias"; $m["25"]="Lamentaciones"
  $m["26"]="Ezequiel"; $m["27"]="Daniel"; $m["28"]="Oseas"; $m["29"]="Joel"; $m["30"]="Amos"
  $m["31"]="Abdias"; $m["32"]="Jonas"; $m["33"]="Miqueas"; $m["34"]="Nahum"; $m["35"]="Habacuc"
  $m["36"]="Sofonias"; $m["37"]="Hageo"; $m["38"]="Zacarias"; $m["39"]="Malaquias"

  $m["40"]="Mateo"; $m["41"]="Marcos"; $m["42"]="Lucas"; $m["43"]="Juan"; $m["44"]="Hechos"
  $m["45"]="Romanos"; $m["46"]="1 Corintios"; $m["47"]="2 Corintios"; $m["48"]="Galatas"; $m["49"]="Efesios"
  $m["50"]="Filipenses"; $m["51"]="Colosenses"; $m["52"]="1 Tesalonicenses"; $m["53"]="2 Tesalonicenses"; $m["54"]="1 Timoteo"
  $m["55"]="2 Timoteo"; $m["56"]="Tito"; $m["57"]="Filemon"; $m["58"]="Hebreos"; $m["59"]="Santiago"
  $m["60"]="1 Pedro"; $m["61"]="2 Pedro"; $m["62"]="1 Juan"; $m["63"]="2 Juan"; $m["64"]="3 Juan"
  $m["65"]="Judas"; $m["66"]="Apocalipsis"

  return $m
}

function Resolve-BookName {
  param([Parameter(Mandatory=$true)][string]$BookId)

  $map = Get-BookMap-Es
  if ($map.ContainsKey($BookId)) { return $map[$BookId] }
  return $BookId
}

Export-ModuleMember -Function Get-BookMap-Es, Resolve-BookName
