# Auto network speed test

This application is intended for use by  Sonic internet installers to automatically do network tests and take photos of said tests.


## Getting Started
to run this project locally you will need an sftp server that accepts public traffic or traffic from the device you are running this program on without a password. I use an ssh key

and a local json file named secrets.json that has
- hostname the IP or domain of your sftp server
- username the username used to connect to your sftp server
- port the port being used for sftp (if you don't know it should be 22)

### Installing

This tool is not intended for public use, and requires the user to install all python libs used by the sonic.py file a list is TBD. reach out to me directly if you would like help setting up a functional version.

installing this on a computer you do not have admin on requires building it yourself.


## License

This project is licensed under the [CC0 1.0 Universal](LICENSE.md)
Creative Commons License - see the [LICENSE.md](LICENSE.md) file for
details

