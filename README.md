# Basic Lang V2
By Max Miller

Basic Lang is a custom language using Python3 as the interpreter. It's very similar to Python, but only allows for fully global vars. It isn't intended as something to use in production, but hopefully could be a good learning tool. 

## Installation
You must also have installed npm and python

```bash
mkdir "BasicLangV2"
cd BasicLangV2
git clone https://github.com/MaxMessWithTech/BasicLangV2.git
```

## Usage
### In a terminal
Command:
```bash
python main.py [filename] [headless]
```
Example:
```bash
python main.py ./script.bsl headless
```
### On Webserver (Must start both)
Start Flask Backend (http://localhost:5000/):
```bash
cd backend
python main.py
```
Start React Frontend (http://localhost:8080/):
```bash
cd frontend
npm start
```

## Contributing
You're free to make whatever pull requests or changes you want, just make sure to follow whatever the standard procedure is. If new features are developed that are useful and helpful to users than I may deploy it to the webserver.

## About the author
Hey! My name is Max Miller, I'm a 16 year old and a softmore in high school, as of when I'm writing this. When I was 8, I started programing with MIT's Scratch. I did that off and on for a few years, I tried to do a few courses at a local community collage, to no avail, until I finally had a reason to move on. At my middle school, we had a theater program, but as you may be able to imagine, having more then 100 little children in a show with a relatively small theater is difficult. My school took it very seriously, and were able to run it like a real production with students as all of the cast and crew. I made a program in Scratch, using the global vars(networked vars - it's a weird name), I was able to show in the dressing rooms what scene was currently going on. But it was a very flawed system, as Scratch isn't intended to work in this way. That summer I decided to learn python for the express purpose of making a stable version of this. I tried to use google sheets as my networked database lol. I tried using Tkinter, PyQT5, and Kivy for interfaces, only to remember that I needed to run it on Chromebooks. I took another python class at the community collage to try to ask someone who knew what they're doing, but the teacher wasn't able to help as it wasn't in his expertise. Anyway, I continued to try to use Scratch and it continued to be bad in future years. I kept trying to use so called "Scratch to Python" converters, which do not work lol. I was incredibly ignorant of how code actually worked lol. Eventually the pandemic caused me to be stuck at home on my computer, and I had an assignment to make a game with Scratch for a class. I had talked up how good I was at coding, when in reality, I really wasn't. So in order to flex, I made it in Python, a language that I wasn't proficient in yet. Anyway, long story a little shorter: This language is being developed to fill a void that I had while I was learning, a typed language that has direct functionality like scratch.

## Will more updates be coming?
I originally started this project a week before school started and then got busy, I then started over with this repository as I'm now a better programmer and my old code base was a mess lol. I'm developing really slow because of school, but my hope is to have a working version relatively soon, in which I'll make sure I add a version on GitHub. 