rm -f ~/env_reqs/*
for i in `ls -1 ~/.virtualenvs`; do
	test -e .virtualenvs/$i/bin/pip && { "$HOME/.virtualenvs/$i/bin/pip" freeze > "$HOME/env_reqs/$i"; }
done
