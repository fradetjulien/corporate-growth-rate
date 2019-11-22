# corporate-profit-revenues

Python script which scrapts data from the financial statements page of a ticker page, then it computes the annual growth rate and the annual profit margin for each year. Finally, it shows two graphics of those results.

## Installation

Python 3 and Pipenv are required in order to run this program.

### OSX

```bash
brew install python3
```
```bash
brew install pipenv
```

## Usage

If you want to test the script manually, you can achieve this by doing :

```bash
cd module
pipenv install
pipenv run python3 index.py graph
```

## Example

<p align="center">
  <img src="assets/cli-illustration.png" width="650">
  <img src="assets/graphics-illustration.png" width="650">
</p>

## Executable

If you want to build a cross-platform executable, you need to execute the following bash commands :

```bash
cd module
pipenv install
pipenv run pyinstaller index.py --onefile
```

The executable file will be located on the generated dist folder.

## License

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)