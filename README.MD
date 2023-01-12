## How to run the tools

run command: `docker-compose up`

## how to deploy each tool to Heroku

- [Heroku guide](https://devcenter.heroku.com/articles/container-registry-and-runtime#getting-started)

1. `heroku container:login`
2. `heroku container:push web --app=dsec-gitleaks`
3. `heroku container:release web --app=dsec-gitleaks`
