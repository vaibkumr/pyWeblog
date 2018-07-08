# pyWeblog
#### A static python blog builder 

## About
pyWeblog is a simple static blog builder completely written in python. It renders the complete blog html, css and js files that can later be hosted anywhere easily. This is my personal project and could be scaled up into a product in future if needed. The css and js are highly customizable and can be changed according to personal needs anytime.The best part about this script is that it can render the complete blog and then even upload to a desired host all within command line which a lot of linux users prefer. Although, I am planning to create a much simpler GUI for windows and user who prefer GUI over command line.

## Features

### - Blog initialization
  ```
python init_blog.py
```
You will be asked to enter the "blog name", "author image URL" and "about author text". These will be saved for future and used in your every post all over the website rendered though this script.

### - Post creation
 First create an input file in a certain fomat mentioned below and save it as anything, lets say "new_post.txt" 
```
#BEGIN

##Title
Title here
##Title

##Tags
tags,seperated,by,commas,here,dont,add,a,new,line,here
##Tags

##Content
Some content here, new line will be added on HTML as this file so be careful while pressing ENTER
##Image
<image url here,can't enter multple urls under same tag>
##Image
##Code
<url here, can't enter multple urls under same tag>
##Code
##Code
https://gist.github.com/TimeTraveller-San/da33f05c64813554f79e0574738a7e57.js
##Code
An example of code above, make sure its a github gist embed URL
As of now using <b></b> and <i></i> in this file breaks the software, dont use them until fix comes.
Also, this file's debugger and comments coming soon.

##Content

#END
```
After saving the above file, run the python script makeblog as follows to commit this post in the current blog files. Remember to enter the file name that is "new_post.txt" as a command line argument for the script
 ```
python makeblog.py new_post.txt
python makeblog.py <input post file name here>
```
### - Post structure overview 
 This script will print the current post structure of your blog
```
python display_structure.py
```
### - Post deletion
 Ever post has a unique ID which can be obtained from the post structure overview feature or by the source code of your post. It's a python generated UUID
```
python dlete_post.py bf91026d-e0d9-41c5-9d16-66e1f027870b
python delete_post.py <UUID HERE>
```

# Showcase
A live example can be seen [here](http://timemachine.netlify.com)
![Screen Shot](https://i.imgur.com/2XiCSqQ.jpg)


## Dependencies 
- Python libraries:-
  - BeautifulSoup4
  - Pickle
  - arrow
 ```
 sudo pip install beautifulsoup4 Pickle arrow
 ```
## To do
- Pagination
- Support for bold and italic tags which break the blog for now
- Post editor for syntax checking and image insertion
- GUI
- Blog editor for no code CSS and HTML editing 
- Inbuilt hosting support
