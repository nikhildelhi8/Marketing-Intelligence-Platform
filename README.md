# Marketing Intelligence Platform (MIP)

## Setup
\`\`\`bash
python3 -m venv venv
source venv/Scripts/activate  # Git Bash on Windows
pip install -e ".[dev]"
\`\`\`

## Verify install
\`\`\`bash
python -c "import mip; print(mip.__version__)"
\`\`\`