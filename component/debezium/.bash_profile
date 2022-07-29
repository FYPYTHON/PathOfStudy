# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# User specific environment and startup programs

PATH=$PATH:$HOME/.local/bin:$HOME/bin

export PATH


export PGPORT=5432
export PGHOME=/opt/midware/postgresql
export PGDATA=/opt/midware/postgresql/pgdata
export PATH=$PGHOME/bin:$PATH
#export MANPATH=$PGHOME/share/man:$MANPATH
export LANG=zh_CN.utf8
export DATE='date +"%Y%m%d%H%M"'
export LD_LIBRARY_PATH=$PGHOME/lib:$LD_LIBRARY_PATH
