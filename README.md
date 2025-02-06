# chessrank
Chess Tournament Manager and ELO processing for the Royal Belgian Chess Federation. Initially, this project aims at having a standard interface to receive tournament results through JSON reports, and visualize them.

## What?
This project aims at creating a common chess results interface for use with various chess programs in use in Belgium (SWAR, PairTwo, SwissManager, ...).

## Getting started
- clone this github repository
- make sure you have [Yarn](https://classic.yarnpkg.com/en/) and [Docker](https://www.docker.com/) installed
- in the repository folder, create a file '.env' with default postgresql credentials:
  
  ```
  DB_NAME=postgres
  DB_USER=postgres
  DB_PASSWORD=postgres
  DB_HOST=db
  DB_PORT=5432
  ```
- download packages, build stylesheet & javascript files

  `yarn install && yarn build && yarn build:css`
- build the docker container

  `yarn docker:build`
- start the application

  `yarn docker:start`
- open up a shell in the chessrank container and apply database migrations
  
  `python manage.py migrate`
- visit your application at [localhost:8000](localhost:8000)
- test with a tournament upload file
  
  ```
  curl -X POST http://127.0.0.1:8000/api/tournament/create/ -H "Content-Type: application/json" --data "@UtopiaBlitz_report.json"
  ```

## Contributors wanted
You are encouraged to inspect, modify the code and create pull requests

## Contact
First contact point for questions is Steven Bellens (steven.bellens@frbe-kbsb-ksb.be)

## Tips & trics
### Docker network access on Windows
In Docker Settings > Resources > Network, ensure 'Enable host networking' is enabled. Otherwise, the container has no internet access, and various functions (e.g. MySQL access) are not working

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
