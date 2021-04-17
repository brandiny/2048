# 2048 in Python3 (Tkinter)

2048 is a classic mobile game. This is a spinoff of 2048 for desktop using Python3's built-in tkinter framework.

## Build Instructions
Run these instructions within the 2048/ folder, in the terminal.
<table>
    <tr>
        <td>Windows</td>
        <td><code>py -m venv env && env\Scripts\activate && py -m pip install -r requirements.txt</code></td>
    </tr>
    <tr>
        <td>Linux</td>
        <td>
            <code>sudo apt-get install python-tk</code>
            <code>python3 -m venv env && source env/bin/activate && python3 -m pip install -r requirements.txt</code>
        </td>
    </tr>
</table>

## Run Instructions
<table>
    <tr>
        <td>Windows</td>
        <td><code>python main.pyw</code></td>
    </tr>
    <tr>
        <td>Linux</td>
        <td><code>python3 main.pyw</code></td>
    </tr>
</table>


## Features
In addition to the traditional game mechanics, there are:
* Local highscore tables
* In-depth game statistics
* Saving and loading capabilities

The code utilises:
* Object oriented design (utilised in switching views)
* Matrix manipulation (core mechanics of the 2048 board)
* File I/O (saving and loading)
* Use of 3rd party libraries (for image manipulation)

## Documentation
If you would like more information, there is a full documentation of the development process and tests used.

## Preview Snippet
<img alt=2048_preview height="400" src="https://github.com/brandiny/2048/blob/main/images/2048preview.PNG">
