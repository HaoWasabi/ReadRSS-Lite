# Deployment Configuration for ReadRSS Lite

## GitHub Actions
- Free tier: 2000 minutes/month
- Runtime limit: 6 hours per workflow
- Auto restart: Every 6 hours
- Monitoring: Actions tab

## Railway
- Free tier: 500 hours/month  
- Auto deployment: On git push
- Custom domain: Available
- Monitoring: Dashboard

## Render  
- Free tier: 750 hours/month
- Auto deployment: On git push
- SSL: Automatic
- Custom domain: Available

## Replit
- Free tier: Always-on with pings
- Requires ping system: Every 14 minutes
- Easy setup: Import from GitHub
- Limited resources: Shared hosting

## Environment Variables Required
- DISCORD_TOKEN: Your Discord bot token
- FIREBASE_CREDENTIALS: Firebase service account JSON

## Health Check Endpoints
- `/` - Basic status
- `/health` - Detailed bot status

## Notes
- Keep bot.log for debugging
- Monitor resource usage
- Set up proper error handling
- Use secrets for sensitive data