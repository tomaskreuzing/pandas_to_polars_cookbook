Pandas cookbook
===============

This repo was copied from [pandas_cookbook](https://github.com/jvns/pandas-cookbook). Do have a look at
the original.

Your job is to turn this pandas cookbook into a polars cookbook.
Some good resources for polars are:
- The official documentation [here](https://docs.pola.rs/api/python/stable/reference/dataframe/index.html)
- Calmcode.io tutorial [here](https://calmcode.io/course/polars/introduction)
- Feel free to use chat bots like ChatGPT, Claude, or Gemini. Or GitHub Copilot.

There are several chapters that guide you through how to use pandas in the [cookbook folder](./cookbook). It will be your job to create a cookbook for polars.

## Exercises
### Set-up
1. Fork this repo.
2. Clone the forked repo and open it in VS Code.
3. Create a virtual environment from the environment.yml:
4. Select this environment as your interpreter in VS Code.

**Create a virtual environment from the environment.yml**

a. Open the terminal

b. Go to your workspace folder if you are not already in it: `cd path_to_repo`

c. Then type `conda env create -f environment.yml`

**Set Up VS Code to Use the New Environment**

a. Open your project folder in VS Code.

b. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) to open the Command Palette.

c. Type "Python: Select Interpreter" and select it.

d. From the list, choose the interpreter that matches your new Conda environment. 
   It should look something like `polars_cookbook`.

e. VS Code will now use this environment for running Python code in this project.

**Verify the Setup**

Open a Python file or create a new one. In the bottom-left corner of VS Code, 
you should see the name of your Conda environment. This confirms that VS Code 
is using the correct environment.

### First changes
1. Create a branch called "chapter_1"
2. Switch to this branch
3. Open the first chapter in the cookbook [here](./cookbook/Chapter%201%20-%20Reading%20from%20a%20CSV.ipynb)
4. Complete the to-dos in the cells, which means rewriting the pandas code into polars.
   - For every to-do, use the git flow and add, commit, push
   - Once you have done your first commit and pushed it to the remote, go to your repo on [GitHub](https://github.com)
   - GitHub will show you that you created a new branch and ask you to do a pull request. Make a pull request.
   - Having started your pull request, have a look at your commit. Can you easily identify the changes you have made?
5. Finish all the to-dos in chapter 1 (do not forget to add, commit, push after every to-do)
6. Once you have done all to-dos in chapter 1, go back to [GitHub](https://github.com) and merge your branch into main.
7. After merging in GitHub, don't forget to pull the changes locally. (First change to the main branch, and then do a git pull)

### Better changes
Above you have seen that doing pull requests with jupyter notebooks are not very visually pleasing.

For this reason, the further chapters are no longer jupyter notebooks but python files. We use a trick, however. You can get all the beauty of the interactiveness of jupyter notebooks using `# %%`. 

Now, for the remaining chapters:
1. Create a branch for each chapter.
2. Complete all to-dos and add, commit, push for each to-do you complete.
   - Have a look at your commits. Can you see how much easier it is to analyse your changes now?
3. Once finished, merge your branch into main.
4. Proceed to the next chapter.