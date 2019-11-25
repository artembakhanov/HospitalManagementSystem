# HospitalManagementSystem
This is a simple project developed by a group of students in Innopolis University in 2019.

### Built With
We used the following frameworks and databases
* [PyQT5](https://www.riverbankcomputing.com/software/pyqt/intro)
* [PostgreSQL](https://www.postgresql.org/)
 
 ### Prerequisites

For running this project you need to install Python 3.6 or higher. <br>
In Ubuntu, Mint and Debian you can install Python like this:
```shell script
sudo apt-get install python3 python3-pip
```
Also PostgreSQL is required. Read [here](https://www.postgresql.org/download/) about installing it.
### Installation
1. Clone the repo
```shell script
git clone https://github.com/artembakhanov/HospitalManagementSystem
```
2. Change the directory
```shell script
cd ./HospitalManagementSystem
```
3. Install dependencies
```shell script
sudo pip3 install -r requirements.txt
```
4. Enter your credentials in [`config.py`](config.py)
```python
DATABASE_LOGIN = "your_login"
DATABASE_PASSWORD = "your_password"
```
You can also change the name of the database using
```python
DATABASE_NAME = "name"
```
5. Run `Controller.py`
```shell script
python3 Controller.py
```

## Advanced
You can also edit the config file [`DataGenerator/config.py`](DataGenerator/config.py) if you want to change parameters of the database population algorithm.

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/yourFeature`)
3. Commit your Changes (`git commit -m 'Add some yourFeature'`)
4. Push to the Branch (`git push origin feature/yourFeature`)
5. Open a Pull Request

## License

Distributed under the GNU General Public License v3.0. See [`LICENSE`](LICENSE) for more information.

## Developed by

1. [@artembakhanov](https://github.com/artembakhanov)
2. [@TooTiredOne](https://github.com/TooTiredOne)
3. Marko Pezer
4. Dinar Zayakhov
5. Utkarsh Kalra
