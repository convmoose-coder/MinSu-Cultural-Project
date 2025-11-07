module.exports = {
  apps: [
    {
      name: 'minsu-backend',
      script: 'python app.py',
      cwd: './',
      env: {
        NODE_ENV: 'production'
      }
    },
    {
      name: 'minsu-frontend',
      script: 'npm run dev',
      cwd: './frontend',
      env: {
        NODE_ENV: 'production'
      }
    },
    {
      name: 'minsu-admin',
      script: 'npm run dev:admin',
      cwd: './frontend',
      env: {
        NODE_ENV: 'production'
      }
    }
  ]
};