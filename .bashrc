# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

setxkbmap fr
XKB_DEFAULT_LAYOUT=fr

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# some more ls aliases
alias ll='ls -l --color -h'
alias la='ls -la --color -h'
alias l='ls -CF --color -h'
alias ls='ls --color -h'

# outils personnels :
PATH=$PATH:/home/$USER/.bin
PATH=$PATH:/home/$USER/.local/bin
PATH=$PATH:/home/$USER/.local/application/

c_red='^[[31m'
c_green='^[[32m'
c_sgr0='^[[00m'

parse_git_branch ()
{
	if git rev-parse --git-dir >/dev/null 2>&1
	then
		gitver=$(git branch 2>/dev/null| sed -n '/^\*/s/^\* //p')
		if git diff --quiet 2>/dev/null >&2 
		then
			gitver=$gitver
		else
			gitver='*'$gitver
		fi
	else
		return 0
	fi
	echo '(git:'$gitver')'
}

parse_svn_branch() {
	if [ -e .svn ]
	then
		echo -n '(svn:'
		echo -n '?'
		echo -n ')'
	fi
	
	#parse_svn_url | sed -e 's#^'"$(parse_svn_repository_root)"'##g' | awk -F / '{print "(svn::"$1 "/" $2 ")"}'
}
parse_svn_url() {
	svn info 2>/dev/null | sed -ne 's#^URL: ##p'
}
parse_svn_repository_root() {
	svn info 2>/dev/null | sed -ne 's#^Repository Root: ##p'
}

parse_cvs_branch() {
	if [ -e CVS/Repository ]
	then
		repo=`cat CVS/Repository`
		echo -n '(CVS:'
		if [ -e CVS/Tag ]
		then
			branch=`cat CVS/Tag`
			echo -n $repo'/'$branch
		else
			echo -n $repo'/HEAD'
		fi
		echo -n ')'
	fi
}



PS1='\033]0;$(workspaceMode.sh \w) \W\007\r\[\033[01;32m\][ \h : \u ]\[\033[01;33m\]$(parse_git_branch)$(parse_svn_branch)$(parse_cvs_branch)\[\033[00m\]\[\033[01;34m\]\w\[\033[00m\]\n\$ '

#export UBUNTU_MENUPROXY=0
export XAUTHORITY=/home/$USER/.Xauthority

#[[ oo $DISPLAY && $XDG_VTNR -eq 1 ]] && exec startx

# force lang of output in english ==> better for developpement
LANG=en_US.UTF-8

export DISPLAY=:0

# prevent the removing by error
alias rm='echo -e "========================================================\n== You must use trash instead of rm ==> prevent error ==\n========================================================\n"; echo > /dev/null'
