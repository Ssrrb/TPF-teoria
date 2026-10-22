#!/usr/bin/env bash
# Reproduce todos los diagramas y el documento desde modelo.yaml.
# Requiere: uv (para pyyaml), plantuml (con la stdlib C4), graphviz, pandoc, libreoffice, poppler y java 21.
set -euo pipefail
cd "$(dirname "$0")"
RAIZ=".."
STRUCTURIZR="$RAIZ/structurizr"
WAR="$STRUCTURIZR/structurizr-application/target/structurizr-1.0.0.war"
PY="uv run --quiet --with pyyaml python3"

echo "==> 1/8  Validando el modelo"
$PY gen/validar.py

echo "==> 2/8  Generando fuentes UML"
rm -f uml/*.puml
$PY gen/gen_puml.py

echo "==> 3/8  Renderizando UML a PNG"
rm -f out/*.png
plantuml -tpng -o ../out uml/*.puml

echo "==> 4/8  Generando las vistas C4 (librería C4-PlantUML)"
rm -f c4/*.puml out/c4/*.png
mkdir -p c4 out/c4
$PY gen/gen_c4.py
# Structurizr valida el mismo modelo y conserva el workspace navegable (workspace.dsl)
$PY gen/gen_dsl.py
if [ ! -f "$WAR" ]; then
  echo "    (compilando Structurizr por primera vez; puede tardar varios minutos)"
  (cd "$STRUCTURIZR" && ./mvnw -B -q -DskipTests -DexcludedGroups=IntegrationTest \
      -P exclude-playwright -pl structurizr-application -am package)
fi
java -jar "$WAR" validate -w workspace.dsl
java -jar "$WAR" inspect  -w workspace.dsl

echo "==> 5/8  Renderizando las vistas C4 a PNG"
plantuml -tpng -o ../out/c4 c4/*.puml

echo "==> 6/8  Generando el archivo de apoyo"
$PY gen/gen_md.py

echo "==> 7/8  Armando el documento"
uv run --quiet --with pyyaml --with python-docx python3 gen/gen_docx.py
rm -f "$RAIZ/TPF-Obra-Studio.pdf"
soffice --headless --convert-to pdf --outdir "$RAIZ" "$RAIZ/TPF-Obra-Studio.docx" > /dev/null 2>&1

echo "==> 8/8  Verificando el documento contra el modelo"
$PY gen/verificar_salida.py

echo
echo "Listo:"
echo "  $(ls out/*.png | wc -l) diagramas UML      -> modelo/out/"
echo "  $(ls out/c4/*.png | wc -l) vistas C4            -> modelo/out/c4/"
echo "  documento             -> TPF-Obra-Studio.docx / .pdf ($(pdfinfo "$RAIZ/TPF-Obra-Studio.pdf" | awk '/Pages/{print $2}') páginas)"
echo "  apoyo                 -> modelo-de-analisis.md"
