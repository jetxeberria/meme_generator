# meme generator

## 1. Overview

Exercises of udacity Python nanodegree - Meme generator Project.

This project generate meme images by merging a given picture, a quote and an
author. If nothing is given, it's chosen automatically from repository examples
and generated a random meme combining default pictures and default quotes. 

Quotes can be read from files of following formats: CSV, PDF, DOCX and TXT. Except in CSV files, remaining formats must have in the content the quote and
the author, with this pattern:

```
"quote" - "author"
```

Generated memes are automatically saved in a folder "./tmp" created in the working directory, combining the source file name, the author of quote and a 
random string of 5 characters to avoid overwritting.

## 2. Use


### From source

First of all build your environment with

```
make env-create
```
Activate environment
```
activate
```

Now you're ready to run package well from command line interface, from
a python console or well in server application mode

#### Run from command line interface (CLI)

You can run package providing no arguments to get a random image mixed with a random
quote, both chosen from default repository examples:

```
python meme.py
```

You can run package providing just 'body' and 'author' argument. This way the 
image will be the default example one and the sentence and author the ones you
give. 'body' and 'author' arguments must be strings.

```
python meme.py --body "What a curious bark" --author "Phylosophal_dog"
```

You can provide just 'path'. This way the image will be the one you provide and
the sentence and author will be randomly chosen from default repository examples.
'path' argument must be an absolute or relative path to file from working directory.

```
python meme.py --path "./_data/photos/dog/suspicious_1.jpeg"
```

And, obviously you can provide the three arguments at once, fully customizing 
your meme.

```
python meme.py --path "./_data/photos/dog/suspicious_1.jpeg" --body "... That smells suspicious" --author "Run"
```

#### Run on a python console

Import start function in a python console :

```
python
> from meme_generator.meme import generate_meme
> input_path = /give/a/true/path
> input_quote = "...That smells suspicious"
> input_author = "RUN"
> generate_meme(input_path, input_quote, input_author)
```

#### Run the application in server

To run application on localhost server, go to folder of app file and run it:

```
cd meme_generator
python app.py
```

On standard output you'll see some Flask messages. The last one says  `Running on http://127.0.0.1:5000/`, you can interact with application going to pointed URL.

There you can both create a new meme giving all arguments or request a random one.

Note that when creating your own meme, the given (local/global) URL must point to JPEG-like file. 

### From package

If you want to use this library in other software projects you must build the package with:
```
   make dist-dev
```

Then, you can install it from generated "*.deb" to any environment. 

Note that you mustn't install package in its development environment, so test
in another environment:

```
   virtualenv new_env
   source new_env/bin/activate
```

Install directly from local file

```
   pip install ./dist/meme_generator-0.1.0-py2.py3-none-any.whl
```

Or you can publish to global pypi server or to your personal one, so you can install it with **pip**.

``` shell
    pip install \
    --extra-index-url=https://mypersonalserverrepository.com/repository/pypi-repository/simple meme_generator
```

Then run python console and import meme_generator as explained above.


## 3. Modules

- app.py: Module that hosts the application alive on server
  - To details about how to run on the server and consume it refer to above topic
"Run the application in server"
meme.py: Module that choses photos and sentences to be mixed
  - To details about how to run it refer to above topic "Run from command line interface (CLI)"

- engine.py: Library to perform on a image the operation of adding text
- errors.py: Library with all custom errors used in project
- fileio.py: Library with util functions to read and write files
- ingestor.py: Library to parse input files into objects consumable by engine.py
- parser.py: Library to parse arguments 


## 4. Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
