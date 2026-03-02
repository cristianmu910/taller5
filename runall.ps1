$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

$nombreEntorno = "taller3"

$existe = (conda env list) | Select-String -Pattern ("^" + $nombreEntorno + "\s")
if (-not $existe) {
    conda env create -f environment.yml
}

conda run -n $nombreEntorno python scripts/01_simulate.py
conda run -n $nombreEntorno python scripts/02_analysis.py
conda run -n $nombreEntorno python scripts/03_visualization.py