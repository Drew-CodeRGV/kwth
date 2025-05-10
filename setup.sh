#!/bin/bash

# Airport Code Guessing Game - Setup Script
# This script sets up the project for deployment and development

echo "🛫 Setting up Airport Code Guessing Game..."

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p static
mkdir -p templates
mkdir -p data

# Create a simple icon (placeholder)
echo "🎨 Creating placeholder icon..."
cat > static/icon.png << 'EOF'
# This is a placeholder. You need to create a proper 192x192 PNG icon.
# See static/ICON.md for instructions.
EOF

# Set up virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create data directory
echo "📊 Setting up data directory..."
touch data/.gitkeep

# Copy environment template
echo "⚙️  Setting up environment..."
cp .env.example .env

# Initialize git (if not already initialized)
if [ ! -d ".git" ]; then
    echo "📚 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - Airport Code Guessing Game"
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your Pixabay API key"
echo "2. Create an icon at static/icon.png (see static/ICON.md)"
echo "3. Run 'python app.py' to start the development server"
echo "4. Push to GitHub and deploy to your preferred platform"
echo ""
echo "Happy coding! ✈️"
