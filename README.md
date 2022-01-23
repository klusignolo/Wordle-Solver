# Wordle Solver
A utility for narrowing down guesses on [Wordle](https://www.powerlanguage.co.uk/wordle/).

## Publishing

The application is built/packaged using the package PyInstaller. The build steps are specified in build.spec. To build a new .exe, open a command prompt window in the project directory and run the following:

```python
pyinstaller build.spec
```
When PyInstaller finishes running, the new .exe file will be located in /dist.

## Contributing
Contributions are welcome! This is already pretty light weight. If there are any words that need to be removed from five_letter_words.txt, just open a PR and I'll approve.

## License
[MIT](https://choosealicense.com/licenses/mit/)
