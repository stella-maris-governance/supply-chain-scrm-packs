#!/bin/bash
# Generate CycloneDX SBOM from project directory
# Stella Maris Governance — 2026
#
# Usage: ./generate-sbom-cyclonedx.sh <project-dir> <output-file>

set -euo pipefail

PROJECT_DIR="${1:-.}"
OUTPUT="${2:-sbom-cyclonedx.json}"

echo "=== Stella Maris SBOM Generator ==="
echo "Project: $PROJECT_DIR"
echo "Output:  $OUTPUT"
echo ""

# Detect project type and generate
if [ -f "$PROJECT_DIR/package.json" ]; then
    echo "Detected: Node.js"
    npx @cyclonedx/cyclonedx-npm --output-file "$OUTPUT" "$PROJECT_DIR"
elif [ -f "$PROJECT_DIR/pom.xml" ]; then
    echo "Detected: Maven"
    mvn -f "$PROJECT_DIR/pom.xml" org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom -DoutputFormat=json
    cp "$PROJECT_DIR/target/bom.json" "$OUTPUT"
elif [ -f "$PROJECT_DIR/requirements.txt" ] || [ -f "$PROJECT_DIR/setup.py" ]; then
    echo "Detected: Python"
    pip install cyclonedx-bom --break-system-packages 2>/dev/null
    cyclonedx-py -r --format json -o "$OUTPUT" -i "$PROJECT_DIR/requirements.txt"
elif [ -f "$PROJECT_DIR/*.csproj" ] || [ -f "$PROJECT_DIR/*.sln" ]; then
    echo "Detected: .NET"
    dotnet CycloneDX "$PROJECT_DIR" -o "$OUTPUT" -j
else
    echo "ERROR: Unable to detect project type."
    echo "Supported: Node.js (package.json), Maven (pom.xml), Python (requirements.txt), .NET (csproj/sln)"
    exit 1
fi

echo ""
echo "SBOM generated: $OUTPUT"
echo "Next: validate with validate-ntia-elements.py"
echo "=== Complete ==="
