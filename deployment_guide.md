# Deployment Guide

This Airport Code Guessing Game can be deployed in several ways. Choose the method that best fits your needs.

## Quick Start (Local Development)

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/airport-game.git
cd airport-game
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Pixabay API key
```

5. Run the application:
```bash
python app.py
```

Visit `http://localhost:5000` to play the game!

## Deployment Options

### 1. Heroku

The easiest cloud deployment option with the included `Procfile`.

```bash
# Install Heroku CLI if you haven't already
brew install heroku/brew/heroku  # macOS
# or
sudo snap install --classic heroku  # Ubuntu

# Login to Heroku
heroku login

# Create a new app
heroku create airport-code-game

# Set environment variables
heroku config:set PIXABAY_API_KEY=your_api_key_here

# Deploy
git push heroku main

# Open the app
heroku open
```

### 2. Google Cloud Run

Using the included `Dockerfile` for containerized deployment.

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/airport-game

# Deploy to Cloud Run
gcloud run deploy airport-game \
  --image gcr.io/YOUR_PROJECT_ID/airport-game \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PIXABAY_API_KEY=your_api_key_here
```

### 3. Vercel

Perfect for static deployment with serverless functions.

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Add environment variables
vercel env add PIXABAY_API_KEY

# Deploy
vercel
```

### 4. AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.9 airport-game

# Set environment variables
eb setenv PIXABAY_API_KEY=your_api_key_here

# Deploy
eb create airport-game-env
eb deploy
```

### 5. DigitalOcean App Platform

1. Fork this repository
2. Connect to your GitHub account in DigitalOcean
3. Create a new App from source
4. Select this repository
5. Add environment variable: `PIXABAY_API_KEY`
6. Deploy!

## iOS Web App Installation

Users can install this as a "native" app on iOS:

1. Open the deployed URL in Safari
2. Tap the share button
3. Select "Add to Home Screen"
4. Tap "Add"

The app will appear on the home screen and launch in fullscreen mode like a native app.

## API Keys Required

### Pixabay API Key
- Free tier: 5,000 requests/month
- Get your key at: https://pixabay.com/api/docs/
- Add to environment variables as `PIXABAY_API_KEY`

## Performance Tips

1. **Caching**: Implement Redis caching for airport data
2. **Image Optimization**: Use image CDN or optimize images before serving
3. **Data Loading**: Pre-fetch airport data during deployment

## Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure your domain is allowed in API settings
2. **Images Not Loading**: Verify Pixabay API key is correctly set
3. **Slow Loading**: Consider using a CDN for static assets

### Logs

Check application logs:
```bash
# Heroku
heroku logs --tail

# Google Cloud Run
gcloud logs read

# Local development
python app.py  # Logs printed to console
```

## Maintenance

### Updating Airport Data

The app automatically fetches fresh airport data from ourairports.com. To manually update:

```python
python -c "from airport_data import save_airport_data_to_json; save_airport_data_to_json()"
```

### Backup Considerations

- Airport data is sourced from public APIs
- User scores are not persistent (add database for this feature)
- API keys should be backed up securely

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

For major changes, please open an issue first to discuss what you would like to change.