<setup git>

git config --global user.name "John Doe"
git config --global user.email johndoe@example.com
(creates file ~/.gitconfig)

cd working-dir
git init
git add *
git status
git commit

<login to github and create a repo>

git pull https://github.com/username/project-git master
git remote add origin https://github.com/username/project-git
git push -u origin master

<reset origin/dump changes>

git show origin
git reset --hard origin
git fetch

via Git clone

    Clone this repository to your home directory.

git clone https://github.com/magicmonty/bash-git-prompt.git ~/.bash-git-prompt --depth=1

Add to the ~/.bashrc:

if [ -f "$HOME/.bash-git-prompt/gitprompt.sh" ]; then
    GIT_PROMPT_ONLY_IN_REPO=1
    source $HOME/.bash-git-prompt/gitprompt.sh
fi

